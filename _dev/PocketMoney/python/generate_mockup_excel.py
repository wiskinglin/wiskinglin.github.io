# -*- coding: utf-8 -*-
"""
PocketMoney 專業級 Excel 匯出模組 (統一時間軸縱向排版版)
=========================================================
本版本依據使用者指定格式重構：
所有月度分頁（01現金流、02信用卡、04信用卡分期、05固定費用）
均統一以「直向時間軸 (2026/01月 ~ 2026/12月)」為列 (Rows)，
各卡片、分期項目、固定費用項目為欄 (Columns)。
最底層統一為「2026 全年累計加總」雙底線。
跨分頁月份完全同列對齊，極致好讀！
"""

import os
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_mockup_excel(output_path, db_path=None):
    wb = Workbook()
    
    # 建立 6 大工作表
    ws_cashflow = wb.active
    ws_cashflow.title = "01_現金流檢核"
    ws_cards = wb.create_sheet(title="02_信用卡12個月")
    ws_big_exp = wb.create_sheet(title="03_大額消費明細")
    ws_installments = wb.create_sheet(title="04_信用卡分期")
    ws_recurring = wb.create_sheet(title="05_固定費用")
    ws_banks = wb.create_sheet(title="06_銀行帳戶與異動")

    # 分頁色彩標籤 (Tab Colors)
    ws_cashflow.sheet_properties.tabColor = "0284C7"      # 天藍 (核心儀表板)
    ws_cards.sheet_properties.tabColor = "F59E0B"         # 暖橘黃 (信用卡)
    ws_big_exp.sheet_properties.tabColor = "EC4899"       # 桃粉 (大額消費)
    ws_installments.sheet_properties.tabColor = "8B5CF6"  # 紫色 (分期管理)
    ws_recurring.sheet_properties.tabColor = "10B981"     # 祖母綠 (固定費用)
    ws_banks.sheet_properties.tabColor = "3B82F6"         # 沉穩藍 (銀行存款)

    # 樣式常數
    FONT_NAME = "Microsoft JhengHei"
    
    title_font = Font(name=FONT_NAME, size=13, bold=True, color="FFFFFF")
    subtitle_font = Font(name=FONT_NAME, size=9, italic=True, color="94A3B8")
    section_font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
    th_font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    th_meta_font = Font(name=FONT_NAME, size=9, bold=False, color="CBD5E1")
    body_font = Font(name=FONT_NAME, size=10, color="0F172A")
    body_bold = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
    month_font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
    total_font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
    note_font = Font(name=FONT_NAME, size=9, color="64748B")
    alert_font = Font(name=FONT_NAME, size=10, bold=True, color="DC2626")
    safe_font = Font(name=FONT_NAME, size=10, bold=True, color="059669")
    
    # 填充色
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")       # 頂部大深藍
    th_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")           # 表頭深岩藍
    th_accent_fill = PatternFill(start_color="0369A1", end_color="0369A1", fill_type="solid")    # 表頭焦點青藍
    th_highlight_fill = PatternFill(start_color="B45309", end_color="B45309", fill_type="solid") # 表頭琥珀棕
    stripe_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")       # 斑馬紋
    total_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")        # 總計行淡藍灰
    safe_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")         # 充裕綠
    alert_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")        # 警戒紅
    
    # 邊框
    thin_gray = Side(style='thin', color='CBD5E1')
    thick_dark = Side(style='medium', color='0F172A')
    double_bottom = Side(style='double', color='0F172A')
    
    grid_border = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
    total_border = Border(top=thin_gray, bottom=double_bottom, left=thin_gray, right=thin_gray)
    header_border = Border(left=thin_gray, right=thin_gray, top=thick_dark, bottom=thick_dark)

    # 對齊
    align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_left = Alignment(horizontal='left', vertical='center')
    align_right = Alignment(horizontal='right', vertical='center')
    
    # 數字格式
    FMT_CURRENCY = "$#,##0;($#,##0);\"-\""
    FMT_INT = "#,##0;(#,##0);\"-\""

    # 月份標籤清單 (統一 1~12 月與累計列)
    MONTH_LABELS = [f"2026 / {m:02d} 月" for m in range(1, 13)]
    
    # 讀取 dummy db 資料
    senior_db = {}
    if db_path and os.path.exists(db_path):
        with open(db_path, "r", encoding="utf-8") as f:
            senior_db = json.load(f)
            
    banks_data = senior_db.get("banks", [
        {"name": "國泰世華 (尊爵VIP財管)", "balance": 1880000, "defaultSalary": 260000, "salaryDay": 5, "minReserve": 300000, "cashDragAlert": 1600000, "note": "高階分紅主力戶・信用卡自動扣款"},
        {"name": "富邦商業 (長線存股戶)", "balance": 820000, "defaultSalary": 0, "salaryDay": 0, "minReserve": 150000, "cashDragAlert": 1000000, "note": "台股波段交割專用"},
        {"name": "台新銀行 (數位日常理財)", "balance": 245000, "defaultSalary": 0, "salaryDay": 0, "minReserve": 50000, "cashDragAlert": 300000, "note": "日常生活小額消費"},
        {"name": "中信商銀 (豪宅置產專戶)", "balance": 460000, "defaultSalary": 0, "salaryDay": 0, "minReserve": 200000, "cashDragAlert": 800000, "note": "房貸與大樓管理費專扣"},
        {"name": "玉山銀行 (海外私校教育)", "balance": 615000, "defaultSalary": 0, "salaryDay": 0, "minReserve": 100000, "cashDragAlert": 800000, "note": "外幣與海外留學儲備"}
    ])

    # 信用卡月度消費數據 (縱向: 1~12月)
    card_ae_centurion = [81000, 96000, 68000, 74000, 115000, 89000, 94000, 132000, 78000, 85000, 92000, 145000]
    card_cathay_cube  = [45000, 52000, 39000, 48000, 86000, 43000, 51000, 67000, 42000, 49000, 55000, 72000]
    card_fubon_prime  = [28000, 34000, 22000, 31000, 45000, 29000, 33000, 48000, 26000, 30000, 35000, 58000]

    # -------------------------------------------------------------
    # 分頁 4：04_信用卡分期 (Installments)
    # 格式：縱軸為 2026/01月 ~ 2026/12月，橫軸為分期項目
    # -------------------------------------------------------------
    ws_installments.views.sheetView[0].showGridLines = True
    ws_installments.freeze_panes = "B8"

    ws_installments.merge_cells("A1:G2")
    ws_installments["A1"].value = "⏳ PocketMoney 信用卡分期付款月度排程 (Installments by Month)"
    ws_installments["A1"].font = title_font
    ws_installments["A1"].fill = header_fill
    ws_installments["A1"].alignment = align_center

    ws_installments["A3"].value = "💡 說明：依使用者指定的直向時間軸排版；每一月份為一列，橫向展開各分期項目之每期攤提，最右側為當月分期合計。"
    ws_installments["A3"].font = subtitle_font

    # 表頭第 5 行：分期項目名稱
    # 表頭第 6 行：綁定卡片 / 總額 / 期數
    inst_items = [
        {"col": 2, "name": "Porsche Macan 原廠大型定保", "card": "美國運通 百夫長白金卡", "total": 600000, "period": 24, "reg": 25000, "active": list(range(1, 13))},
        {"col": 3, "name": "Devialet 帝瓦雷家庭劇院組", "card": "國泰世華 世界卡 (CUBE)", "total": 180000, "period": 12, "reg": 15000, "active": list(range(1, 13))},
        {"col": 4, "name": "Apple 工作站 (Mac Studio)", "card": "富邦 尊御商務卡", "total": 120000, "period": 6, "reg": 20000, "active": list(range(3, 9))},
        {"col": 5, "name": "米蘭暑期商務艙家族機票", "card": "美國運通 百夫長白金卡", "total": 240000, "period": 8, "reg": 30000, "active": list(range(5, 13))},
    ]

    # 表頭設定
    ws_installments.cell(row=5, column=1, value="月份").font = th_font
    ws_installments.cell(row=5, column=1).fill = th_fill
    ws_installments.cell(row=5, column=1).alignment = align_center
    ws_installments.cell(row=5, column=1).border = header_border

    ws_installments.cell(row=6, column=1, value="基本資料說明").font = th_meta_font
    ws_installments.cell(row=6, column=1).fill = th_fill
    ws_installments.cell(row=6, column=1).alignment = align_center
    ws_installments.cell(row=6, column=1).border = header_border

    for item in inst_items:
        c_i = item["col"]
        # 第一層表頭：項目名稱
        cell_name = ws_installments.cell(row=5, column=c_i, value=item["name"])
        cell_name.font = th_font
        cell_name.fill = th_fill
        cell_name.alignment = align_center
        cell_name.border = header_border
        
        # 第二層表頭：卡片與期數
        meta_txt = f"{item['card']}\n(總額 ${item['total']:,} / {item['period']}期 / 每期 ${item['reg']:,})"
        cell_meta = ws_installments.cell(row=6, column=c_i, value=meta_txt)
        cell_meta.font = th_meta_font
        cell_meta.fill = th_fill
        cell_meta.alignment = align_center
        cell_meta.border = header_border

    # 合計欄表頭
    c_tot_head1 = ws_installments.cell(row=5, column=6, value="當月分期攤提總額")
    c_tot_head1.font = th_font
    c_tot_head1.fill = th_accent_fill
    c_tot_head1.alignment = align_center
    c_tot_head1.border = header_border

    c_tot_head2 = ws_installments.cell(row=6, column=6, value="全卡各項目加總")
    c_tot_head2.font = th_meta_font
    c_tot_head2.fill = th_accent_fill
    c_tot_head2.alignment = align_center
    c_tot_head2.border = header_border

    # 填入 12 個月份 (Row 8 ~ Row 19，Row 7 留白或直接接續)
    # 統一將 12 個月份排在 Row 8 ~ Row 19！
    row_inst_start = 7
    for m_idx, m_str in enumerate(MONTH_LABELS, 1):
        cur_r = row_inst_start + m_idx - 1
        
        # 月份欄
        ws_installments.cell(row=cur_r, column=1, value=m_str).font = month_font
        ws_installments.cell(row=cur_r, column=1).alignment = align_center
        ws_installments.cell(row=cur_r, column=1).border = grid_border
        if m_idx % 2 == 0:
            ws_installments.cell(row=cur_r, column=1).fill = stripe_fill

        # 各項目金額
        for item in inst_items:
            c_i = item["col"]
            val = item["reg"] if m_idx in item["active"] else 0
            val_c = ws_installments.cell(row=cur_r, column=c_i, value=val)
            val_c.font = body_font
            val_c.number_format = FMT_CURRENCY
            val_c.alignment = align_right
            val_c.border = grid_border
            if m_idx % 2 == 0:
                val_c.fill = stripe_fill

        # 當月合計
        sum_f = f"=SUM(B{cur_r}:E{cur_r})"
        tot_c = ws_installments.cell(row=cur_r, column=6, value=sum_f)
        tot_c.font = body_bold
        tot_c.number_format = FMT_CURRENCY
        tot_c.alignment = align_right
        tot_c.border = grid_border
        if m_idx % 2 == 0:
            tot_c.fill = stripe_fill

    # 2026 全年累計加總
    inst_tot_row = row_inst_start + 12
    ws_installments.cell(row=inst_tot_row, column=1, value="2026 全年累計加總").font = total_font
    ws_installments.cell(row=inst_tot_row, column=1).alignment = align_center
    ws_installments.cell(row=inst_tot_row, column=1).fill = total_fill
    ws_installments.cell(row=inst_tot_row, column=1).border = total_border

    for col_i in range(2, 6):
        col_let = get_column_letter(col_i)
        f_yr = f"=SUM({col_let}{row_inst_start}:{col_let}{inst_tot_row-1})"
        c_y = ws_installments.cell(row=inst_tot_row, column=col_i, value=f_yr)
        c_y.font = total_font
        c_y.number_format = FMT_CURRENCY
        c_y.alignment = align_right
        c_y.fill = total_fill
        c_y.border = total_border

    # 全年分期總扣繳加總
    f_grand_inst = f"=SUM(F{row_inst_start}:F{inst_tot_row-1})"
    c_gi = ws_installments.cell(row=inst_tot_row, column=6, value=f_grand_inst)
    c_gi.font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
    c_gi.number_format = FMT_CURRENCY
    c_gi.alignment = align_right
    c_gi.fill = safe_fill
    c_gi.border = total_border

    # 額外附註：剩餘未攤還餘額
    ws_installments.cell(row=inst_tot_row+1, column=1, value="剩餘未攤還餘額").font = body_bold
    ws_installments.cell(row=inst_tot_row+1, column=1).alignment = align_center
    ws_installments.cell(row=inst_tot_row+1, column=1).fill = total_fill
    ws_installments.cell(row=inst_tot_row+1, column=1).border = grid_border
    
    for item in inst_items:
        c_i = item["col"]
        col_let = get_column_letter(c_i)
        # 剩餘未攤 = 總額 - 本年已攤
        rem_f = f"={item['total']}-{col_let}{inst_tot_row}"
        c_rem = ws_installments.cell(row=inst_tot_row+1, column=c_i, value=rem_f)
        c_rem.font = body_bold
        c_rem.number_format = FMT_CURRENCY
        c_rem.alignment = align_right
        c_rem.fill = total_fill
        c_rem.border = grid_border

    c_rem_tot = ws_installments.cell(row=inst_tot_row+1, column=6, value=f"=SUM(B{inst_tot_row+1}:E{inst_tot_row+1})")
    c_rem_tot.font = body_bold
    c_rem_tot.number_format = FMT_CURRENCY
    c_rem_tot.alignment = align_right
    c_rem_tot.fill = total_fill
    c_rem_tot.border = grid_border


    # -------------------------------------------------------------
    # 分頁 2：02_信用卡12個月 (Credit Cards)
    # 格式：縱軸為 2026/01月 ~ 2026/12月，橫軸為各信用卡
    # -------------------------------------------------------------
    ws_cards.views.sheetView[0].showGridLines = True
    ws_cards.freeze_panes = "B8"

    ws_cards.merge_cells("A1:H2")
    title_cell = ws_cards["A1"]
    title_cell.value = "💳 PocketMoney 12 個月信用卡支出矩陣 (Credit Cards by Month)"
    title_cell.font = title_font
    title_cell.fill = header_fill
    title_cell.alignment = align_center

    ws_cards["A3"].value = "💡 說明：依使用者指定的直向時間軸排版；每一列為單一月份，清晰對帳各卡刷卡金、分期攤提與扣款銀行小計。"
    ws_cards["A3"].font = subtitle_font

    cards_meta = [
        {"col": 2, "name": "美國運通 百夫長白金卡", "bank": "扣款行：國泰世華", "cycle": "結帳 08 號 / 繳款 26 號", "data": card_ae_centurion},
        {"col": 3, "name": "國泰世華 世界卡 (CUBE)", "bank": "扣款行：國泰世華", "cycle": "結帳 17 號 / 繳款 06 號", "data": card_cathay_cube},
        {"col": 4, "name": "富邦 尊御商務卡", "bank": "扣款行：富邦商業", "cycle": "結帳 23 號 / 繳款 12 號", "data": card_fubon_prime},
    ]

    # 表頭 Row 5 & Row 6
    ws_cards.cell(row=5, column=1, value="月份").font = th_font
    ws_cards.cell(row=5, column=1).fill = th_fill
    ws_cards.cell(row=5, column=1).alignment = align_center
    ws_cards.cell(row=5, column=1).border = header_border

    ws_cards.cell(row=6, column=1, value="基本資料說明").font = th_meta_font
    ws_cards.cell(row=6, column=1).fill = th_fill
    ws_cards.cell(row=6, column=1).alignment = align_center
    ws_cards.cell(row=6, column=1).border = header_border

    for c_info in cards_meta:
        c_i = c_info["col"]
        # 第一層表頭：卡片名稱
        c_h1 = ws_cards.cell(row=5, column=c_i, value=c_info["name"])
        c_h1.font = th_font
        c_h1.fill = th_fill
        c_h1.alignment = align_center
        c_h1.border = header_border
        
        # 第二層表頭：扣款銀行與扣繳日
        c_h2 = ws_cards.cell(row=6, column=c_i, value=f"{c_info['bank']}\n({c_info['cycle']})")
        c_h2.font = th_meta_font
        c_h2.fill = th_fill
        c_h2.alignment = align_center
        c_h2.border = header_border

    # 欄 5: 信用卡分期當月攤提 (公式直接引用分頁 04 對應月份)
    c_f5_1 = ws_cards.cell(row=5, column=5, value="信用卡分期攤提")
    c_f5_1.font = th_font
    c_f5_1.fill = th_highlight_fill
    c_f5_1.alignment = align_center
    c_f5_1.border = header_border

    c_f5_2 = ws_cards.cell(row=6, column=5, value="連動分期表當月總額")
    c_f5_2.font = th_meta_font
    c_f5_2.fill = th_highlight_fill
    c_f5_2.alignment = align_center
    c_f5_2.border = header_border

    # 欄 6: 當月信用卡應繳總額
    c_f6_1 = ws_cards.cell(row=5, column=6, value="當月應繳總額合計")
    c_f6_1.font = th_font
    c_f6_1.fill = th_accent_fill
    c_f6_1.alignment = align_center
    c_f6_1.border = header_border

    c_f6_2 = ws_cards.cell(row=6, column=6, value="常態刷卡+分期 (Grand Total)")
    c_f6_2.font = th_meta_font
    c_f6_2.fill = th_accent_fill
    c_f6_2.alignment = align_center
    c_f6_2.border = header_border

    # 欄 7 & 8: 銀行歸戶扣款小計
    c_f7_1 = ws_cards.cell(row=5, column=7, value="國泰世華扣款小計")
    c_f7_1.font = th_font
    c_f7_1.fill = th_fill
    c_f7_1.alignment = align_center
    c_f7_1.border = header_border

    c_f7_2 = ws_cards.cell(row=6, column=7, value="AE卡 + CUBE卡 + 分期")
    c_f7_2.font = th_meta_font
    c_f7_2.fill = th_fill
    c_f7_2.alignment = align_center
    c_f7_2.border = header_border

    c_f8_1 = ws_cards.cell(row=5, column=8, value="富邦商業扣款小計")
    c_f8_1.font = th_font
    c_f8_1.fill = th_fill
    c_f8_1.alignment = align_center
    c_f8_1.border = header_border

    c_f8_2 = ws_cards.cell(row=6, column=8, value="富邦尊御卡 + 分期")
    c_f8_2.font = th_meta_font
    c_f8_2.fill = th_fill
    c_f8_2.alignment = align_center
    c_f8_2.border = header_border

    # 填入 12 個月份 (Row 7 ~ Row 18)
    row_cards_start = 7
    for m_idx, m_str in enumerate(MONTH_LABELS, 1):
        cur_r = row_cards_start + m_idx - 1

        # 月份
        ws_cards.cell(row=cur_r, column=1, value=m_str).font = month_font
        ws_cards.cell(row=cur_r, column=1).alignment = align_center
        ws_cards.cell(row=cur_r, column=1).border = grid_border
        if m_idx % 2 == 0:
            ws_cards.cell(row=cur_r, column=1).fill = stripe_fill

        # 3 張卡消費
        for c_info in cards_meta:
            c_i = c_info["col"]
            val = c_info["data"][m_idx - 1]
            val_c = ws_cards.cell(row=cur_r, column=c_i, value=val)
            val_c.font = body_font
            val_c.number_format = FMT_CURRENCY
            val_c.alignment = align_right
            val_c.border = grid_border
            if m_idx % 2 == 0:
                val_c.fill = stripe_fill

        # 信用卡分期攤提 (直接引用 04_信用卡分期 同一列 Row cur_r 的 F 欄！)
        f_inst = f"='04_信用卡分期'!F{cur_r}"
        c_inst = ws_cards.cell(row=cur_r, column=5, value=f_inst)
        c_inst.font = body_font
        c_inst.number_format = FMT_CURRENCY
        c_inst.alignment = align_right
        c_inst.border = grid_border
        if m_idx % 2 == 0:
            c_inst.fill = stripe_fill

        # 當月應繳總額合計 (全卡常態 + 分期)
        f_tot = f"=SUM(B{cur_r}:E{cur_r})"
        c_tot = ws_cards.cell(row=cur_r, column=6, value=f_tot)
        c_tot.font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
        c_tot.number_format = FMT_CURRENCY
        c_tot.alignment = align_right
        c_tot.border = grid_border
        if m_idx % 2 == 0:
            c_tot.fill = stripe_fill

        # 國泰世華扣款小計 (AE + CUBE + 分期中的AE與CUBE項)
        # 為簡潔起見：B{cur_r}+C{cur_r}+'04_信用卡分期'!B{cur_r}+'04_信用卡分期'!C{cur_r}+'04_信用卡分期'!E{cur_r}
        f_cathay = f"=B{cur_r}+C{cur_r}+'04_信用卡分期'!B{cur_r}+'04_信用卡分期'!C{cur_r}+'04_信用卡分期'!E{cur_r}"
        c_cat = ws_cards.cell(row=cur_r, column=7, value=f_cathay)
        c_cat.font = body_font
        c_cat.number_format = FMT_CURRENCY
        c_cat.alignment = align_right
        c_cat.border = grid_border
        if m_idx % 2 == 0:
            c_cat.fill = stripe_fill

        # 富邦商業扣款小計 (富邦尊御 + 分期中的富邦項)
        f_fubon = f"=D{cur_r}+'04_信用卡分期'!D{cur_r}"
        c_fub = ws_cards.cell(row=cur_r, column=8, value=f_fubon)
        c_fub.font = body_font
        c_fub.number_format = FMT_CURRENCY
        c_fub.alignment = align_right
        c_fub.border = grid_border
        if m_idx % 2 == 0:
            c_fub.fill = stripe_fill

    # 2026 全年累計加總
    cards_tot_row = row_cards_start + 12
    ws_cards.cell(row=cards_tot_row, column=1, value="2026 全年累計加總").font = total_font
    ws_cards.cell(row=cards_tot_row, column=1).alignment = align_center
    ws_cards.cell(row=cards_tot_row, column=1).fill = total_fill
    ws_cards.cell(row=cards_tot_row, column=1).border = total_border

    for col_i in range(2, 9):
        col_let = get_column_letter(col_i)
        f_yr = f"=SUM({col_let}{row_cards_start}:{col_let}{cards_tot_row-1})"
        c_y = ws_cards.cell(row=cards_tot_row, column=col_i, value=f_yr)
        c_y.font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
        c_y.number_format = FMT_CURRENCY
        c_y.alignment = align_right
        c_y.fill = safe_fill if col_i == 6 else total_fill
        c_y.border = total_border


    # -------------------------------------------------------------
    # 分頁 5：05_固定費用 (Recurring Bills)
    # 格式：縱軸為 2026/01月 ~ 2026/12月，橫軸為固定支出項目
    # -------------------------------------------------------------
    ws_recurring.views.sheetView[0].showGridLines = True
    ws_recurring.freeze_panes = "B8"

    ws_recurring.merge_cells("A1:J2")
    ws_recurring["A1"].value = "📌 PocketMoney 固定費用與循環帳單月度排程 (Recurring Bills by Month)"
    ws_recurring["A1"].font = title_font
    ws_recurring["A1"].fill = header_fill
    ws_recurring["A1"].alignment = align_center

    ws_recurring["A3"].value = "💡 說明：依使用者指定的直向時間軸排版；納入房貸、學費、管理費、保險與公用事業費，右側自動彙整銀行直扣與信用卡代扣。"
    ws_recurring["A3"].font = subtitle_font

    recurring_items = [
        {"col": 2, "name": "信義特區豪宅房貸本息", "method": "銀行直扣 (中信)", "cycle": "每月 28 號扣繳", "amount": 72000, "months": list(range(1, 13)), "is_bank": True},
        {"col": 3, "name": "私立貴族雙語學校雜費", "method": "銀行直扣 (玉山)", "cycle": "半年繳 (2/8月 15號)", "amount": 160000, "months": [2, 8], "is_bank": True},
        {"col": 4, "name": "家庭終身壽險與重大傷病險", "method": "信用卡代扣 (國泰)", "cycle": "年繳 (5月 10號)", "amount": 128000, "months": [5], "is_bank": False},
        {"col": 5, "name": "豪宅社區管理費", "method": "銀行直扣 (中信)", "cycle": "雙月繳 (雙數月 05號)", "amount": 18000, "months": [2, 4, 6, 8, 10, 12], "is_bank": True},
        {"col": 6, "name": "自用住宅水電瓦斯事業費", "method": "銀行直扣 (國泰)", "cycle": "雙月繳 (單數月 20號)", "amount": 8500, "months": [1, 3, 5, 7, 9, 11], "is_bank": True},
        {"col": 7, "name": "家用光纖寬頻與串流", "method": "信用卡代扣 (富邦)", "cycle": "每月 12 號扣繳", "amount": 2500, "months": list(range(1, 13)), "is_bank": False},
    ]

    # 表頭 Row 5 & Row 6
    ws_recurring.cell(row=5, column=1, value="月份").font = th_font
    ws_recurring.cell(row=5, column=1).fill = th_fill
    ws_recurring.cell(row=5, column=1).alignment = align_center
    ws_recurring.cell(row=5, column=1).border = header_border

    ws_recurring.cell(row=6, column=1, value="扣繳週期說明").font = th_meta_font
    ws_recurring.cell(row=6, column=1).fill = th_fill
    ws_recurring.cell(row=6, column=1).alignment = align_center
    ws_recurring.cell(row=6, column=1).border = header_border

    for item in recurring_items:
        c_i = item["col"]
        # 第一層表頭：名稱
        c_h1 = ws_recurring.cell(row=5, column=c_i, value=item["name"])
        c_h1.font = th_font
        c_h1.fill = th_fill
        c_h1.alignment = align_center
        c_h1.border = header_border
        
        # 第二層表頭：管道與週期
        c_h2 = ws_recurring.cell(row=6, column=c_i, value=f"{item['method']}\n({item['cycle']})")
        c_h2.font = th_meta_font
        c_h2.fill = th_fill
        c_h2.alignment = align_center
        c_h2.border = header_border

    # 欄 8: 銀行帳戶直扣小計
    c_b_h1 = ws_recurring.cell(row=5, column=8, value="銀行帳戶直扣小計")
    c_b_h1.font = th_font
    c_b_h1.fill = th_accent_fill
    c_b_h1.alignment = align_center
    c_b_h1.border = header_border

    c_b_h2 = ws_recurring.cell(row=6, column=8, value="房貸+學費+管理費+水電")
    c_b_h2.font = th_meta_font
    c_b_h2.fill = th_accent_fill
    c_b_h2.alignment = align_center
    c_b_h2.border = header_border

    # 欄 9: 信用卡代扣小計
    c_c_h1 = ws_recurring.cell(row=5, column=9, value="信用卡代扣小計")
    c_c_h1.font = th_font
    c_c_h1.fill = th_highlight_fill
    c_c_h1.alignment = align_center
    c_c_h1.border = header_border

    c_c_h2 = ws_recurring.cell(row=6, column=9, value="保險+寬頻 (已包含於卡費)")
    c_c_h2.font = th_meta_font
    c_c_h2.fill = th_highlight_fill
    c_c_h2.alignment = align_center
    c_c_h2.border = header_border

    # 欄 10: 當月固定費用總額
    c_tot_rec1 = ws_recurring.cell(row=5, column=10, value="固定費用應扣總額")
    c_tot_rec1.font = th_font
    c_tot_rec1.fill = th_accent_fill
    c_tot_rec1.alignment = align_center
    c_tot_rec1.border = header_border

    c_tot_rec2 = ws_recurring.cell(row=6, column=10, value="銀行直扣 + 信用卡代扣")
    c_tot_rec2.font = th_meta_font
    c_tot_rec2.fill = th_accent_fill
    c_tot_rec2.alignment = align_center
    c_tot_rec2.border = header_border

    # 填入 12 個月份 (Row 7 ~ Row 18)
    row_rec_start = 7
    for m_idx, m_str in enumerate(MONTH_LABELS, 1):
        cur_r = row_rec_start + m_idx - 1

        # 月份
        ws_recurring.cell(row=cur_r, column=1, value=m_str).font = month_font
        ws_recurring.cell(row=cur_r, column=1).alignment = align_center
        ws_recurring.cell(row=cur_r, column=1).border = grid_border
        if m_idx % 2 == 0:
            ws_recurring.cell(row=cur_r, column=1).fill = stripe_fill

        # 各項目金額
        bank_cols = []
        card_cols = []
        for item in recurring_items:
            c_i = item["col"]
            val = item["amount"] if m_idx in item["months"] else 0
            val_c = ws_recurring.cell(row=cur_r, column=c_i, value=val)
            val_c.font = body_font
            val_c.number_format = FMT_CURRENCY
            val_c.alignment = align_right
            val_c.border = grid_border
            if m_idx % 2 == 0:
                val_c.fill = stripe_fill
            
            if item["is_bank"]:
                bank_cols.append(f"{get_column_letter(c_i)}{cur_r}")
            else:
                card_cols.append(f"{get_column_letter(c_i)}{cur_r}")

        # 銀行直扣小計
        f_bank_sub = f"={'+'.join(bank_cols)}"
        c_bs = ws_recurring.cell(row=cur_r, column=8, value=f_bank_sub)
        c_bs.font = body_bold
        c_bs.number_format = FMT_CURRENCY
        c_bs.alignment = align_right
        c_bs.border = grid_border
        if m_idx % 2 == 0:
            c_bs.fill = stripe_fill

        # 信用卡代扣小計
        f_card_sub = f"={'+'.join(card_cols)}"
        c_cs = ws_recurring.cell(row=cur_r, column=9, value=f_card_sub)
        c_cs.font = body_bold
        c_cs.number_format = FMT_CURRENCY
        c_cs.alignment = align_right
        c_cs.border = grid_border
        if m_idx % 2 == 0:
            c_cs.fill = stripe_fill

        # 固定費用應扣總額 (注意：在現金流檢核中，通常只扣「銀行直扣」，因為信用卡代扣已算在卡費總額中；這裡提供完整總額)
        f_rec_grand = f"=H{cur_r}+I{cur_r}"
        c_rg = ws_recurring.cell(row=cur_r, column=10, value=f_rec_grand)
        c_rg.font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
        c_rg.number_format = FMT_CURRENCY
        c_rg.alignment = align_right
        c_rg.border = grid_border
        if m_idx % 2 == 0:
            c_rg.fill = stripe_fill

    # 2026 全年累計加總
    rec_tot_row = row_rec_start + 12
    ws_recurring.cell(row=rec_tot_row, column=1, value="2026 全年累計加總").font = total_font
    ws_recurring.cell(row=rec_tot_row, column=1).alignment = align_center
    ws_recurring.cell(row=rec_tot_row, column=1).fill = total_fill
    ws_recurring.cell(row=rec_tot_row, column=1).border = total_border

    for col_i in range(2, 11):
        col_let = get_column_letter(col_i)
        f_yr = f"=SUM({col_let}{row_rec_start}:{col_let}{rec_tot_row-1})"
        c_y = ws_recurring.cell(row=rec_tot_row, column=col_i, value=f_yr)
        c_y.font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")
        c_y.number_format = FMT_CURRENCY
        c_y.alignment = align_right
        c_y.fill = safe_fill if col_i == 10 else total_fill
        c_y.border = total_border

    # 月平準化金額列
    ws_recurring.cell(row=rec_tot_row+1, column=1, value="每月平準化負擔").font = body_bold
    ws_recurring.cell(row=rec_tot_row+1, column=1).alignment = align_center
    ws_recurring.cell(row=rec_tot_row+1, column=1).fill = total_fill
    ws_recurring.cell(row=rec_tot_row+1, column=1).border = grid_border

    for col_i in range(2, 11):
        col_let = get_column_letter(col_i)
        c_eq = ws_recurring.cell(row=rec_tot_row+1, column=col_i, value=f"={col_let}{rec_tot_row}/12")
        c_eq.font = body_bold
        c_eq.number_format = FMT_CURRENCY
        c_eq.alignment = align_right
        c_eq.fill = total_fill
        c_eq.border = grid_border


    # -------------------------------------------------------------
    # 分頁 3：03_大額消費明細 (Big Expenses)
    # -------------------------------------------------------------
    ws_big_exp.views.sheetView[0].showGridLines = True
    ws_big_exp.freeze_panes = "A5"

    ws_big_exp.merge_cells("A1:H2")
    ws_big_exp["A1"].value = "🛍️ PocketMoney 信用卡大額消費對帳清單 (Big Expenses Log)"
    ws_big_exp["A1"].font = title_font
    ws_big_exp["A1"].fill = header_fill
    ws_big_exp["A1"].alignment = align_center

    ws_big_exp["A3"].value = "💡 說明：類似銀行消費對帳單，標註超過警示門檻之非日常大額支出，方便核對各月份帳單飆高原因。"
    ws_big_exp["A3"].font = subtitle_font

    big_headers = ["消費日期", "歸屬月份", "消費項目 / 特約商店", "刷卡卡片", "扣繳銀行", "金額 (NT$)", "支出類別", "備註說明"]
    for col_idx, h in enumerate(big_headers, 1):
        c = ws_big_exp.cell(row=4, column=col_idx, value=h)
        c.font = th_font
        c.fill = th_fill if col_idx != 6 else th_accent_fill
        c.alignment = align_center
        c.border = header_border

    mock_big_expenses = [
        ("2026-01-18", "2026 / 01 月", "米其林星級年末家族尾牙饗宴", "美國運通 百夫長白金卡", "國泰世華", 42000, "餐飲社交", "家族三代春節前聚餐"),
        ("2026-02-10", "2026 / 02 月", "日本二世谷家族滑雪全包度假村", "國泰世華 世界卡 (CUBE)", "國泰世華", 138000, "旅遊度假", "早鳥機加酒與滑雪教練"),
        ("2026-04-22", "2026 / 04 月", "國際拍賣會當代藝術版畫收藏", "美國運通 百夫長白金卡", "國泰世華", 85000, "藝術投資", "限量收藏帶保證書"),
        ("2026-05-12", "2026 / 05 月", "綜合所得稅信用卡全額代繳", "富邦 尊御商務卡", "富邦商業", 260000, "稅務法規", "分期零利率首期前全額授權"),
        ("2026-07-08", "2026 / 07 月", "瑞士原廠頂級名錶保養與年檢", "美國運通 百夫長白金卡", "國泰世華", 68000, "精品維護", "十年一度全面洗油調校"),
        ("2026-08-25", "2026 / 08 月", "海外私立雙語學校秋季註冊費", "國泰世華 世界卡 (CUBE)", "國泰世華", 185000, "子女教育", "第一期學雜費與校車"),
        ("2026-10-15", "2026 / 10 月", "義大利頂級原裝進口沙發尾款", "美國運通 百夫長白金卡", "國泰世華", 120000, "居家裝潢", "海運抵台驗收付清"),
        ("2026-11-20", "2026 / 11 月", "黑五頂級影音設備升級預購", "富邦 尊御商務卡", "富邦商業", 75000, "家庭影音", "旗艦級前後級擴大機"),
        ("2026-12-24", "2026 / 12 月", "跨年頂級溫泉渡假會館包棟", "美國運通 百夫長白金卡", "國泰世華", 98000, "旅遊度假", "三代同堂跨年假期")
    ]

    for idx, row_data in enumerate(mock_big_expenses, 5):
        ws_big_exp.cell(row=idx, column=1, value=row_data[0]).alignment = align_center
        ws_big_exp.cell(row=idx, column=2, value=row_data[1]).alignment = align_center
        ws_big_exp.cell(row=idx, column=3, value=row_data[2]).font = body_bold
        ws_big_exp.cell(row=idx, column=4, value=row_data[3]).font = body_font
        ws_big_exp.cell(row=idx, column=5, value=row_data[4]).font = body_font
        
        amt_c = ws_big_exp.cell(row=idx, column=6, value=row_data[5])
        amt_c.font = Font(name=FONT_NAME, size=10, bold=True, color="DC2626")
        amt_c.number_format = FMT_CURRENCY
        amt_c.alignment = align_right

        ws_big_exp.cell(row=idx, column=7, value=row_data[6]).alignment = align_center
        ws_big_exp.cell(row=idx, column=8, value=row_data[7]).font = note_font

        for c_i in range(1, 9):
            ws_big_exp.cell(row=idx, column=c_i).border = grid_border
            if idx % 2 == 1:
                ws_big_exp.cell(row=idx, column=c_i).fill = stripe_fill

    # 大額消費加總
    last_row_exp = 4 + len(mock_big_expenses) + 1
    ws_big_exp.cell(row=last_row_exp, column=1, value="2026 全年累計加總").font = total_font
    ws_big_exp.cell(row=last_row_exp, column=1).alignment = align_center
    ws_big_exp.cell(row=last_row_exp, column=6, value=f"=SUM(F5:F{last_row_exp-1})").font = total_font
    ws_big_exp.cell(row=last_row_exp, column=6).number_format = FMT_CURRENCY
    ws_big_exp.cell(row=last_row_exp, column=6).alignment = align_right
    for c_i in range(1, 9):
        ws_big_exp.cell(row=last_row_exp, column=c_i).fill = total_fill
        ws_big_exp.cell(row=last_row_exp, column=c_i).border = total_border


    # -------------------------------------------------------------
    # 分頁 6：06_銀行帳戶與異動 (Bank Accounts)
    # -------------------------------------------------------------
    ws_banks.views.sheetView[0].showGridLines = True
    ws_banks.freeze_panes = "A5"

    ws_banks.merge_cells("A1:H2")
    ws_banks["A1"].value = "🏦 PocketMoney 銀行帳戶結餘現況與資金異動明細"
    ws_banks["A1"].font = title_font
    ws_banks["A1"].fill = header_fill
    ws_banks["A1"].alignment = align_center

    ws_banks["A3"].value = "💡 說明：掌握各帳戶目前結餘、薪轉日、最低防護準備金與現金拖累警戒線。"
    ws_banks["A3"].font = subtitle_font

    bank_headers = ["銀行機構與專戶名稱", "目前最新餘額 (NT$)", "固定薪資入帳", "發薪入帳日", "最低安全防線", "現金拖累警戒線", "帳戶狀態評估", "專戶定位與用途說明"]
    for col_idx, h in enumerate(bank_headers, 1):
        c = ws_banks.cell(row=4, column=col_idx, value=h)
        c.font = th_font
        c.fill = th_fill if col_idx != 2 else th_accent_fill
        c.alignment = align_center
        c.border = header_border

    r_bank = 5
    for idx, b in enumerate(banks_data):
        ws_banks.cell(row=r_bank, column=1, value=b["name"]).font = body_bold
        
        bal_c = ws_banks.cell(row=r_bank, column=2, value=b["balance"])
        bal_c.font = Font(name=FONT_NAME, size=10, bold=True, color="0284C7")
        bal_c.number_format = FMT_CURRENCY
        bal_c.alignment = align_right

        ws_banks.cell(row=r_bank, column=3, value=b.get("defaultSalary") or 0).number_format = FMT_CURRENCY
        sal_day = b.get("salaryDay") or 0
        ws_banks.cell(row=r_bank, column=4, value=f"{sal_day} 號" if sal_day > 0 else "無").alignment = align_center
        ws_banks.cell(row=r_bank, column=5, value=b.get("minReserve") or 0).number_format = FMT_CURRENCY
        ws_banks.cell(row=r_bank, column=6, value=b.get("cashDragAlert") or 0).number_format = FMT_CURRENCY

        # 狀態公式
        status_f = f'=IF(B{r_bank}<E{r_bank}, "🚨 低於安全線", IF(B{r_bank}>F{r_bank}, "⚡ 閒置資金偏高", "✅ 水位正常"))'
        st_c = ws_banks.cell(row=r_bank, column=7, value=status_f)
        st_c.font = body_bold
        st_c.alignment = align_center

        ws_banks.cell(row=r_bank, column=8, value=b.get("note", "")).font = note_font

        for c_i in range(1, 9):
            ws_banks.cell(row=r_bank, column=c_i).border = grid_border
            if idx % 2 == 1:
                ws_banks.cell(row=r_bank, column=c_i).fill = stripe_fill
        r_bank += 1

    bank_tot_row = r_bank
    ws_banks.cell(row=bank_tot_row, column=1, value="合計總流動性資金").font = body_bold
    ws_banks.cell(row=bank_tot_row, column=2, value=f"=SUM(B5:B{bank_tot_row-1})").font = Font(name=FONT_NAME, size=11, bold=True, color="0F172A")
    ws_banks.cell(row=bank_tot_row, column=2).number_format = FMT_CURRENCY
    ws_banks.cell(row=bank_tot_row, column=2).alignment = align_right

    ws_banks.cell(row=bank_tot_row, column=3, value=f"=SUM(C5:C{bank_tot_row-1})").font = body_bold
    ws_banks.cell(row=bank_tot_row, column=3).number_format = FMT_CURRENCY

    ws_banks.cell(row=bank_tot_row, column=5, value=f"=SUM(E5:E{bank_tot_row-1})").font = body_bold
    ws_banks.cell(row=bank_tot_row, column=5).number_format = FMT_CURRENCY

    for c_i in range(1, 9):
        ws_banks.cell(row=bank_tot_row, column=c_i).fill = total_fill
        ws_banks.cell(row=bank_tot_row, column=c_i).border = total_border

    # 重大事件日誌
    r_evt_start = bank_tot_row + 3
    ws_banks.cell(row=r_evt_start, column=1, value="📋 銀行近期重大入帳與大筆提領異動歷程 (Significant Bank Events)").font = section_font
    
    evt_headers = ["異動日期", "所屬銀行", "異動類別", "項目說明", "金額 (NT$)", "異動後預估影響"]
    for col_idx, h in enumerate(evt_headers, 1):
        c = ws_banks.cell(row=r_evt_start+1, column=col_idx, value=h)
        c.font = th_font
        c.fill = th_fill if col_idx != 5 else th_accent_fill
        c.alignment = align_center
        c.border = header_border

    mock_bank_events = [
        ("2026-01-15", "國泰世華 (尊爵VIP財管)", "年度分紅入帳", "高階主管年度營運分紅入帳", 750000, "流動資金大幅提升"),
        ("2026-01-20", "國泰世華 (尊爵VIP財管)", "大筆現鈔提領", "春節家族長輩與晚輩賀歲紅包", -100000, "短期現金流出"),
        ("2026-02-15", "玉山銀行 (海外私校教育)", "海外留學匯款", "雙語私校下學期學雜費與海外匯款", -400000, "教育專戶資金扣抵"),
        ("2026-05-18", "富邦商業 (長線存股戶)", "股票股利入帳", "高股息 ETF 與權值股首波股息入帳", 125000, "投資待命金補充"),
        ("2026-07-25", "富邦商業 (長線存股戶)", "核心持股除息", "主力科技股現金股利大額入帳", 380000, "股市現金池再投資")
    ]

    r_evt = r_evt_start + 2
    for idx, evt in enumerate(mock_bank_events):
        ws_banks.cell(row=r_evt, column=1, value=evt[0]).alignment = align_center
        ws_banks.cell(row=r_evt, column=2, value=evt[1]).font = body_font
        ws_banks.cell(row=r_evt, column=3, value=evt[2]).alignment = align_center
        ws_banks.cell(row=r_evt, column=4, value=evt[3]).font = body_bold
        
        amt_c = ws_banks.cell(row=r_evt, column=5, value=evt[4])
        amt_c.number_format = FMT_CURRENCY
        amt_c.alignment = align_right
        amt_c.font = alert_font if evt[4] < 0 else safe_font

        ws_banks.cell(row=r_evt, column=6, value=evt[5]).font = note_font

        for c_i in range(1, 7):
            ws_banks.cell(row=r_evt, column=c_i).border = grid_border
            if idx % 2 == 1:
                ws_banks.cell(row=r_evt, column=c_i).fill = stripe_fill
        r_evt += 1


    # -------------------------------------------------------------
    # 分頁 1：01_現金流檢核 (Cashflow Check - 核心防跳票總表)
    # 與 02、04、05 完美同列對齊！ (Row 7 ~ Row 18 為 1~12月)
    # -------------------------------------------------------------
    ws_cashflow.views.sheetView[0].showGridLines = True
    ws_cashflow.freeze_panes = "B8"

    # Banner
    ws_cashflow.merge_cells("A1:K2")
    ws_cashflow["A1"].value = "📊 PocketMoney 2026 年度每月資金防跳票檢核總表 (Cashflow Check)"
    ws_cashflow["A1"].font = title_font
    ws_cashflow["A1"].fill = header_fill
    ws_cashflow["A1"].alignment = align_center

    ws_cashflow["A3"].value = "💡 核心機制：完全同列對齊 02 信用卡與 05 固定費用；嚴密檢核扣繳後存款餘額，杜絕違約跳票風險。"
    ws_cashflow["A3"].font = subtitle_font

    # KPI 摘要卡 (Row 4~5)
    kpis = [
        ("總流動性資金庫存", f"='06_銀行帳戶與異動'!B{bank_tot_row}", "B4", "C5", "0284C7"),
        ("年度信用卡總扣繳", f"='02_信用卡12個月'!F{cards_tot_row}", "D4", "E5", "F59E0B"),
        ("年度固定費用總額", f"='05_固定費用'!J{rec_tot_row}", "F4", "G5", "10B981"),
        ("全戶最低防守水位", f"='06_銀行帳戶與異動'!E{bank_tot_row}", "H4", "I5", "64748B")
    ]
    for label, formula, top_left, bottom_right, color_code in kpis:
        c_top = ws_cashflow[top_left]
        c_top.value = label
        c_top.font = Font(name=FONT_NAME, size=9, bold=True, color="64748B")
        c_top.alignment = align_center

        col_start = ord(top_left[0]) - ord('A') + 1
        row_start = int(top_left[1])
        col_end = ord(bottom_right[0]) - ord('A') + 1
        row_end = int(bottom_right[1])
        
        ws_cashflow.merge_cells(start_row=row_start, start_column=col_start, end_row=row_start, end_column=col_end)
        ws_cashflow.merge_cells(start_row=row_end, start_column=col_start, end_row=row_end, end_column=col_end)
        
        c_val = ws_cashflow.cell(row=row_end, column=col_start, value=formula)
        c_val.font = Font(name=FONT_NAME, size=13, bold=True, color=color_code)
        c_val.number_format = FMT_CURRENCY
        c_val.alignment = align_center
        
        for r_i in range(row_start, row_end+1):
            for c_i in range(col_start, col_end+1):
                ws_cashflow.cell(row=r_i, column=c_i).border = grid_border
                ws_cashflow.cell(row=r_i, column=c_i).fill = total_fill

    # 表格標題 (Row 6)
    chk_headers = [
        "月份",
        "月初起始餘額 (A)",
        "預估收入入帳 (B)",
        "信用卡應扣總額 (C)",
        "銀行直扣固定費 (D)",
        "預估月底餘額 (E=A+B-C-D)",
        "最低防守準備金 (F)",
        "安全防線差額 (E-F)",
        "防跳票狀態檢核",
        "實際月底盤點 (G)",
        "實盤差額 (G-E)"
    ]

    for col_idx, h in enumerate(chk_headers, 1):
        c = ws_cashflow.cell(row=6, column=col_idx, value=h)
        c.font = th_font
        c.fill = th_fill if col_idx not in [6, 9] else th_accent_fill
        c.alignment = align_center
        c.border = header_border

    # 12 個月份 (Row 7 ~ Row 18) - 與 02、04、05 完全一對一同列！
    row_chk_start = 7
    for m_idx, m_str in enumerate(MONTH_LABELS, 1):
        cur_r = row_chk_start + m_idx - 1

        # 月份欄
        ws_cashflow.cell(row=cur_r, column=1, value=m_str).font = month_font
        ws_cashflow.cell(row=cur_r, column=1).alignment = align_center
        ws_cashflow.cell(row=cur_r, column=1).border = grid_border
        if m_idx % 2 == 0:
            ws_cashflow.cell(row=cur_r, column=1).fill = stripe_fill

        # 月初起始餘額 (A)
        if m_idx == 1:
            bal_start_formula = f"='06_銀行帳戶與異動'!B{bank_tot_row}"
        else:
            bal_start_formula = f"=F{cur_r-1}"
            
        c_a = ws_cashflow.cell(row=cur_r, column=2, value=bal_start_formula)
        c_a.number_format = FMT_CURRENCY
        c_a.alignment = align_right
        c_a.font = body_font

        # 預估固定收入 (B)
        bonus_val = 750000 if m_idx == 1 else (125000 if m_idx == 5 else (380000 if m_idx == 7 else 0))
        inc_formula = f"='06_銀行帳戶與異動'!C{bank_tot_row}+{bonus_val}"
        c_b = ws_cashflow.cell(row=cur_r, column=3, value=inc_formula)
        c_b.number_format = FMT_CURRENCY
        c_b.alignment = align_right
        c_b.font = body_font

        # 信用卡應扣總額 (C): 極簡對應！直接引用 02 表同一列 Row cur_r 的 F 欄！
        card_formula = f"='02_信用卡12個月'!F{cur_r}"
        c_c = ws_cashflow.cell(row=cur_r, column=4, value=card_formula)
        c_c.number_format = FMT_CURRENCY
        c_c.alignment = align_right
        c_c.font = Font(name=FONT_NAME, size=10, bold=True, color="DC2626")

        # 銀行直扣固定費 (D): 極簡對應！直接引用 05 表同一列 Row cur_r 的 H 欄 (銀行直扣)！
        rec_formula = f"='05_固定費用'!H{cur_r}"
        c_d = ws_cashflow.cell(row=cur_r, column=5, value=rec_formula)
        c_d.number_format = FMT_CURRENCY
        c_d.alignment = align_right
        c_d.font = Font(name=FONT_NAME, size=10, bold=True, color="D97706")

        # 預估月底餘額 (E = A + B - C - D)
        e_formula = f"=B{cur_r}+C{cur_r}-D{cur_r}-E{cur_r}"
        c_e = ws_cashflow.cell(row=cur_r, column=6, value=e_formula)
        c_e.number_format = FMT_CURRENCY
        c_e.alignment = align_right
        c_e.font = Font(name=FONT_NAME, size=10, bold=True, color="0F172A")

        # 最低防守準備金 (F)
        f_formula = f"='06_銀行帳戶與異動'!E{bank_tot_row}"
        c_f = ws_cashflow.cell(row=cur_r, column=7, value=f_formula)
        c_f.number_format = FMT_CURRENCY
        c_f.alignment = align_right
        c_f.font = note_font

        # 安全防線差額 (E - F)
        diff_formula = f"=F{cur_r}-G{cur_r}"
        c_diff = ws_cashflow.cell(row=cur_r, column=8, value=diff_formula)
        c_diff.number_format = FMT_CURRENCY
        c_diff.alignment = align_right
        c_diff.font = body_bold

        # 防跳票狀態檢核公式
        status_f = f'=IF(F{cur_r}<0, "🚨 扣款不足 (跳票風險)", IF(H{cur_r}<0, "⚠️ 低於安全水位", "✅ 餘額安全無虞"))'
        c_st = ws_cashflow.cell(row=cur_r, column=9, value=status_f)
        c_st.alignment = align_center
        c_st.font = body_bold

        # 實際月底盤點 (G) - 藍字手動輸入
        mock_actual = [4400000, 3950000, 4010000] if m_idx <= 3 else None
        c_g = ws_cashflow.cell(row=cur_r, column=10, value=mock_actual[m_idx-1] if mock_actual else "")
        c_g.number_format = FMT_CURRENCY
        c_g.alignment = align_right
        c_g.font = Font(name=FONT_NAME, size=10, color="0000FF")

        # 實盤差額 (G - E)
        actual_diff_f = f'=IF(J{cur_r}="","",J{cur_r}-F{cur_r})'
        c_ad = ws_cashflow.cell(row=cur_r, column=11, value=actual_diff_f)
        c_ad.number_format = FMT_CURRENCY
        c_ad.alignment = align_right
        c_ad.font = body_bold

        for col_i in range(1, 12):
            ws_cashflow.cell(row=cur_r, column=col_i).border = grid_border
            if m_idx % 2 == 0:
                ws_cashflow.cell(row=cur_r, column=col_i).fill = stripe_fill

    # 2026 全年累計加總
    chk_tot_row = row_chk_start + 12
    ws_cashflow.cell(row=chk_tot_row, column=1, value="2026 全年累計加總").font = total_font
    ws_cashflow.cell(row=chk_tot_row, column=1).alignment = align_center
    ws_cashflow.cell(row=chk_tot_row, column=2, value="-").alignment = align_center
    
    ws_cashflow.cell(row=chk_tot_row, column=3, value=f"=SUM(C7:C{chk_tot_row-1})").font = total_font
    ws_cashflow.cell(row=chk_tot_row, column=3).number_format = FMT_CURRENCY

    ws_cashflow.cell(row=chk_tot_row, column=4, value=f"=SUM(D7:D{chk_tot_row-1})").font = total_font
    ws_cashflow.cell(row=chk_tot_row, column=4).number_format = FMT_CURRENCY

    ws_cashflow.cell(row=chk_tot_row, column=5, value=f"=SUM(E7:E{chk_tot_row-1})").font = total_font
    ws_cashflow.cell(row=chk_tot_row, column=5).number_format = FMT_CURRENCY

    ws_cashflow.cell(row=chk_tot_row, column=6, value=f"=F{chk_tot_row-1}").font = total_font # 年末結餘
    ws_cashflow.cell(row=chk_tot_row, column=6).number_format = FMT_CURRENCY

    ws_cashflow.cell(row=chk_tot_row, column=7, value="-").alignment = align_center
    ws_cashflow.cell(row=chk_tot_row, column=8, value=f"=H{chk_tot_row-1}").font = total_font
    ws_cashflow.cell(row=chk_tot_row, column=8).number_format = FMT_CURRENCY

    ws_cashflow.cell(row=chk_tot_row, column=9, value="全年財務穩健").alignment = align_center
    ws_cashflow.cell(row=chk_tot_row, column=9).font = safe_font

    ws_cashflow.cell(row=chk_tot_row, column=10, value="").alignment = align_center
    ws_cashflow.cell(row=chk_tot_row, column=11, value="").alignment = align_center

    for col_i in range(1, 12):
        ws_cashflow.cell(row=chk_tot_row, column=col_i).fill = total_fill
        ws_cashflow.cell(row=chk_tot_row, column=col_i).border = total_border


    # ==========================================
    # 欄寬最佳化
    # ==========================================
    ws_cashflow.column_dimensions["A"].width = 16
    ws_cashflow.column_dimensions["B"].width = 19
    ws_cashflow.column_dimensions["C"].width = 18
    ws_cashflow.column_dimensions["D"].width = 19
    ws_cashflow.column_dimensions["E"].width = 19
    ws_cashflow.column_dimensions["F"].width = 23
    ws_cashflow.column_dimensions["G"].width = 19
    ws_cashflow.column_dimensions["H"].width = 19
    ws_cashflow.column_dimensions["I"].width = 24
    ws_cashflow.column_dimensions["J"].width = 18
    ws_cashflow.column_dimensions["K"].width = 18

    ws_cards.column_dimensions["A"].width = 16
    ws_cards.column_dimensions["B"].width = 26
    ws_cards.column_dimensions["C"].width = 25
    ws_cards.column_dimensions["D"].width = 24
    ws_cards.column_dimensions["E"].width = 20
    ws_cards.column_dimensions["F"].width = 22
    ws_cards.column_dimensions["G"].width = 22
    ws_cards.column_dimensions["H"].width = 22

    ws_installments.column_dimensions["A"].width = 16
    ws_installments.column_dimensions["B"].width = 30
    ws_installments.column_dimensions["C"].width = 30
    ws_installments.column_dimensions["D"].width = 30
    ws_installments.column_dimensions["E"].width = 30
    ws_installments.column_dimensions["F"].width = 22

    ws_recurring.column_dimensions["A"].width = 16
    ws_recurring.column_dimensions["B"].width = 27
    ws_recurring.column_dimensions["C"].width = 27
    ws_recurring.column_dimensions["D"].width = 27
    ws_recurring.column_dimensions["E"].width = 25
    ws_recurring.column_dimensions["F"].width = 25
    ws_recurring.column_dimensions["G"].width = 25
    ws_recurring.column_dimensions["H"].width = 22
    ws_recurring.column_dimensions["I"].width = 22
    ws_recurring.column_dimensions["J"].width = 22

    ws_big_exp.column_dimensions["A"].width = 14
    ws_big_exp.column_dimensions["B"].width = 16
    ws_big_exp.column_dimensions["C"].width = 34
    ws_big_exp.column_dimensions["D"].width = 24
    ws_big_exp.column_dimensions["E"].width = 18
    ws_big_exp.column_dimensions["F"].width = 16
    ws_big_exp.column_dimensions["G"].width = 14
    ws_big_exp.column_dimensions["H"].width = 28

    ws_banks.column_dimensions["A"].width = 28
    ws_banks.column_dimensions["B"].width = 22
    ws_banks.column_dimensions["C"].width = 18
    ws_banks.column_dimensions["D"].width = 14
    ws_banks.column_dimensions["E"].width = 18
    ws_banks.column_dimensions["F"].width = 18
    ws_banks.column_dimensions["G"].width = 18
    ws_banks.column_dimensions["H"].width = 34

    wb.save(output_path)
    print(f"[SUCCESS] Excel 範本成功產出至: {output_path}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else r"c:\Playground26\wiskinglin.github.io\_dev\PocketMoney\PocketMoney_Export_Mockup.xlsx"
    db = r"c:\Playground26\wiskinglin.github.io\_dev\PocketMoney\database\dummy_db_senior.json"
    build_mockup_excel(out, db)
