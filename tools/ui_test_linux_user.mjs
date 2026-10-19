/* 真浏览器验收：Linux 登录名 + 实操题。

检查 8 件事：
  1. 没填过登录名时，打开 Linux 题会出「先填一下」的卡片
  2. 没填名就交答案 → 拦住（返回 null）
  3. 填 zhangsan 后：卡片消失、标题栏出现「登录名 zhangsan」、题面出现 /home/zhangsan
  4. `{user}` 占位符在渲染时会换成这个名字
  5. 实操题：徽章是「实操题」、题面有「验收」块、满分 25
  6. 填对验收输出 → 本地判题 AC 满分
  7. 写绝对路径 `/home/zhangsan/...` 也能判过（家目录折叠）
  8. 数据结构线的题不该出现登录名卡片

PTA_SITE_DIR 可指向临时静态导出；默认检查仓库 docs/。
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

const find = (title) => {
  const p = items.find(x => x.title === title);
  if (!p) throw Error('题库里找不到：' + title);
  return p;
};
/* 挑一道**填空**题：选择题渲染的是选项而不是输入框，没 #codeBox */
const linuxP = items.find(p => p.subject === 'linux' && p.question_type === 'fill_blank');
const practical = items.filter(p => p.question_type === 'practical');
if (!practical.length) throw Error('静态题库里没有实操题（question_type=practical）');
const dsP = items.find(p => p.subject === 'ds');

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
await new Promise(resolve => server.listen(0, resolve));
const base = `http://127.0.0.1:${server.address().port}/`;

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--no-sandbox'],
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e)));
const check = (name, ok, extra) => {
  if (!ok) throw Error(name + (extra ? ' — ' + extra : ''));
  console.log('PASS ' + name);
};

try {
  await page.goto(base);
  await page.evaluate(() => localStorage.clear());

  /* ── 1. 首次打开 Linux 题：要出填写卡片 ── */
  await page.goto(base + '#/p/' + linuxP.id);
  await page.waitForSelector('#linuxUserCard');
  check('首次打开 Linux 题弹出登录名卡片', true);

  /* ── 2. 没填名时不给交 ── */
  await page.type('#codeBox', 'ls');
  const blocked = await page.evaluate(() => readTheoryAnswer() === null);
  check('没填登录名时提交被拦住', blocked);
  await page.evaluate(() => { const b = document.getElementById('codeBox'); if (b) b.value = ''; });

  /* ── 3. 填名字 + 密码 → 记住 ── */
  await page.type('#linuxUserInp', 'zhangsan');
  await page.type('#linuxPassInp', 'P@ssw0rd');
  await page.click('#linuxUserBtn');
  await page.waitForFunction(() => !document.getElementById('linuxUserCard'));
  const stored = await page.evaluate(() => localStorage.getItem('pta.linuxUser'));
  check('登录名已落 localStorage', stored === 'zhangsan', String(stored));
  const storedPw = await page.evaluate(() => localStorage.getItem('pta.linuxPass'));
  check('密码已落 localStorage（只存本地）', storedPw === 'P@ssw0rd', String(storedPw));
  const chip = await page.$eval('.chips #linuxUserChip', e => e.textContent);
  check('标题栏出现登录名', /zhangsan/.test(chip), chip);
  const envLine = await page.$eval('.pstmt .hintline', e => e.textContent);
  check('题面显示 /home/zhangsan', /\/home\/zhangsan/.test(envLine), envLine);

  /* ── 3b. 密码默认打码，点「显示」才露明文 ── */
  const maskTxt = await page.$eval('#linuxPassVal', e => e.textContent);
  check('密码默认打码', /^●+$/.test(maskTxt), maskTxt);
  await page.click('.pstmt .hintline .miniBtn');
  const shownTxt = await page.$eval('#linuxPassVal', e => e.textContent);
  check('点「显示」才露明文', shownTxt === 'P@ssw0rd', shownTxt);
  await page.click('.pstmt .hintline .miniBtn');
  check('再点一次收回掩码',
        /^●+$/.test(await page.$eval('#linuxPassVal', e => e.textContent)));

  /* ── 4. {user} 占位符替换 ── */
  const sub = await page.evaluate(() => subUser('家目录 /home/{user}/docs 和 {user}'));
  check('占位符 {user} 会被替换', sub === '家目录 /home/zhangsan/docs 和 zhangsan', sub);

  /* ── 5. 实操题的题面 ── */
  const p5 = practical.find(p => p.title === '把 11.txt 改成 -rwxr-x--x');
  await page.goto(base + '#/p/' + p5.id);
  await page.waitForSelector('.chips .tyTag');
  check('实操题徽章', await page.$eval('.chips .tyTag', e => e.textContent === '实操题'));
  const body = await page.$eval('.pstmt', e => e.textContent);
  check('题面带验收命令', /验收/.test(body) && /stat -c/.test(body));
  check('满分 25', /满分 25 分/.test(body), body.slice(0, 0));

  /* ── 6. 填对验收输出 → AC ── */
  await page.evaluate(() => { CUR && (document.getElementById('codeBox').value = ''); });
  await page.click('#codeBox');
  await page.type('#codeBox', '-rwxr-x--x');
  await page.click('#btnSubmit');
  await page.waitForFunction(() => {
    const h = document.querySelector('#resultBox .verdict');
    return h && /答案正确|AC/.test(h.textContent);
  }, { timeout: 8000 });
  const score6 = await page.evaluate(() => {
    const s = JSON.parse(localStorage.getItem('pta.localProgress') || '{}');
    return s[String(CUR.id)];
  });
  check('实操题判题满分', !!score6 && score6.best_score === 25, JSON.stringify(score6));

  /* ── 7. 绝对路径写法也认 ── */
  const p7 = find('复制目录并保留权限与时间戳');
  await page.goto(base + '#/p/' + p7.id);
  await page.waitForSelector('#codeBox');
  await page.type('#codeBox', 'cp -a /home/zhangsan/docs /tmp/');
  await page.click('#btnSubmit');
  await page.waitForFunction(() => {
    const h = document.querySelector('#resultBox .verdict');
    return h && /答案正确|AC|答案错误|WA/.test(h.textContent);
  }, { timeout: 8000 });
  const verdict7 = await page.$eval('#resultBox .verdict', e => e.textContent);
  check('写 /home/zhangsan/... 也判对', /答案正确|AC/.test(verdict7), verdict7);

  /* ── 8. 别的线不该被打扰 ── */
  await page.goto(base + '#/p/' + dsP.id);
  await page.waitForSelector('.pstmt');
  check('数据结构题不出现登录名卡片', (await page.$('#linuxUserCard')) === null);

  check('无脚本错误', errors.length === 0, errors.join(' | '));
} finally {
  await browser.close();
  server.close();
}
