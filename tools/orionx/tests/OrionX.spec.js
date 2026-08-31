const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('OrionX Hardware Test Platform', () => {
  let fileUrl;

  test.beforeAll(() => {
    const htmlPath = path.resolve(__dirname, '../OrionX.html');
    fileUrl = `file:///${htmlPath.replace(/\\/g, '/')}`;
  });

  test.beforeEach(async ({ page }) => {
    // 授予偽造的權限，讓麥克風與攝影機測試可以順利進行 (不會彈出權限請求對話框)
    await page.context().grantPermissions(['microphone', 'camera']);
    await page.goto(fileUrl);
  });

  // 1. 分頁切換功能 (Tab Navigation) 測試
  test('Tab Navigation', async ({ page }) => {
    const sysTabBtn = page.locator('#tab-btn-system');
    const diagTabBtn = page.locator('#tab-btn-diagnostics');
    const sysContent = page.locator('#tab-system');
    const diagContent = page.locator('#tab-diagnostics');

    // 預設應該是系統分頁
    await expect(sysTabBtn).toHaveClass(/active/);
    await expect(sysContent).toHaveClass(/active/);
    
    // 點擊硬體單元測試分頁
    await diagTabBtn.click();
    await expect(diagTabBtn).toHaveClass(/active/);
    await expect(diagContent).toHaveClass(/active/);
    
    // 系統分頁應該失去 active
    await expect(sysTabBtn).not.toHaveClass(/active/);
    await expect(sysContent).not.toHaveClass(/active/);
  });

  // 2. 系統與顯示規格 (System & Display Specs) 測試
  test('System & Display Specs', async ({ page }) => {
    // 驗證規格數值是否成功載入 (預設文字為 "--"，若有值代表 JS 執行成功)
    await expect(page.locator('#sys-cpu-cores')).not.toHaveText('-- Cores');
    await expect(page.locator('#sys-ram-val')).not.toHaveText('-- GB');
    await expect(page.locator('#sys-os-val')).not.toHaveText('--');
    await expect(page.locator('#disp-resolution')).not.toHaveText('-- x --');
    
    // 驗證 RTC 時鐘
    await expect(page.locator('#rtc-time')).not.toHaveText('--:--:--');
  });

  // 3. 電池狀態監控 (Battery Monitoring) 測試
  test('Battery Monitoring', async ({ page }) => {
    // 驗證電池 UI 元素是否存在
    const batteryLevel = page.locator('#cp-bat-level');
    const batteryText = page.locator('#cp-bat-text');
    const batteryStatus = page.locator('#cp-bat-status');

    await expect(batteryLevel).toBeVisible();
    await expect(batteryText).toBeVisible();
    await expect(batteryStatus).toBeVisible();
  });

  // 4. 音訊測試與控制 (Audio Testing) 測試
  test('Audio Testing Module', async ({ page }) => {
    const micBtn = page.locator('#mic-main-btn');
    const muteBtn = page.locator('#mute-btn');
    const volSlider = page.locator('#vol-slider');
    const iconVolOn = page.locator('#icon-vol-on');
    const iconVolOff = page.locator('#icon-vol-off');

    // 驗證按鈕存在且預設狀態正確
    await expect(micBtn).toBeVisible();
    await expect(muteBtn).toBeVisible();
    await expect(volSlider).toBeVisible();
    await expect(iconVolOn).toBeVisible();
    await expect(iconVolOff).toHaveClass(/hidden/);
    
    // 測試靜音切換
    await muteBtn.click();
    await expect(iconVolOff).not.toHaveClass(/hidden/);
    await expect(iconVolOn).toHaveClass(/hidden/);
    
    // 再次點擊取消靜音
    await muteBtn.click();
    await expect(iconVolOn).not.toHaveClass(/hidden/);
    await expect(iconVolOff).toHaveClass(/hidden/);

    // 測試音量滑桿設定
    await volSlider.fill('40');
    await expect(volSlider).toHaveValue('40');
  });

  // 5. 攝影機/視訊鏡頭預覽 (Webcam Preview) 測試
  test('Webcam Preview Module', async ({ page }) => {
    const toggleWebcamBtn = page.locator('#btn-toggle-webcam');
    const videoElement = page.locator('#webcam-preview-video');
    const statusOverlay = page.locator('#webcam-status-overlay');

    // 點擊啟動鏡頭
    await toggleWebcamBtn.click();
    
    // 由於我們授權了 camera，應該能順利啟動並隱藏 overlay
    // 這裡我們等待一小段時間讓串流啟動
    await page.waitForTimeout(1500);
    
    await expect(videoElement).toBeVisible();
    
    // 再次點擊應為關閉鏡頭
    await toggleWebcamBtn.click();
    await expect(statusOverlay).toBeVisible();
  });

  // 6. 硬體單元測試 - 螢幕顯示診斷 (Display Diagnostics)
  test('Display Diagnostics Tests', async ({ page }) => {
    await page.locator('#tab-btn-diagnostics').click();
    const testScreen = page.locator('#test-screen');
    const exitBtn = page.locator('#exit-test');

    // 測試「壞點與亮點」功能
    await page.locator('button[data-test="pixel"]').click();
    await expect(testScreen).toBeVisible();
    await expect(page.locator('#controls-pixel')).toBeVisible();
    await exitBtn.click();
    await expect(testScreen).toBeHidden();

    // 測試「亮度與均勻度」功能
    await page.locator('button[data-test="uniformity"]').click();
    await expect(testScreen).toBeVisible();
    await expect(page.locator('#controls-uniformity')).toBeVisible();
    await exitBtn.click();
    await expect(testScreen).toBeHidden();

    // 測試「反應時間」功能
    await page.locator('button[data-test="response"]').click();
    await expect(testScreen).toBeVisible();
    await exitBtn.click();
    await expect(testScreen).toBeHidden();

    // 測試「可視角度」功能
    await page.locator('button[data-test="viewingangle"]').click();
    await expect(testScreen).toBeVisible();
    await exitBtn.click();
    await expect(testScreen).toBeHidden();
  });

  // 7. 硬體單元測試 - 觸控診斷 (Touch Diagnostics)
  test('Touch Diagnostics Tests', async ({ page }) => {
    await page.locator('#tab-btn-diagnostics').click();
    const testScreen = page.locator('#test-screen');
    const exitBtn = page.locator('#exit-test');

    // 測試各項觸控功能是否能順利開啟與關閉
    const touchTests = ['taps', 'gestures', 'drag', 'drawing', 'edges', 'multitouch'];
    
    for (const testId of touchTests) {
      await page.locator(`button[data-test="${testId}"]`).click();
      await expect(testScreen).toBeVisible();
      if (testId === 'drawing') {
        await expect(page.locator('#controls-drawing')).toBeVisible();
      }
      await exitBtn.click();
      await expect(testScreen).toBeHidden();
    }
  });

  // 8. 測試狀態與報告彈窗 (Report Overlay) 測試
  test('Report Overlay Module', async ({ page }) => {
    // 強制觸發顯示報告
    await page.evaluate(() => {
      const overlay = document.getElementById('report-overlay');
      if (overlay) overlay.classList.add('active');
    });

    const reportOverlay = page.locator('#report-overlay');
    await expect(reportOverlay).toHaveClass(/active/);

    // 關閉按鈕
    const closeBtn = page.locator('#btn-close-report');
    await expect(closeBtn).toBeVisible();
    
    // 點擊關閉
    await closeBtn.click();
    await expect(reportOverlay).not.toHaveClass(/active/);
  });

});
