/* ===================================================================
   浏览器判题引擎的「下载失败 → 重试恢复」回归测试（真 Chrome）

   背景（2026-10-15 线上踩到）
   --------------------------
   C/C++ 判题的编译器是 15.7 MB 的 clang.wasm.gz，用户下载中途被掐
   （fetch 流报 "network error"）→ 评测机内部错误。这本身不是 bug；
   **真 bug 是** cpp-worker.js 把 rejected 的 toolchainPromise 缓存住了，
   之后每次点「提交并判题」都瞬间失败，唯一出路是刷新整页。
   （和编辑器加载失败那次的坑是同一类：失败态被永久缓存。）

   这个测试用自己的静态服务器伺服 docs/，第一次**故意掐断**
   clang.wasm.gz（Python 侧则掐 pyodide.asm.wasm），断言：
     [A] 第一次提交 → 判 IE，且提示里有人话指引（重试即可）
     [B] 第二次提交（放行下载）→ 引擎真的重新加载，判出真实结果（不是再报 IE）
   顺带这是浏览器 C/C++ / Python 判题的第一条端到端测试。

   用法：node tools/ui_e2e_local_engines.mjs   （无需后端，无需网络）
   =================================================================== */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

function loadDep(name, extra) {
  const tries = [createRequire(import.meta.url)];
  const dirs = [process.env.NODE_MODULES_DIR, ...(extra || [])].filter(Boolean);
  for (const d of dirs) tries.push(createRequire(path.join(d, 'noop.js')));
  for (const req of tries) { try { return req(name); } catch (e) { /* 下一个 */ } }
  console.error('找不到 ' + name + '（NODE_MODULES_DIR 或 experiments/pyodide-judge/node_modules）');
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

const DOCS = path.join(process.cwd(), 'docs');
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.wasm': 'application/wasm', '.gz': 'application/gzip',
  '.zip': 'application/zip', '.py': 'text/plain', '.css': 'text/css' };

let PASS = 0; const FAIL = [];
const check = (name, ok, extra) => {
  if (ok) { PASS++; console.log('  [PASS] ' + name + (extra ? '  ' + extra : '')); }
  else { FAIL.push(name); console.log('  [FAIL] ' + name + (extra !== undefined ? '  ' + extra : '')); }
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* 每个资产名都可以被「掐断 N 次」：第 1..N 次请求直接断流（模拟下载中途被掐，
   比返回 404/500 更接近真实故障 —— 流已经开了、正文传一半死掉）。 */
const CUT = { 'clang.wasm.gz': 1, 'pyodide.asm.wasm': 1 };   // 资产名 → 还要掐几次
const cutsMade = {};

function serveDir(root) {
  const srv = http.createServer((req0, res) => {
    const urlPath = decodeURIComponent(new URL(req0.url, 'http://x').pathname)
      .replace(/^\/my-pta\//, '/').replace(/\.\./g, '');
    const base = urlPath === '/' ? path.join(root, 'index.html') : path.join(root, urlPath);
    const name = path.basename(base);
    if (CUT[name] && (cutsMade[name] || 0) < CUT[name]) {
      cutsMade[name] = (cutsMade[name] || 0) + 1;
      res.writeHead(200, { 'Content-Type': MIME['.gz'], 'Content-Length': '999999' });
      res.write(Buffer.alloc(1024));                 // 先给一点正文，让流真的开起来
      setTimeout(() => res.destroy(), 50);            // 然后中途掐断 → 浏览器报 network error
      return;
    }
    fs.readFile(base, (err, data) => {
      if (err) { res.writeHead(404); res.end('not found'); return; }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(base)] || 'application/octet-stream' });
      res.end(data);
    });
  });
  return new Promise(resolve => srv.listen(0, '127.0.0.1', () => resolve(srv)));
}

const resultText = page => page.evaluate(() =>
  (document.getElementById('resultBox') || {}).innerText || '');
const waitResult = (page, ms) => page.waitForFunction(() => {
  const t = (document.getElementById('resultBox') || {}).innerText || '';
  return t && !/正在(加载|评测)/.test(t);
}, { timeout: ms, polling: 400 }).then(() => resultText(page));

async function openProblem(page, BASE, id) {
  await page.evaluate(i => { location.hash = '#/p/' + i; }, id);
  await page.waitForFunction(() => !!document.getElementById('btnSubmit'), { timeout: 30000 });
  await sleep(400);
}
async function typeCode(page, code) {
  await page.click('.cm-content');
  await page.keyboard.type(code);
  await sleep(150);
  const v = await page.evaluate(() => codeValue());
  if (!v.includes(code.split('\n')[0])) throw new Error('代码没写进编辑器：' + JSON.stringify(v.slice(0, 40)));
}

async function run() {
  console.log('== 浏览器判题引擎 · 下载失败重试回归 ==');
  const BANK = JSON.parse(fs.readFileSync(path.join(DOCS, 'problems.json'), 'utf8'));
  const py = BANK.items.find(x => x.line === 'python');
  const ds = BANK.items.find(x => x.subject === 'ds');
  console.log('夹具：Python #' + py.id + ' / 数据结构 #' + ds.id + '\n');

  const srv = await serveDir(DOCS);
  const BASE = 'http://127.0.0.1:' + srv.address().port + '/';
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });

  try {
    await page.goto(BASE, { waitUntil: 'load' });
    await page.waitForFunction(() => {
      const a = document.getElementById('app');
      return a && a.innerHTML && !a.innerHTML.includes('正在加载');
    }, { timeout: 30000 });

    /* ---------- [1] Python：掐断 pyodide.asm.wasm（约 9.6 MB） ---------- */
    console.log('[1] Python 引擎下载被掐断一次');
    await openProblem(page, BASE, py.id);
    await typeCode(page, 'a, b = map(int, input().split())\nprint(a + b)');
    await page.click('#btnSubmit');
    let r = await waitResult(page, 150000);
    check('第一次提交判 IE（引擎没下载完，判不出结果才是对的）',
      /评测机内部错误|浏览器判题失败|IE/.test(r), r.replace(/\n+/g, ' / ').slice(0, 70));
    check('提示告诉用户「再点一次就会重新下载」（人话指引）', /再点一次|重新下载/.test(r));

    console.log('\n[2] 放行下载后再提交一次');
    await page.click('#btnSubmit');
    r = await waitResult(page, 240000);
    check('重试真的恢复了：引擎重新下载并判出结果（不再是 IE）',
      !/浏览器判题失败|评测机内部错误/.test(r), r.replace(/\n+/g, ' / ').slice(0, 70));
    check('A+B 判满分', /满分/.test(r) || /5 \/ 5/.test(r), r.split('\n')[0]);

    /* ---------- [3] C/C++：掐断 clang.wasm.gz（15.7 MB） ---------- */
    console.log('\n[3] C/C++ 编译器下载被掐断一次');
    await openProblem(page, BASE, ds.id);
    await typeCode(page, 'int main(void){return 0;}');   // 错答案没关系，要的是「真的编译运行了」
    await page.click('#btnSubmit');
    r = await waitResult(page, 180000);
    check('第一次提交判 IE', /评测机内部错误|浏览器判题失败|IE/.test(r), r.replace(/\n+/g, ' / ').slice(0, 70));
    check('提示是人话指引', /再点一次|重新下载/.test(r));

    console.log('\n[4] 放行下载后再提交一次');
    await page.click('#btnSubmit');
    r = await waitResult(page, 300000);
    check('重试恢复了：clang 重新下载、真的编译运行（结果应是 WA 而不是 IE）',
      !/评测机内部错误|浏览器判题失败/.test(r), r.replace(/\n+/g, ' / ').slice(0, 70));
    check('错答案被判 WA（证明编译、运行、比对全链路都通了）', /WA|未通过|0 \/ 5/.test(r),
      r.split('\n')[0]);

    /* ---------- [5] 记录进 localStorage ---------- */
    const ls = await page.evaluate(() => Object.keys(localStorage).filter(k => k.startsWith('pta.')));
    check('浏览器判题的成绩进了本地进度', ls.length > 0, ls.slice(0, 4).join(','));
  } finally {
    await browser.close(); srv.close();
  }

  console.log('\n==================================================================');
  console.log('通过 ' + PASS + ' 项，失败 ' + FAIL.length + ' 项' + (FAIL.length ? '' : '，全部通过 ✅'));
  if (FAIL.length) { console.log('失败项：'); FAIL.forEach(f => console.log('  - ' + f)); process.exit(1); }
}

run().catch(e => { console.error(e); process.exit(2); });
