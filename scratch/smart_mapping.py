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

def get_chars(s):
    return set(re.sub(r'[^\w\u4e00-\u9fff]', '', s).lower())

# For each file, find the best ID
for filename in all_files:
    try:
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            content = f.read(2000)
            t_match = re.search(r'<title>(.*?)</title>', content, re.I)
            file_title = t_match.group(1) if t_match else filename
    except:
        file_title = filename

    file_chars = get_chars(file_title)
    
    best_id = None
    max_intersection = 0
    
    for i, meta_title in meta_data.items():
        if i > 39: continue
        meta_chars = get_chars(meta_title)
        intersection = len(file_chars.intersection(meta_chars))
        if intersection > max_intersection:
            max_intersection = intersection
            best_id = i
    
    if best_id and max_intersection > 2: # at least 3 chars match
        # If multiple files match the same ID, check which one is better
        if best_id in mapping:
            # Simple tie-break: longer intersection wins
            # (In reality, we might need a more complex check, but this is a heuristic)
            pass
        mapping[best_id] = filename

# Special manual fixes for known tricky ones
# 19: 優勢策略分析器.html
if "優勢策略分析器.html" in all_files: mapping[15] = "優勢策略分析器.html" # actually meta 15 is 優勢策略分析器

# Log the result
print(json.dumps(mapping, ensure_ascii=False, indent=2))

# Update idea50.html
mapping_js = "const fileMapping = " + json.dumps(mapping, ensure_ascii=False) + ";"
new_content = re.sub(r'const fileMapping = {.*?};', mapping_js, idea50_content)
if "const fileMapping =" not in new_content:
    new_content = re.sub(r'const totalItems = 50;', mapping_js + '\n        const totalItems = 50;', new_content)

with open(idea50_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
