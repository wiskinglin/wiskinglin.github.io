import { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, AlignmentType, BorderStyle, HeadingLevel, TabStopPosition } from 'docx';
import fs from 'fs';

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: [
      // === 標題 ===
      new Paragraph({
        children: [
          new TextRun({ text: "團體作業2(基礎A)", bold: true, underline: {}, size: 28, font: "微軟正黑體" }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "請按照之前的＜作業練習＞，依序填寫以下各圖表", size: 24, font: "微軟正黑體" }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
      }),
      new Paragraph({
        children: [
          new TextRun({ text: "重新閱讀報導並挑選有價值容易作之觀點，進行＜全新的＞研究提案：資料收集設計方式為＜實驗加問卷法＞", bold: true, size: 24, font: "微軟正黑體", highlight: "yellow" }),
        ],
        spacing: { after: 400 },
      }),

      // === 企業困境列表 ===
      new Paragraph({ children: [new TextRun({ text: "1. 歐德加盟擴張過快引發的品牌價值下滑", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "2. 歐德規模化後的缺乏管理制度", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "3. 歐德業務成長集中於房地產熱潮", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 400 } }),

      // === (A) V推導 ===
      new Paragraph({ children: [new TextRun({ text: "(A) V推導", bold: true, size: 28, font: "微軟正黑體" })], spacing: { after: 300 } }),

      // 文獻搜尋
      new Paragraph({ children: [new TextRun({ text: "文獻搜尋", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({
        children: [new TextRun({
          text: "搜尋關於「產品服務系統 (Product-Service Systems, PSS)」、「服務化 (Servitization)」、「B2B 組織採購行為 (Organizational Buying Behavior)」、「知覺風險 (Perceived Risk)」與「採購意願 (Purchase Intention)」的相關學術文獻。參考 Webster & Wind (1972) 的組織採購行為通用模型、Johnston & Lewin (1996) 的整合性架構、Mont (2002) 的 PSS 概念釐清，以及 Bardhi & Eckhardt (2012) 的使用權消費理論。",
          size: 22, font: "微軟正黑體"
        })],
        spacing: { after: 200 },
      }),

      // 企業困境
      new Paragraph({ children: [new TextRun({ text: "企業困境/難題", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "1. 歐德加盟擴張過快引發的品牌價值下滑。", size: 22, font: "微軟正黑體" })], spacing: { after: 50 } }),
      new Paragraph({ children: [new TextRun({ text: "2. 歐德規模化後的缺乏管理制度。", size: 22, font: "微軟正黑體" })], spacing: { after: 50 } }),
      new Paragraph({ children: [new TextRun({ text: "3. 歐德業務成長集中於房地產熱潮，營收來源過度依賴單一市場。", size: 22, font: "微軟正黑體" })], spacing: { after: 200 } }),

      // 管理問題
      new Paragraph({ children: [new TextRun({ text: "管理問題", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "1. 規模化後，如何順利引進專業經理人建立制度，同時避免組織僵化？", size: 22, font: "微軟正黑體" })], spacing: { after: 50 } }),
      new Paragraph({ children: [new TextRun({ text: "2. 如何跨足商用家具，降低營收集中風險？", size: 22, font: "微軟正黑體" })], spacing: { after: 200 } }),

      // 研究問題
      new Paragraph({ children: [new TextRun({ text: "研究問題", bold: true, size: 24, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({
        children: [new TextRun({
          text: "歐德以「產品服務系統 (PSS)」跨足商用家具市場時，不同租賃方案的設計是否會透過影響「組織採購行為」，進而改變企業客戶的「採購意願」？此效果是否會因「知覺風險」的高低而產生差異？",
          size: 22, font: "微軟正黑體"
        })],
        spacing: { after: 100 },
      }),

      new Paragraph({ children: [new TextRun({ text: "圖1 V推導", size: 20, font: "微軟正黑體", italics: true })], spacing: { after: 400 } }),

      // === (B) 研究變數與假設 ===
      new Paragraph({ children: [new TextRun({ text: "(B) 研究變數與假設", bold: true, size: 28, font: "微軟正黑體" })], spacing: { after: 200 } }),
      new Paragraph({
        children: [new TextRun({ text: "*針對研究主題，請列出自變數、依變數、如有中介變數或干擾變數也請列出，並根據表格填寫相關內容。", size: 22, font: "微軟正黑體", bold: true })],
        spacing: { after: 200 },
      }),

      // 表1 研究變數說明表
      new Paragraph({ children: [new TextRun({ text: "表1 研究變數說明表", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),

      // --- Variable Table ---
      createVariableTable(),

      new Paragraph({ spacing: { after: 200 }, children: [] }),

      // 表2 真實驗設計說明表
      new Paragraph({ children: [new TextRun({ text: "表2 真實驗設計說明表", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),
      createExperimentTable(),

      new Paragraph({ spacing: { after: 200 }, children: [] }),

      // 研究架構圖
      new Paragraph({ children: [new TextRun({ text: "圖2 研究架構圖", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({
        children: [new TextRun({
          text: "[PSS方案 IV] ──H2──→ [組織採購行為 MV] ──H3──→ [採購意願 DV]",
          size: 22, font: "Consolas"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 50 },
      }),
      new Paragraph({
        children: [new TextRun({
          text: "                              ↑ H4 (干擾)",
          size: 22, font: "Consolas"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 50 },
      }),
      new Paragraph({
        children: [new TextRun({
          text: "                     [知覺風險 MoV]",
          size: 22, font: "Consolas"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 100 },
      }),
      new Paragraph({
        children: [new TextRun({
          text: "[PSS方案 IV] ──────── H1 ────────→ [採購意願 DV]",
          size: 22, font: "Consolas"
        })],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
      }),

      // 表3 假設文獻表
      new Paragraph({ children: [new TextRun({ text: "表3 研究假設說明表", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),
      createHypothesisTable(),

      new Paragraph({ spacing: { after: 200 }, children: [] }),

      // === (C) 問卷調查設計 ===
      new Paragraph({ children: [new TextRun({ text: "(C)", bold: true, size: 28, font: "微軟正黑體" })], spacing: { after: 200 } }),
      new Paragraph({ children: [new TextRun({ text: "表4 問卷調查設計之程序說明表", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),
      createSurveyTable(),

      new Paragraph({ spacing: { after: 400 }, children: [] }),

      // === (D) 雜誌/新聞報導 ===
      new Paragraph({ children: [new TextRun({ text: "(D) 雜誌/新聞報導", bold: true, size: 28, font: "微軟正黑體" })], spacing: { after: 200 } }),
      new Paragraph({
        children: [new TextRun({ text: "今周刊報導－歐德家具集團", bold: true, underline: {}, size: 24, font: "微軟正黑體" })],
        spacing: { after: 100 },
      }),
      new Paragraph({ children: [new TextRun({ text: "2006-09-07", size: 22, font: "微軟正黑體" })], spacing: { after: 100 } }),
      new Paragraph({
        children: [new TextRun({
          text: "擁有全台灣三十七家直營點，每年每股稅後純益逾三元的歐德家具，位居系統家具之冠，總經理陳國都以創新及迅速反映市場需求，堅持用最好的原料，不僅打造出品質最好的家具，也創造全台第一的口碑。",
          size: 22, font: "微軟正黑體"
        })],
        spacing: { after: 100 },
      }),
      new Paragraph({
        children: [new TextRun({
          text: "最近，歐德準備搶攻辦公室的OA家具市場，以租賃的創新方式打入這塊新市場。陳國都分析：「歐德在櫃體類相當擅長，辦公室的櫃子最重要的就是耐用，加上採取租賃方式，減少企業開創初期的資金成本，對中小企業是最好的選擇。」歐德這項獨特的創新策略，能否在辦公家具這塊新市場打下一片天，樹立另一根營收新支柱？正是歐德要從家用家具大王跨足到辦公市場的關鍵戰役。",
          size: 22, font: "微軟正黑體"
        })],
        spacing: { after: 100 },
      }),
    ],
  }],
});

function cell(text, opts = {}) {
  return new TableCell({
    children: [new Paragraph({
      children: [new TextRun({ text, size: 20, font: "微軟正黑體", bold: opts.bold || false })],
      spacing: { after: 50 },
    })],
    width: opts.width ? { size: opts.width, type: WidthType.PERCENTAGE } : undefined,
  });
}

function createVariableTable() {
  const header = new TableRow({
    children: [
      cell("變數", { bold: true, width: 15 }),
      cell("操作型定義", { bold: true, width: 25 }),
      cell("問項(如果有)+尺度", { bold: true, width: 25 }),
      cell("文獻(APA格式)", { bold: true, width: 25 }),
      cell("影響係數/Q1;2", { bold: true, width: 10 }),
    ],
  });

  const ivRow = new TableRow({
    children: [
      cell("自變數(IV):\nPSS方案類型"),
      cell("歐德跨足商用家具市場所提供的產品服務系統(PSS)租賃方案形式，分為「標準租賃方案」與「彈性租賃方案」兩種層次。"),
      cell("(此為實驗操弄變數，不設問項尺度，由情境分派決定)"),
      cell("Mont, O. K. (2002). Clarifying the concept of product-service system. Journal of Cleaner Production, 10(3), 237-245."),
      cell("IF: 11.1\n(Q1)"),
    ],
  });

  const mvRow = new TableRow({
    children: [
      cell("中介變數(MV):\n組織採購行為"),
      cell("企業內部採購決策單位在評估商用家具租賃方案時，所經歷的資訊搜尋、方案評估與共識形成等組織採購流程的積極程度。"),
      cell("1. 我們公司會主動蒐集多家商用家具租賃方案進行比較。\n2. 採購決策會經過多部門共同討論後才決定。\n3. 我們對此方案進行了充分的內部評估。\n(李克特五點量表：1=非常不同意~5=非常同意)"),
      cell("Johnston, W. J., & Lewin, J. E. (1996). Organizational buying behavior: Toward an integrative framework. Journal of Business Research, 35(1), 1-15."),
      cell("IF: 11.3\n(Q1)"),
    ],
  });

  const movRow = new TableRow({
    children: [
      cell("干擾變數(MoV):\n知覺風險"),
      cell("企業採購決策者對選用商用家具租賃方案可能帶來的財務損失、服務品質不確定性及營運中斷等負面後果的主觀評估。"),
      cell("1. 採用此租賃方案可能造成公司額外的財務負擔。\n2. 我擔心租賃的商用家具品質無法達到公司標準。\n3. 長期租賃可能使公司受制於單一供應商。\n(李克特五點量表：1=非常不同意~5=非常同意)"),
      cell("Mitchell, V.-W. (1999). Consumer perceived risk: Conceptualisations and models. European Journal of Marketing, 33(1/2), 163-195."),
      cell("IF: 5.2\n(Q1)"),
    ],
  });

  const dvRow = new TableRow({
    children: [
      cell("依變數(DV):\n採購意願"),
      cell("企業採購決策者在未來實際選用歐德商用家具租賃方案的可能性與意願強烈程度。"),
      cell("1. 如果公司有商用家具需求，我會優先考慮採用歐德的租賃方案。\n2. 在未來半年內，我有極高意願為公司引入此租賃方案。\n3. 我願意向其他企業推薦歐德的商用家具租賃方案。\n(李克特五點量表：1=非常不同意~5=非常同意)"),
      cell("Dodds, W. B., Monroe, K. B., & Grewal, D. (1991). Effects of price, brand, and store information on buyers' product evaluations. Journal of Marketing Research, 28(3), 307-319."),
      cell("IF: 6.1\n(Q1)"),
    ],
  });

  return new Table({ rows: [header, ivRow, mvRow, movRow, dvRow], width: { size: 100, type: WidthType.PERCENTAGE } });
}

function createHypothesisTable() {
  const header = new TableRow({
    children: [
      cell("假設", { bold: true, width: 50 }),
      cell("文獻(APA格式)", { bold: true, width: 35 }),
      cell("影響係數/Q1;2", { bold: true, width: 15 }),
    ],
  });

  const rows = [
    ["H1: 不同PSS方案類型會顯著影響企業客戶對商用家具的採購意願。",
     "Hao, X., Xu, J., & Wang, Y. (2025). How generative AI shapes user perceived value and adoption intention. npj Heritage Science, 13, 608.",
     "IF: 3.3\n(Q1)"],
    ["H2: 不同PSS方案類型會顯著影響企業內部的組織採購行為積極程度。",
     "Johnston, W. J., & Lewin, J. E. (1996). Organizational buying behavior: Toward an integrative framework. Journal of Business Research, 35(1), 1-15.",
     "IF: 11.3\n(Q1)"],
    ["H3: 組織採購行為在「PSS方案類型」與「採購意願」之間具有顯著的中介效果。",
     "Saraswat, S. (2025). The moderating role of perceived trust in predicting the adoption intention. IJPHM, 19(4).",
     "IF: 3.2\n(Q1)"],
    ["H4: 知覺風險對「組織採購行為」與「採購意願」之間的關係具有顯著的干擾效果：知覺風險越高，組織採購行為對採購意願的正向影響越弱。",
     "Mitchell, V.-W. (1999). Consumer perceived risk: Conceptualisations and models. European Journal of Marketing, 33(1/2), 163-195.",
     "IF: 5.2\n(Q1)"],
  ];

  return new Table({
    rows: [header, ...rows.map(r => new TableRow({ children: [cell(r[0]), cell(r[1]), cell(r[2])] }))],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

function createExperimentTable() {
  const rows = [
    ["研究主題:", "商用家具PSS租賃方案對中小企業採購意願之影響"],
    ["1 自變數", "提供給企業客戶的「產品服務系統 (PSS) 租賃方案類型」。"],
    ["2 自變數處理層次", "分為兩個實驗組別進行操弄 (Between-subjects design)：\n► 實驗組A（標準租賃方案）：提供歐德商用家具的「固定月付、期滿歸還」情境說明書。\n► 實驗組B（彈性租賃方案）：提供歐德商用家具的「按需調整數量、期滿可換新或買斷」情境說明書。"],
    ["3 控制實驗環境", "1. 刺激物控制：兩組情境說明書中的「家具品牌(歐德)」、「家具品質」、「設計圖面」與「五年總花費金額」皆設定為完全一致，僅在方案彈性與期滿選項上做文字替換。\n2. 流程控制：受試者皆透過線上問卷平台(如Surveycake)隨機分派進入其中一個情境進行閱讀與填答。\n3. 隱藏意圖：標題統一稱為「新世代辦公環境配置調查」，以避免受測者猜測實驗目的。"],
    ["4 選擇與招募樣本", "1. 條件限制：受測者必須為「台灣中小企業(員工人數200人以下)的現職人員」，且在公司內「具有採購決策權或採購建議權」。\n2. 招募方式：透過 LinkedIn 商業社群、FB 創業家與總務人員社團發送邀請連結。\n3. 隨機分派：利用問卷系統的隨機跳題邏輯，將填答者自動且隨機分派至「標準方案組」或「彈性方案組」。"],
  ];

  return new Table({
    rows: rows.map(r => new TableRow({
      children: [
        cell(r[0], { bold: true, width: 20 }),
        cell(r[1], { width: 80 }),
      ],
    })),
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

function createSurveyTable() {
  const rows = [
    ["研究主題:", "商用家具PSS租賃方案對中小企業採購意願之影響"],
    ["1 以80字以內，提出＜合作請求＞文案", "您好！我們是台科大研究團隊，正在探討「商用家具租賃方案」如何幫助企業降低營運成本與營收集中風險。懇請您撥冗3分鐘填答此問卷，您的寶貴意見將協助業界優化採購服務，感謝您的參與！"],
    ["2 設計8-10個基本資料與主題相關之行為調查問題", "1. 您的企業規模為何？(5人以下/6-20人/21-50人/51-200人)\n2. 您在公司是否具備採購決策權？(是/否)\n3. 貴公司成立時間？(1年內/1-3年/3-5年/5年以上)\n4. 貴公司所屬產業別？(科技業/服務業/製造業/其他)\n5. 目前公司辦公家具主要取得方式？(買斷新品/買斷二手/租賃/其他)\n(以下接續情境題填寫：請閱讀完情境後回答以下問題)\n6. 我們公司會主動蒐集多家商用家具租賃方案進行比較。(1-5分)\n7. 採購決策會經過多部門共同討論後才決定。(1-5分)\n8. 採用此租賃方案可能造成公司額外的財務負擔。(1-5分)\n9. 如果公司有商用家具需求，我會優先考慮採用此租賃方案。(1-5分)\n10. 在未來半年內，我有極高意願為公司引入此租賃方案。(1-5分)"],
    ["3 加入重要變數的調查問題(整合表1的問項與尺度,但套入本次報導案例的情境)", "(已整合於上述第6-10題中，涵蓋組織採購行為MV、知覺風險MoV、採購意願DV三個變數的問項)"],
  ];

  return new Table({
    rows: rows.map(r => new TableRow({
      children: [
        cell(r[0], { bold: true, width: 30 }),
        cell(r[1], { width: 70 }),
      ],
    })),
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

// Generate
const buffer = await Packer.toBuffer(doc);
const outPath = 'c:\\Playground26\\wiskinglin.github.io\\_data\\NTUST\\homework\\Week7_Opus.docx';
fs.writeFileSync(outPath, buffer);
console.log('Generated:', outPath);
