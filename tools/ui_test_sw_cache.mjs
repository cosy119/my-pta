/* =============================================================================
   Service Worker 缓存 + 超大测试点按需拉取（真 Chrome，跑 docs/ 发布产物）
   -----------------------------------------------------------------------------
   背景：GitHub Pages 对所有静态文件写死 `Cache-Control: max-age=600`，站点侧改不了。
   实测国内直连 `bank/index.json` gzip 后 62 KB 要 14 秒；10 分钟内重开能命中浏览器
   缓存（1.9 秒），超过就要重下 —— 体感就是「每次打开都要等十几秒」。

   本脚本验四件事（缺一条这类改动就是白做）：
     1. sw.js 能注册并接管页面
     2. 二次访问时 index.html / bank/index.json 由 SW 提供（fromServiceWorker）
     3. 拆出去的测试点（bank/cases/<id>.json）进题时才拉，且拉到的点数正确
     4. **SW 不会把用户锁在旧版本上** —— 改完 HTML 刷新必须立刻看到新版

   第 4 条最容易翻车：network-first 里 `fetch(req)` 不写 `cache:'no-cache'` 的话，
   浏览器自己的 HTTP 缓存（Pages 那个 max-age=600）会先答话，SW 拿到的还是旧版，
   结果「部署了但用户永远看不到新版」。这条是有过真实失败复现的，别删。

   前置：
       python tools/serve_docs.py 8802 docs          # ★ 不能用 python -m http.server
       PTA_LOCAL=http://127.0.0.1:8802/ node tools/ui_test_sw_cache.mjs

   ★ 为什么不能用 `python -m http.server`：它把 .mjs 当 text/plain，module worker
     里的 import 会被浏览器拒绝，页面报「Python Worker 加载失败」。见 serve_docs.py。
   ============================================================================= */
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(path.join(process.cwd(), 'experiments/pyodide-judge/node_modules', 'noop.js'));
const puppeteer = require('puppeteer-core');

const BASE = (process.env.PTA_LOCAL || 'http://127.0.0.1:8801/').replace(/\/*$/, '/');
const HTML = process.env.PTA_HTML || 'docs/index.html';
const PROFILE = mkdtempSync(join(tmpdir(), 'pta-sw-'));

/* 拆出来的题：取 index.json 里记录的第一道，别写死 id（题库会变） */
const idx = JSON.parse(readFileSync(path.join(path.dirname(HTML), 'bank/index.json'), 'utf8'));
const SPLIT_ID = (idx.cases_split || [])[0];
const TOTAL = (idx.items || []).length;

let fail = 0;
const ok = (n, c, d = '') => { console.log(`  ${c ? '✓' : '✗'} ${n}${d ? '  — ' + d : ''}`); if (!c) fail++; };
const sleep = ms => new Promise(r => setTimeout(r, ms));

if (!SPLIT_ID) {
  console.log('这份产物里没有拆分题（bank/cases/ 为空），先跑 export_static.py --with-cases');
  process.exit(2);
}

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new',
  userDataDir: PROFILE,                     // 固定 profile → SW 与缓存跨页面复用
  protocolTimeout: 900000,
  args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
});

/* ---------- 1. 首访：注册并接管 ---------- */
console.log(`\n[1] 首次访问 ${BASE}`);
let page = await browser.newPage();
await page.goto(BASE + '#/set/cpp', { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.waitForSelector('.grpbox', { timeout: 300000 });

const reg = await page.evaluate(async () => {
  if (!('serviceWorker' in navigator)) return { supported: false };
  const r = await navigator.serviceWorker.getRegistration();
  return { supported: true, scope: r ? r.scope : null, active: !!(r && r.active) };
});
ok('浏览器支持 Service Worker', reg.supported);
ok('sw.js 已注册并激活', !!reg.active, reg.scope || '');

await page.waitForFunction(() => !!navigator.serviceWorker.controller, { timeout: 30000 }).catch(() => {});
ok('当前页已被 SW 接管', await page.evaluate(() => !!navigator.serviceWorker.controller));
const firstMs = await page.evaluate(() => performance.now());
await page.close();

/* ---------- 2. 再访问：走缓存 ---------- */
console.log('\n[2] 再次访问（应走 SW 缓存）');
page = await browser.newPage();
const viaSW = [];
page.on('response', r => {
  const u = r.url();
  if (!u.startsWith(BASE)) return;
  let sw = false;
  try { sw = r.fromServiceWorker(); } catch {}
  if (/index\.html$|\/bank\/index\.json$/.test(u)) viaSW.push({ f: u.replace(BASE, '') || 'index.html', sw });
});

const t0 = Date.now();
await page.goto(BASE + '#/set/cpp', { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.waitForSelector('.grpbox', { timeout: 300000 });
const ms = Date.now() - t0;
ok('页面正常渲染', true, `就绪 ${ms} ms`);
const idxHit = viaSW.find(x => x.f.startsWith('bank/index.json'));
ok('bank/index.json 由 SW 提供', !!(idxHit && idxHit.sw),
   viaSW.map(x => `${x.f}:${x.sw ? 'SW' : 'net'}`).join(' | ') || '（无请求记录）');

const n = await page.evaluate(() => (typeof PROBLEMS !== 'undefined' ? PROBLEMS.length : 0));
ok('题目数正确', n === TOTAL, `${n} / ${TOTAL} 道`);

/* ---------- 3. 拆分题：按需拉测试点 ---------- */
console.log(`\n[3] 拆分题 #${SPLIT_ID}（测试点单独成文件）`);
const caseReqs = [];
page.on('response', r => { if (/\/bank\/cases\//.test(r.url())) caseReqs.push({ f: r.url().split('/').pop(), st: r.status() }); });

const t1 = Date.now();
await page.goto(`${BASE}#/p/${SPLIT_ID}`, { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.waitForFunction((i) => typeof CUR !== 'undefined' && CUR && CUR.id === i, { timeout: 180000 }, SPLIT_ID);

const split = await page.evaluate(() => ({
  split: !!CUR.cases_split,
  bytes: CUR.cases_bytes || 0,
  hasStatement: !!(CUR.statement_md && CUR.statement_md.length),
  btnRow: document.getElementById('btnRow')?.textContent || '',
}));
ok('题面已渲染（不等测试点）', split.hasStatement, `${Date.now() - t1} ms 内`);
ok('标记为拆分题', split.split, `${(split.bytes / 1048576).toFixed(2)} MB`);
console.log('     刚进题按钮区：' + split.btnRow.replace(/\s+/g, ' ').slice(0, 60));

await page.waitForFunction(() => CUR && (CUR.cases || []).length > 0, { timeout: 180000 }).catch(() => {});
const got = await page.evaluate(() => ({ cases: (CUR.cases || []).length }));
ok('测试点已拉到', got.cases > 0, `${got.cases} 个点`);
ok('确实请求了 bank/cases/', caseReqs.some(r => String(r.f).startsWith(String(SPLIT_ID))),
   JSON.stringify(caseReqs.slice(0, 2)));

const btnAfter = await page.evaluate(() => document.getElementById('btnRow')?.textContent || '');
ok('按钮从「加载中」变成可判题', !btnAfter.includes('测试点加载中') && /提交并判题|提交评测/.test(btnAfter),
   btnAfter.replace(/\s+/g, ' ').slice(0, 50));

/* ---------- 4. 普通题不受影响 ---------- */
console.log('\n[4] 普通题（测试点没拆）');
await page.goto(BASE + '#/p/1', { waitUntil: 'domcontentloaded', timeout: 300000 });
await page.waitForFunction(() => typeof CUR !== 'undefined' && CUR && CUR.id === 1, { timeout: 180000 });
const p1 = await page.evaluate(() => ({ split: !!CUR.cases_split, cases: (CUR.cases || []).length }));
ok('#1 不是拆分题', !p1.split);
ok('#1 测试点直接来自科目包', p1.cases > 0, `${p1.cases} 个点`);

/* ---------- 5. 不能被锁在旧版本 ---------- */
console.log('\n[5] 改完 HTML 刷新，必须看到新版（SW 不能卡住更新）');
const MARK = '<!-- sw-update-probe-' + Date.now() + ' -->';
const orig = readFileSync(HTML, 'utf8');
try {
  writeFileSync(HTML, orig.replace('</body>', MARK + '\n</body>'), 'utf8');
  await sleep(400);                       // 让文件 mtime 落地
  const p2 = await browser.newPage();
  await p2.goto(BASE + '#/set/cpp', { waitUntil: 'domcontentloaded', timeout: 300000 });
  await p2.waitForSelector('.grpbox', { timeout: 300000 });
  const hit = await p2.evaluate(() => document.documentElement.outerHTML.includes('sw-update-probe-'));
  ok('刷新即拿到新版本', hit, hit ? '' : '★ 检查 networkFirst 里的 cache:"no-cache" 是否被去掉了');
  await p2.close();
} finally {
  writeFileSync(HTML, orig, 'utf8');
}

/* ---------- 6. 缓存桶 ---------- */
console.log('\n[6] 缓存桶');
const buckets = await page.evaluate(async () => (await caches.keys()).filter(k => k.startsWith('pta-')));
ok('有 pta-* 缓存桶', buckets.length > 0, buckets.join(', '));

await browser.close();
console.log(`\n${fail ? '✗ 失败 ' + fail + ' 项' : '✓ 全部通过'}`);
process.exit(fail ? 1 : 0);
