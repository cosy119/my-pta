import { loadPyodide } from './pyodide/pyodide.mjs';

const base = new URL('python/', import.meta.url);
let judge = null;
let run = null;

async function boot() {
  const py = await loadPyodide({ indexURL: new URL('pyodide/', import.meta.url).href });
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
      payload: { verdict: 'IE', detail: String(error), stdout: '', stderr: '', ms: 0 } });
  }
});

boot().catch(error => self.postMessage({ type: 'fatal', detail: String(error) }));
