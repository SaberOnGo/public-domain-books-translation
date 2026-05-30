import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function extractFunction(source, signature) {
  const start = source.indexOf(signature);
  assert(start >= 0, `Could not find function signature: ${signature}`);
  const braceStart = source.indexOf("{", start);
  assert(braceStart >= 0, `Could not find function body: ${signature}`);
  let depth = 0;
  for (let index = braceStart; index < source.length; index += 1) {
    const char = source[index];
    if (char === "{") depth += 1;
    if (char === "}") depth -= 1;
    if (depth === 0) return source.slice(start, index + 1);
  }
  throw new Error(`Could not extract function body: ${signature}`);
}

const capability = JSON.parse(readText("src-tauri/capabilities/default.json"));
const permissions = new Set(capability.permissions ?? []);
assert(
  permissions.has("core:event:default") || (
    permissions.has("core:event:allow-listen") &&
    permissions.has("core:event:allow-unlisten")
  ),
  "Launcher main window must allow Tauri event listen/unlisten for progress subscriptions.",
);

const appSource = readText("src/App.tsx");
assert(
  appSource.includes("useState<RuntimeBootstrapState>(\"ready\")"),
  "Launcher must treat runtime bootstrap as optional at startup instead of blocking the first screen.",
);
assert(
  appSource.includes("useState(false)") && !appSource.includes("useState(hasTauriRuntime())"),
  "Runtime bootstrap blocking state must default to false.",
);
assert(
  !appSource.includes("startRuntimeBootstrap(true)"),
  "Runtime preparation must not be started in blocking mode.",
);
assert(
  /if\s*\(!runtimeBootstrapStartedRef\.current\)\s*\{[\s\S]*?startRuntimeBootstrap\(false\)/.test(appSource),
  "Launcher should keep optional runtime preparation in the background after initial UI startup.",
);
assert(
  appSource.includes("void prepareLifeBookInBackground();"),
  "Launcher should keep automatic LifeBook project preparation in the background after initial UI startup.",
);

const tauriSource = readText("src-tauri/src/lib.rs");
const runBlocking = extractFunction(tauriSource, "async fn run_blocking");
assert(
  runBlocking.includes("catch_unwind"),
  "Blocking background tasks must convert panics into errors instead of relying on task runtime behavior.",
);
const runtimePrepare = extractFunction(tauriSource, "fn start_runtime_prepare");
assert(
  runtimePrepare.includes("catch_unwind"),
  "Runtime preparation worker must convert panics into logged failure events.",
);
const nodeModulesInstall = extractFunction(tauriSource, "fn start_node_modules_install");
assert(
  nodeModulesInstall.includes("catch_unwind"),
  "Node modules installation worker must convert panics into logged failure events.",
);
const archiveInstall = extractFunction(tauriSource, "fn download_lifebook_archive_repo");
assert(
  !archiveInstall.includes("lifebook_latest_remote_commit_best_effort()"),
  "Initial archive install must start the ZIP download without a prior best-effort GitHub commit probe.",
);

console.log("startup contract ok");
