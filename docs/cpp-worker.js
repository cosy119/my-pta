/* Isolated browser C/C++ compiler. No source or test data leaves this worker. */
importScripts('clang/clang-wasm-toolchain.global.js');
const TOOLCHAIN_URL = new URL('clang/', self.location.href).href;
// A response can return 200 and still fail halfway through its body.
const nativeFetch = self.fetch.bind(self);
self.fetch = async function (input, options) {
  const url = new URL(typeof input === 'string' || input instanceof URL ? input : input.url, self.location.href);
  if (!url.href.startsWith(TOOLCHAIN_URL) ||
      !/\/(?:runtime-manifest\.v1\.json|bin\/(?:clang|lld|memfs)\.wasm\.gz|bin\/sysroot\.tar\.gz)$/.test(url.pathname)) {
    return nativeFetch(input, options);
  }
  const name = url.pathname.split('/').pop();
  let lastError;
  for (let attempt = 1; attempt <= 3; attempt++) {
    const label = '正在下载 ' + name + (attempt > 1 ? '（重试 ' + (attempt - 1) + '/2）' : '');
    self.postMessage({ type: 'load-status', detail: label });
    const controller = new AbortController();
    let timer;
    function resetIdleTimer() {
      clearTimeout(timer);
      timer = setTimeout(() => controller.abort(), 55000);
    }
    resetIdleTimer();
    try {
      const response = await nativeFetch(input, { ...options, signal: controller.signal, ...(attempt > 1 ? { cache: 'reload' } : {}) });
      resetIdleTimer();
      if (response.status === 429 || response.status >= 500) {
        await response.body?.cancel();
        throw Error('HTTP ' + response.status);
      }
      if (!response.ok) return response;
      const total = response.headers.has('content-encoding') ? 0 : Number(response.headers.get('content-length'));
      let received = 0;
      let lastUpdate = -Infinity;
      const formatSize = size => size >= 1024 * 1024
        ? (size / (1024 * 1024)).toFixed(1) + ' MiB' : (size / 1024).toFixed(1) + ' KiB';
      const stream = response.body?.pipeThrough(new TransformStream({
        transform(chunk, output) {
          resetIdleTimer();
          received += chunk.byteLength;
          const now = performance.now();
          if (now - lastUpdate >= 250 || received === total) {
            lastUpdate = now;
            const progress = total > 0 ? ' / ' + formatSize(total) : '';
            self.postMessage({ type: 'load-status', detail: label + ' · ' + formatSize(received) + progress });
          }
          output.enqueue(chunk);
        }
      }));
      const bytes = await new Response(stream).arrayBuffer();
      return new Response(bytes, { status: response.status, headers: response.headers });
    } catch (error) {
      lastError = controller.signal.aborted ? '连续 55 秒未收到下载数据' : String(error.message || error);
    } finally { clearTimeout(timer); }
    if (attempt < 3) await new Promise(resolve => setTimeout(resolve, 700 * attempt));
  }
  throw Error('编译器资源 ' + name + ' 下载失败，已自动重试 2 次：' + lastError + '。请换一个网络后再试。');
};
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
      self.postMessage({ type: 'compile-start', id: m.id });
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
