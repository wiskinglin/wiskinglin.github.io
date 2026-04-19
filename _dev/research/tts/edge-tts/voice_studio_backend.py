"""
Local AI Voice Studio Backend
使用 edge-tts (Microsoft Edge TTS 雲端引擎) 提供真實語音合成功能

啟動方式:
    cd c:\Dev\wiskinglin.github.io\_dev\on-going
    python voice_studio_backend.py

前端頁面:
    http://127.0.0.1:8000/           → Edge TTS 語音合成 (主頁)
    http://127.0.0.1:8000/edge-tts   → 同上 (別名)
    http://127.0.0.1:8000/docs       → API 文件 (Swagger)
"""
import os
import re
import unicodedata
import uuid
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Edge TTS Voice Studio")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 輸出目錄
OUTPUT_DIR = os.path.join(os.path.abspath("."), "output")
UPLOAD_DIR = os.path.join(os.path.abspath("."), "uploads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --------------------------------------------------------------------------
# 語音角色設定 (使用 Microsoft Edge TTS Neural 語音)
# 每個角色針對不同語言映射到最適合的 Edge TTS 語音
# --------------------------------------------------------------------------
VOICE_PROFILES = {
    "xiaochen": {
        "display_name": "曉晨",
        "edge_voice_id": "HsiaoChenNeural",
        "gender": "female",
        "description": "溫柔知性女聲。語調自然流暢，適合有聲書朗讀、故事敘述、品牌旁白。",
        "voices": {
            "zh-TW": "zh-TW-HsiaoChenNeural",
            "zh-CN": "zh-CN-XiaoxiaoNeural",
            "en":    "en-US-JennyNeural",
            "ja":    "ja-JP-NanamiNeural",
        },
    },
    "yunzhe": {
        "display_name": "雲哲",
        "edge_voice_id": "YunJheNeural",
        "gender": "male",
        "description": "沉穩專業男聲。清晰有力，適合新聞播報、商業簡報、教學課程。",
        "voices": {
            "zh-TW": "zh-TW-YunJheNeural",
            "zh-CN": "zh-CN-YunxiNeural",
            "en":    "en-US-GuyNeural",
            "ja":    "ja-JP-KeitaNeural",
        },
    },
    "xiaoyu": {
        "display_name": "曉雨",
        "edge_voice_id": "HsiaoYuNeural",
        "gender": "female",
        "description": "甜美活潑女聲。輕快親切，適合日常對話、廣告配音、社群影片。",
        "voices": {
            "zh-TW": "zh-TW-HsiaoYuNeural",
            "zh-CN": "zh-CN-XiaoyiNeural",
            "en":    "en-US-AriaNeural",
            "ja":    "ja-JP-MayuNeural",
        },
    },
    "yunjian": {
        "display_name": "雲健",
        "edge_voice_id": "YunjianNeural",
        "gender": "male",
        "description": "磁性渾厚男聲。莊重大氣，適合紀錄片旁白、演講朗誦、廣播節目。",
        "voices": {
            "zh-TW": "zh-TW-YunJheNeural",
            "zh-CN": "zh-CN-YunjianNeural",
            "en":    "en-US-DavisNeural",
            "ja":    "ja-JP-KeitaNeural",
        },
    },
}


# --------------------------------------------------------------------------
# 語言自動偵測
# --------------------------------------------------------------------------
def detect_language(text: str) -> str:
    """根據文字內容的字元分布自動判斷主要語言"""
    ja_count = 0  # 平假名 + 片假名
    zh_count = 0  # CJK 統一字元
    en_count = 0  # ASCII 字母

    for ch in text:
        cp = ord(ch)
        # 平假名 U+3040-U+309F / 片假名 U+30A0-U+30FF
        if 0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF:
            ja_count += 1
        # CJK 統一字元
        elif 0x4E00 <= cp <= 0x9FFF:
            zh_count += 1
        # ASCII 字母
        elif ch.isascii() and ch.isalpha():
            en_count += 1

    total = ja_count + zh_count + en_count
    if total == 0:
        return "zh-TW"

    # 日文假名佔比 > 15% 就判定為日文 (因為日文也混用漢字)
    if ja_count / total > 0.15:
        return "ja"
    if zh_count > en_count:
        return "zh-TW"
    if en_count > 0:
        return "en"
    return "zh-TW"


# --------------------------------------------------------------------------
# 路由 - 頁面
# --------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
@app.get("/edge-tts", response_class=HTMLResponse)
async def edge_tts_page():
    html_path = os.path.join(os.path.abspath("."), "edge-tts.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>找不到 edge-tts.html</h1>"


# --------------------------------------------------------------------------
# API - 取得語音角色清單
# --------------------------------------------------------------------------
@app.get("/api/voices")
async def get_voices():
    return {
        vid: {
            "display_name": p["display_name"],
            "gender": p["gender"],
            "description": p["description"],
        }
        for vid, p in VOICE_PROFILES.items()
    }


# --------------------------------------------------------------------------
# API - TTS 合成（核心功能）
# --------------------------------------------------------------------------
@app.post("/api/tts")
async def tts_synthesize(data: dict):
    import edge_tts

    text = data.get("text", "").strip()
    voice_id = data.get("voice", "xiaochen")
    speed = data.get("speed", 1.0)
    pitch = data.get("pitch", 0)

    if not text:
        return JSONResponse(status_code=400, content={"error": "請輸入要合成的文字"})

    # 自動偵測語言
    detected_lang = detect_language(text)

    # 取得對應的 Edge TTS 語音名稱
    profile = VOICE_PROFILES.get(voice_id, VOICE_PROFILES["xiaochen"])
    edge_voice = profile["voices"].get(detected_lang, profile["voices"]["zh-TW"])

    # 速率轉換: 1.0 -> "+0%", 1.5 -> "+50%", 0.5 -> "-50%"
    rate_pct = int((speed - 1.0) * 100)
    rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"

    # 音高轉換
    pitch_hz = int(pitch * 10)
    pitch_str = f"+{pitch_hz}Hz" if pitch_hz >= 0 else f"{pitch_hz}Hz"

    output_file = os.path.join(OUTPUT_DIR, f"tts_{uuid.uuid4().hex[:8]}.mp3")

    try:
        communicate = edge_tts.Communicate(text, edge_voice, rate=rate_str, pitch=pitch_str)
        await communicate.save(output_file)

        return FileResponse(
            output_file,
            media_type="audio/mpeg",
            filename=f"voice_{profile['display_name']}.mp3",
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"合成失敗: {str(e)}"})


# --------------------------------------------------------------------------
# API - 偵測語言 (供前端預覽用)
# --------------------------------------------------------------------------
@app.post("/api/detect_lang")
async def detect_lang_api(data: dict):
    text = data.get("text", "")
    lang = detect_language(text)
    labels = {"zh-TW": "繁體中文", "zh-CN": "簡體中文", "en": "English", "ja": "日本語"}
    return {"lang": lang, "label": labels.get(lang, lang)}


# --------------------------------------------------------------------------
# API - 列出所有 Edge TTS 語音 (進階)
# --------------------------------------------------------------------------
@app.get("/api/all_voices")
async def list_all_voices():
    import edge_tts
    voices = await edge_tts.list_voices()
    zh_voices = [v for v in voices if v["Locale"].startswith("zh")]
    return {"total": len(voices), "zh_voices": zh_voices}


# --------------------------------------------------------------------------
# 啟動
# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 56)
    print("  Edge TTS Voice Studio")
    print("  ─────────────────────────────────────")
    print("  主頁面:  http://127.0.0.1:8000")
    print("  API 文件: http://127.0.0.1:8000/docs")
    print("=" * 56)
    uvicorn.run(app, host="127.0.0.1", port=8000)
