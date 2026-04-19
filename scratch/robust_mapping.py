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

for i, meta_title in meta_data.items():
    if i > 39: continue
    c_meta = clean(meta_title)
    
    # Heuristic: find file that contains most of the meta title characters or vice versa
    best_f = None
    best_score = 0
    
    for f in all_files:
        c_f = clean(f)
        # Check title in file content too
        try:
            with open(os.path.join(directory, f), 'r', encoding='utf-8') as tf:
                head = tf.read(1000)
                t_match = re.search(r'<title>(.*?)</title>', head, re.I)
                if t_match:
                    c_f = clean(t_match.group(1))
        except: pass
        
        # Intersection score
        common = len(set(c_meta) & set(c_f))
        score = common / max(len(c_meta), 1)
        
        if score > best_score:
            best_score = score
            best_f = f
            
    if best_f and best_score > 0.4:
        mapping[i] = best_f

# Re-inject mapping
mapping_js = "const fileMapping = " + json.dumps(mapping, ensure_ascii=False) + ";"
updated_content = re.sub(r'const fileMapping = {.*?};', mapping_js, idea50_content)
with open(idea50_path, 'w', encoding='utf-8') as f:
    f.write(updated_content)

print(f"Mapped {len(mapping)} items.")
