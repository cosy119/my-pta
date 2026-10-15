/* Isolated browser C/C++ compiler. No source or test data leaves this worker. */
importScripts('clang/clang-wasm-toolchain.global.js');
const TOOLCHAIN_URL = new URL('clang/', self.location.href).href;
let toolchainPromise = null;
let artifact = null;

function toolchain() {
  if (!toolchainPromise) {
    /* ★ 失败的加载不能缓存：一次网络中断不该变成「这辈子都用不上编译器」。
       清掉缓存，下一次请求会重新走 fetch（大文件下载中途被掐是常态，重试往往就过了）。 */
    toolchainPromise = self.clangWasmToolchain.createToolchain({ baseUrl: TOOLCHAIN_URL,
      onProgress: value => self.postMessage({ type: 'load', value }) })
      .catch(error => { toolchainPromise = null; throw error; });
  }
  return toolchainPromise;
}

function diagnostics(raw) {
  return String(raw || '').replace(/\x1b\[[0-9;]*[A-Za-z]/g, '')
    .split(/\r?\n/).map(s => s.trimEnd())
    .filter(s => s && !/^\s*>|^\s*done\.?\s*$/.test(s)).join('\n');
}

self.onmessage = async event => {
  const m = event.data || {};
  const start = performance.now();
  let phase = 'load';
  try {
    const tc = await toolchain();
    phase = m.type;
    if (m.type === 'compile') {
      artifact = null;
      const lang = m.lang === 'c' ? 'C' : 'CPP';
      const built = await tc.lock(() => tc.captureCompilerOutput(() =>
        tc.runtime.compileArtifact(m.code, { language: lang,
          fileName: lang === 'C' ? 'main.c' : 'main.cpp',
          compileArgs: ['-fgnuc-version=4.2.1', lang === 'C' ? '-std=gnu11' : '-std=gnu++17'] })));
      if (built.error) {
        self.postMessage({ type: 'result', id: m.id,
          payload: { verdict: 'CE', detail: diagnostics(built.raw) || String(built.error),
            stdout: '', stderr: '', ms: Math.round(performance.now() - start) } });
      } else {
        artifact = built.result;
        self.postMessage({ type: 'result', id: m.id,
          payload: { verdict: 'OK', ms: Math.round(performance.now() - start) } });
      }
      return;
    }
    if (m.type !== 'run' || !artifact) throw Error('请先编译程序');
    let sent = false, stdout = '', stderr = '', overflow = false;
    const cap = 128 * 1024;
    const append = (previous, chunk) => {
      if (previous.length + chunk.length > cap) overflow = true;
      return (previous + chunk).slice(0, cap);
    };
    const result = await tc.execute(artifact, { args: [],
      stdin: () => { if (sent) return null; sent = true; return m.stdin || ''; },
      stdout: chunk => { stdout = append(stdout, chunk); },
      stderr: chunk => { stderr = append(stderr, chunk); } });
    self.postMessage({ type: 'result', id: m.id,
      payload: { verdict: overflow ? 'OLE' : result.exitCode === 0 ? 'OK' : 'RE',
        stdout, stderr, ms: Math.round(performance.now() - start),
        detail: result.exitCode === 0 ? '' : '程序退出码：' + result.exitCode } });
  } catch (error) {
    self.postMessage({ type: 'result', id: m.id,
      payload: { verdict: phase === 'load' ? 'IE' : m.type === 'compile' ? 'CE' : 'RE',
        stdout: '', stderr: '', detail: String(error && error.message || error),
        ms: Math.round(performance.now() - start) } });
  }
};
