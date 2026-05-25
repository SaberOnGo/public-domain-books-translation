const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

function findExecutable(dir, fileName) {
  if (!dir || !fs.existsSync(dir)) return null;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isFile() && entry.name.toLowerCase() === fileName.toLowerCase()) return fullPath;
    if (entry.isDirectory()) {
      const found = findExecutable(fullPath, fileName);
      if (found) return found;
    }
  }
  return null;
}

function privatePython() {
  if (process.env.LIFEBOOK_PYTHON && fs.existsSync(process.env.LIFEBOOK_PYTHON)) {
    return { program: process.env.LIFEBOOK_PYTHON, args: [] };
  }
  const localAppData = process.env.LOCALAPPDATA;
  if (!localAppData) return null;
  const found = findExecutable(path.join(localAppData, 'LifeBook', 'runtimes', 'python'), 'python.exe');
  return found ? { program: found, args: [] } : null;
}

function commandWorks(program, args) {
  const result = spawnSync(program, [...args, '--version'], {
    encoding: 'utf8',
    stdio: 'ignore',
  });
  return !result.error && result.status === 0;
}

function resolvePython() {
  const privateRuntime = privatePython();
  if (privateRuntime) return privateRuntime;
  if (process.platform === 'win32' && commandWorks('py', ['-3'])) {
    return { program: 'py', args: ['-3'] };
  }
  if (commandWorks('python', [])) return { program: 'python', args: [] };
  if (commandWorks('python3', [])) return { program: 'python3', args: [] };
  return null;
}

const python = resolvePython();
if (!python) {
  console.error('Python runtime is not ready. Open LifeBook Launcher and retry Python / Java runtime preparation.');
  process.exit(1);
}

const result = spawnSync(python.program, [...python.args, ...process.argv.slice(2)], {
  cwd: process.cwd(),
  env: process.env,
  stdio: 'inherit',
});
if (result.error) {
  console.error(`Failed to run Python: ${result.error.message}`);
  process.exit(1);
}
process.exit(result.status ?? 1);
