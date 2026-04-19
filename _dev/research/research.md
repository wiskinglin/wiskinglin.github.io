# 開源應用研究摘要 (Open Source Applications Research)

此文件摘要了目前位於 `_dev/research` 目錄下的開源 AI 應用與模型，主要分為影片生成與語音合成兩大領域。這些研究成果作為 Web 前端應用（位於 `_dev/ideas/app`）的後端支援核心。

## 🎥 影片生成 (Video Generation)

### [Wan2.2](file:///c:/Dev/wiskinglin.github.io/_dev/research/Wan2.2)
*   **概覽**: 阿里巴巴推出的先進影片生成模型系列。
*   **核心功能**:
    *   **Text-to-Video (T2V)**: 支援高解析度（最高 720p/1080p）的影片生成。
    *   **Image-to-Video (I2V)**: 將靜態圖片轉化為生動的動態影片。
    *   **Video-to-Video (S2V)**: 支援影片風格遷移與內容重構。
*   **技術特點**: 基於 14B MoE 架構，提供高品質的構圖與穩定的動態效果。
*   **對應應用**: [影片生成工作站.html](file:///c:/Dev/wiskinglin.github.io/_dev/ideas/app/影片生成工作站.html)

---

## 🎙️ 語音合成 (TTS - Text-to-Speech)

位於 `_dev/research/tts` 目錄下，包含目前最前沿的開源語音模型，支援高品質的語音克隆與合成。

### [GPT-SoVITS](file:///c:/Dev/wiskinglin.github.io/_dev/research/tts/GPT-SoVITS)
*   **概覽**: 強大的 Few-shot 語音克隆工具。
*   **核心功能**: 僅需 5 秒樣本即可進行語音克隆，1 分鐘樣本可進行微調，支援中、英、日、韓語。
*   **特點**: 逼真度極高，是目前最受歡迎的開源語音克隆方案之一。

### [CosyVoice](file:///c:/Dev/wiskinglin.github.io/_dev/research/tts/CosyVoice)
*   **概覽**: 阿里巴巴開發的多語言語音生成模型。
*   **核心功能**: 支援 Zero-shot 語音複製、跨語言語音合成。
*   **特點**: 語氣自然，具有豐富的情緒表達能力，適合內容創作與數位人開發。

### [Fish Speech](file:///c:/Dev/wiskinglin.github.io/_dev/research/tts/fish-speech)
*   **概覽**: Fish Audio 推出的 SOTA 級別神經網路語音引擎。
*   **核心功能**: 支援多語種、低時延的語音生成。
*   **特點**: 聲音質地細膩，支援大規模語音風格遷移。

### [ChatTTS](file:///c:/Dev/wiskinglin.github.io/_dev/research/tts/ChatTTS)
*   **概覽**: 專為對話場景設計的語音生成模型。
*   **核心功能**: 支援插入 `[oral_2]`, `[laugh]`, `[break]` 等標籤來控制口語排版。
*   **特點**: 非常適合處理日常對話，能夠生成極其自然的口語化語音（包含停頓與情緒）。

---

## 🛠️ 開發說明
目前的開發重點在於將這些本地執行的 Python 模型（後端）與現代化 Web 介面（前端）進行串接，主要透過 **FastAPI** 建立 API 介面供前端 HTML/JS 呼叫。

*最後更新時間: 2026-04-19*
