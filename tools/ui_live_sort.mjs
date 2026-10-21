/* 线上验收：真浏览器检查「按难易程度排序」改造在**已部署站点**上是否真的生效。
 *
 * 与 tools/ui_test_sort_order.mjs 的分工：
 *   ui_test_sort_order.mjs  → 跑本地 docs/ 或本地反代 uvicorn，验代码
 *   ui_live_sort.mjs（本文件）→ 跑真实 GitHub Pages 线上地址，验**部署结果**
 *
 * 检查四件事：
 *   1. 分组顺序 = 教学路径序号递增（用前端自己的 SECTION_RANKS 判）
 *   2. 组内题目难度升序（从 td.c-df 的 ★ 数读）
 *   3. 题号（CP-/PY-/DS-/LX-）随新顺序重编且严格递增
 *   4. 分组标题带「均难」标签
 *
 * 环境变量：
 *   PTA_SITE_URL   站点地址，默认 https://cosy119.github.io/my-pta/
 *   CHROME_PROXY   Chrome 代理，默认 http://127.0.0.1:10808
 *   CHROME_PATH    Chrome 可执行文件路径
 *
 * 注意两个坑：
 *   ① 线上 problems.json 有 9MB，首次下载走代理可能上百秒 → protocolTimeout 要放宽
 *   ② Pages 静态站没有后端，apiBase() 会去打 /api/* 拿到 404（前端自动降级为
 *      读 problems.json 的离线模式）。这个 404 属于既有设计，不算失败。
 */
import path from 'node:path';
import { createRequire } from 'node:module';

const repo = process.cwd();
const moduleDir = path.join(repo, 'experiments/pyodide-judge/node_modules');
const require = createRequire(path.join(moduleDir, 'noop.js'));
const puppeteer = require('puppeteer-core');

const SITE = (process.env.PTA_SITE_URL || 'https://cosy119.github.io/my-pta/').replace(/\/*$/, '/');
const PROXY = process.env.CHROME_PROXY || 'http://127.0.0.1:10808';

const SUBJ = [
  { key: 'cpp', pfx: 'CP' },
  { key: 'python', pfx: 'PY' },
  { key: 'ds', pfx: 'DS' },
  { key: 'linux', pfx: 'LX' },
];

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new',
  protocolTimeout: 900000,
  args: ['--no-sandbox', '--disable-dev-shm-usage', `--proxy-server=${PROXY}`],
});

const page = await browser.newPage();
/* 三类要分开：
 *   pageErrors  —— 真 JS 异常（前端代码炸了），算失败
 *   resErrors   —— 资源加载失败（404 / 连接中断），静态站 + 代理环境下属网络噪音
 *   notFound    —— 404 的具体 URL，用来确认「除了预期的 /api/* 没有别的资源丢了」
 */
const pageErrors = [];
const resErrors = [];
const notFound = [];
page.on('pageerror', e => pageErrors.push('pageerror: ' + String(e)));
page.on('console', m => { if (m.type() === 'error') resErrors.push(m.text()); });
page.on('requestfailed', r => resErrors.push('requestfailed: ' + r.url() + ' ' + (r.failure()?.errorText || '')));
page.on('response', r => { if (r.status() === 404) notFound.push(r.url()); });

let fail = 0;

/* 代理偶发瞬时失败是常态（ERR_TIMED_OUT），导航失败要重试而不是直接判死 */
async function gotoWithRetry(url, tries = 3) {
  let last = null;
  for (let i = 1; i <= tries; i++) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 300000 });
      return;
    } catch (e) {
      last = e;
      console.log(`   (第 ${i}/${tries} 次导航失败：${String(e).split('\n')[0]}，重试…)`);
      await new Promise(r => setTimeout(r, 5000));
    }
  }
  throw last;
}

for (const s of SUBJ) {
  await gotoWithRetry(`${SITE}#/set/${s.key}`);
  await page.waitForSelector('.grpbox', { timeout: 600000 });

  const r = await page.evaluate((s) => {
    const boxes = [...document.querySelectorAll('.grpbox')];
    // SECTION_RANKS 是顶层 let 声明，不挂在 window 上，要用裸标识符取
    const RANKS = (typeof SECTION_RANKS !== 'undefined') ? SECTION_RANKS : {};
    const groups = boxes.map(b => {
      const name = b.dataset.g;
      const rows = [...b.querySelectorAll('tbody tr')];
      const codes = rows.map(tr => (tr.querySelector('td.c-no') || {}).textContent?.trim() || '');
      const diffs = rows.map(tr => {
        const td = tr.querySelector('td.c-df');
        if (!td) return 0;
        return [...td.querySelectorAll('.stars > *')].filter(e => !e.classList.contains('off')).length;
      });
      const avg = [...b.querySelectorAll('.grpHead .pill')].map(e => e.textContent || '').find(t => t.includes('均难')) || '';
      return { name, rank: (RANKS[s.key] || {})[name] ?? null, codes, diffs, avg };
    });
    const allCodes = groups.flatMap(g => g.codes);
    // 题号按「前缀 + 数字后缀」比，不能直接比字符串（CP-100 < CP-99 会误判）
    const numOf = c => { const m = /-(\d+)$/.exec(c || ''); return m ? parseInt(m[1], 10) : -1; };
    return {
      groups: groups.length,
      rankAllKnown: groups.every(g => g.rank !== null),
      rankInc: groups.every((g, i) => i === 0 || g.rank > groups[i - 1].rank),
      firstRank: groups[0]?.rank, lastRank: groups[groups.length - 1]?.rank,
      diffViol: groups.filter(g => g.diffs.some((d, i) => i && d < g.diffs[i - 1])).length,
      avgLabels: groups.filter(g => g.avg.includes('均难')).length,
      codeFirst: allCodes[0] || '', codeLast: allCodes[allCodes.length - 1] || '',
      codeInc: allCodes.every((c, i) => i === 0 || numOf(c) > numOf(allCodes[i - 1])),
      total: allCodes.length,
    };
  }, s);

  const ok = r.rankAllKnown && r.rankInc && r.diffViol === 0 && r.avgLabels === r.groups && r.codeInc && r.total > 0;
  if (!ok) fail++;
  console.log(`\n[${ok ? 'PASS' : 'FAIL'}] ${s.key}`);
  console.log(`   分组 ${r.groups}（序号 ${r.firstRank}→${r.lastRank}，递增 ${r.rankInc}）| 组内难度升序违规 ${r.diffViol}`);
  console.log(`   题号 ${r.codeFirst} → ${r.codeLast}（共 ${r.total} 题，递增 ${r.codeInc}）| 均难标签 ${r.avgLabels}/${r.groups}`);
}

/* ---- 排序方式：在线上切一次「难度」档，确认部署产物真的带这个功能 ---- */
console.log('\n--- 排序方式（线上实测，cpp 线）---');
await gotoWithRetry(`${SITE}#/set/cpp`);
await page.waitForSelector('.grpbox');
const sortCheck = await page.evaluate(async () => {
  const snap = () => [...document.querySelectorAll('.grpbox')].map(b => ({
    name: b.dataset.g,
    codes: [...b.querySelectorAll('tbody tr td.c-no')].map(t => t.textContent.trim()),
    diffs: [...b.querySelectorAll('tbody tr td.c-df')].map(td =>
      [...td.querySelectorAll('.stars > *')].filter(e => !e.classList.contains('off')).length),
  }));
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const sel = document.getElementById('sortSelect');
  if (!sel) return { error: '线上没有 #sortSelect（Pages 还没重建完？）' };

  const opts = [...sel.options].map(o => o.textContent.trim());
  const chapter = snap();
  sel.value = 'difficulty'; sel.dispatchEvent(new Event('change')); await wait(500);
  const up = snap();
  sel.value = 'difficulty_desc'; sel.dispatchEvent(new Event('change')); await wait(500);
  const dn = snap();
  sel.value = 'chapter'; sel.dispatchEvent(new Event('change')); await wait(500);
  const back = snap();

  const asc = a => a.every((v, i) => i === 0 || v >= a[i - 1]);
  const desc = a => a.every((v, i) => i === 0 || v <= a[i - 1]);
  const chapterCodes = chapter.flatMap(g => g.codes).slice().sort();
  const c2 = up[0] ? up[0].codes.slice().sort() : [];
  return {
    opts,
    chapterGroups: chapter.length,
    upGroups: up.length, upMono: up[0] ? asc(up[0].diffs) : false, upName: up[0]?.name || '',
    dnGroups: dn.length, dnMono: dn[0] ? desc(dn[0].diffs) : false,
    sameSet: JSON.stringify(chapterCodes) === JSON.stringify(c2),
    backGroups: back.length,
    backSame: back.map(g => g.name).join('|') === chapter.map(g => g.name).join('|'),
  };
});

if (sortCheck.error) {
  console.log('  [FAIL] ' + sortCheck.error);
  fail++;
} else {
  const rows = [
    ['排序下拉三档齐全', JSON.stringify(sortCheck.opts) === JSON.stringify(['按章节', '难度 易→难', '难度 难→易']), sortCheck.opts.join(' | ')],
    ['按章节仍分组显示', sortCheck.chapterGroups > 1, sortCheck.chapterGroups + ' 组'],
    ['难度 易→难 合并为单组', sortCheck.upGroups === 1, sortCheck.upGroups + ' 组｜' + sortCheck.upName],
    ['难度 易→难 组内单调不减', sortCheck.upMono === true, ''],
    ['难度 难→易 组内单调不增', sortCheck.dnMono === true, ''],
    ['难度档题目集合与章节档一致', sortCheck.sameSet === true, ''],
    ['切回按章节分组数复原', sortCheck.backGroups === sortCheck.chapterGroups, sortCheck.backGroups + ' vs ' + sortCheck.chapterGroups],
    ['切回按章节顺序不变', sortCheck.backSame === true, ''],
  ];
  for (const [name, ok, extra] of rows) {
    if (!ok) fail++;
    console.log(`  [${ok ? 'PASS' : 'FAIL'}] ${name}${extra ? '  -- ' + extra : ''}`);
  }
}

// Pages 静态站没有后端，/api/* 必然 404（前端自动降级），不算失败
const apiMiss = notFound.filter(u => /\/api\//.test(u));
const realMiss = notFound.filter(u => !/\/api\//.test(u));
console.log(`\n真 JS 异常: ${pageErrors.length}`);
pageErrors.slice(0, 8).forEach(e => console.log('   ' + e));
console.log(`资源加载错误: ${resErrors.length}（代理抖动 / 静态站无后端，属噪音，不判失败）`);
console.log(`404: 共 ${notFound.length}（其中 /api/* ${apiMiss.length} 个 = 静态站无后端，属预期；其余 ${realMiss.length} 个）`);
[...new Set(realMiss)].slice(0, 8).forEach(u => console.log('   ! ' + u));

await browser.close();
// 只按「真 JS 异常 + 非 /api/ 的 404」判失败；资源噪音与 /api 404 不算
process.exit(fail || pageErrors.length || realMiss.length ? 1 : 0);
