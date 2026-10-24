// Puppeteer screenshot runner for localhost visual verification
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const targetUrl = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';

const outDir = path.join(process.cwd(), 'temporary screenshots');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

// Auto-increment screenshot number
const existing = fs.readdirSync(outDir).filter(f => f.startsWith('screenshot-'));
const nextIndex = existing.length + 1;
const filename = label ? `screenshot-${nextIndex}-${label}.png` : `screenshot-${nextIndex}.png`;
const outPath = path.join(outDir, filename);

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await page.goto(targetUrl, { waitUntil: 'networkidle0' });
  await page.screenshot({ path: outPath, fullPage: true });
  await browser.close();
  console.log(`Screenshot saved to: ${outPath}`);
})();