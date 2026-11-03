# -*- coding: utf-8 -*-
import os
import shutil
import subprocess

def run_git(args):
    print("Running:", "git " + " ".join(args))
    res = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8")
    if res.stdout:
        print(res.stdout[:500])
    if res.stderr:
        print("ERR:", res.stderr[:500])
    return res

# 1. 將現有的 _dev/PocketMoney 完整備份到 temp 目錄
src = os.path.abspath('_dev/PocketMoney')
temp_dir = os.path.abspath('_temp_pocketmoney_export')

if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
shutil.copytree(src, temp_dir)
print(f"Copied {src} to {temp_dir}")

# 2. 用 git rm -rf . 將所有 tracked 檔案自 git stage 與工作目錄移除
run_git(["rm", "-rf", "."])

# 3. 確保根目錄清理乾淨（除 .git 之外）
for item in os.listdir('.'):
    if item in ['.git', os.path.basename(temp_dir)]:
        continue
    p = os.path.abspath(item)
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        try:
            os.remove(p)
        except Exception as e:
            print("Could not remove:", p, e)

# 4. 把 temp_dir 移動為根目錄的 pocketmoney
target = os.path.abspath('pocketmoney')
if os.path.exists(target):
    shutil.rmtree(target)
shutil.move(temp_dir, target)
print(f"Moved {temp_dir} to {target}")

# 5. git add pocketmoney
run_git(["add", "pocketmoney"])

# 6. commit
run_git(["commit", "-m", "feat(pocketmoney): isolate pocketmoney directory at root"])
print("Isolation complete.")
