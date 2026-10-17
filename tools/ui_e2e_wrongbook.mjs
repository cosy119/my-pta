/* ===================================================================
   错题本 / 收藏 —— 真 Chrome 端到端测试

   为什么必须真浏览器
   ------------------
   这块全是交互：点星星就地翻面、备注框展开/保存、筛选后重绘、
   刷新后还在（后端持久化）、离线时靠 localStorage 也还在。
   jsdom 没有真实布局和 localStorage 生命周期，测这些等于没测。

   两轮
   ----
   ① **在线**：真起 uvicorn（测试库），页面走后端 `/api/wrongbook`。
      验的是「刷新后备注还在」= 真存进库了。
   ② **离线**：只服务 `docs/`（发布产物，没有后端）。
      验的是「静态站照样能收藏、能写备注、刷新不丢」。

   用法（仓库根目录）：
     NODE_MODULES_DIR=<含 puppeteer-core 的目录> node tools/ui_e2e_wrongbook.mjs

   默认用系统 Chrome/Edge，不下载浏览器；用独立 user-data-dir，不碰你日常的 profile。
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
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
    + '  然后：NODE_MODULES_DIR=<含它的目录> node tools/ui_e2e_wrongbook.mjs');
  process.exit(3);
}
const puppeteer = loadDep('puppeteer-core',
  [path.join(process.cwd(), 'experiments', 'pyodide-judge', 'node_modules')]);

const CHROME_PATHS = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
];
const CHROME = CHROME_PATHS.find(p => fs.existsSync(p));
if (!CHROME) { console.error('找不到系统 Chrome/Edge'); process.exit(3); }

const ROOT = process.cwd();
const PY = process.env.PTA_PY || 'D:/Pythontools/Python/python.exe';
const LIVE_PORT = 8801;
const LIVE_WEB_PORT = 8802;   // docs/ + /api 反代
const STATIC_PORT = 8803;     // docs/ 纯静态（无后端）

let passed = 0, failed = 0;
const fails = [];
function ok(name, cond, extra) {
  if (cond) { passed++; console.log('  [OK]   ' + name + (extra ? '  -- ' + extra : '')); }
  else { failed++; fails.push(name); console.log('  [FAIL] ' + name + (extra ? '  -- ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* ---------- 静态服务（只用 node，不引额外依赖） ----------
   ★ 在线模式不能直接访问 uvicorn 的 `/`：它返回 web/index.html，但页面里的
     `judge_text.js` 等是**相对路径**，后端只把 web/ 挂在 `/static`，
     `/judge_text.js` 会 404 → 整个页面脚本全灭（第一版就这么挂的）。
   所以两种模式**都服务 docs/**（发布产物），只是在线模式把 `/api/` 反代到
   uvicorn —— 这恰好就是「Pages 静态前端 + Render 后端」的真实部署形态。 */
const MIME = { '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8',
  '.json':'application/json; charset=utf-8', '.css':'text/css; charset=utf-8',
  '.wasm':'application/wasm', '.txt':'text/plain; charset=utf-8', '.mjs':'text/javascript; charset=utf-8' };

function serveStatic(dir, port, apiProxy) {
  return new Promise((resolve, reject) => {
    const srv = http.createServer((req, res) => {
      const pathname = decodeURIComponent(String(req.url || '/').split('?')[0]);
      if (apiProxy && pathname.startsWith('/api/')) {
        const up = http.request({
          host: '127.0.0.1', port: apiProxy, path: req.url, method: req.method, headers: req.headers,
        }, ur => {
          res.writeHead(ur.statusCode || 502, ur.headers);
          ur.pipe(res);
        });
        up.on('error', () => { res.writeHead(502); res.end('bad gateway'); });
        req.pipe(up);
        return;
      }
      let p = pathname === '/' ? '/index.html' : pathname;
      const f = path.join(dir, p.replace(/^\/+/, ''));
      if (!f.startsWith(dir) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) {
        res.writeHead(404); res.end('not found'); return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(f).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(res);
    });
    srv.on('error', reject);
    srv.listen(port, '127.0.0.1', () => resolve(srv));
  });
}

/* 等「真渲染完」，不是等「网络闲了」。
   ★ 这个坑第一版踩穿了：`waitUntil:'networkidle2'` 在 boot() 还在 await 第一批
     fetch 之前就达标（那时页面刚显示「正在加载题库…」），
     而我的等待条件里包含了 `.loading` —— 于是拿到的是一张骨架，
     断言全打在空节点上（假红三项，看起来像功能坏了）。
   判据改成「#app 里不再有 loading 骨架」，再等具体的元素。 */
async function waitApp(page, sel, timeout = 90000) {
  await page.waitForFunction(() => {
    const a = document.getElementById('app');
    return !!a && a.innerHTML.length > 0 && !/class="loading"/.test(a.innerHTML);
  }, { timeout });
  if (sel) await page.waitForSelector(sel, { timeout });
}

async function waitJson(url, tries = 200) {
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(url);
      if (r.ok) return await r.json();
    } catch (e) { /* 还没起来 */ }
    await sleep(400);
  }
  return null;
}

/* ---------- 一、在线（真后端 + 测试库） ---------- */
async function runOnline(browser) {
  console.log('\n[1] 在线模式（真 uvicorn + 测试库）');
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); });

  const base = `http://127.0.0.1:${LIVE_WEB_PORT}`;
  await page.goto(base + '/#/wrongbook', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await waitApp(page, '.wbHero');

  // 起点：新用户（全新 token）→ 空态
  const emptyTxt = await page.evaluate(() => (document.querySelector('.wbHint') || {}).textContent || '');
  ok('新用户进错题本是空态', /还什么都没有/.test(emptyTxt), emptyTxt.slice(0, 40));
  ok('导航有「错题本」入口且高亮',
    await page.evaluate(() => {
      const a = document.getElementById('navWB');
      return !!a && a.textContent.trim() === '错题本' && a.classList.contains('on');
    }));

  // 进「题集广场 → Python」的题目表，点第一题的星星
  // ★ 别用 `#/`：那是科目卡片页，表格在 `#/set/<subject>`。
  await page.goto(base + '/#/set/python', { waitUntil: 'domcontentloaded' });
  await waitApp(page, 'table.ptable .wbStarSm');
  const pid = await page.evaluate(() => {
    const b = document.querySelector('table.ptable .wbStarSm');
    return b ? parseInt(b.dataset.star, 10) : 0;
  });
  ok('题集列表里每题都有星标按钮', pid > 0, 'pid=' + pid);
  await page.click('table.ptable .wbStarSm');
  await sleep(900);
  ok('点一下星星就变实心',
    await page.evaluate(id => {
      const b = document.querySelector('td.c-tt .wbStarSm[data-star="' + id + '"]');
      return !!b && b.classList.contains('on') && b.textContent.trim() === '★';
    }, pid));

  // 错题本里能看到它（收藏筛选）
  await page.goto(base + '/#/wrongbook', { waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats');
  const starredN = await page.evaluate(() => {
    const card = document.querySelector('.wbStat[data-k="starred"] .n');
    return card ? parseInt(card.textContent, 10) : -1;
  });
  ok('统计卡「已收藏」= 1', starredN === 1, 'got=' + starredN);

  /* ★ 回归用例（线上 Pages 实测踩到）：刚收藏的题还没做过，attempts=0，
     按 is_wrong 的定义它**不是错题**。默认筛选若是「待攻克」，用户点完星标进来
     看到的是空列表，只有统计卡写着「已收藏 1」—— 看着像收藏没生效。
     默认改「全部」之后，这里必须直接看得见。 */
  const defFilter = await page.evaluate(() => {
    const on = document.querySelector('.wbSeg button.on');
    return { k: on ? on.dataset.k : '', t: on ? on.textContent.trim() : '',
             items: document.querySelectorAll('.wbItem').length };
  });
  ok('默认筛选是「全部」', defFilter.k === 'all', 'k=' + defFilter.k + ' t=' + defFilter.t);
  ok('默认筛选下直接看得见刚收藏的题（未做过也算）', defFilter.items === 1, 'items=' + defFilter.items);

  await page.click('.wbSeg button[data-k="starred"]');
  await page.waitForSelector('.wbItem', { timeout: 15000 });
  ok('收藏筛选里正好这一题',
    await page.evaluate(id => document.querySelectorAll('.wbItem').length === 1
      && document.querySelector('.wbItem').dataset.pid === String(id), pid));

  // ★ 核心：写备注并保存
  const NOTE = '边界忘了判 n=0；下次先写特殊值再动循环。';
  await page.click('.wbItem .wbNote');
  await page.waitForSelector('.wbEditor:not([hidden]) textarea', { timeout: 8000 });
  ok('点备注框能展开编辑区', true);
  await page.type('.wbItem .wbEditor textarea', NOTE, { delay: 6 });
  const counter = await page.evaluate(() =>
    (document.querySelector('.wbItem .wbEditor .cnt') || {}).textContent || '');
  ok('字数计数器跟着走', counter.startsWith(String(NOTE.length)), counter);
  await page.click('.wbItem .wbEditor button[data-act="save"]');
  await sleep(900);
  const noteView = await page.evaluate(() =>
    (document.querySelector('.wbItem .wbNote') || {}).textContent || '');
  ok('保存后备注显示出来', noteView === NOTE, noteView.slice(0, 30));

  // ★★ 刷新页面 —— 在线模式下这就是「真进库了」的证明
  await page.reload({ waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats');
  const notedAfterReload = await page.evaluate(() => {
    const c = document.querySelector('.wbStat[data-k="noted"] .n');
    return c ? parseInt(c.textContent, 10) : -1;
  });
  ok('★★ 刷新后备注还在（真存进库）', notedAfterReload === 1, 'noted=' + notedAfterReload);

  await page.click('.wbSeg button[data-k="noted"]');
  await page.waitForSelector('.wbItem', { timeout: 15000 });
  const noteText2 = await page.evaluate(() =>
    (document.querySelector('.wbItem .wbNote') || {}).textContent || '');
  ok('「有备注」筛选里备注原文一字不差', noteText2 === NOTE, noteText2.slice(0, 30));

  // 掌握度三档
  await page.click('.wbItem .wbLvl button[data-l="1"]');
  await sleep(700);
  ok('掌握度能改（薄弱）',
    await page.evaluate(() =>
      !!document.querySelector('.wbItem .wbLvl button[data-l="1"].on')));

  // 题目详情页：收藏按钮 + 备注区都已就位
  await page.goto(base + '/#/p/' + pid, { waitUntil: 'domcontentloaded' });
  await waitApp(page, '#pStarBtn');
  ok('题面有收藏按钮且状态是已收藏',
    await page.evaluate(() => {
      const b = document.getElementById('pStarBtn');
      return b.classList.contains('on') && /已收藏/.test(b.textContent);
    }));
  ok('题面有「我的错题备注」区',
    await page.evaluate(() => {
      const box = document.querySelector('[data-pnotebox]');
      return !!box && /我的错题备注/.test(box.textContent)
        && box.querySelector('.wbNote').textContent.indexOf('边界忘了判') >= 0;
    }));

  // 在题面写备注（走同一个 wbNote/wbEditor，验证不是只在错题本里好用）
  await page.click('[data-pnotebox] .wbNote');
  await page.waitForSelector('[data-pnotebox] .wbEditor:not([hidden]) textarea', { timeout: 8000 });
  await page.evaluate(() => { document.querySelector('[data-pnotebox] .wbEditor textarea').value = ''; });
  await page.type('[data-pnotebox] .wbEditor textarea', '在题面改的备注', { delay: 6 });
  await page.click('[data-pnotebox] .wbEditor button[data-act="save"]');
  await sleep(900);
  ok('题面能改备注，且留在题面（没被甩到错题本）',
    page.url().indexOf('/#/p/') >= 0
    && await page.evaluate(() => document.querySelector('[data-pnotebox] .wbNote').textContent === '在题面改的备注'));

  // 删除备注 → 「有备注」清空
  await page.click('[data-pnotebox] .wbNote');
  await page.waitForSelector('[data-pnotebox] .wbEditor:not([hidden]) button[data-act="delnote"]', { timeout: 8000 });
  await page.click('[data-pnotebox] .wbEditor button[data-act="delnote"]');
  await sleep(900);
  await page.goto(base + '/#/wrongbook', { waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats');
  const notedZero = await page.evaluate(() => {
    const c = document.querySelector('.wbStat[data-k="noted"] .n');
    return c ? parseInt(c.textContent, 10) : -1;
  });
  ok('删除后「写了备注」归零', notedZero === 0, 'noted=' + notedZero);

  ok('全程没有 JS 报错', errs.length === 0, errs.slice(0, 3).join(' | '));
  await page.close();
  return pid;
}

/* ---------- 二、离线（发布产物 docs/，没有后端） ---------- */
async function runOffline(browser) {
  console.log('\n[2] 离线模式（只服务 docs/，没有后端）');
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  const base = `http://127.0.0.1:${STATIC_PORT}`;

  await page.goto(base + '/#/set/python', { waitUntil: 'domcontentloaded' });
  await waitApp(page, 'table.ptable .wbStarSm');
  ok('离线也能列出题目（problems.json 兜底）',
    await page.evaluate(() => document.querySelectorAll('table.ptable .wbStarSm').length > 0));
  ok('离线标记显示出来了',
    await page.evaluate(() => {
      const t = document.getElementById('offlineTag');
      return !!t && t.style.display !== 'none';
    }));

  const pid = await page.evaluate(() => {
    const b = document.querySelector('table.ptable .wbStarSm');
    return b ? parseInt(b.dataset.star, 10) : 0;
  });
  await page.click('table.ptable .wbStarSm');
  await sleep(500);
  ok('离线点星星也能亮（本地存）',
    await page.evaluate(id => {
      const b = document.querySelector('td.c-tt .wbStarSm[data-star="' + id + '"]');
      return !!b && b.classList.contains('on');
    }, pid));

  await page.goto(base + '/#/wrongbook', { waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats');
  ok('错题本离线可打开且带收藏', await page.evaluate(() => {
    const c = document.querySelector('.wbStat[data-k="starred"] .n');
    return c && parseInt(c.textContent, 10) === 1;
  }));

  await page.click('.wbSeg button[data-k="starred"]');
  await page.waitForSelector('.wbItem', { timeout: 15000 });
  await page.click('.wbItem .wbNote');
  await page.waitForSelector('.wbEditor:not([hidden]) textarea', { timeout: 8000 });
  await page.type('.wbItem .wbEditor textarea', '离线写的备注', { delay: 6 });
  await page.click('.wbItem .wbEditor button[data-act="save"]');
  await sleep(600);

  // ★ 刷新（离线）后还得在 —— localStorage 的持久性
  await page.reload({ waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats');
  ok('★★ 离线刷新后备注还在（localStorage）',
    await page.evaluate(() => {
      const c = document.querySelector('.wbStat[data-k="noted"] .n');
      return c && parseInt(c.textContent, 10) === 1;
    }));

  ok('离线全程没有 JS 报错（后端 404 是被 catch 掉的）', errs.length === 0, errs.slice(0, 2).join(' | '));
  await page.close();
}

/* ---------- 三、线上 Pages（--live，可选） ----------
   前面两轮跑的是本地 docs/，能证明"代码是对的"；这一轮跑真实部署，
   证明"推上去真的生效了"。两者会分开是因为线上有自己的坑：
   Pages 没有后端，前端会先探 /api/* 再降级 —— 那三个 404 是**设计如此**，
   但 Chrome 会把它们记成 console error，所以这轮的报错断言按 URL 白名单放过。
   跑法：node tools/ui_e2e_wrongbook.mjs --live */
const LIVE_URL = 'https://cosy119.github.io/my-pta/';

async function runLive(browser) {
  console.log('\n[3] 线上 Pages（' + LIVE_URL + '）');
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 950 });
  const errs = [];
  const bad = [];
  page.on('pageerror', e => errs.push('JS: ' + String(e).slice(0, 200)));
  page.on('response', r => {
    if (r.status() >= 400 && !/\/api\//.test(r.url())) bad.push(r.status() + ' ' + r.url().slice(0, 90));
  });

  const t0 = Date.now();
  await page.goto(LIVE_URL + '#/wrongbook', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await waitApp(page, '.wbHero', 90000);
  console.log('    首屏 %.1fs（Pages CDN）', (Date.now() - t0) / 1000);

  ok('线上错题本首屏渲染', await page.evaluate(() => !!document.querySelector('.wbHero')));
  ok('线上导航「错题本」高亮',
    await page.evaluate(() => (document.getElementById('navWB') || {}).className === 'on'));
  ok('线上统计卡 4 张', await page.evaluate(() => document.querySelectorAll('.wbStats .wbStat').length) === 4);
  ok('线上识别为离线（Pages 无后端）',
    await page.evaluate(() => /离线/.test((document.getElementById('offlineTag') || {}).textContent || '')));

  // 收藏一道没做过的题
  await page.goto(LIVE_URL + '#/set/python', { waitUntil: 'domcontentloaded' });
  await waitApp(page, 'table.ptable .wbStarSm', 90000);
  const pid = await page.evaluate(() => {
    const b = document.querySelector('table.ptable .wbStarSm');
    return b ? parseInt(b.dataset.star, 10) : 0;
  });
  ok('线上题集列表每题都有星标', pid > 0, 'pid=' + pid);
  await page.click('table.ptable .wbStarSm');
  await sleep(700);
  ok('线上点星变实心',
    await page.evaluate(id => {
      const b = document.querySelector('.wbStarSm[data-star="' + id + '"]');
      return !!b && b.classList.contains('on');
    }, pid));

  await page.goto(LIVE_URL + '#/wrongbook', { waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats', 90000);
  const st = await page.evaluate(() => ({
    on: (document.querySelector('.wbSeg button.on') || {}).dataset?.k || '',
    items: document.querySelectorAll('.wbItem').length,
    starred: (() => { const c = document.querySelector('.wbStat[data-k="starred"] .n'); return c ? parseInt(c.textContent, 10) : -1; })(),
  }));
  ok('线上统计卡「已收藏」>= 1', st.starred >= 1, 'got=' + st.starred);
  ok('线上默认「全部」直接看得见收藏的题', st.on === 'all' && st.items >= 1,
    'filter=' + st.on + ' items=' + st.items);

  // 备注：写 → 刷新 → 还在（Pages 无后端，全靠 localStorage）
  await page.click('.wbItem .wbNote');
  await page.waitForSelector('.wbItem .wbEditor:not([hidden]) textarea', { timeout: 10000 });
  const NOTE = '线上实测：边界没判，先写特殊值再动循环';
  await page.type('.wbItem .wbEditor textarea', NOTE, { delay: 5 });
  await page.evaluate(() => {
    const box = document.querySelector('.wbItem');
    [...box.querySelectorAll('button')].find(b => /保存/.test(b.textContent))?.click();
  });
  await sleep(900);
  ok('线上备注保存进 localStorage',
    await page.evaluate(t => (localStorage.getItem('pta.mastery') || '').includes(t), NOTE));

  await page.reload({ waitUntil: 'domcontentloaded' });
  await waitApp(page, '.wbStats', 90000);
  ok('线上刷新后备注还在',
    await page.evaluate(t => document.body.innerText.includes(t), NOTE));

  // 按备注文字搜索
  await page.evaluate(() => {
    const i = document.getElementById('wbQ');
    if (!i) return;
    i.value = '线上实测';
    i.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await sleep(700);
  ok('线上按备注文字搜索命中', await page.evaluate(() => document.querySelectorAll('.wbItem').length >= 1));

  ok('线上零 JS 抛错', errs.length === 0, errs.slice(0, 2).join(' | '));
  /* 白名单：/api/* 的 404 是静态站降级探测，属设计；其余 404 都算回归 */
  ok('线上无非预期的 404（/api 降级探测不计）', bad.length === 0, bad.slice(0, 3).join(' | '));
  await page.close();
}

/* ---------- main ---------- */
console.log('='.repeat(72));
console.log('错题本 / 收藏 —— 真 Chrome 端到端');
console.log('='.repeat(72));
console.log('Chrome:', CHROME);

const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pta-wb-'));

// 后端：测试库
const dbPath = path.join(ROOT, 'data', '_bank_test.db');
const procs = [];
const be = spawn(PY, ['-m', 'uvicorn', 'app.main:app',
  '--host', '127.0.0.1', '--port', String(LIVE_PORT), '--log-level', 'warning'], {
  cwd: ROOT, env: Object.assign({}, process.env, { PTA_DB: dbPath }),
  stdio: ['ignore', 'ignore', 'pipe'],
});
procs.push(be);
be.stderr.on('data', d => { const s = String(d); if (/Traceback|Error/.test(s)) console.error('[uvicorn] ' + s.slice(0, 400)); });

let staticSrv = null, staticSrv2 = null;
let browser = null;
try {
  const health = await waitJson(`http://127.0.0.1:${LIVE_PORT}/api/health`);
  if (!health) throw new Error('后端没起来（uvicorn 启动失败？）');
  console.log('后端就绪：' + health.db);

  staticSrv = await serveStatic(path.join(ROOT, 'docs'), LIVE_WEB_PORT, LIVE_PORT);
  console.log('在线前端就绪（docs/ + /api 反代）：http://127.0.0.1:' + LIVE_WEB_PORT);
  staticSrv2 = await serveStatic(path.join(ROOT, 'docs'), STATIC_PORT);
  console.log('离线前端就绪（docs/ 纯静态）：http://127.0.0.1:' + STATIC_PORT);

  browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    userDataDir,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--no-first-run',
           '--disable-features=Translate', '--lang=zh-CN'],
    defaultViewport: { width: 1280, height: 900 },
  });

  await runOnline(browser);
  await runOffline(browser);
  if (process.argv.includes('--live')) await runLive(browser);
} catch (e) {
  failed++;
  fails.push('异常：' + String(e && e.message || e));
  console.error('\n[异常] ' + (e && e.stack || e));
} finally {
  if (browser) { try { await browser.close(); } catch (e) {} }
  if (staticSrv) { try { staticSrv.close(); } catch (e) {} }
  if (staticSrv2) { try { staticSrv2.close(); } catch (e) {} }
  for (const p of procs) { try { p.kill(); } catch (e) {} }
  try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch (e) {}
}

console.log('\n' + '='.repeat(72));
console.log(`通过 ${passed} 项 / 失败 ${failed} 项`);
if (fails.length) console.log('失败项：\n  - ' + fails.join('\n  - '));
console.log('='.repeat(72));
process.exit(failed ? 1 : 0);
