document.addEventListener("DOMContentLoaded", () => {
    const scaleGroups = ['各規模VS薪資分佈', '<100', '100-500', '500-1000', '1000-5000', '>5000'];
    const scaleListEl = document.getElementById("scale-list");
    const kpiCardsEl = document.getElementById("kpi-cards");
    const currentGroupTitle = document.getElementById("current-group-title");
    const singleLegend = document.getElementById("single-legend");
    const summaryToggle = document.getElementById("summary-toggle");
    const summaryYearSelect = document.getElementById("summary-year-select");
    
    // Outlier Card Elements
    const outlierContainer = document.getElementById("outlier-container");
    const outlierContent = document.getElementById("outlier-content");

    // Info Modal Elements
    const infoBtn = document.getElementById("infoBtn");
    const infoModal = document.getElementById("infoModal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    if (infoBtn && infoModal && closeModalBtn) {
        infoBtn.addEventListener("click", () => infoModal.classList.add("active"));
        closeModalBtn.addEventListener("click", () => infoModal.classList.remove("active"));
        infoModal.addEventListener("click", (e) => {
            if (e.target === infoModal) infoModal.classList.remove("active");
        });
    }
    
    // Checkbox Elements
    const check108 = document.getElementById("check-108");
    const check114 = document.getElementById("check-114");

    if (check108 && check114) {
        const triggerUpdate = () => {
            const activeGroup = document.querySelector("#scale-list li.active").dataset.group;
            if (activeGroup !== '各規模VS薪資分佈') updateDashboard(activeGroup);
        };
        check108.addEventListener("change", triggerUpdate);
        check114.addEventListener("change", triggerUpdate);
    }
    
    let currentChart = null;

    // 根據您的需求固定全局最大值
    const globalMaxX = 200;
    const globalMaxY = 300;

    // 1. 初始化側邊欄
    scaleGroups.forEach((group, index) => {
        const li = document.createElement("li");
        li.textContent = group;
        li.dataset.group = group;
        if (index === 0) li.classList.add("active");
        
        li.addEventListener("click", () => {
            document.querySelectorAll("#scale-list li").forEach(el => el.classList.remove("active"));
            li.classList.add("active");
            updateDashboard(group);
        });
        
        scaleListEl.appendChild(li);
    });

    if (summaryYearSelect) {
        summaryYearSelect.addEventListener("change", () => {
            updateDashboard('各規模VS薪資分佈');
        });
    }

    // 2. 更新儀表板內容
    function updateDashboard(group) {
        currentGroupTitle.textContent = group === '各規模VS薪資分佈' ? '公司規模vs 薪資總覽' : `組織規模：${group} 人`;
        
        if (group === '各規模VS薪資分佈') {
            kpiCardsEl.style.display = "none";
            singleLegend.style.display = "none";
            if (summaryToggle) summaryToggle.style.display = "flex";
            renderSummaryChart(summaryYearSelect ? summaryYearSelect.value : '114');
            return;
        }

        kpiCardsEl.style.display = "grid";
        singleLegend.style.display = "flex";
        if (summaryToggle) summaryToggle.style.display = "none";

        const data108 = dashboardData.distributions[group]["108"];
        const data114 = dashboardData.distributions[group]["114"];
        
        if (!data108 || !data114) {
            kpiCardsEl.innerHTML = `<div style="color:red; padding: 20px;">此級距資料不足，無法進行比較。</div>`;
            if (currentChart) currentChart.destroy();
            outlierContainer.style.display = "none";
            return;
        }

        renderKPIs(data108.stats, data114.stats);
        renderChart(data108, data114);
    }

    // 3. 渲染 KPI 卡片 (數值從仟元轉換為萬元)
    function renderKPIs(stats108, stats114) {
        const meanGrowth = ((stats114.mean - stats108.mean) / stats108.mean * 100).toFixed(1);
        const medianGrowth = ((stats114.median - stats108.median) / stats108.median * 100).toFixed(1);
        
        // 將數值除以 10 轉換為萬元，並保留 1 位小數
        const median108_wan = (stats108.median / 10).toFixed(1);
        const median114_wan = (stats114.median / 10).toFixed(1);
        const max114_wan = (stats114.max / 10).toFixed(1);
        const min114_wan = (stats114.min / 10).toFixed(1);
        
        kpiCardsEl.innerHTML = `
            <div class="kpi-card glass-panel" style="--accent-color: #38bdf8;">
                <h3>108年 薪資中位數 (平均值)</h3>
                <div class="kpi-value">${median108_wan} 萬元</div>
                <div class="kpi-trend">
                    <span style="color: var(--text-secondary)">樣本數: ${stats108.count} 家</span>
                </div>
            </div>
            
            <div class="kpi-card glass-panel" style="--accent-color: #f43f5e;">
                <h3>114年 薪資中位數 (平均值)</h3>
                <div class="kpi-value">${median114_wan} 萬元</div>
                <div class="kpi-trend ${medianGrowth >= 0 ? 'trend-up' : 'trend-down'}">
                    ${medianGrowth >= 0 ? '▲' : '▼'} ${Math.abs(medianGrowth)}% 成長率
                    <span style="color: var(--text-secondary); margin-left: 8px;">(樣本: ${stats114.count} 家)</span>
                </div>
            </div>
            
            <div class="kpi-card glass-panel" style="--accent-color: #10b981;">
                <h3>114年 薪資分佈極值</h3>
                <div class="kpi-value">${max114_wan} 萬元</div>
                <div class="kpi-trend">
                    <span style="color: var(--text-secondary)">最高中位數 (最低: ${min114_wan})</span>
                </div>
            </div>
        `;
    }
    
    // 萃取離群值 HTML 區塊 (大於 maxLimit 的所有點)
    function buildOutliersHtml(datasets, maxLimit) {
        let hasOutliers = false;
        let html = '';
        
        datasets.forEach(ds => {
            const outliers = ds.data.filter(pt => pt.x > maxLimit && pt.y > 0);
            if (outliers.length > 0) {
                hasOutliers = true;
                html += `
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px;">
                    <div style="color: ${ds.borderColor || ds.backgroundColor.replace('0.4', '1').replace('0.6', '1')}; font-weight: 600; margin-bottom: 8px;">
                        ${ds.label}
                    </div>
                    <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px;">
                `;
                
                outliers.forEach(pt => {
                    html += `<li style="font-size: 0.9rem; color: #e2e8f0;">約 <span style="color: #fff; font-weight: bold;">${pt.x.toFixed(0)}</span> 萬：<span style="color: #10b981; font-weight: bold;">${pt.y}</span> 家</li>`;
                });
                
                html += `</ul></div>`;
            }
        });
        
        return { hasOutliers, html };
    }

    // 4. 渲染單一群組圖表 (完全使用直方圖)
    function renderChart(data108, data114) {
        const ctx = document.getElementById("distributionChart").getContext("2d");
        
        if (currentChart) {
            currentChart.destroy();
        }

        const hist108 = data108.histogram.bins.map((val, i) => ({
            x: (val + (data108.histogram.bin_width / 2)) / 10,
            y: data108.histogram.counts[i]
        }));

        const hist114 = data114.histogram.bins.map((val, i) => ({
            x: (val + (data114.histogram.bin_width / 2)) / 10,
            y: data114.histogram.counts[i]
        }));
        
        const datasets = [];
        
        if (check108 && check108.checked) {
            datasets.push({
                type: 'bar',
                label: '108年 實際分佈',
                data: hist108,
                backgroundColor: 'rgba(56, 189, 248, 0.4)',
                borderColor: 'rgba(56, 189, 248, 0.8)',
                borderWidth: 1,
                barThickness: 8
            });
        }
        
        if (check114 && check114.checked) {
            datasets.push({
                type: 'bar',
                label: '114年 實際分佈',
                data: hist114,
                backgroundColor: 'rgba(244, 63, 94, 0.4)',
                borderColor: 'rgba(244, 63, 94, 0.8)',
                borderWidth: 1,
                barThickness: 8
            });
        }
        
        // 處理離群值
        const outlierInfo = buildOutliersHtml(datasets, globalMaxX);
        if (outlierInfo.hasOutliers) {
            outlierContainer.style.display = "flex";
            outlierContent.innerHTML = outlierInfo.html;
        } else {
            outlierContainer.style.display = "none";
        }

        currentChart = new Chart(ctx, {
            type: 'scatter',
            data: { datasets },
            options: getChartOptions(false)
        });
    }

    // 5. 渲染綜合比較表 (完全使用直方圖)
    function renderSummaryChart(year) {
        const ctx = document.getElementById("distributionChart").getContext("2d");
        if (currentChart) currentChart.destroy();
        
        const colors = [
            '#3b82f6', // <100 blue
            '#10b981', // 100-500 green
            '#f59e0b', // 500-1000 yellow
            '#8b5cf6', // 1000-5000 purple
            '#ef4444'  // >5000 red
        ];
        
        const realGroups = ['<100', '100-500', '500-1000', '1000-5000', '>5000'];
        const datasets = [];
        realGroups.forEach((group, idx) => {
            const data = dashboardData.distributions[group]?.[year];
            if (data && data.histogram) {
                const histData = data.histogram.bins.map((val, i) => ({
                    x: (val + (data.histogram.bin_width / 2)) / 10,
                    y: data.histogram.counts[i]
                }));
                datasets.push({
                    type: 'bar',
                    label: `${group} 人`,
                    data: histData,
                    backgroundColor: colors[idx] + '80', // 加深透明度
                    borderColor: colors[idx],
                    borderWidth: 1,
                    barThickness: 6 // 綜合比較表稍細一點以容納疊加
                });
            }
        });
        
        // 處理離群值
        const outlierInfo = buildOutliersHtml(datasets, globalMaxX);
        if (outlierInfo.hasOutliers) {
            outlierContainer.style.display = "flex";
            outlierContent.innerHTML = outlierInfo.html;
        } else {
            outlierContainer.style.display = "none";
        }

        currentChart = new Chart(ctx, {
            type: 'scatter',
            data: { datasets: datasets },
            options: getChartOptions(true)
        });
    }

    function getChartOptions(isSummary) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: isSummary,
                    labels: { color: '#a0aabf' }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 17, 26, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#a0aabf',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    min: 0,
                    max: globalMaxX,
                    title: { display: true, text: '薪資中位數 (萬元)', color: '#a0aabf', font: { size: 14 } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                    ticks: { 
                        color: '#a0aabf',
                        stepSize: 50
                    }
                },
                y: {
                    min: 0,
                    // 移除全局鎖定 Y 軸，讓 Chart.js 依據各群組資料自動縮放，解決小規模群組被壓縮的問題
                    // max: globalMaxY,
                    title: { display: true, text: '企業家數', color: '#a0aabf', font: { size: 14 } },
                    grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                    ticks: { 
                        color: '#a0aabf',
                        // stepSize: 50,
                        callback: function(value, index, values) {
                            // 當 Y 軸數值為 0 時隱藏標籤，避免與 X 軸的原點 0 發生重疊
                            if (value === 0) return '';
                            return value;
                        }
                    }
                }
            }
        };
    }

    // 初始化載入第一組 (綜合比較)
    updateDashboard(scaleGroups[0]);
});
