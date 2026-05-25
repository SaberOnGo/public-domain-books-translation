import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const checkOnly = process.argv.includes("--check");
const versionFile = path.join(root, "launcher-version.json");
const versionManifest = JSON.parse(fs.readFileSync(versionFile, "utf8"));
const version = String(versionManifest.version ?? "").trim();

if (!/^\d+\.\d+\.\d+$/.test(version)) {
  throw new Error(`Invalid launcher version in ${versionFile}: ${version}`);
}

const dirty = [];

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function writeText(relativePath, next) {
  const absolutePath = path.join(root, relativePath);
  const current = fs.readFileSync(absolutePath, "utf8");
  if (current === next) return;
  if (checkOnly) {
    dirty.push(relativePath);
    return;
  }
  fs.writeFileSync(absolutePath, next);
}

function writeJson(relativePath, value) {
  writeText(relativePath, `${JSON.stringify(value, null, 2)}\n`);
}

function replaceRequired(relativePath, pattern, replacement) {
  const current = readText(relativePath);
  if (!pattern.test(current)) {
    throw new Error(`Unable to update version in ${relativePath}`);
  }
  writeText(relativePath, current.replace(pattern, replacement));
}

const packageJson = JSON.parse(readText("package.json"));
packageJson.version = version;
writeJson("package.json", packageJson);

const packageLock = JSON.parse(readText("package-lock.json"));
packageLock.version = version;
if (packageLock.packages?.[""]) {
  packageLock.packages[""].version = version;
}
writeJson("package-lock.json", packageLock);

replaceRequired(
  "src-tauri/Cargo.toml",
  /(^version\s*=\s*")[^"]+(")/m,
  `$1${version}$2`,
);

replaceRequired(
  "src-tauri/Cargo.lock",
  /(\[\[package\]\]\s+name = "lifebook-launcher"\s+version = ")[^"]+(")/m,
  `$1${version}$2`,
);

const tauriConfig = JSON.parse(readText("src-tauri/tauri.conf.json"));
tauriConfig.version = version;
writeJson("src-tauri/tauri.conf.json", tauriConfig);

if (dirty.length) {
  console.error(`Launcher version is not synchronized with ${path.relative(root, versionFile)}:`);
  for (const relativePath of dirty) {
    console.error(`- ${relativePath}`);
  }
  process.exit(1);
}
