const fs = require('fs');
const path = require('path');

const mobileDir = path.join(__dirname, '..', '..', '..', 'mobile');
const logsDir = path.join(__dirname, '..', '..', '..', '_dev', 'logs');
const stateFile = path.join(__dirname, '..', '..', '..', '.agents', 'memory', 'checked_mobile_files.json');

// Ensure directories exist
if (!fs.existsSync(logsDir)) {
    fs.mkdirSync(logsDir, { recursive: true });
}
const memoryDir = path.dirname(stateFile);
if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
}

// Load state
let state = {};
if (fs.existsSync(stateFile)) {
    try {
        state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    } catch (e) {
        state = {};
    }
}

// Scan files
const files = fs.readdirSync(mobileDir).filter(f => f.endsWith('.html'));

let report = `# 📱 Mobile HTML 檢查報告\n\n`;
report += `> 檢查時間：${new Date().toLocaleString('zh-TW', { timeZone: 'Asia/Taipei' })}\n`;
report += `> 參考標準：260327_M_gtc2026.html, 260327_M_Ateam_v2.html\n`;
report += `> \n`;
report += `> **檢查項目包含**：\n`;
report += `> 1. 是否具備 Mobile Viewport Meta Tag\n`;
report += `> 2. 是否注入 Tailwind CSS CDN\n`;
report += `> 3. 是否套用標準字體 (Inter, Noto Sans TC)\n`;
report += `> 4. 是否殘留編輯器用屬性指令 (contenteditable)\n`;
report += `> 5. 是否殘留桌面版工具或控制面板 (id="control-panel")\n\n`;

let checkedCount = 0;
let passedCount = 0;
let failedCount = 0;

const details = [];

files.forEach(file => {
    const filePath = path.join(mobileDir, file);
    const stats = fs.statSync(filePath);
    const mtime = stats.mtimeMs;

    // Check if we already inspected this exact file (based on modified time)
    if (state[file] && state[file] === mtime) {
        return; // Skip, already checked and not modified
    }

    checkedCount++;
    let content = fs.readFileSync(filePath, 'utf8');
    let issues = [];

    // 1. Check viewport
    if (!content.includes('meta name="viewport"')) {
        issues.push('❌ 缺少 meta viewport 標籤。');
    }

    // 2. Check Tailwind
    if (!content.includes('cdn.tailwindcss.com')) {
        issues.push('❌ 缺少 Tailwind CSS CDN。');
    }

    // 3. Check Fonts
    if (!content.includes('Inter') || !content.includes('Noto Sans TC')) {
        issues.push('❌ 缺少或者未引用標準字體組合 (Inter & Noto Sans TC)。');
    }

    // 4. Check Editor residues
    if (content.match(/contenteditable=["']?true["']?/i)) {
        issues.push('❌ 發現殘留編輯模式屬性 (contenteditable="true")。');
    }
    
    // 5. Check Control Panel residues
    if (content.match(/id=["']?control-panel["']?/i)) {
        issues.push('❌ 發現殘留的編輯器控制面板 (id="control-panel")。');
    }

    if (issues.length > 0) {
        failedCount++;
        details.push(`### 📄 ${file}\n` + issues.map(i => `- ${i}`).join('\n') + '\n');
    } else {
        passedCount++;
        details.push(`### 📄 ${file}\n- ✅ 檢查通過，符合行動版 HTML 規格標準。\n`);
    }
    
    // Update state to current modification time
    state[file] = mtime;
});

if (checkedCount === 0) {
    console.log("✅ 沒有新的或已修改的 Mobile HTML 檔案需要檢查。");
    // Ensure we still update the state format if needed
    fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
    return;
}

report += `## 📊 檢查摘要\n`;
report += `- 新增檢查檔案數：**${checkedCount}**\n`;
report += `- 通過數：**${passedCount}**\n`;
report += `- 失敗/需修正數：**${failedCount}**\n\n`;
report += `## 🔍 詳細檢查結果\n\n`;
report += details.join('\n');

const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const reportName = `mobile_check_${timestamp}.md`;
const reportPath = path.join(logsDir, reportName);

fs.writeFileSync(reportPath, report);
fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));

console.log(`✅ 檢查完成！本次總共檢查 ${checkedCount} 個檔案 (${passedCount} 通過, ${failedCount} 須修正)。`);
console.log(`📄 報告已儲存至：_dev/logs/${reportName}`);
