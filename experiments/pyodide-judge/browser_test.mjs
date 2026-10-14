/**
 * headless Chrome 验证「浏览器版判题」。
 *
 * 为什么必须用真浏览器
 * --------------------
 * 项目现有的 `ui_smoke.mjs` 用 jsdom —— 它**跑不了 WebAssembly，也没有 Worker**。
 * 所以浏览器版只能拿真 Chrome 验。用 `puppeteer-core` + 系统已装的 Chrome，
 * 不下载浏览器（省 150MB，也免得卡在网络上）。
 *
 * 验证 6 项，正反都有
 * -------------------
 *   [1] 引擎就绪：页面里跑的是真 CPython
 *   [2] 单题参考解 → AC
 *   [3] 错解 → WA（证比对不是恒真）
 *   [4] 全量：56 题 109 样例参考解 → 全 AC
 *   [5] 死循环 → TLE，且**主线程没被冻住**（这是放 Worker 的全部意义）
 *   [6] 被终止后引擎能自愈，继续正常判题
 *
 * 用法：node browser_test.mjs
 */
import puppeteer from "puppeteer-core";

const CHROME = process.env.CHROME_PATH
  || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const POC_URL = process.env.POC_URL || "http://127.0.0.1:8899/";

let nPass = 0, nFail = 0;
const fails = [];
function check(label, ok, detail = "") {
  if (ok) { nPass++; console.log(`  [PASS] ${label}${detail ? "  → " + detail : ""}`); }
  else { nFail++; fails.push(label); console.log(`  [FAIL] ${label}${detail ? "  → " + detail : ""}`); }
}
function section(t) { console.log("\n" + "─".repeat(64) + "\n" + t + "\n" + "─".repeat(64)); }

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});

try {
  const page = await browser.newPage();
  const noisy = [];
  page.on("console", (m) => noisy.push("console: " + m.text()));
  page.on("pageerror", (e) => noisy.push("pageerror: " + e.message));

  section("[0] 打开页面");
  await page.goto(POC_URL, { waitUntil: "load", timeout: 30000 });
  console.log(`  URL ${POC_URL}`);

  section("[1] 引擎就绪");
  try {
    await page.waitForFunction(
      () => document.querySelector("#status")?.classList.contains("ok"),
      { timeout: 90000, polling: 250 });
  } catch (err) {
    // 等待超时时必须把现场打出来，否则只能看到一个光秃秃的 TimeoutError
    console.log("  等待超时，诊断信息：");
    const st = await page.$eval("#status", (el) => el.textContent).catch(() => "(取不到)");
    console.log("    #status =", st);
    for (const l of noisy.slice(0, 25)) console.log("    " + l);
    throw err;
  }
  const status = await page.$eval("#status", (el) => el.textContent);
  check("浏览器内加载出真 CPython", /CPython \d+\.\d+\.\d+/.test(status), status);

  const bankSize = await page.evaluate(() => window.__poc.bank.items.length);
  check("题库已载入", bankSize > 0, `${bankSize} 道题`);

  section("[2] 单题判题（参考解）");
  const first = await page.evaluate(() => {
    const it = window.__poc.bank.items[0];
    return { id: it.id, title: it.title, ref: it.reference_solution,
             s: it.samples[0], checker: it.checker, eps: it.float_eps };
  });
  const ac = await page.evaluate(async (p) => window.__poc.judgeCase({
    code: p.ref, stdin: p.s.stdin ?? "", expected: p.s.expected_stdout ?? "",
    checker: p.checker, eps: p.eps,
  }, 10000), first);
  check(`题 #${first.id}《${first.title}》参考解判 AC`,
    ac.verdict === "AC", `${ac.verdict} · ${ac.ms} ms`);

  section("[3] 反例：错解必须判 WA");
  const wa = await page.evaluate(async (p) => window.__poc.judgeCase({
    code: 'print("__NOT_THE_ANSWER__")',
    stdin: p.s.stdin ?? "", expected: p.s.expected_stdout ?? "",
    checker: p.checker, eps: p.eps,
  }, 10000), first);
  check("错解被判 WA（不是恒真）", wa.verdict === "WA", `${wa.verdict} · ${wa.ms} ms`);

  section("[4] 全量：所有题 × 所有样例");
  const full = await page.evaluate(async () => {
    const out = { total: 0, ac: 0, bad: [], ms: 0, max: 0 };
    for (const it of window.__poc.bank.items) {
      for (const s of it.samples) {
        out.total++;
        const r = await window.__poc.judgeCase({
          code: it.reference_solution, stdin: s.stdin ?? "",
          expected: s.expected_stdout ?? "", checker: it.checker, eps: it.float_eps,
        }, 15000);
        out.ms += r.ms;
        out.max = Math.max(out.max, r.ms);
        if (r.verdict === "AC") out.ac++;
        else if (out.bad.length < 6) out.bad.push({ id: it.id, v: r.verdict, d: r.detail });
      }
    }
    return out;
  });
  check(`参考解全部 AC`, full.ac === full.total, `${full.ac}/${full.total}`);
  for (const b of full.bad) console.log(`      ✗ 题 ${b.id} → ${b.v} ${b.d}`);
  console.log(`  判题合计耗时 ${Math.round(full.ms)} ms · 单样例最大 ${full.max.toFixed(1)} ms`);

  section("[5] 死循环必须能被中断");
  const t0 = Date.now();
  const tle = await page.evaluate(async () => window.__poc.judgeCase({
    code: "while True:\n    pass",
    stdin: "", expected: "", checker: "standard", eps: 1e-6,
  }, 2000));
  const waited = Date.now() - t0;
  check("返回 TLE", tle.verdict === "TLE", `${tle.verdict} · 实际等待 ${waited} ms`);
  check("中断及时（< 8 秒）", waited < 8000, `${waited} ms`);

  // ★ 最关键的一条：主线程必须还活着。冻住了这里就 evaluate 不出来。
  const alive = await page.evaluate(() => 1 + 1);
  check("主线程未被冻结（页面仍可执行脚本）", alive === 2);

  section("[6] 被强制终止后能自愈");
  const again = await page.evaluate(async (p) => window.__poc.judgeCase({
    code: p.ref, stdin: p.s.stdin ?? "", expected: p.s.expected_stdout ?? "",
    checker: p.checker, eps: p.eps,
  }, 15000), first);
  check("引擎自动重建后继续正常判题", again.verdict === "AC", `${again.verdict} · ${again.ms} ms`);

  const errs = noisy.filter((x) => x.startsWith("pageerror"));
  check("全程无 JS 异常", errs.length === 0, errs.slice(0, 3).join(" | "));

  section("汇总");
  console.log(`  通过 ${nPass} 项，失败 ${nFail} 项`);
  if (nFail) console.log(`  失败项：${fails.join(" / ")}`);
  console.log(`\n  ${nFail === 0
    ? "★ 结论：浏览器内判题链路完整成立，且死循环不会冻住页面"
    : "✗ 结论：还有问题"}\n`);
} finally {
  await browser.close();
}

process.exit(nFail === 0 ? 0 : 1);
