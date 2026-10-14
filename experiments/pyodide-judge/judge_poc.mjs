/**
 * 前端判题 PoC —— 验证「在浏览器里判 Python 题」是不是真的可行。
 *
 * 为什么跑在 Node 里
 * ------------------
 * 同一份 Pyodide 运行时（WASM），但 Node 里我能拿到**真实输出、能断言、能复现**。
 * 浏览器版只是把这段逻辑搬进 Web Worker，判题口径完全一致。
 * （反过来只写个 HTML 页面、靠肉眼看着"好像对了"，那不叫验证。）
 *
 * 验证四节，每节都要有正反两面，不能只证「能跑」
 * ------------------------------------------------
 * [1] 基础设施：真 CPython / input() 能读替换后的 stdin / stdout 能抓 / 中文不乱码
 * [2] compare.py **原样** import 成功，语义抽查全过（含 PE / oneof / float）
 * [3] 真题全量：56 题 109 样例 × 题库自己的参考解 → 必须全 AC
 * [4] 反例：恒定错解 → 必须全 WA（证【比对不是恒真】）
 */
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");            // -> pta/
const PYODIDE_DIR = path.join(HERE, "node_modules", "pyodide");

let nPass = 0, nFail = 0;
const fails = [];

function check(label, ok, detail = "") {
  if (ok) { nPass++; console.log(`    [PASS] ${label}${detail ? "  → " + detail : ""}`); }
  else    { nFail++; fails.push(label); console.log(`    [FAIL] ${label}${detail ? "  → " + detail : ""}`); }
}

function section(title) {
  console.log("\n" + "─".repeat(64));
  console.log(title);
  console.log("─".repeat(64));
}

// ────────────────────────────────────────────────────────────
section("[0] 启动 Pyodide");
const tBoot = Date.now();
const { loadPyodide } = await import(
  pathToFileURL(path.join(PYODIDE_DIR, "pyodide.mjs")).href);
const py = await loadPyodide();
const bootMs = Date.now() - tBoot;
py.setStdout({ batched: () => {} });     // 吞掉运行时自身的输出，别污染报告
py.setStderr({ batched: () => {} });
console.log(`    启动耗时 ${bootMs} ms`);
console.log(`    CPython ${py.runPython("import sys; sys.version.split()[0]")}`);

// 挂载：题库真实的 compare.py + 共用 driver.py
py.FS.writeFile("/home/pyodide/compare.py",
  readFileSync(path.join(ROOT, "app", "judge", "compare.py"), "utf8"));
py.FS.writeFile("/home/pyodide/driver.py",
  readFileSync(path.join(HERE, "driver.py"), "utf8"));
py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");

// ────────────────────────────────────────────────────────────
section("[1] 基础设施自检");
const ver = py.runPython("import sys; sys.version.split()[0]");
check("真 CPython 运行时", /^3\.\d+\.\d+$/.test(String(ver)), `版本 ${ver}`);

const readBack = py.runPython(`
import io, sys
sys.stdin = io.StringIO("hello-from-stdin\\n")
try:
    line = input()
finally:
    sys.stdin = sys.__stdin__
line
`);
check("input() 能读替换后的 stdin", String(readBack) === "hello-from-stdin", JSON.stringify(String(readBack)));

const zh = py.runPython(`
import io, sys
b = io.StringIO()
old = sys.stdout
sys.stdout = b
print("中文输出·测试")
sys.stdout = old
b.getvalue()
`);
check("中文输出不乱码", String(zh).trim() === "中文输出·测试", JSON.stringify(String(zh).trim()));

const crlf = py.runPython(`
import io, sys
a = io.StringIO()
old = sys.stdout
sys.stdout = a
print("A"); print("B")
sys.stdout = old
a.getvalue()
`);
check("print 自动补换行可捕获", String(crlf) === "A\nB\n", JSON.stringify(String(crlf)));

// ────────────────────────────────────────────────────────────
section("[2] 复用题库自带的 compare.py（口径零重写）");
const checkers = String(py.runPython("import compare; ','.join(compare.CHECKERS)"));
check("原样 import 成功，5 种 checker 齐全",
  checkers === "standard,ignore_trailing,token,float,oneof", checkers);

const cmpFn = py.runPython("import compare; compare.compare");
function cmpCase(expected, actual, checker = "standard", eps = 1e-6) {
  const r = cmpFn(expected, actual, checker, eps);
  return { ok: r.ok === true, kind: String(r.kind) };
}

const cmpCases = [
  ["换行归一化 CRLF→LF", "1\n2\n", "1\r\n2\r\n", "standard", "ok"],
  ["末尾多余空行", "3\n", "3\n\n\n", "standard", "ok"],
  ["行尾空白", "3\n", "3   \n", "standard", "ok"],
  ["token 口径折叠空白", "1 2", "1    2", "token", "ok"],
  ["float eps 容差", "0.333333", "0.3333333", "float", "ok"],
  ["oneof 备选答案命中", "|B\n|b", "B", "oneof", "ok"],
  ["内容对格式乱 → PE", "1\n2", "1 2", "standard", "pe"],
  ["真不一样 → WA", "1", "2", "standard", "wa"],
];
for (const [label, e, a, ck, want] of cmpCases) {
  const got = cmpCase(e, a, ck);
  const ok = want === "ok" ? got.ok : got.kind === want;
  check(label, ok, `kind=${got.kind}`);
}

// ────────────────────────────────────────────────────────────
section("[3] 真题全量：参考解 × 样例");
const fx = JSON.parse(readFileSync(path.join(HERE, "fixtures.json"), "utf8"));
const judge = py.runPython("from driver import judge; judge");
console.log(`    题库夹具：${fx.count} 道题 / ${fx.total_samples} 个样例（${fx.generated_at}）`);

const times = [];
let nCases = 0, nAc = 0;
const notAc = [];

for (const item of fx.items) {
  for (const sc of item.samples) {
    nCases++;
    const raw = judge(item.reference_solution, sc.stdin ?? "", sc.expected_stdout ?? "",
                      item.checker, item.float_eps);
    const r = JSON.parse(String(raw));
    times.push(r.ms);
    if (r.verdict === "AC") nAc++;
    else notAc.push({ id: item.id, title: item.title, checker: item.checker, r });
  }
}

console.log(`    跑完 ${nCases} 个样例，用时合计 ${Math.round(times.reduce((a, b) => a + b, 0))} ms`);
check("参考解全部 AC", nAc === nCases, `${nAc}/${nCases}`);
for (const f of notAc.slice(0, 8)) {
  console.log(`      ✗ 题 ${f.id}《${f.title}》[${f.checker}] → ${f.r.verdict}  ${f.r.detail}`);
  if (f.r.stderr) console.log(`        stderr: ${f.r.stderr.trim().split("\n").slice(-3).join(" | ")}`);
  if (f.r.stdout) console.log(`        stdout: ${JSON.stringify(f.r.stdout.slice(0, 120))}`);
}
if (notAc.length > 8) console.log(`      …还有 ${notAc.length - 8} 个未列出`);

times.sort((a, b) => a - b);
const pct = (p) => times[Math.min(times.length - 1, Math.floor(times.length * p))];
console.log(`    单样例耗时：P50 ${pct(0.5).toFixed(1)} ms · P95 ${pct(0.95).toFixed(1)} ms · 最大 ${times[times.length - 1].toFixed(1)} ms`);

// ────────────────────────────────────────────────────────────
section("[4] 反例：恒定错解必须全部判错");
const WRONG = 'print("__NOT_THE_ANSWER__")';
let nWrongAc = 0;
for (const item of fx.items) {
  for (const sc of item.samples) {
    const r = JSON.parse(String(
      judge(WRONG, sc.stdin ?? "", sc.expected_stdout ?? "", item.checker, item.float_eps)));
    if (r.verdict === "AC") nWrongAc++;
  }
}
check("错解没有任何一个被误判为 AC", nWrongAc === 0, `误判 AC ${nWrongAc} 个`);

// ────────────────────────────────────────────────────────────
section("汇总");
console.log(`    Pyodide 冷启动        ${bootMs} ms`);
console.log(`    通过 ${nPass} 项，失败 ${nFail} 项`);
if (nFail) console.log(`    失败项：${fails.join(" / ")}`);
console.log(`\n    ${nFail === 0 ? "★ 结论：前端判 Python 题的链路成立" : "✗ 结论：还有问题没解决"}\n`);

process.exit(nFail === 0 ? 0 : 1);
