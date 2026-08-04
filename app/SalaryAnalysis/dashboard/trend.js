document.addEventListener("DOMContentLoaded", () => {
    // 搜尋功能相關元素
    const searchInput = document.getElementById("companySearch");
    const datalist = document.getElementById("companyOptions");
    const trendCard = document.getElementById("trend-card");
    const trendTitle = document.getElementById("trend-title");
    const emptyState = document.getElementById("empty-state");
    
    let trendChartObj = null;

    let searchHistory = JSON.parse(localStorage.getItem('salaryTrendHistory') || '[]');
    const historyTagsContainer = document.getElementById("history-tags");

    // 0. 初始化搜尋 Datalist 與排行榜
    if (dashboardData && dashboardData.company_trends) {
        Object.keys(dashboardData.company_trends).forEach(code => {
            const name = dashboardData.company_trends[code].name;
            const option = document.createElement("option");
            option.value = code;
            option.textContent = name;
            datalist.appendChild(option);
        });

        // 渲染排行榜
        renderRankings(dashboardData.company_trends);
        // 渲染歷史紀錄
        renderHistory();

        // 監聽搜尋輸入
        searchInput.addEventListener("change", (e) => {
            const code = e.target.value.trim();
            if (dashboardData.company_trends[code]) {
                emptyState.style.display = "none";
                trendCard.style.display = "flex";
                document.getElementById('trend-subtitle').style.display = 'none';
                renderTrendChart(code, dashboardData.company_trends[code]);
                saveToHistory(code);
            } else {
                trendCard.style.display = "none";
                emptyState.style.display = "flex";
                trendTitle.innerHTML = "🏆 各公司薪資分析排行榜";
                document.getElementById('trend-subtitle').style.display = 'block';
            }
        });
    }

    // 歷史紀錄相關函數
    function saveToHistory(code) {
        if (!searchHistory.includes(code)) {
            searchHistory.unshift(code);
            if (searchHistory.length > 10) searchHistory.pop(); // 最多存 10 筆
            localStorage.setItem('salaryTrendHistory', JSON.stringify(searchHistory));
            renderHistory();
        }
    }

    function renderHistory() {
        if (!historyTagsContainer) return;
        historyTagsContainer.innerHTML = '';
        if (searchHistory.length === 0) {
            historyTagsContainer.innerHTML = '<span style="color: var(--text-secondary); font-size: 0.8rem;">尚無紀錄</span>';
            return;
        }
        searchHistory.forEach(code => {
            const name = dashboardData.company_trends[code]?.name || '';
            const tag = document.createElement("div");
            tag.textContent = `${code} ${name}`;
            tag.style.cssText = `
                padding: 4px 10px; background: rgba(255,255,255,0.1); border-radius: 12px;
                font-size: 0.8rem; cursor: pointer; transition: 0.2s; white-space: nowrap;
            `;
            tag.onmouseover = () => tag.style.background = 'rgba(255,255,255,0.2)';
            tag.onmouseout = () => tag.style.background = 'rgba(255,255,255,0.1)';
            tag.onclick = () => {
                searchInput.value = code;
                searchInput.dispatchEvent(new Event('change'));
            };
            historyTagsContainer.appendChild(tag);
        });
    }

    // 排行榜相關函數
    function renderRankings(trends) {
        const top10List = document.getElementById('top10-list');
        const bottom10List = document.getElementById('bottom10-list');
        if (!top10List || !bottom10List) return;

        const growthData = [];
        const highestRawData = [];
        
        Object.keys(trends).forEach(code => {
            const data = trends[code];
            const idx108 = data.years.indexOf(108);
            const idx114 = data.years.indexOf(114);

            // 最高薪資排行：只要有 114 年資料即可納入
            if (idx114 !== -1) {
                const last114 = data.medians[idx114];
                let growth = 0;
                if (idx108 !== -1 && data.medians[idx108] > 0) {
                    growth = ((last114 - data.medians[idx108]) / data.medians[idx108]) * 100;
                }
                highestRawData.push({ code, name: data.name, last: last114, growth });
            }

            // 成長率/衰退排行：必須同時擁有 108 年與 114 年資料才能做公平比較
            if (idx108 !== -1 && idx114 !== -1) {
                const first = data.medians[idx108];
                const last = data.medians[idx114];
                if (first > 0) {
                    const growth = ((last - first) / first) * 100;
                    growthData.push({ code, name: data.name, growth, last });
                }
            }
        });

        // 排序
        growthData.sort((a, b) => b.growth - a.growth);
        const top10 = growthData.slice(0, 10);
        const bottom10 = growthData.slice(-10).reverse();
        
        const highestData = highestRawData.sort((a, b) => b.last - a.last).slice(0, 10);

        const highest10List = document.getElementById('highest10-list');
        if (highest10List) {
            highestData.forEach((item, index) => {
                highest10List.innerHTML += `
                    <li onclick="document.getElementById('companySearch').value='${item.code}'; document.getElementById('companySearch').dispatchEvent(new Event('change'));"
                        onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(0,0,0,0.2)'"
                        style="display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: rgba(0,0,0,0.2); border-radius: 8px; cursor: pointer; transition: 0.2s;">
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <span style="font-weight: bold; color: #38bdf8; width: 18px; font-size: 0.9rem;">${index + 1}</span>
                            <div style="display: flex; flex-direction: column; line-height: 1.2;">
                                <span style="color: #fff; font-size: 0.95rem;">${item.name}</span>
                                <span style="color: var(--text-secondary); font-size: 0.75rem;">(${item.code})</span>
                            </div>
                        </div>
                        <div style="text-align: right; line-height: 1.2; white-space: nowrap;">
                            <div style="color: #38bdf8; font-weight: bold; font-size: 0.95rem;">${(item.last/10).toFixed(1)} 萬</div>
                            <div style="color: var(--text-secondary); font-size: 0.7rem;">${item.growth > 0 ? '+' : ''}${item.growth.toFixed(1)}%</div>
                        </div>
                    </li>
                `;
            });
        }

        top10.forEach((item, index) => {
            top10List.innerHTML += `
                    <li onclick="document.getElementById('companySearch').value='${item.code}'; document.getElementById('companySearch').dispatchEvent(new Event('change'));"
                        onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(0,0,0,0.2)'"
                        style="display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: rgba(0,0,0,0.2); border-radius: 8px; cursor: pointer; transition: 0.2s;">
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <span style="font-weight: bold; color: #10b981; width: 18px; font-size: 0.9rem;">${index + 1}</span>
                            <div style="display: flex; flex-direction: column; line-height: 1.2;">
                                <span style="color: #fff; font-size: 0.95rem;">${item.name}</span>
                                <span style="color: var(--text-secondary); font-size: 0.75rem;">(${item.code})</span>
                            </div>
                        </div>
                        <div style="text-align: right; line-height: 1.2; white-space: nowrap;">
                            <div style="color: #10b981; font-weight: bold; font-size: 0.95rem;">+${item.growth.toFixed(1)}%</div>
                            <div style="color: var(--text-secondary); font-size: 0.7rem;">${(item.last/10).toFixed(1)} 萬</div>
                        </div>
                    </li>
            `;
        });

        bottom10.forEach((item, index) => {
            bottom10List.innerHTML += `
                    <li onclick="document.getElementById('companySearch').value='${item.code}'; document.getElementById('companySearch').dispatchEvent(new Event('change'));"
                        onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='rgba(0,0,0,0.2)'"
                        style="display: flex; justify-content: space-between; align-items: center; padding: 6px 12px; background: rgba(0,0,0,0.2); border-radius: 8px; cursor: pointer; transition: 0.2s;">
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <span style="font-weight: bold; color: #f43f5e; width: 18px; font-size: 0.9rem;">${index + 1}</span>
                            <div style="display: flex; flex-direction: column; line-height: 1.2;">
                                <span style="color: #fff; font-size: 0.95rem;">${item.name}</span>
                                <span style="color: var(--text-secondary); font-size: 0.75rem;">(${item.code})</span>
                            </div>
                        </div>
                        <div style="text-align: right; line-height: 1.2; white-space: nowrap;">
                            <div style="color: #f43f5e; font-weight: bold; font-size: 0.95rem;">${item.growth.toFixed(1)}%</div>
                            <div style="color: var(--text-secondary); font-size: 0.7rem;">${(item.last/10).toFixed(1)} 萬</div>
                        </div>
                    </li>
            `;
        });
    }

    // 5. 渲染個股趨勢圖
    function renderTrendChart(code, trendData) {
        trendTitle.textContent = `[${code}] ${trendData.name} - 薪資中位數動態追蹤`;
        
        // 更新快速看板數據
        const idx108 = trendData.years.indexOf(108);
        const idx114 = trendData.years.indexOf(114);
        
        const val108 = idx108 !== -1 ? trendData.medians[idx108] : null;
        const val114 = idx114 !== -1 ? trendData.medians[idx114] : null;

        document.getElementById('trend-stat-108').textContent = val108 ? `${(val108/10).toFixed(1)} 萬` : '無資料';
        
        const stat114El = document.getElementById('trend-stat-114');
        stat114El.innerHTML = val114 ? `<span>${(val114/10).toFixed(1)} 萬</span>` : '<span>無資料</span>';
        
        if (val108 && val114 && val108 > 0) {
            const growth = ((val114 - val108) / val108) * 100;
            const growthColor = growth > 0 ? '#10b981' : '#f43f5e';
            const growthSign = growth > 0 ? '▲' : '▼';
            stat114El.innerHTML += `<span id="trend-stat-growth" style="font-size: 0.9rem; color: ${growthColor};">${growthSign} ${Math.abs(growth).toFixed(1)}%</span>`;
        }

        // 更新歷年數據表格
        const historyContainer = document.getElementById('trend-stat-history');
        historyContainer.innerHTML = '';
        const fixedYears = [108, 109, 110, 111, 112, 113, 114];
        fixedYears.forEach(year => {
            const idx = trendData.years.indexOf(year);
            const val = idx !== -1 ? (trendData.medians[idx]/10).toFixed(1) : '-';
            historyContainer.innerHTML += `
                <div style="display: flex; gap: 6px; align-items: baseline; background: rgba(255,255,255,0.05); padding: 4px 8px; border-radius: 4px;">
                    <span style="color: var(--text-secondary); font-size: 0.75rem;">${year}</span>
                    <span style="font-weight: 500;">${val}</span>
                </div>
            `;
        });

        const ctx = document.getElementById("trendChart").getContext("2d");
        
        if (trendChartObj) {
            trendChartObj.destroy();
        }

        const alignedMedians = fixedYears.map(year => {
            const idx = trendData.years.indexOf(year);
            return idx !== -1 ? parseFloat((trendData.medians[idx] / 10).toFixed(1)) : null;
        });

        trendChartObj = new Chart(ctx, {
            type: 'line',
            data: {
                labels: fixedYears,
                datasets: [{
                    label: '薪資中位數 (萬元)',
                    data: alignedMedians,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    pointBackgroundColor: '#10b981',
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    fill: true,
                    tension: 0.2,
                    spanGaps: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 17, 26, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#10b981',
                        padding: 12
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: '年度', color: '#a0aabf' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a0aabf' }
                    },
                    y: {
                        title: { display: true, text: '薪資中位數 (仟元)', color: '#a0aabf' },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#a0aabf' },
                        beginAtZero: false
                    }
                }
            }
        });
    }
});
