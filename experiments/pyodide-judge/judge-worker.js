/* Web Worker —— 整个判题引擎跑在这里。
 *
 * 为什么必须放 Worker
 * -------------------
 * Pyodide 执行 Python 时**独占 JS 线程**。放在主线程上，一段 `while True: pass`
 * 就能把页面彻底冻死 —— 用户连刷新按钮都点不动。
 * 放进 Worker 之后，主线程可以靠定时器超时 → `worker.terminate()` 强杀。
 * 代价是重建要重新加载 Pyodide（本地约 1.5 秒），所以只有真超时才付这个代价。
 *
 * 判题口径：直接 import 题库里的 `compare.py` + 共用 `driver.py`，零重写。
 */
import { loadPyodide } from "/pyodide/pyodide.mjs";

let judgeFn = null;

async function boot() {
  const py = await loadPyodide({
    // ★ 真实部署时换成 CDN，例如：
    //   https://cdn.jsdelivr.net/pyodide/v314.0.7/full/
    indexURL: "/pyodide/",
  });
  py.setStdout({ batched: () => {} });   // 别让运行时自身的输出干扰
  py.setStderr({ batched: () => {} });

  const [compareSrc, driverSrc] = await Promise.all([
    fetch("/compare.py").then((r) => r.text()),
    fetch("/driver.py").then((r) => r.text()),
  ]);
  py.FS.writeFile("/home/pyodide/compare.py", compareSrc);
  py.FS.writeFile("/home/pyodide/driver.py", driverSrc);
  py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
  judgeFn = py.runPython("from driver import judge; judge");

  self.postMessage({
    type: "ready",
    python: String(py.runPython("import sys; sys.version.split()[0]")),
  });
}

self.addEventListener("message", (e) => {
  const msg = e.data || {};
  if (msg.type !== "judge") return;

  if (!judgeFn) {
    self.postMessage({ type: "result", id: msg.id,
      payload: { verdict: "IE", ms: 0, detail: "判题引擎尚未就绪", stdout: "", stderr: "" } });
    return;
  }

  try {
    const raw = judgeFn(msg.code, msg.stdin ?? "", msg.expected ?? "",
                        msg.checker ?? "standard", msg.eps ?? 1e-6);
    self.postMessage({ type: "result", id: msg.id, payload: JSON.parse(String(raw)) });
  } catch (err) {
    self.postMessage({ type: "result", id: msg.id,
      payload: { verdict: "IE", ms: 0, detail: String((err && err.message) || err), stdout: "", stderr: "" } });
  }
});

boot().catch((err) => {
  self.postMessage({ type: "fatal", detail: String((err && err.stack) || err) });
});
