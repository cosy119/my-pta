/* Service Worker：把题库真正缓存在本地。
 *
 * 为什么需要它
 * ------------
 * GitHub Pages 对所有静态文件一律 `Cache-Control: max-age=600`，这个头站点侧改不了。
 * 实测（国内直连）：`bank/index.json` gzip 后 62 KB 要 14 秒，10 分钟内重开命中
 * 浏览器缓存只要 1.9 秒 —— 但人不会在 10 分钟内反复刷同一个页面，所以真实体感是
 * **每次打开都要等十几秒**。
 *
 * SW 的缓存不受 HTTP TTL 约束，等于把「600 秒后必重下」这条规则绕开。
 * 首访仍是十几秒，之后永久秒开。
 *
 * 策略（按资源分，别一刀切）
 * --------------------------
 *   index.html               network-first，1.5 秒拿不到就用缓存再后台更新
 *                            —— 页面得能更新，但不能让人对着白屏等
 *   bank/index.json          stale-while-revalidate
 *                            —— 先给缓存秒开，同时后台拿新的写回；下次打开即最新
 *   bank/<科目>.json?v=…     cache-first
 *   bank/cases/<id>.json?v=… cache-first
 *                            —— 版本号在 URL 里，题库一变 URL 就变，天然失效；
 *                               所以同一个 URL 的内容永远不用再校验
 *   其它（js/css/图片）      network-first，失败回缓存
 *
 * ★ 不要 cache-first 缓存 index.html：那样改完部署，用户永远看不到新版本。
 */

const VERSION = 'v1';
const SHELL = 'pta-shell-' + VERSION;
const BANK = 'pta-bank-' + VERSION;

/* 页面超时兜底：国内拉一次 HTML 要 1.5 秒左右，给到 2.5 秒。
   超时就用缓存先渲染，网络那边继续跑，回来了顺手把缓存更新掉。 */
const NET_TIMEOUT = 2500;

self.addEventListener('install', () => {
  // 新 SW 立刻进等待态，不把用户卡在旧版本上
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    // 清掉本 SW 之前版本的缓存（别的站点/应用的数据不要碰）
    const keys = await caches.keys();
    await Promise.all(
      keys.filter(k => k.startsWith('pta-') && k !== SHELL && k !== BANK)
          .map(k => caches.delete(k)),
    );
    await self.clients.claim();
  })());
});

/* ---------------- 三种策略 ---------------- */

async function cacheFirst(req, cacheName) {
  const c = await caches.open(cacheName);
  const hit = await c.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  // 只缓存成功响应：404/5xx 存进去就再也刷不掉了
  if (res && res.ok) c.put(req, res.clone());
  return res;
}

async function revalidate(req, cacheName) {
  const c = await caches.open(cacheName);
  const hit = await c.match(req);
  // 不管有没有命中，都在后台去拿一份新的。
  // ★ `cache:'no-cache'` 不能省：默认会让**浏览器自己的 HTTP 缓存**先答话，
  //   而 Pages 给的是 max-age=600，于是「后台更新」拿回来的可能还是十分钟前那份。
  //   no-cache 的语义是「可以用缓存，但必须先跟服务器验证」，能走 304 省流量。
  const net = fetch(req, { cache: 'no-cache' }).then(res => {
    if (res && res.ok) c.put(req, res.clone());
    return res;
  }).catch(() => null);

  if (hit) {
    net.catch(() => {});          // 后台更新失败无所谓，用户手上这份是好的
    return hit;
  }
  const res = await net;
  if (res) return res;
  throw new Error('offline');
}

async function networkFirst(req, cacheName, timeout) {
  const c = await caches.open(cacheName);
  const hit = await c.match(req);
  // ★ 同上，必须 `no-cache`。这里踩过一次真坑：不加的时候改完 index.html 部署，
  //   用户刷新看到的还是旧页面（浏览器 HTTP 缓存把 fetch 挡住了），
  //   等于 SW 把版本更新卡死。实测拿掉 no-cache → 新版本读不到，加上就正常。
  const net = fetch(req, { cache: 'no-cache' }).then(res => {
    if (res && res.ok) c.put(req, res.clone());
    return res;
  }).catch(() => null);

  if (!hit) {
    const res = await net;
    if (res) return res;
    throw new Error('offline');
  }
  const res = await Promise.race([
    net,
    new Promise(r => setTimeout(() => r(null), timeout || NET_TIMEOUT)),
  ]);
  return res || hit;              // 超时就用缓存，别让人干等
}

/* ---------------- 路由 ---------------- */

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch (e) { return; }

  // 只接管同源请求；后端 API、第三方引擎（Pyodide / Clang CDN）一概不碰
  if (url.origin !== self.location.origin) return;

  // ★ /api/* 一律放行：后端在线时它有自己的缓存语义，
  //   离线时本来就会 404 让前端降级，SW 插手只会更乱。
  if (/\/api\//.test(url.pathname)) return;

  const path = url.pathname;

  // 1) 轻索引：秒开 + 后台校验
  if (/\/bank\/index\.json$/.test(path)) {
    event.respondWith(revalidate(req, BANK));
    return;
  }

  // 2) 科目包与拆分出来的测试点：URL 带 ?v=，可以当成永久有效
  if (/\/bank\/cases\/[^/]+\.json$/.test(path) || /\/bank\/[^/]+\.json$/.test(path)) {
    event.respondWith(cacheFirst(req, BANK));
    return;
  }

  // 3) 页面与前端资源
  if (/\.(html|js|css|json|svg|png|jpg|jpeg|webp|ico|woff2?)$/.test(path) || path.endsWith('/')) {
    event.respondWith(networkFirst(req, SHELL, NET_TIMEOUT));
    return;
  }

  // 4) 其它（题库里的 wav 之类）走默认，不缓存
});

/* 前端发消息可以主动清缓存（调试用）：
     navigator.serviceWorker.controller.postMessage({type:'clear-bank'}) */
self.addEventListener('message', event => {
  const t = event.data && event.data.type;
  if (t === 'clear-bank') event.waitUntil(caches.delete(BANK));
  if (t === 'clear-all') event.waitUntil(Promise.all([caches.delete(BANK), caches.delete(SHELL)]));
});
