# LINE 官方帳號：本地端資料儲存與 AI 串接指南 (SQLite + 圖片存檔)

本專案旨在建立一個功能完善的 LINE Bot 後端，能將收到的**文字、網址、圖片**自動儲存於本地端，並可選擇性串接運行於本機的 Ollama AI 模型。透過 Tailscale Funnel 提供 HTTPS 網址，解決 LINE Webhook 的安全性需求。

---

## 系統架構

1.  **資料儲存**：使用 SQLite 記錄文字訊息與網址；圖片檔案存於本地資料夾。
2.  **網路穿透**：Tailscale Funnel 將本地 Port 5000 對外開放。
3.  **異步處理**：利用 Threading 避免 LINE Webhook 逾時 (1秒限制)。

---

## 階段一：準備開發環境

1.  **安裝 Python 套件**：
    ```bash
    pip install flask line-bot-sdk requests
    ```

2.  **建立專案目錄結構**：
    系統會自動建立 `data/images` 用於存放圖片。

---

## 階段二：撰寫後端程式 (`app.py`)

此版本包含**自動建立資料庫**、**文字/網址紀錄**、以及**圖片自動下載**功能。

```python
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage
import requests
import threading
import sqlite3
import os
import re
from datetime import datetime

app = Flask(__name__)

# ================= 設定區 =================
LINE_CHANNEL_ACCESS_TOKEN = '請填入_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = '請填入_CHANNEL_SECRET'
DB_PATH = 'data/linebot_records.db'
IMAGE_DIR = 'data/images'
OLLAMA_ENABLED = False  # 設定為 True 即可啟用 AI 回覆
OLLAMA_MODEL = 'llama3'
# ==========================================

# 初始化環境
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            msg_type TEXT,
            content TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    """處理文字與網址紀錄"""
    user_id = event.source.user_id
    user_msg = event.message.text
    
    # 1. 儲存原始文字
    save_to_db(user_id, 'text', user_msg)
    
    # 2. 提取網址並紀錄
    urls = re.findall(r'(https?://[^\s]+)', user_msg)
    for url in urls:
        save_to_db(user_id, 'url', url)

    # 3. 異步處理 AI (若啟用)
    if OLLAMA_ENABLED:
        threading.Thread(target=ai_reply, args=(event,)).start()
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="[系統] 訊息已紀錄。"))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    """處理圖片下載與紀錄"""
    user_id = event.source.user_id
    msg_id = event.message.id
    
    # 下載圖片
    message_content = line_bot_api.get_message_content(msg_id)
    file_path = os.path.join(IMAGE_DIR, f"{msg_id}.jpg")
    
    with open(file_path, 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)
    
    # 紀錄圖片路徑
    save_to_db(user_id, 'image', file_path)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="[系統] 圖片已存檔。"))

def save_to_db(user_id, msg_type, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (user_id, msg_type, content, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, msg_type, content, datetime.now())
    )
    conn.commit()
    conn.close()

def ai_reply(event):
    """(選配) 呼叫本地端 Ollama"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": OLLAMA_MODEL,
            "prompt": event.message.text,
            "stream": False
        })
        ai_text = response.json().get("response", "AI 無回應")
    except:
        ai_text = "Ollama 服務未啟動"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_text))

if __name__ == "__main__":
    app.run(port=5000)
```

---

## 階段三：穿透與設定 (Tailscale + LINE)

1.  **啟動 Funnel**：
    ```bash
    tailscale funnel 5000
    ```
    取得對外網址（例如：`https://msi.tail7921f2.ts.net`）。

2.  **LINE Webhook 設定**：
    *   在 LINE Developers 後台將 Webhook URL 設為：`https://你的網址.ts.net/callback`。
    *   點擊 **Verify** 確認連線成功。

---

## 測試與資料驗證

*   **文字與連結**：傳送包含網址的文字，檢查 `data/linebot_records.db`。
*   **圖片**：傳送照片，檢查 `data/images/` 是否出現新的 `.jpg` 檔案。
*   **查看資料庫**：
    您可以使用 [SQLite Browser](https://sqlitebrowser.org/) 或 VS Code 的 SQLite 套件查看 `records` 資料表內容。
