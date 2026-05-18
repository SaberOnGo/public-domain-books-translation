const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const javaRoot = path.join(root, 'tools', 'zulu17-jre');
const epub = path.join(root, 'output', 'book.epub');
const report = path.join(root, 'output', 'epubcheck.json');

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
  if (!fs.existsSync(dir)) return null;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const p = path.join(dir, entry.name);
    if (entry.isFile() && entry.name.toLowerCase() === 'java.exe') return p;
    if (entry.isDirectory()) {
      const found = findJava(p);
      if (found) return found;
    }
  }
  return null;
}

function firstExisting(paths) {
  return paths.find((item) => item && fs.existsSync(item)) || null;
}

const nodeModules = findSharedNodeModules(root);
const jar = nodeModules
  ? path.join(nodeModules, 'epubchecker', 'vendors', 'epubcheck-5.2.1', 'epubcheck.jar')
  : null;

const java = findJava(javaRoot) || firstExisting([
  process.env.JAVA_HOME && path.join(process.env.JAVA_HOME, 'bin', 'java.exe'),
]) || 'java';

if (!jar || !fs.existsSync(jar)) {
  console.error(`Missing epubcheck jar: ${jar || '(node_modules not found)'}`);
  console.error('Run npm install from the books/ directory so this script can find books/node_modules while walking upward.');
  process.exit(1);
}

if (fs.existsSync(report)) fs.unlinkSync(report);
const result = spawnSync(java, ['-jar', jar, epub, '--json', report, '--failonwarnings', '-q'], {
  cwd: root,
  stdio: 'inherit',
});
if (fs.existsSync(report)) {
  const parsed = JSON.parse(fs.readFileSync(report, 'utf8'));
  console.log(`epubcheck: fatal=${parsed.checker.nFatal}, error=${parsed.checker.nError}, warning=${parsed.checker.nWarning}`);
}
if (result.error) {
  console.error(`Failed to run Java: ${result.error.message}`);
}
process.exit(result.status ?? 1);
