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

## 階段三：環境穿透與 LINE 平台綁定 (詳細步驟)

本階段是讓外部的 LINE 伺服器能成功連線到您家裡電腦的關鍵。

### 1. 使用 Tailscale Funnel 開放對外通道
Tailscale Funnel 能將本機的 `localhost:5000` 變成一個具備 HTTPS 的公網網址。

1.  **檢查狀態**：確認電腦右下角的工作列中，Tailscale 已登入且顯示為 `Connected`。
2.  **執行穿透指令**：
    開啟一個新的終端機 (PowerShell 或 CMD)，輸入以下指令並保持視窗開啟：
    ```bash
    tailscale funnel 5000
    ```
3.  **確認網址**：
    執行後，畫面上會出現一行 `https://[你的電腦名].[隨機編號].ts.net/`。
    *   這就是您的 **公開伺服器網址**。
    *   請嘗試將此網址貼到瀏覽器，若看到畫面上出現 `404 Not Found` (這是來自 Flask 的正確回應)，代表穿透已成功。
4.  **注意**：此終端機視窗**不可關閉**，否則連線會中斷。

---

### 2. LINE Developers Console 關鍵設定
請開啟瀏覽器並登入 [LINE Developers Console](https://developers.line.biz/console/)。

#### A. 取得與設定金鑰 (填入 app.py)
1.  點擊進入您的 **Messaging API Channel**。
2.  **Channel Secret**：
    *   切換到 **Basic settings** 分頁。
    *   往下捲動找到 `Channel secret`，點擊旁邊的複製按鈕。
    *   填入 `app.py` 中的 `LINE_CHANNEL_SECRET`。
3.  **Channel Access Token**：
    *   切換到 **Messaging API** 分頁。
    *   捲動到最底部的 `Channel access token`。
    *   若為空，請點擊 **Issue** 產生；若已有，請點擊複製。
    *   填入 `app.py` 中的 `LINE_CHANNEL_ACCESS_TOKEN`。
4.  **重新啟動程式**：儲存 `app.py` 後，重新執行 `python app.py` 確保金鑰生效。

#### B. 配置 Webhook (連通測試)
1.  回到 **Messaging API** 分頁，找到 **Webhook URL** 欄位。
2.  點擊 **Edit** 按鈕。
3.  **填寫格式**：將您的 Tailscale 網址完整貼上，並在結尾加上 `/callback`。
    *   範例：`https://msi.tail7921f2.ts.net/callback`
4.  點擊 **Update** 儲存。
5.  **重要開關**：在 Webhook URL 下方的 **Use webhook** 開關，請確認已切換為 **開啟 (綠色)**。
6.  **連通測試**：點擊 **Verify** 按鈕。
    *   若顯示 **Success**：代表 LINE 已經找到您的電腦，連線成功！
    *   若顯示 **Error 500**：請檢查 `python app.py` 是否有錯誤訊息。
    *   若顯示 **Error 404**：請檢查 Webhook URL 是否有漏打 `/callback`。

---

### 3. 關閉 LINE 預設自動回覆 (避免干擾)
為了讓您的 AI 或儲存系統看起來更專業，建議關閉 LINE 官方預設的「罐頭回應」：
1.  在 **Messaging API** 分頁中，找到 **LINE Official Account features** 區塊。
2.  點擊 **Edit** 進入 **LINE Official Account Manager**。
3.  在左側選單進入 **回應設定** (Response settings)：
    *   **回應模式**：設為 `聊天機器人 (Bot)`。
    *   **自動回應訊息**：設為 `停用`。
    *   **Webhook**：設為 `啟用`。

---

## 測試與資料驗證

現在，請拿出手機傳送訊息給您的官方帳號：
1.  **傳送文字**：傳送 "你好，這是測試"，然後檢查 `data/linebot_records.db`。
2.  **傳送圖片**：傳送一張照片，檢查本機 `data/images/` 資料夾是否出現對應的 `.jpg` 檔案。
3.  **傳送網址**：傳送 `https://www.google.com`，驗證資料庫是否單獨提取了該網址。

---

## 測試與資料驗證

*   **文字與連結**：傳送包含網址的文字，檢查 `data/linebot_records.db`。
*   **圖片**：傳送照片，檢查 `data/images/` 是否出現新的 `.jpg` 檔案。
*   **查看資料庫**：
    您可以使用 [SQLite Browser](https://sqlitebrowser.org/) 或 VS Code 的 SQLite 套件查看 `records` 資料表內容。
