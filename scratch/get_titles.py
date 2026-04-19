import os
import re

directory = r'c:\Dev\wiskinglin.github.io\_dev\ideas'
results = []

for i in range(1, 40):
    filename = f"{i}.html"
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Unknown"
            results.append((i, title))

for i, title in results:
    print(f"{i}: {title}")
