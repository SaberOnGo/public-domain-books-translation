const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const outputRoot = path.join(projectRoot, 'output');
const stagingNames = new Set(['epub_work', 'epub_work_bilingual']);

if (fs.existsSync(outputRoot)) {
  for (const name of stagingNames) {
    const target = path.join(outputRoot, name);
    const relative = path.relative(outputRoot, target);
    if (relative.startsWith('..') || path.isAbsolute(relative) || !stagingNames.has(path.basename(target))) {
      throw new Error(`Refusing to clean unexpected staging path: ${target}`);
    }
    fs.rmSync(target, { recursive: true, force: true });
  }
}

console.log('staging cleanup PASS');
