/* 浏览器判题 PoC 的本地服务器。
 *
 * 把仓库里的**真实文件**映射出去（`compare.py` / `driver.py` 不拷副本），
 * Pyodide 也从 node_modules 直接提供 —— 这样 PoC 完全不依赖外网 CDN，
 * 测出来的结果才是确定的、可复现的。
 *
 * 真实部署时把 worker 里的 indexURL 换成 CDN 即可（那里已注明）。
 *
 * 用法：node serve.mjs [port]
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");          // -> pta/
const PYODIDE_DIR = path.join(HERE, "node_modules", "pyodide");
const PORT = Number(process.argv[2] || 8899);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".py": "text/plain; charset=utf-8",
  ".wasm": "application/wasm",
  ".zip": "application/zip",
  ".map": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
};

const ROUTES = {
  "/":                path.join(HERE, "index.html"),
  "/index.html":      path.join(HERE, "index.html"),
  "/judge-worker.js": path.join(HERE, "judge-worker.js"),
  "/driver.py":       path.join(HERE, "driver.py"),
  "/compare.py":      path.join(ROOT, "app", "judge", "compare.py"),
  "/fixtures.json":   path.join(HERE, "fixtures.json"),
};

function send(res, code, body, type) {
  res.writeHead(code, { "Content-Type": type, "Cache-Control": "no-store" });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  let pathname = decodeURIComponent(url.pathname);

  // Pyodide 运行时（含 .wasm / stdlib.zip）
  if (pathname.startsWith("/pyodide/")) {
    const rel = pathname.slice("/pyodide/".length);
    const abs = path.join(PYODIDE_DIR, rel);
    if (!abs.startsWith(PYODIDE_DIR) || !fs.existsSync(abs) || fs.statSync(abs).isDirectory()) {
      return send(res, 404, "not found", "text/plain");
    }
    return send(res, 200, fs.readFileSync(abs), MIME[path.extname(abs)] || "application/octet-stream");
  }

  const abs = ROUTES[pathname];
  if (!abs || !fs.existsSync(abs)) {
    return send(res, 404, "not found: " + pathname, "text/plain");
  }
  send(res, 200, fs.readFileSync(abs), MIME[path.extname(abs)] || "application/octet-stream");
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`浏览器判题 PoC 已启动：http://127.0.0.1:${PORT}/`);
});
