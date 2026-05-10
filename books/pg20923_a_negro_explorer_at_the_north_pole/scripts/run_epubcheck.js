const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const javaRoot = path.join(root, 'tools', 'zulu17-jre');
const jar = path.join(root, 'node_modules', 'epubchecker', 'vendors', 'epubcheck-5.2.1', 'epubcheck.jar');
const epub = path.join(root, 'output', 'book.epub');
const report = path.join(root, 'output', 'epubcheck.json');

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

const java = findJava(javaRoot) || 'java';
if (fs.existsSync(report)) fs.unlinkSync(report);
const result = spawnSync(java, ['-jar', jar, epub, '--json', report, '--failonwarnings', '-q'], {
  cwd: root,
  stdio: 'inherit',
});
if (fs.existsSync(report)) {
  const parsed = JSON.parse(fs.readFileSync(report, 'utf8'));
  console.log(`epubcheck: fatal=${parsed.checker.nFatal}, error=${parsed.checker.nError}, warning=${parsed.checker.nWarning}`);
}
process.exit(result.status ?? 1);
