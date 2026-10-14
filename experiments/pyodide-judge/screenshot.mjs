/* 给 PoC 页面截个图，确认 UI 真的正常（顺便验证「填入参考解 + 判题」两个按钮能用）。
 * 用法：node screenshot.mjs
 */
import puppeteer from "puppeteer-core";

const CHROME = process.env.CHROME_PATH || "C:/Program Files/Google/Chrome/Application/chrome.exe";
const POC_URL = process.env.POC_URL || "http://127.0.0.1:8899/";

const browser = await puppeteer.launch({
  executablePath: CHROME, headless: true,
  args: ["--no-sandbox", "--disable-dev-shm-usage"],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 960, deviceScaleFactor: 1 });
  await page.goto(POC_URL, { waitUntil: "load", timeout: 30000 });
  await page.waitForFunction(
    () => document.querySelector("#status")?.classList.contains("ok"),
    { timeout: 90000, polling: 250 });

  // 选一道样例多一点的题，界面信息量大些
  await page.evaluate(() => {
    const picker = document.querySelector("#picker");
    const it = window.__poc.bank.items.find((x) => x.samples.length >= 2);
    if (it) { picker.value = String(it.id); picker.dispatchEvent(new Event("change")); }
  });

  await page.click("#fill");                 // 填入参考解
  await page.click("#run");                  // 判题
  await page.waitForFunction(
    () => document.querySelectorAll("#results .row").length > 0,
    { timeout: 30000, polling: 120 });
  await new Promise((r) => setTimeout(r, 600));

  await page.screenshot({ path: "poc_result.png", fullPage: true });
  const rows = await page.$$eval("#results .row", (els) =>
    els.map((e) => e.className.replace("row ", "") + " " + e.textContent.trim().split("·")[0].trim()));
  console.log("判题结果行：", rows.join(" | "));
  console.log("截图已保存 poc_result.png");
} finally {
  await browser.close();
}
