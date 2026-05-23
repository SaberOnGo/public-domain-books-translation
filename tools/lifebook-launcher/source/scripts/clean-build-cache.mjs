import { rm } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const sourceRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const removable = [
  "dist",
  path.join("src-tauri", "target"),
  path.join("src-tauri", "gen"),
];

for (const relativePath of removable) {
  const absolutePath = path.resolve(sourceRoot, relativePath);
  if (!absolutePath.startsWith(sourceRoot + path.sep)) {
    throw new Error(`Refusing to remove path outside launcher source: ${absolutePath}`);
  }
  await rm(absolutePath, { recursive: true, force: true });
  console.log(`Removed ${relativePath}`);
}
