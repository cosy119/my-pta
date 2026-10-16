/* ===================================================================
   笔记区（Obsidian → 静态站）—— 真 Chrome 端到端测试

   为什么必须真浏览器
   ------------------
   笔记区全是**交互**：hash 路由（`#/notes/py-05-05#4.2 切片：…` 这种带锚点的
   两层 `#`）、动态 import 渲染器、`<details>` 展开、搜索结果点击、锚点滚动。
   jsdom 里没有布局也没有真实滚动，测这些等于没测。

   它验的是**发布产物**：直接服务 `docs/`，跟 GitHub Pages 上那一份是同一批
   文件 —— 所以顺带证明了「公开静态网页无需额外服务即可使用」。
   ★ 全程不连后端：笔记区本来就是离线可用的。

   用法（仓库根目录）：
     NODE_MODULES_DIR=<含 puppeteer-core 的目录> node tools/ui_e2e_notes.mjs

   默认用系统 Chrome，不下载浏览器。
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

function loadDep(name, extra) {
  const tries = [createRequire(import.meta.url)];
  const dirs = [process.env.NODE_MODULES_DIR, ...(extra || [])].filter(Boolean);
  for (const d of dirs) tries.push(createRequire(path.join(d, 'noop.js')));
  for (const req of tries) {
    try { return req(name); } catch (e) { /* 试下一个 */ }
  }
  console.error('找不到 ' + name + '。\n'
    + '  装：npm install ' + name + '\n'
    + '  然后：NODE_MODULES_DIR=<含它的目录> node tools/ui_e2e_notes.mjs');
  process.exit(3);
}
const puppeteer = loadDep('puppeteer-core', [path.join(process.cwd(), 'experiments', 'pyodide-judge', 'node_modules')]);

const CHROME_PATHS = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
];
const CHROME = CHROME_PATHS.find(p => fs.existsSync(p));
if (!CHROME) { console.error('找不到系统 Chrome/Edge'); process.exit(3); }

const CWD = process.cwd();
const DOCS = path.join(CWD, 'docs');
const NOTES = path.join(DOCS, 'notes');

if (!fs.existsSync(path.join(NOTES, 'index.json'))) {
  console.error('docs/notes 还没生成。先跑：\n'
    + '  python tools/export_notes.py\n  python tools/export_static.py --with-cases');
  process.exit(5);
}

let PASS = 0;
const FAIL = [];
function check(name, cond, extra) {
  if (cond) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra !== undefined ? '  ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

function serveDir(root) {
  const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
                 '.gz': 'application/octet-stream', '.wasm': 'application/wasm' };
  const srv = http.createServer((req, res) => {
    const p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    const f = path.normalize(path.join(root, p === '/' ? 'index.html' : p));
    if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
      res.statusCode = 404; return res.end('404');
    }
    res.setHeader('Content-Type', (MIME[path.extname(f)] || 'application/octet-stream') + '; charset=utf-8');
    res.end(fs.readFileSync(f));
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r(srv)));
}

/* ---------------- 夹具：从产物里挑，别写死 ---------------- */
const INDEX = JSON.parse(fs.readFileSync(path.join(NOTES, 'index.json'), 'utf8'));
const BANK = JSON.parse(fs.readFileSync(path.join(DOCS, 'problems.json'), 'utf8'));

function scanPages() {
  const dir = path.join(NOTES, 'p');
  return fs.readdirSync(dir).map(f => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
}
const PAGES = scanPages();
const bySlug = s => PAGES.find(p => p.slug === s);

const FOLD_PAGE = PAGES.find(p => /:::callout \w+ fold/.test(p.md) && /```\w+/.test(p.md));
const LINK_PAGE = PAGES.find(p => p.slug.endsWith('-00') && /\(#\/notes\//.test(p.md));
const ANCHOR_PAGE = PAGES.find(p => /\(#\/notes\/[a-z0-9-]+#/.test(p.md));
if (!FOLD_PAGE || !LINK_PAGE) {
  console.error('产物里找不到合适的夹具（折叠 callout / 站内链接），测试无法进行');
  process.exit(5);
}

const PY_PROB = BANK.items.find(x => x.subject === 'python' && /第\s*\d+\s*讲/.test(x.source_section || ''));

async function main() {
  const srv = await serveDir(DOCS);
  const BASE = 'http://127.0.0.1:' + srv.address().port + '/';
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 950 });

  const jsErrors = [];
  const badRes = [];
  page.on('pageerror', e => jsErrors.push(String(e.message || e)));
  page.on('console', m => {
    if (m.type() !== 'error') return;
    /* 离线模式下 /api/* 必然 404 —— 那是设计如此（前端会退到 problems.json），
       不是异常。真要紧的是笔记自己的资源加载。 */
    if (/Failed to load resource/.test(m.text())) return;
    jsErrors.push('console: ' + m.text());
  });
  page.on('response', r => {
    if (r.status() >= 400 && /\/(notes|editor)\//.test(r.url())) badRes.push(r.status() + ' ' + r.url());
  });
  const hosts = new Set();
  page.on('request', r => { try { hosts.add(new URL(r.url()).host); } catch (e) {} });

  const gotoHash = async (h, sel) => {
    await page.evaluate(x => { location.hash = x; }, h);
    if (sel) await page.waitForSelector(sel, { timeout: 25000 });
    await sleep(150);
  };

  console.log('夹具：折叠 callout → ' + FOLD_PAGE.slug + '、站内链接 → ' + LINK_PAGE.slug
    + '、题目 → #' + (PY_PROB ? PY_PROB.id : '（无）') + '\n');

  /* ---------------- [1] 笔记首页 ---------------- */
  console.log('[1] 笔记首页（#/notes）');
  await page.goto(BASE + '#/notes', { waitUntil: 'load' });
  await page.waitForSelector('.noteLineCard', { timeout: 25000 });
  check('三张学习线卡片都渲染出来', (await page.$$('.noteLineCard')).length === INDEX.lines.length,
    (await page.$$('.noteLineCard')).length + ' 张 / 预期 ' + INDEX.lines.length);
  const lineNames = await page.$$eval('.noteLineName', els => els.map(e => e.textContent));
  check('线名与 index.json 一致', lineNames.join('|') === INDEX.lines.map(l => l.name).join('|'),
    lineNames.join('、'));
  const lecCount = await page.$$eval('.noteLec', els => els.length);
  const expectLec = INDEX.lines.reduce((a, l) => a + l.lectures.length, 0);
  check('讲次入口数量对得上', lecCount === expectLec, lecCount + ' / ' + expectLec);
  check('搜索框在', !!(await page.$('#notesSearchTop')));

  /* ---------------- [2] 单篇渲染 ---------------- */
  console.log('\n[2] 单篇渲染（' + FOLD_PAGE.slug + '）');
  await page.goto(BASE + '#/notes/' + FOLD_PAGE.slug, { waitUntil: 'load' });
  await page.waitForSelector('#noteBody', { timeout: 25000 });
  await page.waitForFunction(() => document.querySelectorAll('#noteBody .callout').length > 0,
    { timeout: 25000 });
  const title = await page.$eval('.noteTitle', e => e.textContent.trim());
  check('标题渲染出来', title.length > 0, title);
  check('面包屑有「笔记」入口', (await page.$eval('.crumb', e => e.textContent)).includes('笔记'));

  const nCallout = await page.$$eval('#noteBody .callout', els => els.length);
  const nFold = await page.$$eval('#noteBody details.callout', els => els.length);
  check('callout 渲染成块（2210 个那批）', nCallout > 0, nCallout + ' 个，其中折叠 ' + nFold);
  check('折叠 callout 用 <details>', nFold > 0);

  const hl = await page.$$eval('#noteBody pre code span[class^="hljs-"]', els => els.length);
  check('代码高亮真的出 token', hl > 0, hl + ' 个 span');
  check('代码块有语言类名', await page.$eval('#noteBody pre code', e => /\blanguage-\w+|\bhljs\b/.test(e.className)),
    await page.$eval('#noteBody pre code', e => e.className));

  const hIds = await page.$$eval('#noteBody h2,#noteBody h3', els => els.filter(e => e.id).length);
  check('标题都带 id（锚点要靠它）', hIds > 0, hIds + ' 个');

  /* 折叠的默认收起、点一下能展开 */
  if (nFold) {
    const before = await page.$eval('details.callout', d => d.open);
    await page.click('details.callout > summary');
    await sleep(160);
    const after = await page.$eval('details.callout', d => d.open);
    check('折叠 callout 默认收起、点击后展开', before === false && after === true,
      before + ' → ' + after);
  }

  /* ---------------- [3] 目录树 + 双链跳转 ---------------- */
  console.log('\n[3] 目录树与双链（' + LINK_PAGE.slug + '）');
  await page.goto(BASE + '#/notes/' + LINK_PAGE.slug, { waitUntil: 'load' });
  await page.waitForSelector('#noteBody', { timeout: 25000 });
  const treeLinks = await page.$$eval('.noteSide a', els => els.length);
  check('左侧目录树渲染出来', treeLinks > 3, treeLinks + ' 个链接');
  check('当前节在树里被标出来', !!(await page.$('.treePages a.on')));

  const firstLink = await page.$eval('#noteBody a[href^="#/notes/"]', e => e.getAttribute('href'));
  check('正文里有站内链接', !!firstLink, firstLink || '（没有）');
  if (firstLink) {
    await page.click('#noteBody a[href^="#/notes/"]');
    await page.waitForFunction(h => location.hash === h, { timeout: 25000 }, firstLink);
    await page.waitForSelector('#noteBody', { timeout: 25000 });
    await sleep(220);
    const target = firstLink.replace('#/notes/', '').split('#')[0];
    const shown = await page.evaluate(() => (document.querySelector('.noteTitle') || {}).textContent || '');
    const want = bySlug(target);
    check('点站内链接跳到了目标笔记', !!want && shown.trim() === want.title,
      JSON.stringify(shown.trim()) + ' vs ' + JSON.stringify(want ? want.title : '?'));
    /* ★ 同线消歧：`NN-01 一页速览` 在 Python 和 DS 里重名，
       索引页点过去的必须是自己那条线的，不能串到隔壁教材去。 */
    check('没有串到别的学习线（重名消歧）',
      firstLink.startsWith('#/notes/' + LINK_PAGE.line + '-'),
      firstLink + ' ← 源在 ' + LINK_PAGE.line + ' 线');
  }

  /* ---------------- [4] 锚点 ---------------- */
  if (ANCHOR_PAGE) {
    /* ★ 锚点属于**链接指向的那一篇**，不是链接所在的这一篇 ——
       第一版拿 ANCHOR_PAGE.slug 去开页，当然找不到那个标题（测试写错了，
       不是产品的问题）。 */
    const am = ANCHOR_PAGE.md.match(/\(#\/notes\/([a-z0-9-]+)#([^)]+)\)/);
    const targetSlug = am[1], anchor = am[2];
    console.log('\n[4] 锚点跳转（' + targetSlug + ' → #' + anchor.slice(0, 30) + '…）');
    await page.goto(BASE + '#/notes/' + targetSlug + '#' + anchor, { waitUntil: 'load' });
    await page.waitForSelector('#noteBody', { timeout: 25000 });
    await page.waitForFunction(() => document.querySelectorAll('.anchorFlash').length > 0,
      { timeout: 25000 }).catch(() => {});
    const flashed = await page.$$eval('.anchorFlash', els => els.length);
    const top = await page.evaluate(() => {
      const el = document.querySelector('.anchorFlash');
      return el ? Math.round(el.getBoundingClientRect().top) : -9999;
    });
    check('带锚点的链接能定位到那个标题', flashed > 0, '命中 ' + flashed + ' 个，距视口顶 ' + top + 'px');
  }

  /* ---------------- [5] 全文搜索 ---------------- */
  console.log('\n[5] 全文搜索');
  await page.goto(BASE + '#/notes', { waitUntil: 'load' });
  await page.waitForSelector('#notesSearchTop', { timeout: 25000 });
  await page.click('#notesSearchTop');
  await page.type('#notesSearchTop', '陷阱清单');
  /* ★ 等"有结果"或"确实没搜到"，不能接受"正在加载索引…"就放行 ——
     第一版就是被那个占位提示骗了，`nHit` 数出来是 0。 */
  await page.waitForFunction(() => {
    const o = document.getElementById('notesSearchTopOut');
    return o && (o.querySelector('.nsItem') || /没搜到/.test(o.textContent));
  }, { timeout: 90000 });
  const nHit = await page.$$eval('#notesSearchTopOut .nsItem', els => els.length);
  check('搜索出结果（首次会拉 3 MB 索引）', nHit > 0, nHit + ' 条');
  const marked = await page.$$eval('#notesSearchTopOut mark', els => els.length);
  check('命中词被高亮', marked > 0, marked + ' 处');
  if (nHit) {
    const href = await page.$eval('#notesSearchTopOut .nsItem', e => e.getAttribute('href'));
    /* 用直接派发点击：下拉面板是绝对定位、又靠着 sticky 顶栏，
       puppeteer 的可见性预检会判 "not clickable"，那是它的检查方式问题。 */
    await page.$eval('#notesSearchTopOut .nsItem', el => el.click());
    await page.waitForFunction(h => location.hash === h, { timeout: 25000 }, href);
    await page.waitForSelector('#noteBody', { timeout: 25000 });
    check('点搜索结果能直达那篇', (await page.$eval('.noteTitle', e => e.textContent)).length > 0,
      href);
  }

  /* ---------------- [6] 上下节导航 ---------------- */
  console.log('\n[6] 上一节 / 下一节');
  const midPage = PAGES.find(p => p.prev && p.next);
  await page.goto(BASE + '#/notes/' + midPage.slug, { waitUntil: 'load' });
  await page.waitForSelector('.notePager', { timeout: 25000 });
  const pager = await page.$$eval('.notePager a', els => els.map(e => e.getAttribute('href')));
  check('上下节导航两个方向都在', pager.length === 2, pager.join(' | '));
  check('导航指向的正是 prev/next',
    pager[0] === '#/notes/' + midPage.prev.slug && pager[1] === '#/notes/' + midPage.next.slug);

  /* ---------------- [7] 题目 ↔ 笔记 双向联动 ---------------- */
  if (PY_PROB) {
    console.log('\n[7] 题目 ↔ 笔记（题目 #' + PY_PROB.id + '）');
    await page.goto(BASE + '#/p/' + PY_PROB.id, { waitUntil: 'load' });
    await page.waitForSelector('.pill.p-note', { timeout: 25000 });
    const chipHref = await page.$eval('.pill.p-note', e => e.getAttribute('href'));
    const wantSlug = 'py-' + String(parseInt(/第\s*(\d+)\s*讲/.exec(PY_PROB.source_section)[1], 10)).padStart(2, '0') + '-00';
    check('题目页有「看本讲笔记」并指对讲次', chipHref === '#/notes/' + wantSlug,
      chipHref + ' / 预期 #/notes/' + wantSlug);
    await page.click('.pill.p-note');
    await page.waitForFunction(h => location.hash === h, { timeout: 25000 }, chipHref);
    await page.waitForSelector('#noteBody', { timeout: 25000 });
    check('点进去确实是那一讲的笔记',
      await page.evaluate(s => location.hash === '#/notes/' + s, wantSlug), await page.evaluate(() => location.hash));

    await page.waitForSelector('#noteProbs .notePbar', { timeout: 25000 });
    const ptext = await page.$eval('#noteProbs', e => e.textContent.trim());
    check('笔记页反过来显示「本讲配了 N 道题」', /本讲配了\s*\d+\s*道题/.test(ptext), ptext.slice(0, 40));
  }

  /* ---------------- [8] 干净度 ---------------- */
  console.log('\n[8] 干净度');
  const offsite = [...hosts].filter(h => !h.startsWith('127.0.0.1') && !h.includes('kaspersky'));
  check('全程只连本站，无第三方 CDN', offsite.length === 0, offsite.join(',') || '（零外部主机）');
  check('笔记自己的资源没有一个 404', badRes.length === 0, badRes.slice(0, 3).join(' | ') || '（全 200）');
  check('全程没有 JS 异常', jsErrors.length === 0, jsErrors.slice(0, 3).join(' | ') || '（无）');

  await browser.close();
  srv.close();

  console.log('\n通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项');
  if (FAIL.length) { console.log('未通过：'); FAIL.forEach(f => console.log('  - ' + f)); }
  process.exit(FAIL.length ? 1 : 0);
}

main().catch(e => { console.error('测试自身出错：', e); process.exit(2); });
