import { chromium } from 'playwright-extra';
import stealthPlugin from 'puppeteer-extra-plugin-stealth';
import fs from 'fs';

// Use stealth plugin
chromium.use(stealthPlugin());

/**
 * Main Extractor Function
 * @param {string} url 
 * @returns {Promise<object>}
 */
export async function extractData(url) {
  if (!url.startsWith('http')) {
    url = 'https://' + url;
  }

  console.log(`[🔍] Starting analysis for: ${url}`);
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 800 }
  });

  const page = await context.newPage();

  try {
    await context.route('**/*', (route) => {
      const type = route.request().resourceType();
      if (['image', 'font', 'media'].includes(type)) return route.abort();
      route.continue();
    });

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);

    const data = await page.evaluate(() => {
      const getAllTexts = (selector) => Array.from(document.querySelectorAll(selector))
        .map(el => el.innerText.trim()).filter(t => t.length > 0);

      const metadata = {
        title: document.title,
        description: document.querySelector('meta[name="description"]')?.content || '',
        ogTitle: document.querySelector('meta[property="og:title"]')?.content || ''
      };

      const headings = {
        h1: getAllTexts('h1'),
        h2: getAllTexts('h2'),
        h3: getAllTexts('h3')
      };

      const scripts = document.querySelectorAll('script, style, nav, footer, header, noscript');
      scripts.forEach(s => s.remove());

      const paragraphs = Array.from(document.querySelectorAll('p, article, section'))
        .map(p => p.innerText.trim())
        .filter(t => t.split(/\s+/).length > 5)
        .sort((a, b) => b.length - a.length);

      const links = Array.from(document.querySelectorAll('a[href]'))
        .map(a => ({ text: a.innerText.trim(), href: a.href }))
        .filter(l => l.text.length > 2 && l.href.startsWith('http'))
        .slice(0, 15);

      return {
        metadata,
        headings,
        mainContent: paragraphs.slice(0, 8),
        links,
        timestamp: new Date().toISOString()
      };
    });

    return data;

  } catch (err) {
    console.error(`[❌] Failed: ${err.message}`);
    throw err;
  } finally {
    await browser.close();
  }
}

// Keep CLI support
if (process.argv[1].endsWith('extractor.js')) {
  const argUrl = process.argv[2];
  if (argUrl) {
    extractData(argUrl).then(data => {
      console.log(JSON.stringify(data, null, 2));
      process.exit(0);
    });
  } else {
    console.log('Usage: node extractor.js <URL>');
    process.exit(1);
  }
}


