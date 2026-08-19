#!/usr/bin/env node
// Render thumbnail.html to a 1080x1920 JPG using Playwright + bundled Chromium.
import { chromium } from "playwright";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const projectRoot = resolve(new URL(import.meta.url).pathname, "..", "..");
const htmlPath = resolve(projectRoot, "thumbnail.html");
const outPath = resolve(projectRoot, "public", "thumbnail.jpg");

const executablePath = process.env.PLAYWRIGHT_BROWSER_EXEC
  || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";

const browser = await chromium.launch({ executablePath });
try {
  const ctx = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
  });
  const page = await ctx.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: outPath, type: "jpeg", quality: 92, fullPage: false });
  console.log(`✓ wrote ${outPath}`);
} finally {
  await browser.close();
}
