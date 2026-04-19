import os
import re

directory = r'c:\Dev\wiskinglin.github.io\_dev\ideas'
status_modal_template = """
<!-- Help Info Button Module -->
<div id="help-module">
    <button id="help-info-btn" style="position:fixed; top:1rem; right:1rem; z-index:9999;" class="bg-indigo-600/80 hover:bg-indigo-500 backdrop-blur-md border border-white/20 text-white rounded-full w-10 h-10 flex items-center justify-center shadow-lg transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm16-40a8,8,0,0,1-8,8,16,16,0,0,1-16-16V128a8,8,0,0,1,0-16,16,16,0,0,1,16,16v40A8,8,0,0,1,144,176ZM112,84a12,12,0,1,1,12,12A12,12,0,0,1,112,84Z"></path></svg>
    </button>
    <div id="help-info-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.6); backdrop-filter:blur(4px); z-index:10000; align-items:center; justify-content:center;">
        <div style="background:#1e293b; border:1px solid #334155; border-radius:1rem; max-width:32rem; width:100%; margin:1rem; padding:1.5rem; box-shadow:0 25px 50px -12px rgba(0,0,0,0.25); position:relative; font-family:sans-serif;">
            <button id="close-help-btn" style="position:absolute; top:1rem; right:1rem; color:#94a3b8; background:none; border:none; cursor:pointer; font-size:1.5rem;">&times;</button>
            <h2 style="font-size:1.25rem; font-weight:bold; color:white; margin-bottom:1rem; display:flex; align-items:center; gap:0.5rem;">
                ℹ️ 應用程式功能說明
            </h2>
            <div style="color:#cbd5e1; font-size:0.875rem; line-height:1.5; display:flex; flex-direction:column; gap:1rem;">
                <div>
                    <h3 style="color:#4ade80; font-weight:600; margin-bottom:0.25rem;">✅ 已實作功能</h3>
                    <ul style="list-style-type:disc; padding-left:1.25rem; color:#e2e8f0;">
                        {implemented}
                    </ul>
                </div>
                <div>
                    <h3 style="color:#fbbf24; font-weight:600; margin-bottom:0.25rem;">🚧 尚未實作 (純前端/Mock)</h3>
                    <ul style="list-style-type:disc; padding-left:1.25rem; color:#94a3b8;">
                        {mocked}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
<script>
    document.getElementById('help-info-btn').addEventListener('click', () => {{
        document.getElementById('help-info-modal').style.display = 'flex';
    }});
    document.getElementById('close-help-btn').addEventListener('click', () => {{
        document.getElementById('help-info-modal').style.display = 'none';
    }});
    document.getElementById('help-info-modal').addEventListener('click', (e) => {{
        if (e.target === document.getElementById('help-info-modal')) {{
            document.getElementById('help-info-modal').style.display = 'none';
        }}
    }});
</script>
"""

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '', name).strip()
    # Remove some common prefix/suffix garbage if needed
    name = name.split('|')[0].split('//')[0].split('-')[0].strip()
    return name

mapping = {}

for i in range(1, 40):
    old_name = f"{i}.html"
    old_path = os.path.join(directory, old_name)
    if os.path.exists(old_path):
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else f"Idea_{i}"
        sanitized = sanitize_filename(title)
        if not sanitized: sanitized = f"Idea_{i}"
        
        new_name = f"{sanitized}.html"
        new_path = os.path.join(directory, new_name)
        
        # Analyze content for features
        implemented = ["現代化 RWD 使用者介面設計", "前端互動邏輯與動畫效果", "本地瀏覽器端資料處理"]
        mocked = ["後端 API 真實數據介接", "雲端資料庫持久化儲存", "涉及 AI 運算的部分為模擬效果"]
        
        # Specific overrides based on content keywords
        if "canvas" in content:
            implemented.append("Canvas 影像繪製與處理")
        if "xlsx" in content or "SheetJS" in content:
            implemented.append("Excel 文件導出/解析功能")
        if "localStorage" in content:
            implemented.append("本地瀏覽器快取儲存")
        if "chart.js" in content.lower() or "echarts" in content.lower():
            implemented.append("動態資料視覺化圖表")

        impl_str = "\\n".join([f"<li>{item}</li>" for item in implemented])
        mock_str = "\\n".join([f"<li>{item}</li>" for item in mocked])
        
        modal = status_modal_template.format(implemented=impl_str, mocked=mock_str)
        
        # Inject before </body>
        if "</body>" in content:
            new_content = content.replace("</body>", f"{modal}\\n</body>")
        else:
            new_content = content + modal
            
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        mapping[i] = new_name
        print(f"Renamed {old_name} -> {new_name}")
        
        # If the filename changed, delete the old one
        if new_name != old_name:
            os.remove(old_path)

# Output mapping for script 2
import json
with open('scratch/mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
