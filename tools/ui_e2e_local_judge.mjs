/* ===================================================================
   离线本地判题 —— 真 Chrome 端到端测试

   为什么还要一个
   --------------
   `ui_test_local_judge.mjs` 用 jsdom，跑得很快、覆盖也够细，但 jsdom 里
   `URL.createObjectURL` / 真实下载 / 真实文件上传 都是替身。
   而「导出进度」这个功能的价值偏偏就在于**真的落下一个文件、再真的读回来**。
   这一层只有真浏览器能验。

   它验的是**发布产物**：直接服务 `docs/`（也就是 GitHub Pages 上那一份），
   而不是 `web/` 源码。所以要先把题库导出好。

   用法（在仓库根目录下）：
     NODE_MODULES_DIR=<含 puppeteer-core 的目录> node tools/ui_e2e_local_judge.mjs

   默认用系统 Chrome，不下载浏览器。
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
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
    + '  然后：NODE_MODULES_DIR=<含它的目录> node tools/ui_e2e_local_judge.mjs');
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
const BANK = JSON.parse(fs.readFileSync(path.join(DOCS, 'problems.json'), 'utf8'));
if (!BANK.items[0] || !BANK.items[0].cases) {
  console.error('docs/problems.json 里没有 cases，先跑：python tools/export_static.py --with-cases');
  process.exit(4);
}

let PASS = 0;
const FAIL = [];
function check(name, cond, extra) {
  if (cond) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra !== undefined ? '  ' + extra : '')); }
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

function serveDir(root) {
  const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
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

/* 独立算一份「正确答案」做夹具。
   ★ 刻意不复用页面的 window.PROBLEMS / TextJudge：
     · PROBLEMS 是 `let` 声明的脚本级绑定，根本没挂在 window 上（取不到）；
     · 更重要的，夹具自己算一遍，才不会变成「拿页面自己的答案去考页面自己」。
   注意这条路径的口径正确性由 tools/verify_text_judge.mjs 负责（3463 条对拍），
   这里只需要够用：按 `|` 行取备选答案。 */
function altsOf(p) {
  const exp = (p.cases && p.cases[0] && p.cases[0].expected_stdout) || '';
  return String(exp).replace(/\r\n?/g, '\n').split('\n')
    .filter(l => l.indexOf('|') === 0)
    .map(l => l.slice(1).trim())
    .filter(Boolean);
}
const isAscii = s => /^[\x20-\x7e]+$/.test(s);

/* 页面「加载完成」的可靠信号：renderNav() 在离线时会把角标显示出来。
   ★ 别用「#navScore 不是空」——初始 HTML 里那个「—」也不是空，会提前放行。 */
async function waitBooted(page) {
  await page.waitForFunction(() => {
    const t = document.getElementById('offlineTag');
    return t && t.style.display !== 'none';
  }, { timeout: 25000 });
}

const EXPECT_LOCAL = BANK.items.filter(x => x.line === 'text' && x.cases && x.cases.length).length;

const fill = BANK.items.find(x => x.line === 'text' && (!x.choices || !x.choices.length)
  && altsOf(x).some(isAscii));
const mc = BANK.items.find(x => x.line === 'text' && x.choices && x.choices.length > 2
  && altsOf(x).some(a => /^[A-Za-z]$/.test(a)));
if (!fill || !mc) { console.error('题库里找不到合适的填空题/单选题，测试无法进行'); process.exit(5); }
const good = altsOf(fill).find(isAscii);
const letter = altsOf(mc).find(a => /^[A-Za-z]$/.test(a)).toUpperCase();

async function run() {
  console.log('== 离线本地判题 · 真 Chrome 端到端 ==');
  console.log('服务目录：docs/（发布产物）  ' + BANK.count + ' 题\n');

  const srv = await serveDir(DOCS);
  const PORT = srv.address().port;
  const BASE = 'http://127.0.0.1:' + PORT + '/';
  const DL = fs.mkdtempSync(path.join(os.tmpdir(), 'pta-dl-'));

  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  const pageErrors = [];
  page.on('pageerror', e => pageErrors.push(String(e && e.message || e)));
  page.on('console', m => { if (m.type() === 'error') pageErrors.push('console: ' + m.text()); });

  const cdp = await page.createCDPSession();
  try {
    await cdp.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: DL, eventsEnabled: true });
  } catch (e) {
    await cdp.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: DL });
  }

  /* ---------- [1] 站点起来，进入离线模式 ---------- */
  console.log('[1] 打开站点（没有后端 → 应进入离线模式）');
  await page.goto(BASE, { waitUntil: 'load' });
  await page.waitForFunction(() => !(document.getElementById('app') || {}).innerHTML
    || !document.getElementById('app').innerHTML.includes('正在加载'), { timeout: 30000 });
  check('判题脚本被浏览器真的执行（window.TextJudge 存在）',
    await page.evaluate(() => typeof window.TextJudge === 'object' && typeof window.TextJudge.judgeTextProblem === 'function'));
  const banner = await page.$eval('.banner.warn', el => el.textContent).catch(() => '');
  check('显示了离线横幅', !!banner, banner.slice(0, 60));
  const nLocal = await page.evaluate(() => {
    const m = /(\d+)\s*道理论题/.exec(document.querySelector('.banner.warn').textContent || '');
    return m ? +m[1] : -1;
  });
  check('横幅里现算出「' + EXPECT_LOCAL + ' 道理论题可本地判」',
    nLocal === EXPECT_LOCAL, String(nLocal));
  check('非理论题不会混进来（另有 ' + (BANK.count - EXPECT_LOCAL) + ' 道代码题）',
    nLocal < BANK.count, nLocal + ' < ' + BANK.count);

  /* ---------- [2] 填空题：真点按钮判题 ---------- */
  console.log('\n[2] 填空题：填对答案 → 点「提交并判题」');
  await page.goto(BASE + '#/p/' + fill.id, { waitUntil: 'load' });
  await page.waitForSelector('#btnRow .btn', { timeout: 20000 });
  const btnText = await page.$eval('#btnRow', el => el.textContent);
  check('按钮是「提交并判题」', btnText.includes('提交并判题'), btnText.trim());

  check('夹具答案已就绪（来自题库期望值，不是页面自己算的）', !!good && isAscii(good), good);

  await page.evaluate(() => { document.getElementById('codeBox').value = ''; });
  await page.click('#codeBox');
  await page.type('#codeBox', 'WRONG_ANSWER_ZZZ');
  await page.click('#btnSubmit');
  await sleep(300);
  check('错答案显示「答案错误」',
    (await page.$eval('#resultBox', el => el.textContent)).includes('答案错误'));

  await page.evaluate(() => { document.getElementById('codeBox').value = ''; });
  await page.click('#codeBox');
  await page.type('#codeBox', good);
  await page.click('#btnSubmit');
  await sleep(400);
  const res = await page.$eval('#resultBox', el => el.textContent);
  check('正确答案显示「答案正确」', res.includes('答案正确'), res.slice(0, 50));
  check('拿到满分 ' + fill.total_score, res.includes(fill.total_score + ' / ' + fill.total_score), res.slice(0, 60));
  check('题面里能展开看到每个测试点', (await page.$$('#resultBox .caseRow')).length === fill.cases.length);

  const prog1 = await page.evaluate(() => JSON.parse(localStorage.getItem('pta.localProgress') || '{}'));
  check('进度落在 localStorage（满分）', (prog1[fill.id] || {}).best_score === fill.total_score,
    JSON.stringify(prog1[fill.id]));

  await page.evaluate(() => { document.getElementById('codeBox').value = ''; });
  await page.click('#codeBox');
  await page.type('#codeBox', 'ALSO_WRONG_QQQ');
  await page.click('#btnSubmit');
  await sleep(400);
  const prog2 = await page.evaluate(() => JSON.parse(localStorage.getItem('pta.localProgress') || '{}'));
  check('★ 真浏览器里：答对后再答错，最高分也没被冲掉',
    (prog2[fill.id] || {}).best_score === fill.total_score, JSON.stringify(prog2[fill.id]));

  /* ---------- [3] 刷新后进度还在 ---------- */
  console.log('\n[3] 刷新页面');
  await page.reload({ waitUntil: 'load' });
  await waitBooted(page);
  const nav = await page.$eval('#navScore', el => el.textContent);
  check('刷新后顶栏总分仍在（进度没丢）', nav.includes(String(fill.total_score)), nav.trim());

  /* ---------- [4] 单选题 ---------- */
  console.log('\n[4] 单选题：真点选项');
  await page.goto(BASE + '#/p/' + mc.id, { waitUntil: 'load' });
  await page.waitForSelector('#choiceList .choice', { timeout: 20000 });
  const idx = letter.charCodeAt(0) - 65;
  check('夹具给出的正确选项是 ' + letter + '（第 ' + (idx + 1) + ' 个）',
    idx >= 0 && idx < mc.choices.length, letter);
  await page.click('#choiceList .choice:nth-child(' + (idx + 1) + ')');
  await page.click('#btnSubmit');
  await sleep(350);
  const res2 = await page.$eval('#resultBox', el => el.textContent);
  check('单选题选对判「答案正确」', res2.includes('答案正确'), res2.slice(0, 50));
  check('单选题满分 ' + mc.total_score, res2.includes(mc.total_score + ' / ' + mc.total_score), res2.slice(0, 60));

  /* ---------- [5] 导出进度 → 真的落下一个文件 ---------- */
  console.log('\n[5] 导出进度（真下载）');
  await page.evaluate(() => window.openSettings());
  await page.waitForSelector('#impFile', { timeout: 10000 });
  const btns = await page.$$('.modal .btn.ghost');
  let clicked = false;
  for (const b of btns) {
    const t = await b.evaluate(el => el.textContent.trim());
    if (t === '导出进度') { await b.click(); clicked = true; break; }
  }
  check('设置里有「导出进度」按钮', clicked);

  let dlFile = null;
  for (let i = 0; i < 60; i++) {
    const f = fs.readdirSync(DL).filter(x => /^pta-progress-.*\.json$/.test(x) && !x.endsWith('.crdownload'));
    if (f.length) { dlFile = path.join(DL, f[0]); break; }
    await sleep(200);
  }
  check('真的下载下来一个文件', !!dlFile, dlFile ? path.basename(dlFile) : '(没等到)');
  let bundle = null;
  if (dlFile) {
    try { bundle = JSON.parse(fs.readFileSync(dlFile, 'utf8')); } catch (e) { bundle = null; }
    check('下载的 JSON 能解析', !!bundle);
    check('文件里有这道题的满分记录', bundle && (bundle.local[fill.id] || {}).best_score === fill.total_score,
      bundle ? JSON.stringify(bundle.local[fill.id]) : '');
  }

  /* ---------- [6] 清空 → 导入文件 → 进度回来 ---------- */
  console.log('\n[6] 清空进度后导入刚才那个文件');
  await page.evaluate(() => localStorage.removeItem('pta.localProgress'));
  await page.reload({ waitUntil: 'load' });
  await waitBooted(page);
  const navCleared = await page.$eval('#navScore', el => el.textContent.trim());
  check('清空后顶栏总分为 0', /^0\s*\/\s*2615/.test(navCleared), navCleared);

  await page.evaluate(() => window.openSettings());
  await page.waitForSelector('#impFile', { timeout: 10000 });
  const input = await page.$('#impFile');
  await input.uploadFile(dlFile);
  await sleep(1200);
  const prog3 = await page.evaluate(() => JSON.parse(localStorage.getItem('pta.localProgress') || '{}'));
  check('导入后进度回来了', (prog3[fill.id] || {}).best_score === fill.total_score,
    JSON.stringify(prog3[fill.id]));
  /* ★ 断言「包里有几道题就该回来几分」——之前只断言其中一道，是把对的当成错的。
     导出时已解了填空题和单选题两道（各 10 分），所以导入后应该是 20。 */
  const expectTotal = bundle
    ? Object.keys(bundle.local).reduce((a, k) => a + (parseInt(bundle.local[k].best_score || 0, 10) || 0), 0)
    : fill.total_score;
  const navBack = await page.$eval('#navScore', el => el.textContent.trim());
  check('导入后顶栏总分 = 包里所有题的分数之和（' + expectTotal + '）',
    navBack === expectTotal + ' / 2615 分', navBack);
  check('导入的是整份备份，不止一道题',
    bundle && Object.keys(bundle.local).length >= 2, bundle ? Object.keys(bundle.local).length + ' 道' : '');

  /* ---------- [7] 没报错 ---------- */
  const errs = pageErrors.filter(e => !/favicon|404 \(Not Found\)|Failed to load resource/.test(e));
  check('全程没有 JS 异常', errs.length === 0, errs.slice(0, 3).join(' | '));

  await browser.close();
  srv.close();
  fs.rmSync(DL, { recursive: true, force: true });

  console.log('\n' + '='.repeat(66));
  console.log('通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项');
  if (FAIL.length) console.log('失败项：' + FAIL.join('、'));
  else console.log('全部通过 ✅');
  console.log('='.repeat(66));
  return FAIL.length ? 1 : 0;
}

run().then(c => process.exit(c)).catch(e => { console.error(e); process.exit(2); });
