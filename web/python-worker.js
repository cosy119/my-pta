import { loadPyodide } from './pyodide/pyodide.mjs';

const base = new URL('python/', import.meta.url);
let judge = null;
let run = null;

/* ★ 加载失败的原因不一定是 Error：Pyodide / 浏览器在流被掐断时偶尔抛普通对象，
   直接被 String() 一裹就变成界面上毫无信息量的「[object Object]」。统一describe。 */
function describe(error) {
  if (error == null) return '未知错误';
  if (typeof error === 'string') return error;
  if (error instanceof Error || error.stack) return String(error.message || error);
  if (error.message) return String(error.message);
  try { const s = JSON.stringify(error); if (s && s !== '{}') return s; } catch (e) { /* 忽略 */ }
  return String(error);
}

/* ★ 标准库这一步 Pyodide 会「吞掉」失败（installStdlib 里只 console.error 就继续启动），
   于是 Python 在没有标准库的情况下崩成一句没头没脑的 'Failed to import encodings module'
   → 'Program terminated with exit(1)'，用户完全看不出该怎么办。先自己拉一遍验字节数，
   把话说清楚，并告诉他出路。 */
async function assertStdlib(url) {
  let status = 0, bytes = 0;
  try {
    const response = await fetch(url);
    status = response.status;
    bytes = (await response.arrayBuffer()).byteLength;
  } catch (error) {
    throw Error('判题引擎的 Python 标准库下载失败（' + describe(error) + '）。'
      + '检查网络后**再点一次「提交并判题」**就会重新下载，不用刷新页面。');
  }
  if (!bytes)
    throw Error('判题引擎的 Python 标准库没拿到内容：python_stdlib.zip 返回 HTTP ' + status
      + '、0 字节。**再点一次「提交并判题」**重试；若每次都是这句，多半是本机安全软件 /'
      + ' 浏览器策略拦了 .zip 下载（网页防护、下载保护这类开关），关掉它或换个浏览器再试。');
}

async function boot() {
  const indexURL = new URL('pyodide/', import.meta.url).href;
  await assertStdlib(indexURL + 'python_stdlib.zip');
  let py;
  try {
    py = await loadPyodide({ indexURL });
  } catch (error) {
    const reason = describe(error);
    /* 标准库没装成时 Pyodide 会在 bootstrap 阶段直接 exit(1)，翻译成人话。 */
    if (/encodings|Program terminated/i.test(reason))
      throw Error('判题引擎的 Python 标准库没装成（' + reason + '）。'
        + '**再点一次「提交并判题」**重试；若每次都是这句，多半是本机安全软件 /'
        + ' 浏览器策略拦了 .zip 下载，关掉它或换个浏览器再试。');
    throw error;
  }
  const [compare, driver] = await Promise.all([
    fetch(new URL('compare.py', base)).then(r => { if (!r.ok) throw Error('compare.py: HTTP ' + r.status); return r.text(); }),
    fetch(new URL('driver.py', base)).then(r => { if (!r.ok) throw Error('driver.py: HTTP ' + r.status); return r.text(); }),
  ]);
  py.FS.writeFile('/home/pyodide/compare.py', compare);
  py.FS.writeFile('/home/pyodide/driver.py', driver);
  py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
  judge = py.runPython('from driver import judge; judge');
  run = py.runPython('from driver import run; run');
  self.postMessage({ type: 'ready', python: String(py.runPython('import sys; sys.version.split()[0]')) });
}

self.addEventListener('message', event => {
  const m = event.data || {};
  if (m.type !== 'case') return;
  try {
    const raw = m.mode === 'run'
      ? run(m.code, m.stdin || '')
      : judge(m.code, m.stdin || '', m.expected || '', m.checker || 'standard', m.eps || 1e-6);
    self.postMessage({ type: 'result', id: m.id, payload: JSON.parse(String(raw)) });
  } catch (error) {
    self.postMessage({ type: 'result', id: m.id,
      payload: { verdict: 'IE', detail: describe(error), stdout: '', stderr: '', ms: 0 } });
  }
});

boot().catch(error => self.postMessage({ type: 'fatal', detail: describe(error) }));
