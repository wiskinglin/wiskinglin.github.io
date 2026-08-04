import pandas as pd
import numpy as np
import json
import scipy.stats as stats
import os

# 1. 讀取資料
csv_path = r"c:\Playground26\wiskinglin.github.io\thesis\database\260804_salary_master_panel.csv"
df = pd.read_csv(csv_path)

# 只取需要的欄位
df = df[['年度', '公司代號', '公司名稱', '員工人數', '薪資中位數_仟元', '平均薪資_仟元']]

# 處理遺失值
df['薪資中位數_仟元'] = pd.to_numeric(df['薪資中位數_仟元'], errors='coerce')
df['員工人數'] = pd.to_numeric(df['員工人數'], errors='coerce')

# --- 新增需求 1: 匯出同公司歷年排序的 CSV 資料 ---
data_dir = r"c:\Playground26\wiskinglin.github.io\thesis\analysis\07_organization_scale_vs_salary\data"
os.makedirs(data_dir, exist_ok=True)

# 依公司與年度排序
df_sorted = df.sort_values(by=['公司代號', '年度'])
sorted_csv_path = os.path.join(data_dir, "salary_median_7years_sorted.csv")
df_sorted.to_csv(sorted_csv_path, index=False, encoding='utf-8-sig')
print(f"Sorted data saved to {sorted_csv_path}")

# --- 原需求: 組織規模分類 (以 114 年為準) ---
df_114 = df[df['年度'] == 114].dropna(subset=['員工人數'])
def get_scale_group(emp_count):
    if emp_count < 100:
        return '<100'
    elif 100 <= emp_count < 500:
        return '100-500'
    elif 500 <= emp_count < 1000:
        return '500-1000'
    elif 1000 <= emp_count < 5000:
        return '1000-5000'
    else:
        return '>5000'

df_114['Scale_Group'] = df_114['員工人數'].apply(get_scale_group)
scale_mapping = dict(zip(df_114['公司代號'], df_114['Scale_Group']))

# --- 產生 Dashboard JS 數據 ---
dashboard_data = {
    "distributions": {},
    "company_trends": {}
}

# 1. 計算常態分佈數據 (108 vs 114)
df_filtered = df[df['年度'].isin([108, 114])].copy()
df_filtered = df_filtered.dropna(subset=['薪資中位數_仟元'])
df_filtered['Scale_Group'] = df_filtered['公司代號'].map(scale_mapping)
df_filtered = df_filtered.dropna(subset=['Scale_Group'])

groups = ['<100', '100-500', '500-1000', '1000-5000', '>5000']
years = [108, 114]

for group in groups:
    dashboard_data["distributions"][group] = {}
    for year in years:
        year_data = df_filtered[(df_filtered['Scale_Group'] == group) & (df_filtered['年度'] == year)]['薪資中位數_仟元'].values
        
        if len(year_data) < 2:
            dashboard_data["distributions"][group][year] = None
            continue
            
        mean = np.mean(year_data)
        std = np.std(year_data)
        median = np.median(year_data)
        
        hist, bin_edges = np.histogram(year_data, bins=20, density=False)
        
        x = np.linspace(max(0, mean - 3*std), mean + 3*std, 100)
        y = stats.norm.pdf(x, mean, std) * len(year_data) * (bin_edges[1] - bin_edges[0])
        
        dashboard_data["distributions"][group][year] = {
            'stats': {
                'count': int(len(year_data)),
                'mean': float(mean),
                'median': float(median),
                'std': float(std),
                'min': float(np.min(year_data)),
                'max': float(np.max(year_data))
            },
            'histogram': {
                'bins': bin_edges[:-1].tolist(),
                'counts': hist.tolist(),
                'bin_width': float(bin_edges[1] - bin_edges[0])
            },
            'normal_curve': {
                'x': x.tolist(),
                'y': y.tolist()
            }
        }

# 2. 計算每間公司的七年趨勢資料 (為了 Dashboard 搜尋功能)
# 排除 107 年中位數為空的資料
df_trend = df_sorted.dropna(subset=['薪資中位數_仟元'])
for _, row in df_trend.iterrows():
    code = str(row['公司代號'])
    if code not in dashboard_data["company_trends"]:
        dashboard_data["company_trends"][code] = {
            "name": row['公司名稱'],
            "years": [],
            "medians": []
        }
    dashboard_data["company_trends"][code]["years"].append(int(row['年度']))
    dashboard_data["company_trends"][code]["medians"].append(float(row['薪資中位數_仟元']))

# 輸出為 JS 檔案
dashboard_dir = r"c:\Playground26\wiskinglin.github.io\thesis\analysis\07_organization_scale_vs_salary\dashboard"
os.makedirs(dashboard_dir, exist_ok=True)

js_content = f"const dashboardData = {json.dumps(dashboard_data, indent=2, ensure_ascii=False)};"

output_path = os.path.join(dashboard_dir, "data.js")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"JS Data processed and saved to {output_path}")
