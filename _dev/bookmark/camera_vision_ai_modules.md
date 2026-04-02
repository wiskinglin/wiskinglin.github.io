# 相機模組、電腦視覺與 AI 辨識分析 (Camera & CV AI)

本文件整理了各類工業級與嵌入式相機模組供應商（如 Arducam, Innodisk）、電腦視覺（CV）開發工具、OCR 辨識方案及 AI 影像分析應用案例。

## 🔍 如何使用此資料
1. **硬體選型**：查閱 Arducam、Innodisk 及立景創新的相機規格，適用於樹莓派與 Jetson 平台。
2. **開發工具**：利用 NVIDIA cuDNN, OpenCV, YOLO11 及 CVAT 進行模型訓練與標註。
3. **AI 應用**：參考 ADLINK, Solomon 及 Keyence 的 AI 視覺瑕疵檢測與行為分析案例。

---

## 📷 相機模組與供應商 (Camera Modules)
專位嵌入式系統與工業應用設計的影像擷取設備。

| 供應商 / 產品 | 介面 / 特色 | 官方連結 | 說明 |
| :--- | :--- | :--- | :--- |
| **Arducam IMX519** | MIPI CSI / 自動對焦 | [arducam.com](https://www.arducam.com/imx519-autofocus-camera-module-for-raspberry-pi-arducam-b0371.html) | 提供 16MP 高畫質與 PDAF 自動對焦。 |
| **Innodisk EV5M** | MIPI CSI-2 / 5MP | [innodisk.com](https://www.innodisk.com/cht/products/camera/mipi-csi-2/ev5m-csm1-rtcf) | 工業級嵌入式相機模組。 |
| **Sunny Optical** | 全系列相機模組 | [sunnyoptical.com](https://www.sunnyoptical.com/default.html) | 全球領先的光學鏡頭與模組供應商。 |
| **立景創新** | 汽車與行動應用 | [luxvisions.com](https://www.luxvisions-inno.com/motor-01.html) | 專注於車載鏡頭與微型相機模組。 |
| **IPEVO P2V** | USB / 實物攝影 | [ipevo.com](https://international.ipevo.com/tw) | 適用於遠距教學與視訊會議的微距攝影。 |

---

## 🧠 電腦視覺與 AI 辨識工具 (CV & AI Tools)
提升影像辨識準確度與開發速度的框架與平台。

| 軟體 / 框架 | 領域 | 官方連結 | 特色 |
| :--- | :--- | :--- | :--- |
| **YOLO 11** | 物件偵測 | [ultralytics.com](https://docs.ultralytics.com/models/yolo11/) | 即時物件偵測的業界標準。 |
| **CVAT** | 影像標註 | [cvat.ai](https://www.cvat.ai/) | 開源且強大的影像/影片數據標註平台。 |
| **cuDNN** | 深度學習加速 | [developer.nvidia.com](https://developer.nvidia.com/cudnn) | NVIDIA 專為深度神經網路設計的 GPU 加速庫。 |
| **Tesseract OCR** | 文字辨識 | [github.com](https://github.com/tesseract-ocr/tesseract) | 全球最知名的開源 OCR 引擎。 |
| **MONAI** | 醫療影像 AI | [github.com](https://github.com/Project-MONAI/MONAI) | 專為醫療影像設計的 AI 工具包。 |

---

## 🏭 工業級 AI 視覺解決方案 (Industrial AI Vision)
針對製造業與自動化開發的解決方案。

| 方案名稱 | 供應商 | 連結 | 應用場景 |
| :--- | :--- | :--- | :--- |
| **SolVision** | 所羅門 Solomon | [查看方案](https://www.solomon-3d.com/tw/products/solvision/) | AI 瑕疵檢測與圖像辨識，適用於自動化產線。 |
| **EVA SDK** | 凌華 ADLINK | [查看方案](https://www.adlinktech.com/tw/EVA_SDK_ADLINK_Edge_AI_Vision_Analytics) | 邊緣 AI 視覺分析開發套件。 |
| **VS 系列** | KEYENCE 基恩斯 | [查看方案](https://www.keyence.com.tw/products/vision/) | 高精度 2D/3D 通用視覺系統。 |

---

*資料最後更新時間: 2026-04-02*
