# Playwright 進階網頁資料採集與反爬蟲繞過技術深度解析報告

在現代網頁技術的快速演進下，單頁應用程式（Single Page Application, SPA）、伺服器端渲染（Server-Side Rendering, SSR）以及複雜的非同步資料載入機制已成為全球資訊網的標準配備。傳統的 HTTP 請求式網頁爬蟲（如 Python 的 Requests 搭配 BeautifulSoup 或 Node.js 的 Axios 搭配 Cheerio）在面對高度依賴 JavaScript 動態生成 DOM 結構的網頁時，已逐漸顯得力不從心。

為了解析動態內容並有效模擬真實使用者的互動行為，以 Chrome DevTools Protocol (CDP) 為基礎的自動化瀏覽器控制工具成為了業界進行大規模資料萃取的主流方案。在眾多自動化工具中，由微軟維護的 Playwright 憑藉其卓越的跨瀏覽器支援（Chromium、Firefox、WebKit）、原生的非同步事件驅動架構、強大且細緻的網路請求攔截能力，以及基於 Browser Context（瀏覽器上下文）的輕量級資源隔離機制，已成為當前數據採集工程與自動化領域的核心基礎設施。

不同於 Selenium 依賴 WebDriver 進行中介通訊，Playwright 直接透過 WebSocket 與瀏覽器底層進行雙向通訊，這使其在執行速度、事件監聽的精準度以及網路層級的控制力上具有決定性的優勢。本報告將專注於 Playwright 在「進階網頁資料爬取」領域的深度應用，並完全排除其作為端到端（End-to-End）自動化測試框架的相關功能與概念（如斷言、測試報告生成等）。

本深度技術分析將聚焦於五大核心範疇：
1. 反爬蟲機制的繞過與隱身技術
2. 網路請求攔截與底層 API 數據擷取
3. 資源最佳化與極速爬取策略
4. 複雜動態網頁與非同步渲染處理
5. 結合代理伺服器池與高併發架構的記憶體管理實務

透過剖析底層通訊原理並輔以具體程式碼實作，本報告旨在提供一套適用於企業級高吞吐量數據採集的最佳實踐與架構指南。

---

## 1. 反爬蟲機制的繞過與隱身技術

在 2026 年的防護環境中，以 Cloudflare Bot Management、DataDome、Akamai 以及 Kasada 為首的進階 Web 應用程式防火牆 (WAF) 與反爬蟲系統，已從單純的 IP 聲譽檢查與請求頻率限制，全面進化為全方位的會話（Session）分析與硬體環境特徵檢測。

原生且未經特殊處理的 Playwright 或 Puppeteer 實例，由於具有明顯的機器人特徵，通常在發起網路請求的數秒內即會遭到精準攔截，並被重導向至 Turnstile 驗證碼頁面或陷入無盡的 JavaScript 挑戰迴圈。要實現高成功率的資料爬取，工程師必須深入理解防禦方的檢測機制，並針對網路層與應用層進行徹底的瀏覽器指紋（Browser Fingerprinting）竄改與隱身。

### 1.1 網路層防護：TLS 指紋與 HTTP/2 檢測機制

現代防護系統的檢測從 TCP 連線建立的那一刻起便已展開。在網路層面，Cloudflare 等系統會深度分析 TLS 握手（TLS Handshake）過程中的 JA3 與 JA4 指紋特徵。JA3/JA4 指紋是透過雜湊用戶端在 Client Hello 封包中提供的 TLS 版本、Cipher Suites（密碼套件）排列順序、擴充欄位（Extensions）以及橢圓曲線參數所生成的一組唯一識別碼。

原生 Node.js 環境或未經調校的無頭瀏覽器（Headless Browser）所發出的 TLS 握手特徵，與真實的家用版 Chrome 瀏覽器存在細微卻致命的差異。當防護系統發現一個聲稱自己是 Chrome 120 的請求，其 TLS 握手特徵卻與已知的 Node.js 函式庫或異常工具庫相符時，該請求的信任分數（Trust Score）便會瞬間歸零，並在後續引發嚴格的封鎖。

除了 TLS 指紋，HTTP/2 的網路流量特徵也成為近期反爬蟲系統的偵測重點。HTTP/2 引入了多工處理（Multiplexing）與優先權樹（Priority Trees）的概念，不同的瀏覽器引擎（Blink、Gecko、WebKit）在建立 HTTP/2 連線時，其分配串流優先權與處理併發請求的底層邏輯各不相同。若自動化工具無法完美模擬目標瀏覽器的 HTTP/2 網路特徵，即便應用層的指紋偽裝得再完美，仍會在網路基礎設施層面被識破。解決此問題的進階方案通常涉及使用經過修補的 cURL 函式庫（如 curl-impersonate）或依賴完全託管的防護繞過 API 服務。

### 1.2 應用層防護：瀏覽器指紋特徵解析

一旦網路層的檢測通過，防護系統會向客戶端發送一段經過高度混淆（Obfuscated）的 JavaScript 挑戰腳本。該腳本會在瀏覽器環境中非同步執行，蒐集極其詳盡的硬體與軟體環境指紋，並將結果回傳至伺服器進行機器學習模型評分。

核心的檢測維度包含：
*   **WebDriver 標記**：根據 W3C 規範，自動化瀏覽器會在 `navigator` 物件中強制注入 `webdriver: true` 屬性。這是防禦方最容易辨識也是最致命的自動化特徵。
*   **硬體渲染指紋 (Canvas & WebGL)**：防護腳本會利用 HTML5 Canvas 繪製包含特定文字與幾何圖形的隱藏畫布，並提取其像素資料轉化為 Base64 雜湊值；同時透過 WebGL API 查詢顯示卡的渲染器（Renderer）與供應商（Vendor）資訊。由於伺服器環境通常缺乏實體 GPU，其依賴軟體渲染所產生的特徵與真實設備截然不同。
*   **外掛程式與媒體特徵**：真實瀏覽器通常內建多種外掛（如 PDF Viewer），而無頭瀏覽器的 `navigator.plugins` 陣列往往為空。此外，還會透過 AudioContext 產生音訊波形特徵（Audio Fingerprinting），以及檢查字型列表與螢幕解析度。
*   **行為模式分析 (Behavioral Analysis)**：進階系統會記錄使用者的滑鼠移動軌跡、點擊節奏、滾動頻率以及輸入延遲。

### 1.3 結合 Stealth 套件與底層 API 覆寫實務

在 Playwright 生態系中，最為成熟的實務作法是結合 `playwright-extra` 框架與 `puppeteer-extra-plugin-stealth` 擴充套件。該套件會在文件建立前，透過 CDP 通訊動態注入大量的 JavaScript 墊片（Polyfills）與代理函式（Proxies），抹除自動化特徵。

以下程式碼示範了如何整合 Stealth 隱身套件，並結合自訂的環境變數覆寫來提升隱身效果：

```javascript
import { chromium } from 'playwright-extra';
import stealthPlugin from 'puppeteer-extra-plugin-stealth';

// 將隱身套件掛載至 Chromium 實例
const stealth = stealthPlugin();
chromium.use(stealth);

(async () => {
  // 啟動瀏覽器時，注入特定的啟動參數以移除自動化指示器 
  const browser = await chromium.launch({
    headless: true, 
    args: [
      '--disable-web-security',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage'
    ]
  });
  
  // 建立具有擬真設定的 Context 
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'zh-TW',
    timezoneId: 'Asia/Taipei',
    colorScheme: 'dark',
    viewport: { width: 1920, height: 1080 }
  });

  // 進階實務：針對高度敏感的防護，手動透過 addInitScript 在環境中進行更深度的覆寫
  await context.addInitScript(() => {
    // 徹底抹除 webdriver 標記
    if (navigator.webdriver !== undefined) {
      delete Object.getPrototypeOf(navigator).webdriver;
    }
    
    // 偽裝 Plugins 陣列
    Object.defineProperty(navigator, 'plugins', {
      get: () => [
        { name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer' },
        { name: 'Microsoft Edge PDF Viewer', filename: 'internal-pdf-viewer' }
      ],
    });

    // 偽裝 WebGL 渲染器，避免暴露雲端伺服器的 SwiftShader 特徵
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
      if (parameter === 37445) return 'Google Inc. (NVIDIA)'; // UNMASKED_VENDOR_WEBGL
      if (parameter === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)'; // UNMASKED_RENDERER_WEBGL
      return getParameter.call(this, parameter);
    };
  });

  const page = await context.newPage();
  
  // 加入隨機延遲與擬真導覽行為
  await page.waitForTimeout(Math.random() * 2000 + 1000);
  await page.goto('https://cloudflare-protected-site.example.com', { waitUntil: 'domcontentloaded' });
})();
```

在實務中，單純依賴 Stealth 套件並無法保證永久免疫。防禦系統會持續更新其腳本，透過反射與內省技術檢查 API 是否被劫持。因此，工程師必須定期驗證其偽裝策略的有效性。

### 1.4 C++ 核心修補與進階防護繞過架構

隨著防護機制的升級，純 JavaScript 層級的指紋修補逐漸遭遇瓶頸。因此，進階的數據採集架構開始轉向修改瀏覽器原始碼（Source Code Patching）的深層解決方案。

| 工具/方案 | 底層引擎 | 實作機制 | 隱蔽性與檢測率 | 適用情境與優勢 |
| :--- | :--- | :--- | :--- | :--- |
| **Playwright-Extra (Stealth)** | 官方 Chromium / WebKit | JavaScript 屬性覆寫與 Proxy 代理劫持 | 中等。易被進階反射 API 識破 | 適用於中低強度防護網站。部署簡單。 |
| **Patchright** | 修改版 Chromium | C++ 層級修補 CDP 洩漏點，透過 JS 隔離防止追蹤 | 高。減少約 67% 無頭瀏覽器檢測率 | 適用於需保留 Chrome 生態系擴充功能的情境。 |
| **Camoufox** | 修改版 Firefox | C++ 層級直接篡改指紋生成邏輯，阻斷自動化 API 暴露 | 極高。可達 0% 無頭檢測率 | 應對頂級防禦（如嚴格的 Cloudflare Turnstile）。 |

---

## 2. 網路請求攔截與底層 API 數據擷取

高階的數據採集策略已發生典範轉移：完全跳過繁瑣且脆弱的 HTML DOM 解析，轉而利用 Playwright 強大的網路攔截能力，直接監聽並擷取底層 API 數據。

### 2.1 監聽與攔截 XHR/Fetch 請求獲取 JSON 數據

爬蟲工程師應先利用瀏覽器的 DevTools 觀察目標資料所在的 API 端點。一旦確認了模式，即可在腳本中使用 `page.waitForResponse()` 方法精確捕捉回應內容。

```javascript
// 定義目標 API 的 URL 特徵
const targetApiUrl = '**/api/v1/products/search*';

// 啟動 Promise.all 確保網路監聽器在動作觸發前已就緒
const [response] = await Promise.all([
  page.waitForResponse(res => res.url().includes('/api/v1/products/search') && res.status() === 200, { timeout: 15000 }),
  // 執行觸發請求的動作
  page.locator('button#submit-search').click() 
]);

// 獲取底層網路回應並解析為 JSON
const responseBody = await response.json();

// 直接操作 JSON 數據
const extractedData = responseBody.data.results.map(item => ({
  productId: item.id,
  productName: item.title,
  currentPrice: item.pricing.discounted_price,
  stockAvailable: item.inventory.quantity,
  hiddenSupplierId: item.internal_supplier_id
}));

console.log(`成功提取 ${extractedData.length} 筆商品資料`);
```

### 2.2 動態修改 Request Headers 與偽造 Referer

Playwright 允許開發者透過 `page.route()` 攔截網路流量，並動態竄改 HTTP Headers，藉此完美偽裝請求來源。

```javascript
// 攔截特定 API 請求，動態修改 Headers
await page.route('**/api/v1/secure-endpoint', async (route) => {
  const request = route.request();
  
  const headers = {
    ...request.headers(),
    'Referer': 'https://trusted-partner.example.com/portal',
    'Origin': 'https://trusted-partner.example.com',
    'X-Custom-Client-Version': 'v2.4.1'
  };

  // 移除自動化身分標頭
  delete headers['x-playwright-trace'];
  delete headers['x-forwarded-for'];

  await route.continue({ headers });
});
```

### 2.3 Browser Context 級別的 Cookies 管理與會話注入

最佳實務是將「認證流程」與「採集流程」解耦。先由專門模組登入並保存 `Session State`，隨後將 Cookies 注入至獨立的 `Browser Context` 中。

```javascript
// 注入 Cookies 實現免登入採集
const context = await browser.newContext();
await context.addCookies(validSessionCookies);

const page = await context.newPage();
await page.goto('https://target-site.example.com/user-dashboard');
```

---

## 3. 資源最佳化與極速爬取策略

在導覽至網頁時，瀏覽器會加載所有資源。對於純粹的數據採集而言，阻擋圖片、樣式、字型等無關資源可顯著提升速度。

### 3.1 阻擋不必要的資源載入與第三方追蹤腳本

```javascript
await context.route('**/*', (route) => {
  const request = route.request();
  const resourceType = request.resourceType();

  // 1. 阻擋靜態資源與媒體
  const blockedTypes = ['image', 'stylesheet', 'font', 'media', 'manifest', 'other'];
  if (blockedTypes.includes(resourceType)) {
    return route.abort('aborted');
  }

  // 2. 阻擋第三方分析腳本
  const blockedDomains = ['google-analytics.com', 'googletagmanager.com', 'sentry.io'];
  const url = new URL(request.url());
  if (blockedDomains.some(domain => url.hostname.includes(domain))) {
    return route.abort('blockedbyclient');
  }

  route.continue();
});

// 強制關閉動畫與轉場
await context.addInitScript(() => {
  const style = document.createElement('style');
  style.textContent = `
    *, *::before, *::after {
      transition: none!important;
      animation: none!important;
      scroll-behavior: auto!important;
    }
  `;
  document.documentElement.appendChild(style);
});
```

### 3.2 導覽等待策略與批量 DOM 擷取優化

將 `waitUntil` 設定為 `domcontentloaded` 以提早介入。同時，將 DOM 解析邏輯封裝至單一的 `page.evaluate()` 區塊內，一次性完成批量解析，減少跨進程通訊延遲。

### 3.3 架構設計：Browser、Context 與 Page 的資源消耗比較

| 架構層級 | 資源佔用 | 隔離程度 | 核心應用場景 |
| :--- | :--- | :--- | :--- |
| **Browser** | 極高 (數百 MB) | 絕對隔離 | 僅適用於跨瀏覽器核心的情境。應避免頻繁啟動。 |
| **Browser Context** | 極低 (輕量級) | 會話級隔離 | 高併發資料採集的核心單位。每個任務建立專屬 Context。 |
| **Page** | 中低 | 無隔離 | 適用於在同一身份下抓取多個分頁的情境。 |

**黃金法則**：維持單一常駐 `Browser`，為每個任務創建獨立 `Context`，完成後立即銷毀。

---

## 4. 複雜動態網頁與非同步渲染處理

### 4.1 穩定處理無限捲動與延遲載入頁面

精準的實作方式是利用 `Promise.all` 將「觸發動作」與「監聽回應」緊密結合，並透過 `waitForFunction` 確認 DOM 渲染完成。

```javascript
while (currentItemCount < targetItemCount && consecutiveFailures < maxRetries) {
  try {
    const [response] = await Promise.all([
      page.waitForResponse(res => res.url().includes('/api/v2/catalog/infinite-feed'), { timeout: 8000 }),
      page.evaluate(() => window.scrollBy(0, document.body.scrollHeight))
    ]);
    
    await page.waitForFunction((prevCount) => {
      return document.querySelectorAll('.product-card-item').length > prevCount;
    }, currentItemCount);

    currentItemCount = await page.locator('.product-card-item').count();
    consecutiveFailures = 0; 
  } catch (error) {
    consecutiveFailures++;
    await page.waitForTimeout(1500 + Math.random() * 1000);
  }
}
```

### 4.2 解析前端框架狀態變數（如 Next.js 的 __NEXT_DATA__）

直接從 HTML 原始碼中的隱藏 `<script>` 標籤提取 JSON 物件，避開繁瑣的 DOM 解析。

```javascript
const nextDataString = await page.evaluate(() => {
  const scriptTag = document.querySelector('script#__NEXT_DATA__');
  return scriptTag ? scriptTag.textContent : null;
});

if (nextDataString) {
  const nextData = JSON.parse(nextDataString);
  const products = nextData.props.pageProps.initialState.productCatalog.items;
  console.log(`提取 ${products.length} 筆商品資料`);
}
```

---

## 5. 代理伺服器池與高併發架構記憶體管理

### 5.1 動態配置與切換 Proxy 的實務作法

在建立新的 `Context` 時隨機抽取或依權重分配代理伺服器，實現大規模的 IP 輪替。

### 5.2 結合 p-limit 實現高併發控制

使用 `p-limit` 提供確定性的併發數量控制，確保系統資源維持在安全範圍內。

```javascript
import pLimit from 'p-limit';
const limit = pLimit(15); 

const tasks = urls.map(url => limit(() => executeScrapeTask(browser, url)));
await Promise.all(tasks);
```

### 5.3 V8 引擎記憶體溢出 (OOM) 預防與記憶體管理最佳實務

1.  **提升記憶體上限**：使用 `--max-old-space-size=8192`。
2.  **生命週期控管**：嚴格執行 `try-catch-finally` 中的 `.close()`。
3.  **定期強制重啟**：例如每處理 1,000 個任務後重啟 `Browser` 實例，清除底層緩存。

---

綜上所述，將 Playwright 應用於高階網頁資料採集，是一門橫跨底層網路通訊協定、瀏覽器核心機制、非同步系統架構與防護繞過的深度工程。從反爬蟲機制的對抗來看，必須深度結合 API 覆寫與 stealth 套件，甚至依賴核心修補技術。在效能優化方面，轉向基於 CDP 的底層網路攔截，方能實現真正的高效運作。最終，透過精準掌控併發量與嚴謹的記憶體管理，確保系統得以長效穩定運作。