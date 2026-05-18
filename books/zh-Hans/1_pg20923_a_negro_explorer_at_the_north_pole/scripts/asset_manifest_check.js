const fs = require('fs');
const path = require('path');

const args = new Set(process.argv.slice(2));
const getArg = (name, fallback = null) => {
  const prefix = `${name}=`;
  const found = process.argv.slice(2).find((arg) => arg.startsWith(prefix));
  return found ? found.slice(prefix.length) : fallback;
};

const scriptRoot = path.resolve(__dirname, '..');
const cwdRoot = process.cwd();
const projectRoot = fs.existsSync(path.join(cwdRoot, 'chapters')) ? cwdRoot : scriptRoot;
const writeReport = args.has('--write-report');
const reportPath = getArg('--report', path.join('output', 'asset_manifest_check.json'));

const sourceRoots = [
  'frontmatter',
  path.join('chapters', 'final'),
  'preproduction',
  'output',
].map((rel) => path.join(projectRoot, rel)).filter((dir) => fs.existsSync(dir));

const allowedAssetExts = new Set([
  '.svg',
  '.png',
  '.jpg',
  '.jpeg',
  '.webp',
  '.gif',
  '.css',
  '.woff',
  '.woff2',
  '.otf',
  '.ttf',
]);

const textExts = new Set(['.md', '.xhtml', '.html', '.opf', '.css']);
const imageMd = /!\[[^\]]*]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;
const htmlSrc = /\b(?:src|href)=["']([^"']+)["']/g;
const cssUrl = /url\(["']?([^"')]+)["']?\)/g;
const opfItem = /<item\b[^>]*\bhref=["']([^"']+)["'][^>]*>/g;
const absolutePath = /^(?:[A-Za-z]:[\\/]|\\\\|\/|file:\/\/)/;
const remoteUrl = /^https?:\/\//i;

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (textExts.has(path.extname(entry.name).toLowerCase())) out.push(full);
  }
  return out;
}

function normalizeRel(file) {
  return path.relative(projectRoot, file).split(path.sep).join('/');
}

function isInside(child, parent) {
  const relative = path.relative(parent, child);
  return relative === '' || (!!relative && !relative.startsWith('..') && !path.isAbsolute(relative));
}

function stripFragment(ref) {
  return ref.split('#')[0].split('?')[0];
}

function resolveRef(fromFile, ref) {
  const clean = decodeURIComponent(stripFragment(ref));
  if (!clean || clean.startsWith('#') || remoteUrl.test(clean) || absolutePath.test(clean)) return null;
  return path.resolve(path.dirname(fromFile), clean);
}

function collectRefs(file, text) {
  const refs = [];
  const addMatches = (regex, kind) => {
    regex.lastIndex = 0;
    let match;
    while ((match = regex.exec(text))) {
      refs.push({ kind, ref: match[1], index: match.index });
    }
  };
  addMatches(imageMd, 'markdown_image');
  addMatches(htmlSrc, 'html_src_href');
  addMatches(cssUrl, 'css_url');
  return refs;
}

function lineAt(text, index) {
  let line = 1;
  for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
}

function collectOpfManifests() {
  const opfFiles = [];
  const output = path.join(projectRoot, 'output');
  const preproduction = path.join(projectRoot, 'preproduction');
  for (const root of [output, preproduction].filter((dir) => fs.existsSync(dir))) {
    for (const file of walk(root)) {
      if (path.extname(file).toLowerCase() === '.opf') opfFiles.push(file);
    }
  }

  const manifests = [];
  for (const file of opfFiles) {
    const text = fs.readFileSync(file, 'utf8');
    const hrefs = new Set();
    let match;
    opfItem.lastIndex = 0;
    while ((match = opfItem.exec(text))) {
      const resolved = resolveRef(file, match[1]);
      if (resolved) hrefs.add(path.normalize(resolved));
    }
    manifests.push({ file, packageRoot: path.dirname(file), hrefs });
  }
  return { opfFiles, manifests };
}

const files = sourceRoots.flatMap((dir) => walk(dir));
const { opfFiles, manifests } = collectOpfManifests();
const issues = [];
const assetRefs = [];

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8');
  for (const item of collectRefs(file, text)) {
    const relFile = normalizeRel(file);
    const cleanRef = stripFragment(item.ref);
    if (!cleanRef || cleanRef.startsWith('#')) continue;

    if (absolutePath.test(cleanRef)) {
      issues.push({ file: relFile, line: lineAt(text, item.index), rule: 'absolute_asset_path', ref: item.ref });
      continue;
    }
    if (remoteUrl.test(cleanRef)) {
      issues.push({ file: relFile, line: lineAt(text, item.index), rule: 'remote_asset_hotlink', ref: item.ref });
      continue;
    }

    const resolved = resolveRef(file, item.ref);
    if (!resolved) continue;
    const ext = path.extname(resolved).toLowerCase();
    const relAsset = normalizeRel(resolved);

    if (!fs.existsSync(resolved)) {
      issues.push({ file: relFile, line: lineAt(text, item.index), rule: 'missing_asset', ref: item.ref, resolved: relAsset });
      continue;
    }
    if (ext && !allowedAssetExts.has(ext) && item.kind !== 'html_src_href') {
      issues.push({ file: relFile, line: lineAt(text, item.index), rule: 'unexpected_asset_extension', ref: item.ref, resolved: relAsset });
    }
    assetRefs.push({ file: relFile, line: lineAt(text, item.index), kind: item.kind, ref: item.ref, resolved: relAsset });
  }
}

if (opfFiles.length) {
  for (const ref of assetRefs) {
    const ext = path.extname(ref.resolved).toLowerCase();
    if (!allowedAssetExts.has(ext)) continue;
    const abs = path.normalize(path.join(projectRoot, ref.resolved));
    const refFile = path.normalize(path.join(projectRoot, ref.file));
    const ownerManifest = manifests.find((manifest) => isInside(refFile, manifest.packageRoot));
    if (!ownerManifest) continue;
    if (!ownerManifest.hrefs.has(abs)) {
      issues.push({ file: ref.file, line: ref.line, rule: 'asset_not_in_opf_manifest', ref: ref.ref, resolved: ref.resolved });
    }
  }
}

const report = {
  projectRoot: '.',
  opfFiles: opfFiles.map(normalizeRel),
  totals: {
    files: files.length,
    assetRefs: assetRefs.length,
    issues: issues.length,
  },
  assetRefs,
  issues,
};

if (writeReport) {
  const out = path.join(projectRoot, reportPath);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(report, null, 2), 'utf8');
}

console.log(JSON.stringify(report.totals, null, 2));
if (issues.length) {
  for (const issue of issues.slice(0, 50)) {
    console.error(`${issue.file}:${issue.line} ${issue.rule}: ${issue.ref}`);
  }
  if (issues.length > 50) console.error(`... ${issues.length - 50} more issues`);
  process.exit(1);
}
