import os
import re
import json

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

mapping = {}

# Clean up existing files and inject modal where missing
# We also need to find which file is which.
# I'll re-run for IDs 1..39. Some might not exist anymore as numbered files.

# Step 1: Recover mapping by looking into every file for its title
all_html_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'idea50.html']

# To recover mapping, we need the original metaData as ground truth for what the titles WERE.
idea50_path = os.path.join(directory, 'idea50.html')
with open(idea50_path, 'r', encoding='utf-8') as f:
    idea50_content = f.read()

meta_data_matches = re.findall(r'(\d+):\s*{\s*title:\s*"(.*?)",\s*desc:\s*"(.*?)"\s*}', idea50_content)
meta_data = {int(m[0]): m[1] for m in meta_data_matches}

def sanitize_fn(name):
    name = re.sub(r'[\\/*?:"<>|]', '', name).strip()
    name = name.split('|')[0].split('//')[0].split('-')[0].strip()
    return name

# Redo everything for all IDs
for i in range(1, 40):
    expected_title = meta_data.get(i)
    sanitized = sanitize_fn(expected_title)
    
    # Try to find the file
    target_file = f"{i}.html"
    if not os.path.exists(os.path.join(directory, target_file)):
        # Maybe it was already renamed
        renamed_target = f"{sanitized}.html"
        if os.path.exists(os.path.join(directory, renamed_target)):
            target_file = renamed_target
        else:
            # Try to search for it among all files
            found = False
            for f in all_html_files:
                # If we can't find it by filename, maybe by ID?
                # Actually, I'll just check if the ID is 39, which might still be 39.html
                pass
            if not found:
                continue

    # Now we have the file
    path = os.path.join(directory, target_file)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if modal already exists
    if 'id="help-module"' not in content:
        implemented = ["現代化 RWD 使用者介面設計", "前端互動邏輯與動畫效果", "本地瀏覽器端資料處理"]
        mocked = ["後端 API 真實數據介接", "雲端資料庫持久化儲存", "涉及 AI 運算的部分為模擬效果"]
        if "canvas" in content.lower(): implemented.append("Canvas 影像繪製與處理")
        if "xlsx" in content or "SheetJS" in content: implemented.append("Excel 文件導出/解析功能")
        if "localStorage" in content: implemented.append("本地瀏覽器快取儲存")
        
        impl_str = "".join([f"<li>{item}</li>" for item in implemented])
        mock_str = "".join([f"<li>{item}</li>" for item in mocked])
        modal = status_modal_template.format(implemented=impl_str, mocked=mock_str)
        
        if "</body>" in content:
            content = content.replace("</body>", f"{modal}\\n</body>")
        else:
            content += modal
            
    # Always ensure it is renamed to the sanitized title
    new_name = f"{sanitized}.html"
    new_path = os.path.join(directory, new_name)
    
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    mapping[i] = new_name
    if target_file != new_name:
        os.remove(os.path.join(directory, target_file))
        
# Final update of idea50.html
mapping_js = "const fileMapping = " + json.dumps(mapping, ensure_ascii=False) + ";"
# Find where to insert mapping_js. 
# I previously inserted it, so I should replace it if it exists.
if "const fileMapping =" in idea50_content:
    idea50_content = re.sub(r'const fileMapping = {.*?};', mapping_js, idea50_content)
else:
    idea50_content = re.sub(r'const totalItems = 50;', mapping_js + '\n        const totalItems = 50;', idea50_content)

# Ensure the links use the mapping
idea50_content = idea50_content.replace('`${i}.html`', 'fileMapping[i] || `${i}.html`')
idea50_content = idea50_content.replace('${i}.html', '${fileMapping[i] || i + ".html"}')

with open(idea50_path, 'w', encoding='utf-8') as f:
    f.write(idea50_content)

print("Done")
