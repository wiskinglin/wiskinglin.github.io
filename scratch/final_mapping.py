import os
import re
import json

directory = r'c:\Dev\wiskinglin.github.io\_dev\ideas'
idea50_path = os.path.join(directory, 'idea50.html')

with open(idea50_path, 'r', encoding='utf-8') as f:
    idea50_content = f.read()

meta_data_matches = re.findall(r'(\d+):\s*{\s*title:\s*"(.*?)",\s*desc:\s*"(.*?)"\s*}', idea50_content)
meta_data = {int(m[0]): m[1] for m in meta_data_matches}

all_files = [f for f in os.listdir(directory) if f.endswith('.html') and f != 'idea50.html']

mapping = {}

def clean(s):
    return re.sub(r'[^\w\u4e00-\u9fff]', '', s).lower()

# Rebuild mapping by comparing metaData titles with actual file titles or names
for i, meta_title in meta_data.items():
    if i > 39: continue
    
    clean_meta = clean(meta_title)
    best_match = None
    
    # Try filename match
    for f in all_files:
        clean_f = clean(f.replace('.html', ''))
        if clean_meta in clean_f or clean_f in clean_meta:
            best_match = f
            break
            
    if best_match:
        mapping[i] = best_match
    else:
        # Try reading the file's <title> tag
        for f in all_files:
            try:
                with open(os.path.join(directory, f), 'r', encoding='utf-8') as tf:
                    t_content = tf.read(1000) # just read head
                    t_match = re.search(r'<title>(.*?)</title>', t_content, re.I)
                    if t_match:
                        clean_tag = clean(t_match.group(1))
                        if clean_meta in clean_tag or clean_tag in clean_meta:
                            best_match = f
                            break
            except:
                continue
        if best_match:
            mapping[i] = best_match

# Special cases if still missing
# Idea 19 was "賽局決策工具 v2" -> likely "優勢策略分析器.html"
if 19 not in mapping:
    if "優勢策略分析器.html" in all_files: mapping[19] = "優勢策略分析器.html"
# Idea 12 "財富養成鏡" vs "財富養成鏡  投資複利視覺化工具.html"
# Idea 30 "電流急急棒 Pro" vs "極限電流急急棒.html"
if 30 not in mapping and "極限電流急急棒.html" in all_files: mapping[30] = "極限電流急急棒.html"

# Output mapping for verification
print(json.dumps(mapping, ensure_ascii=False, indent=2))

# Update idea50.html
mapping_js = "const fileMapping = " + json.dumps(mapping, ensure_ascii=False) + ";"
new_content = re.sub(r'const fileMapping = {.*?};', mapping_js, idea50_content)
# If it wasn't there (first time), handled by previous script, but let's be sure
if "const fileMapping =" not in new_content:
    new_content = re.sub(r'const totalItems = 50;', mapping_js + '\n        const totalItems = 50;', new_content)

# Ensure the template literals are correct
new_content = new_content.replace('`${i}.html`', 'fileMapping[i] || `${i}.html`')
# Handle the text span
new_content = new_content.replace('${i}.html', '${fileMapping[i] || i + ".html"}')

with open(idea50_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done")
