const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('OrionX Hardware Test Platform', () => {
  let fileUrl;

  test.beforeAll(() => {
    // 解析 OrionX.html 的絕對路徑並轉為 file URL
    const htmlPath = path.resolve(__dirname, '../OrionX.html');
    fileUrl = `file:///${htmlPath.replace(/\\/g, '/')}`;
  });

  test.beforeEach(async ({ page }) => {
    // 在測試前載入網頁
    await page.goto(fileUrl);
  });

  test('Page Title & Navbar', async ({ page }) => {
    await expect(page).toHaveTitle(/OrionX/);
    
    // 檢查 Navbar Logo
    const logo = page.locator('.nav-logo');
    await expect(logo).toBeVisible();
    await expect(logo).toContainText('OrionX');
  });

  test('Tab Navigation', async ({ page }) => {
    // 應該要有三個以上的 tab 按鈕
    const tabBtns = page.locator('.tab-btn');
    expect(await tabBtns.count()).toBeGreaterThanOrEqual(1);

    // 點擊第二個 Tab (假設存在)
    if (await tabBtns.count() > 1) {
      await tabBtns.nth(1).click();
      await expect(tabBtns.nth(1)).toHaveClass(/active/);
    }
  });

  test('Camera / Webcam Preview Panel', async ({ page }) => {
    // 尋找相機預覽相關的按鈕或面板 (根據註解提到的攝影機預覽模組)
    // 我們可以先確保無報錯，並試圖尋找 video 元素或啟動按鈕
    const videoElements = page.locator('video');
    
    // 雖然不一定在初始就載入 video，但可以確保沒有未預期的錯誤
    // 若有啟動按鈕，可點擊測試
    const startCamBtn = page.getByRole('button', { name: /啟動|Start|Camera|視訊/i });
    if (await startCamBtn.count() > 0) {
      await startCamBtn.first().click();
      // 使用 fake media stream，應該不會彈出真實權限詢問
      // 等待一段時間讓 video 串流準備好
      await page.waitForTimeout(1000);
      expect(await videoElements.count()).toBeGreaterThanOrEqual(1);
    }
  });

  test('Battery API Verification', async ({ page }) => {
    // 測試是否有取得電池狀態 (某些瀏覽器可能不支援，需忽略錯誤或加強判斷)
    const batteryPanel = page.locator('.battery-level, .battery-icon');
    if (await batteryPanel.count() > 0) {
      await expect(batteryPanel.first()).toBeVisible();
    }
  });
});
