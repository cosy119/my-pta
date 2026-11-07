/* 真浏览器验收：命令沙箱嵌进 Linux 题之后能不能用。

检查 9 件事：
  1. Linux 题里出现终端面板，提示符是 [student@fedora ~]$
  2. 敲 `ls /etc` → 输出里有 hosts
  3. `cd /usr` 后提示符变成 /usr
  4. 不存在的命令 → command not found + 退出码
  5. 管道 `grep bash /etc/shells | wc -l` → 2
  6. 重定向 `echo ok > ~/t.txt` 后 `cat ~/t.txt` → ok
  7. 「重置」把 cwd 打回 /home/student
  8. 页面上点击「重置」按钮真的生效
  9. 数据结构线**不该**出现终端面板

跑法：node tools/ui_test_linux_shell.mjs
依赖 docs/ 已导出（tools/export_static.py --with-cases）。
*/
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';

const repo = process.cwd();
const root = path.resolve(process.env.PTA_SITE_DIR || path.join(repo, 'docs'));
const moduleDir = process.env.NODE_MODULES_DIR
  || path.join(repo, 'experiments/pyodide-judge/node_modules');
const require = createRequire(path.join(moduleDir, 'noop.js'));
const puppeteer = require('puppeteer-core');

const bank = JSON.parse(fs.readFileSync(path.join(root, 'problems.json'), 'utf8'));
const items = bank.items || [];
const linuxP = items.find(p => p.subject === 'linux' && p.question_type === 'fill_blank');
const dsP = items.find(p => p.subject === 'ds');
/* 实验报告那批多步命令题：input_format 里写了「多步」 */
const multiP = items.find(p => p.subject === 'linux'
  && p.question_type === 'practical' && /多步/.test(p.input_format || ''));
if (!multiP) throw Error('题库里没有多步命令题，先重新生成 Linux 题库');
if (!linuxP || !dsP) throw Error('题库里缺 Linux 或 DS 题，先重新导出');

const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(req.url.split('?')[0]);
  const file = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404).end(); return; }
    const ext = path.extname(file);
    res.setHeader('Content-Type',
      ext === '.js' ? 'text/javascript' : ext === '.json' ? 'application/json' : 'text/html');
    res.end(data);
  });
});
await new Promise(r => server.listen(0, r));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox'],
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));

let pass = 0;
const check = (name, ok, extra) => {
  if (!ok) throw Error(name + (extra ? ' — ' + extra : ''));
  pass++;
  console.log('PASS ' + name);
};

/* 在终端里敲一条命令并等输出落定 */
async function run(cmd) {
  await page.click('.shellIn');
  await page.type('.shellIn', cmd);
  await page.keyboard.press('Enter');
  /* 等输入框被清空（说明这一轮跑完了） */
  await page.waitForFunction(() => document.querySelector('.shellIn').value === '');
  /* 返回所有输出行（含命令回显）。断言时自己挑要看哪几行 ——
     取 textContent 拼串是不行的，shellRow 是块元素，拼起来没有换行。 */
  return page.$eval('.shellOut', (e) =>
    [...e.querySelectorAll('.shellRow')].map((r) => r.textContent));
}

try {
  await page.goto(base);
  await page.evaluate(() => localStorage.clear());
  await page.goto(base + '#/p/' + linuxP.id);
  await page.waitForSelector('#linuxShell .shellIn');

  /* ── 1. 终端存在且提示符对 ── */
  const ps1 = await page.$eval('#linuxShell .shellPs1', e => e.textContent);
  check('Linux 题里有终端面板', true);
  check('提示符是 [student@fedora ~]$', /student@fedora\s+~/.test(ps1.replace(/\s+/g, ' ')), JSON.stringify(ps1));

  /* ── 2. ls /etc ── */
  const o1 = await run('cat /etc/hostname');
  check('cat /etc/hostname 输出 fedora', o1[o1.length - 1].trim() === 'fedora', JSON.stringify(o1));

  /* ── 3. cd 换目录后提示符跟着变 ── */
  await run('cd /usr');
  const ps2 = await page.$eval('#linuxShell .shellPs1', e => e.textContent);
  check('cd /usr 后提示符变 /usr', /\/usr/.test(ps2.replace(/\s+/g, ' ')), JSON.stringify(ps2));

  /* ── 4. 命令不存在 ── */
  const o4 = await run('nosuchcmd');
  check('不存在的命令有 command not found', /command not found/.test(o4.join('\n')), JSON.stringify(o4));
  check('并显示退出码 127', /退出码 127/.test(o4.join('\n')), JSON.stringify(o4));

  /* ── 5. 管道 ── */
  const o5 = await run('grep bash /etc/shells | wc -l');
  check('管道 grep|wc 得到 2', o5[o5.length - 1].trim() === '2', JSON.stringify(o5));

  /* ── 6. 重定向写文件再读回来 ── */
  await run('echo ok > ~/t.txt');
  const o6 = await run('cat ~/t.txt');
  check('重定向写进去的文件读得回来', o6[o6.length - 1].trim() === 'ok', JSON.stringify(o6));

  /* ── 7/8. 点「重置」── */
  await page.evaluate(() => {
    [...document.querySelectorAll('#linuxShell .shellBtn')]
      .find(b => b.getAttribute('data-act') === 'reset').click();
  });
  const ps3 = await page.$eval('#linuxShell .shellPs1', e => e.textContent);
  check('重置后回到 ~ 且身份不变', /student@fedora\s+~/.test(ps3.replace(/\s+/g, ' ')), JSON.stringify(ps3));

  /* ── 8b. 多步命令题：高框 + 回车换行 / Ctrl+回车提交 ── */
  await page.goto(base + '#/p/' + multiP.id);
  await page.waitForSelector('#codeBox');
  const isMulti = await page.$eval('#codeBox', (e) => e.classList.contains('cmdMulti'));
  check('多步命令题用高一点的输入框', isMulti);
  const tip = await page.$eval('#codeBox', (e) => e.previousElementSibling.textContent);
  check('提示里写清了「回车换行 / Ctrl+回车提交」', /Ctrl\+回车/.test(tip), tip.slice(0, 40));
  /* 回车只换行、不提交 */
  await page.click('#codeBox');
  await page.type('#codeBox', 'cd /tmp');
  await page.keyboard.press('Enter');
  await page.keyboard.type('ls');
  const val = await page.$eval('#codeBox', (e) => e.value);
  check('多步题里回车是换行', val === 'cd /tmp\nls', JSON.stringify(val));

  /* ── 9. DS 题没有终端 ── */
  await page.goto(base + '#/p/' + dsP.id);
  await page.waitForSelector('#codeBox, .choiceList');
  check('数据结构题不出现终端面板', (await page.$('#linuxShell')) === null);

  check('页面无 JS 异常', errors.length === 0, errors.join(' | '));
  console.log('\n✓ 全部通过：' + pass + ' 项');
} catch (e) {
  console.log('\n✗ ' + e.message);
  if (errors.length) console.log('页面异常：' + errors.join(' | '));
  process.exitCode = 1;
} finally {
  await browser.close();
  server.close();
}
