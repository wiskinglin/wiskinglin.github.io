import os
import re
import json

directory = r'c:\Dev\wiskinglin.github.io\_dev\ideas'

# Let's try to find which file belongs to which ID based on metaData in idea50.html
# and the actual filenames currently in the directory.

# First, read idea50.html to get the metaData and the original intended titles.
idea50_path = os.path.join(directory, 'idea50.html')
with open(idea50_path, 'r', encoding='utf-8') as f:
    idea50_content = f.read()

# Extract the existing metaData from JS (lines 158-199 approx)
meta_data_matches = re.findall(r'(\d+):\s*{\s*title:\s*"(.*?)",\s*desc:\s*"(.*?)"\s*}', idea50_content)
meta_data = {int(m[0]): m[1] for m in meta_data_matches}

# Current files in directory
files = os.listdir(directory)
html_files = [f for f in files if f.endswith('.html') and f != 'idea50.html']

mapping = {} # ID -> Filename

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).strip().split('|')[0].split('//')[0].split('-')[0].strip()

# Attempt to match current files to IDs
for i in range(1, 40):
    expected_title = meta_data.get(i, f"Idea_{i}")
    sanitized_expected = sanitize(expected_title)
    
    # Find a file that matches this sanitized title
    match = None
    for f in html_files:
        if sanitized_expected in f:
            match = f
            break
    
    if match:
        mapping[i] = match
    else:
        # Fallback: check if i.html still exists (unlikely)
        if f"{i}.html" in html_files:
            mapping[i] = f"{i}.html"

# If some are missing (e.g. Pikmin duplicates), try harder
# Actually, I'll just check if 1.html ... 39.html still exist.
# If they don't, I'll assume they were renamed.

print(json.dumps(mapping, ensure_ascii=False, indent=2))

# Now update idea50.html
# 1. Update line 220: <span class="text-[10px] text-slate-600 font-mono">${i}.html</span>
# 2. Update line 228: card.onclick = () => window.open(`${i}.html`, '_blank');

new_idea50 = idea50_content

# We need to pass the mapping to the client side JS or replace the logic.
# I'll replace the loop logic to use a lookup.

mapping_js = "const fileMapping = " + json.dumps(mapping, ensure_ascii=False) + ";"
new_idea50 = re.sub(r'const totalItems = 50;', mapping_js + '\n        const totalItems = 50;', new_idea50)

# Replace the HTML and onclick logic
new_idea50 = new_idea50.replace('`${i}.html`', 'fileMapping[i] || `${i}.html`')
new_idea50 = new_idea50.replace('${i}.html', '${fileMapping[i] || i + ".html"}')

with open(idea50_path, 'w', encoding='utf-8') as f:
    f.write(new_idea50)

print("Updated idea50.html")
