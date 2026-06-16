/**
 * LoopRunner Validator Gate
 *
 * 以 Playwright 開啟本地 HTML 報告，執行 5 項客觀品質檢查。
 * 輸出結構化 Observation JSON（遵循 OpenClaw Gate-as-Observation 模式）。
 *
 * Usage:
 *   node validator.js <filepath>              # 驗證單一報告
 *   node validator.js <filepath> --iteration 2 # 指定目前迴圈輪次
 *   node validator.js --test                   # 對既有報告做冒煙測試
 *
 * 設計原則：
 *   - 驗證失敗 ≠ Error，而是回傳 passed: false 的 Observation
 *   - Agent 可直接讀取 results 陣列中的 detail 進行自動修復
 *   - 硬性上限 maxIterations = 3，防止 token 燒錢失控
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 專案根目錄（_dev/loop/ 的上兩層）
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');

const MAX_ITERATIONS = 3;

/**
 * 核心驗證函式
 * @param {string} filePath - HTML 報告的相對或絕對路徑
 * @param {number} iteration - 目前迴圈輪次（預設 1）
 * @returns {Promise<object>} Observation JSON
 */
async function validate(filePath, iteration = 1) {
  // 解析路徑
  const absolutePath = path.isAbsolute(filePath)
    ? filePath
    : path.resolve(PROJECT_ROOT, filePath);

  if (!fs.existsSync(absolutePath)) {
    return buildObservation(filePath, iteration, [
      { rule: 'file-exists', passed: false, detail: `File not found: ${absolutePath}` }
    ]);
  }

  const fileUrl = `file:///${absolutePath.replace(/\\/g, '/')}`;

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });

  const page = await context.newPage();
  const results = [];

  try {
    // ─── Rule 1: JS Console Error ───
    const consoleErrors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    page.on('pageerror', (err) => {
      consoleErrors.push(err.message);
    });

    await page.goto(fileUrl, { waitUntil: 'networkidle', timeout: 30000 });
    // 等待 Tailwind CDN 或其他資源載入完畢
    await page.waitForTimeout(2000);

    results.push({
      rule: 'js-console-error',
      passed: consoleErrors.length === 0,
      detail: consoleErrors.length === 0
        ? '0 errors'
        : `${consoleErrors.length} error(s): ${consoleErrors.slice(0, 3).join(' | ')}`
    });

    // ─── Rule 2: 內文字級 ≥ 14pt ───
    const fontSizeCheck = await page.evaluate(() => {
      const paragraphs = document.querySelectorAll('.a4-page p');
      const violations = [];

      paragraphs.forEach((p) => {
        const computed = window.getComputedStyle(p);
        const fontSize = parseFloat(computed.fontSize);
        // 14pt ≈ 18.67px，給 0.5px 容差
        const minPx = 18.0;

        // 排除有明確小字 class 的元素（這些是刻意縮小的）
        const hasSmallClass = p.classList.contains('text-xs')
          || p.classList.contains('text-sm')
          || p.classList.contains('sub-text')
          || p.className.match(/text-\[\d+px\]/);

        if (!hasSmallClass && fontSize < minPx) {
          // 取得可辨識的 selector
          const selector = p.closest('[class]')
            ? `.${[...p.closest('[class]').classList].slice(0, 2).join('.')} > p`
            : 'p';
          violations.push({
            selector,
            actual: `${fontSize.toFixed(1)}px (${(fontSize * 0.75).toFixed(1)}pt)`,
            text: p.textContent.trim().substring(0, 40)
          });
        }
      });

      return { total: paragraphs.length, violations };
    });

    results.push({
      rule: 'font-size-14pt',
      passed: fontSizeCheck.violations.length === 0,
      detail: fontSizeCheck.violations.length === 0
        ? `All ${fontSizeCheck.total} <p> elements ≥ 14pt`
        : `${fontSizeCheck.violations.length} element(s) below 14pt: ${JSON.stringify(fontSizeCheck.violations.slice(0, 5))}`
    });

    // ─── Rule 3: Markdown 殘留 ───
    const markdownCheck = await page.evaluate(() => {
      const body = document.body.innerText;
      const patterns = [
        // 偵測未解析的 Markdown 反引號（但排除正常英文縮寫如 it's）
        { name: 'triple-backtick', regex: /```/g },
        // 偵測殘留的 Markdown 標題符號（行首 ## ）
        { name: 'md-heading', regex: /^#{2,6}\s/gm },
        // 偵測殘留的 Markdown 粗體/斜體
        { name: 'md-bold-italic', regex: /\*{2,3}[^*]+\*{2,3}/g }
      ];

      const found = [];
      for (const { name, regex } of patterns) {
        const matches = body.match(regex);
        if (matches) {
          found.push({ pattern: name, count: matches.length, sample: matches[0] });
        }
      }

      return found;
    });

    results.push({
      rule: 'markdown-residual',
      passed: markdownCheck.length === 0,
      detail: markdownCheck.length === 0
        ? 'No Markdown residuals detected'
        : `Found ${markdownCheck.length} pattern(s): ${JSON.stringify(markdownCheck)}`
    });

    // ─── Rule 4: 內部連結有效性 ───
    const linkCheck = await page.evaluate(() => {
      const links = document.querySelectorAll('a[href]');
      const internalLinks = [];

      links.forEach((a) => {
        const href = a.getAttribute('href');
        // 只檢查相對路徑連結（排除 http, mailto, #, javascript）
        if (href && !href.startsWith('http') && !href.startsWith('mailto:')
          && !href.startsWith('#') && !href.startsWith('javascript:')) {
          internalLinks.push({ href, text: a.textContent.trim().substring(0, 30) });
        }
      });

      return internalLinks;
    });

    // 在 Node.js 端檢查檔案是否存在
    const brokenLinks = [];
    const reportDir = path.dirname(absolutePath);

    for (const link of linkCheck) {
      const linkTarget = path.resolve(reportDir, link.href.split('?')[0].split('#')[0]);
      if (!fs.existsSync(linkTarget)) {
        brokenLinks.push({ ...link, resolved: linkTarget });
      }
    }

    results.push({
      rule: 'internal-links',
      passed: brokenLinks.length === 0,
      detail: brokenLinks.length === 0
        ? `All ${linkCheck.length} internal link(s) valid`
        : `${brokenLinks.length} broken link(s): ${JSON.stringify(brokenLinks.slice(0, 5))}`
    });

    // ─── Rule 5: HTML 結構完整性 ───
    const structureCheck = await page.evaluate(() => {
      const issues = [];

      // title 不能為空
      if (!document.title || document.title.trim().length === 0) {
        issues.push('Missing or empty <title>');
      }

      // charset meta 必須存在
      const charset = document.querySelector('meta[charset]');
      if (!charset) {
        issues.push('Missing <meta charset>');
      }

      // viewport meta 必須存在
      const viewport = document.querySelector('meta[name="viewport"]');
      if (!viewport) {
        issues.push('Missing <meta name="viewport">');
      }

      // lang 屬性
      const lang = document.documentElement.getAttribute('lang');
      if (!lang) {
        issues.push('Missing lang attribute on <html>');
      }

      return issues;
    });

    results.push({
      rule: 'html-structure',
      passed: structureCheck.length === 0,
      detail: structureCheck.length === 0
        ? 'All structural checks passed (title, charset, viewport, lang)'
        : `${structureCheck.length} issue(s): ${structureCheck.join(', ')}`
    });

  } catch (err) {
    results.push({
      rule: 'runtime-error',
      passed: false,
      detail: `Validator runtime error: ${err.message}`
    });
  } finally {
    await browser.close();
  }

  return buildObservation(filePath, iteration, results);
}

/**
 * 建構 Observation JSON（OpenClaw Gate-as-Observation 模式）
 */
function buildObservation(filePath, iteration, results) {
  const passedCount = results.filter((r) => r.passed).length;
  const totalCount = results.length;
  const allPassed = passedCount === totalCount;
  const failedRules = results.filter((r) => !r.passed);

  let summary;
  if (allPassed) {
    summary = `✅ All ${totalCount} checks passed.`;
  } else if (iteration >= MAX_ITERATIONS) {
    summary = `❌ ${passedCount}/${totalCount} passed after ${MAX_ITERATIONS} iterations. Human intervention required.`;
  } else {
    summary = `⚠️ ${passedCount}/${totalCount} passed. Fix: ${failedRules.map((r) => r.rule).join(', ')}`;
  }

  return {
    file: filePath,
    timestamp: new Date().toISOString(),
    passed: allPassed,
    iteration,
    maxIterations: MAX_ITERATIONS,
    results,
    summary
  };
}

// ─── CLI Entry Point ───
const args = process.argv.slice(2);

if (args.includes('--test')) {
  // 冒煙測試：對 reports/ 下的第一份報告做驗證
  const reportsDir = path.join(PROJECT_ROOT, 'reports');
  const files = fs.readdirSync(reportsDir).filter((f) => f.endsWith('.html'));

  if (files.length === 0) {
    console.log('No HTML reports found in reports/');
    process.exit(1);
  }

  const target = `reports/${files[files.length - 1]}`;
  console.log(`[🧪] Smoke test: ${target}\n`);

  validate(target).then((obs) => {
    console.log(JSON.stringify(obs, null, 2));
    process.exit(obs.passed ? 0 : 1);
  });

} else if (args.length >= 1) {
  const filePath = args[0];
  const iterIdx = args.indexOf('--iteration');
  const iteration = iterIdx !== -1 ? parseInt(args[iterIdx + 1], 10) : 1;

  validate(filePath, iteration).then((obs) => {
    console.log(JSON.stringify(obs, null, 2));
    process.exit(obs.passed ? 0 : 1);
  });

} else {
  console.log(`
LoopRunner Validator Gate
─────────────────────────
Usage:
  node validator.js <filepath>                # Validate a report
  node validator.js <filepath> --iteration 2  # Specify loop iteration
  node validator.js --test                    # Smoke test on latest report

Examples:
  node validator.js reports/20260616_loop_engineering.html
  node validator.js m/reports/20260616_loop_engineering.html --iteration 2
`);
  process.exit(0);
}
