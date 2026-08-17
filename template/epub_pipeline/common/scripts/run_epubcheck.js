const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const argv = process.argv.slice(2);
const epubArg = argv.find((arg) => arg.startsWith('--epub='));
const reportArg = argv.find((arg) => arg.startsWith('--report='));
const allEnabled = argv.includes('--all-enabled');
const javaRoot = path.join(root, 'tools', 'zulu17-jre');

function findSharedNodeModules(start) {
  let dir = start;
  while (true) {
    const candidate = path.join(dir, 'node_modules');
    if (fs.existsSync(candidate)) return candidate;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

function findJava(dir) {
  if (!dir || !fs.existsSync(dir)) return null;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const candidate = path.join(dir, entry.name);
    if (entry.isFile() && entry.name.toLowerCase() === 'java.exe') return candidate;
    if (entry.isDirectory()) {
      const found = findJava(candidate);
      if (found) return found;
    }
  }
  return null;
}

function firstExisting(paths) {
  return paths.find((item) => item && fs.existsSync(item)) || null;
}

function findLifeBookPrivateJava() {
  const fromEnv = firstExisting([process.env.LIFEBOOK_JAVA]);
  if (fromEnv) return fromEnv;
  const localAppData = process.env.LOCALAPPDATA;
  if (!localAppData) return null;
  return findJava(path.join(localAppData, 'LifeBook', 'runtimes', 'java'));
}

function findSharedTool(start, relativePath) {
  let dir = start;
  while (true) {
    const candidate = path.join(dir, relativePath);
    if (fs.existsSync(candidate)) return candidate;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function relativeOrAbsolute(file) {
  const relative = path.relative(root, file);
  return relative && !relative.startsWith('..') && !path.isAbsolute(relative)
    ? relative.split(path.sep).join('/')
    : file;
}

function safeEditionType(value) {
  return String(value || 'edition').replace(/[^A-Za-z0-9_-]+/g, '_');
}

function reportForEdition(editionType) {
  return path.join(
    root,
    'output',
    editionType === 'target_only' ? 'epubcheck.json' : `epubcheck_${safeEditionType(editionType)}.json`,
  );
}

function enabledJobs() {
  if (!allEnabled) {
    return [{
      editionType: 'target_only',
      epub: epubArg ? path.resolve(root, epubArg.slice('--epub='.length)) : path.join(root, 'output', 'book.epub'),
      report: reportArg ? path.resolve(root, reportArg.slice('--report='.length)) : path.join(root, 'output', 'epubcheck.json'),
    }];
  }
  if (epubArg || reportArg) throw new Error('--all-enabled cannot be combined with --epub or --report');
  const statePath = path.join(root, 'state', 'pipeline_state.json');
  const state = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : {};
  const configured = Array.isArray(state.output_editions)
    ? state.output_editions.filter((item) => item && item.enabled === true)
    : [];
  const editions = configured.length
    ? configured
    : [{ edition_type: 'target_only', artifact: 'output/book.epub' }];
  return editions.map((item) => {
    const editionType = String(item.edition_type || 'target_only');
    const artifact = String(item.artifact || 'output/book.epub');
    return {
      editionType,
      epub: path.isAbsolute(artifact) ? artifact : path.resolve(root, artifact),
      report: reportForEdition(editionType),
    };
  });
}

const nodeModules = findSharedNodeModules(root);
const jar = nodeModules
  ? path.join(nodeModules, 'epubchecker', 'vendors', 'epubcheck-5.2.1', 'epubcheck.jar')
  : null;
const java = findLifeBookPrivateJava()
  || findJava(javaRoot)
  || findJava(findSharedTool(root, path.join('tools', 'zulu17-jre')))
  || firstExisting([process.env.JAVA_HOME && path.join(process.env.JAVA_HOME, 'bin', 'java.exe')])
  || 'java';

if (!jar || !fs.existsSync(jar)) {
  console.error(`Missing epubcheck jar: ${jar || '(node_modules not found)'}`);
  console.error('Run npm install from the books/ directory so this script can find books/node_modules while walking upward.');
  process.exit(1);
}

function runOne(job) {
  if (!fs.existsSync(job.epub)) {
    console.error(`Missing enabled EPUB artifact: ${relativeOrAbsolute(job.epub)}`);
    return 1;
  }
  fs.mkdirSync(path.dirname(job.report), { recursive: true });
  const tempReport = `${job.report}.tmp-${process.pid}`;
  if (fs.existsSync(tempReport)) fs.rmSync(tempReport, { force: true });
  const result = spawnSync(java, ['-jar', jar, job.epub, '--json', tempReport, '--failonwarnings', '-q'], {
    cwd: root,
    stdio: 'inherit',
  });
  if (fs.existsSync(tempReport)) {
    const parsed = JSON.parse(fs.readFileSync(tempReport, 'utf8'));
    parsed.lifebook_evidence = {
      schema_version: '1.0',
      edition_type: job.editionType,
      artifact_path: relativeOrAbsolute(job.epub),
      artifact_sha256: sha256(job.epub),
      checker_jar_sha256: sha256(jar),
      checked_at: new Date().toISOString(),
    };
    fs.writeFileSync(tempReport, `${JSON.stringify(parsed, null, 2)}\n`, 'utf8');
    if (fs.existsSync(job.report)) fs.rmSync(job.report, { force: true });
    fs.renameSync(tempReport, job.report);
    const checker = parsed.checker || {};
    console.log(`${job.editionType}: fatal=${checker.nFatal}, error=${checker.nError}, warning=${checker.nWarning} sha256=${parsed.lifebook_evidence.artifact_sha256}`);
  }
  if (result.error) console.error(`Failed to run Java: ${result.error.message}`);
  return result.status ?? 1;
}

let exitCode = 0;
try {
  for (const job of enabledJobs()) exitCode = Math.max(exitCode, runOne(job));
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  exitCode = 1;
}
process.exit(exitCode);
