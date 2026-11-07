/* 题库分片验收：首屏只拉轻索引，进题才拉本科目整包，且判题仍然可用。
   跑法：node tools/ui_test_bank_split.mjs            （对着 docs/ 起本地服务）
*/
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const repo = process.cwd();
const root = path.resolve(process.env.PTA_SITE_DIR || path.join(repo, 'docs'));
const require = createRequire(path.join(repo, 'experiments/pyodide-judge/noop.js'));
const puppeteer = require('puppeteer-core');

const hits = [];
const srv = http.createServer((req, res) => {
  const p = decodeURIComponent(req.url.split('?')[0]);
  hits.push(p);
  const f = path.resolve(root, '.' + (p === '/' ? '/index.html' : p));
  if (!f.startsWith(root)) { res.writeHead(403).end(); return; }
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404).end(); return; }
    const ext = path.extname(f);
    res.setHeader('Content-Type', ext === '.js' ? 'text/javascript'
      : ext === '.json' ? 'application/json' : 'text/html');
    res.end(d);
  });
});
await new Promise(r => srv.listen(0, r));
const url = `http://127.0.0.1:${srv.address().port}`;
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox'],
});
let fails = 0;
const check = (name, ok, extra) => {
  console.log((ok ? 'PASS ' : 'FAIL ') + name + (ok ? '' : '  ← ' + (extra ?? '')));
  if (!ok) fails++;
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

try {
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push(String(e)));

  const t0 = Date.now();
  await page.goto(url + '/', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(
    () => typeof PROBLEMS !== 'undefined' && PROBLEMS.length > 0, { timeout: 30000 });
  const bootMs = Date.now() - t0;

  const idx = hits.filter(h => h.endsWith('/bank/index.json')).length;
  const early = hits.filter(h => h.endsWith('/problems.json')).length;
  const subjEarly = hits.filter(h => /\/bank\/(linux|ds|cpp|python)\.json$/.test(h)).length;
  check('首屏拉的是轻索引 bank/index.json', idx === 1, JSON.stringify(hits.slice(0, 6)));
  check('首屏不拉整包 problems.json', early === 0, 'hits=' + early);
  check('首屏不预先拉任何科目包', subjEarly === 0, 'hits=' + subjEarly);

  const stat = await page.evaluate(() => ({
    n: PROBLEMS.length, split: BANK_SPLIT, hasStmt: !!PROBLEMS[0].statement_md,
  }));
  check('轻索引里题目数正确（1524）', stat.n === 1524, stat.n);
  check('识别为分片模式', stat.split === true);
  check('轻索引里**不带**题面（省流量）', stat.hasStmt === false);

  /* 进一道 Linux 题：应该只拉 linux.json */
  const linuxId = await page.evaluate(() =>
    PROBLEMS.find(p => p.subject === 'linux' && p.title.includes('实验 4-1')).id);
  await page.evaluate(id => { location.hash = '#/p/' + id; }, linuxId);
  await page.waitForSelector('.shellIn', { timeout: 30000 });
  const gotLinux = hits.filter(h => h.endsWith('/bank/linux.json')).length;
  const gotDs = hits.filter(h => h.endsWith('/bank/ds.json')).length;
  check('进 Linux 题才拉 bank/linux.json', gotLinux === 1);
  check('进 Linux 题**不**拉 ds.json', gotDs === 0);
  const wantStmt = await page.evaluate(() => !!(CUR && CUR.statement_md && CUR.statement_md.length > 10));
  check('题面加载成功', wantStmt);
  const wantCases = await page.evaluate(() => !!(CUR && CUR.cases && CUR.cases.length));
  check('测试点跟着科目包一起到了（本地判题可用）', wantCases);

  /* 本地判题：填参考答案，应当判 AC 且拿满分 */
  const exp = await page.evaluate(() => (CUR.cases[0].expected_stdout || '').split('\n')[0].replace(/^\|/, ''));
  await page.evaluate(() => {
    const el = document.getElementById('codeBox');
    el.value = '';
    el.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.type('#codeBox', exp);
  await page.evaluate(() => doSubmitLocal());
  await sleep(300);
  const box = await page.evaluate(() => (document.getElementById('resultBox') || {}).textContent || '');
  check('分片模式下本地判题仍然判对', box.includes('答案正确'), box.slice(0, 60));

  /* ★ 真实反馈复现（2026-11-07）：题面「切换到 /etc 后列出含 pass 的文件」，
     学生按实验步骤写两行 `cd /etc` + `ls -d *pass*`，老判题判错 ——
     答案里只有 `cd /etc && ls -d *pass*`，换行折成 `;` 后差在 && 与 ; 上。 */
  const passId = await page.evaluate(() =>
    PROBLEMS.find(p => p.subject === 'linux' && p.title.includes('名字含 pass'))?.id);
  if (passId) {
    await page.evaluate(id => { location.hash = '#/p/' + id; }, passId);
    await page.waitForSelector('#codeBox', { timeout: 30000 });
    await page.evaluate(() => {
      const el = document.getElementById('codeBox');
      el.value = '';
      el.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await page.type('#codeBox', 'cd /etc');
    await page.keyboard.down('Shift');
    await page.keyboard.press('Enter');
    await page.keyboard.up('Shift');
    await page.type('#codeBox', 'ls -d *pass*');
    await page.evaluate(() => doSubmitLocal());
    await sleep(300);
    const box2 = await page.evaluate(() => (document.getElementById('resultBox') || {}).textContent || '');
    check('「cd 与命令分两行写」判对（学生最自然的写法）', box2.includes('答案正确'), box2.slice(0, 80));

    /* 而同一条命令写错（少个通配符）仍要判错 */
    await page.evaluate(() => {
      const el = document.getElementById('codeBox');
      el.value = 'cd /etc\nls -d passwd';
      el.dispatchEvent(new Event('input', { bubbles: true }));
    });
    await page.evaluate(() => doSubmitLocal());
    await sleep(300);
    const box3 = await page.evaluate(() => (document.getElementById('resultBox') || {}).textContent || '');
    check('写错仍判错（宽松不能宽到没边）', box3.includes('答案错误'), box3.slice(0, 60));
  }

  /* 再进一道数据结构题：这次才该拉 ds.json，且只拉一次 */
  const dsId = await page.evaluate(() => PROBLEMS.find(p => p.subject === 'ds').id);
  await page.evaluate(id => { location.hash = '#/p/' + id; }, dsId);
  await page.waitForFunction(() => !!CUR && CUR.subject === 'ds' && !!CUR.statement_md, { timeout: 60000 });
  check('进 DS 题拉 bank/ds.json', hits.filter(h => h.endsWith('/bank/ds.json')).length === 1);
  check('DS 题面也到了', await page.evaluate(() => !!CUR.statement_md));

  /* 回到 Linux 题：科目包已缓存，不该重复下载 */
  const before = hits.length;
  await page.evaluate(id => { location.hash = '#/p/' + id; }, linuxId);
  await page.waitForSelector('.shellIn', { timeout: 20000 });
  const again = hits.slice(before).filter(h => h.endsWith('/bank/linux.json')).length;
  check('回看同一科目不再重复下载', again === 0, '重复 ' + again + ' 次');

  check('页面无 JS 异常', errs.length === 0, errs.slice(0, 2).join(' | '));
  console.log(`\n首屏到「题库可用」用时 ${bootMs} ms`);
  console.log(fails ? `✗ 失败 ${fails} 项` : '✓ 全部通过');
} finally {
  await browser.close();
  srv.close();
}
process.exit(fails ? 1 : 0);
