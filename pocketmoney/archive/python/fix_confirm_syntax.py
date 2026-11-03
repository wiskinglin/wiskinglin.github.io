# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8', newline='') as f:
    text = f.read()

# Replace actual newline in confirm literal
old_str = "if (confirm('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！\n\n確定要完全清空嗎？'))"
old_str_crlf = "if (confirm('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！\r\n\r\n確定要完全清空嗎？'))"
new_str = r"if (confirm('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！\n\n確定要完全清空嗎？'))"

if old_str in text:
    text = text.replace(old_str, new_str)
    print("Replaced old_str LF")
elif old_str_crlf in text:
    text = text.replace(old_str_crlf, new_str)
    print("Replaced old_str CRLF")
else:
    print("Not found old_str, checking regex")
    import re
    text = re.sub(
        r"if\s*\(confirm\('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！[\r\n]+確定要完全清空嗎？'\)\)",
        r"if (confirm('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！\\n\\n確定要完全清空嗎？'))",
        text
    )

with open(target_file, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("Saved!")
