# generate_all.ps1 - Top 50 UX/UI Design Style Demo Generator
# Usage: pwsh -File generate_all.ps1 -ProjectRoot <path>

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectRoot
)

$ErrorActionPreference = "Stop"
$OutputDir = Join-Path $ProjectRoot "top50-demos"
$DataFile = Join-Path $PSScriptRoot "styles_data.json"

# Load styles data
$styles = Get-Content $DataFile -Raw -Encoding UTF8 | ConvertFrom-Json

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host "=== Top 50 UX/UI Demo Generator ===" -ForegroundColor Cyan
Write-Host "Output: $OutputDir" -ForegroundColor Gray

# ============================================================
# INDEX PAGE
# ============================================================
Write-Host "Generating index.html..." -ForegroundColor Yellow

$catColors = @{
    "極簡與結構化設計" = "#6366f1"
    "3D、空間與沉浸式設計" = "#06b6d4"
    "復古、懷舊與文化符號轉譯" = "#f59e0b"
    "AI 生成、動態與微互動體驗" = "#10b981"
    "特殊材質、反叛與情感化設計" = "#ef4444"
}

$catIcons = @{
    "極簡與結構化設計" = "🏗️"
    "3D、空間與沉浸式設計" = "🌐"
    "復古、懷舊與文化符號轉譯" = "🎨"
    "AI 生成、動態與微互動體驗" = "🤖"
    "特殊材質、反叛與情感化設計" = "⚡"
}

$cards = ""
foreach ($s in $styles) {
    $color = $catColors[$s.cat]
    $icon = $catIcons[$s.cat]
    $cards += @"
        <a href="$($s.id).html" class="card" style="--accent:$color">
            <span class="card-num">$($s.id)</span>
            <span class="card-icon">$icon</span>
            <h3>$($s.en)</h3>
            <p>$($s.zh)</p>
            <span class="card-cat">$($s.cat)</span>
        </a>
"@
}

$indexHtml = @"
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Top 50 UX/UI 設計風格範例集</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Noto+Sans+TC:wght@300;400;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter','Noto Sans TC',sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh}
.hero{text-align:center;padding:80px 20px 40px;background:linear-gradient(135deg,#0a0a1a 0%,#1a1a3a 50%,#0a0a1a 100%)}
.hero h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;background:linear-gradient(135deg,#6366f1,#06b6d4,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}
.hero p{font-size:1.1rem;color:#888;max-width:600px;margin:0 auto}
.legend{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;padding:20px;max-width:1200px;margin:0 auto}
.legend-item{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#aaa}
.legend-dot{width:12px;height:12px;border-radius:50%}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;padding:20px;max-width:1200px;margin:0 auto}
.card{display:flex;flex-direction:column;padding:24px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:16px;text-decoration:none;color:#e0e0e0;transition:all .3s ease;position:relative;overflow:hidden}
.card:hover{transform:translateY(-4px);border-color:var(--accent);box-shadow:0 8px 32px rgba(0,0,0,.3),0 0 0 1px var(--accent)}
.card-num{position:absolute;top:12px;right:16px;font-size:2.5rem;font-weight:800;opacity:.1;color:var(--accent)}
.card-icon{font-size:1.5rem;margin-bottom:8px}
.card h3{font-size:1rem;font-weight:600;margin-bottom:4px}
.card p{font-size:.85rem;color:#888;margin-bottom:8px}
.card-cat{font-size:.7rem;color:var(--accent);border:1px solid;border-radius:20px;padding:2px 10px;align-self:flex-start;opacity:.7}
footer{text-align:center;padding:40px;color:#555;font-size:.85rem}
</style>
</head>
<body>
<div class="hero">
<h1>🎯 Top 50 UX/UI 設計風格</h1>
<p>2025-2026 全球主流設計風格的互動範例集，涵蓋五大分類、50 種風格</p>
</div>
<div class="legend">
<div class="legend-item"><div class="legend-dot" style="background:#6366f1"></div>極簡與結構化</div>
<div class="legend-item"><div class="legend-dot" style="background:#06b6d4"></div>3D 與沉浸式</div>
<div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div>復古與文化</div>
<div class="legend-item"><div class="legend-dot" style="background:#10b981"></div>AI 與動態</div>
<div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>材質與反叛</div>
</div>
<div class="grid">
$cards
</div>
<footer>Top 50 UX/UI Design Style Demos &copy; 2026</footer>
</body>
</html>
"@

Set-Content -Path (Join-Path $OutputDir "index.html") -Value $indexHtml -Encoding UTF8
Write-Host "  ✅ index.html" -ForegroundColor Green

# ============================================================
# INDIVIDUAL STYLE PAGES - generate via template + style-specific CSS/content
# ============================================================

# Navigation helper
function Get-Nav($id, $total) {
    $num = [int]$id
    $prev = if ($num -gt 1) { "{0:D2}" -f ($num - 1) } else { "" }
    $next = if ($num -lt $total) { "{0:D2}" -f ($num + 1) } else { "" }
    $prevLink = if ($prev) { "<a href='$prev.html' class='nav-btn'>← 上一頁</a>" } else { "<span></span>" }
    $nextLink = if ($next) { "<a href='$next.html' class='nav-btn'>下一頁 →</a>" } else { "<span></span>" }
    return @"
<nav class="page-nav">$prevLink<a href="index.html" class="nav-btn nav-home">🏠 回首頁</a>$nextLink</nav>
"@
}

$navCSS = @"
.page-nav{display:flex;justify-content:space-between;align-items:center;padding:16px 24px;position:fixed;bottom:0;left:0;right:0;z-index:9999;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.nav-btn{text-decoration:none;padding:8px 20px;border-radius:8px;font-size:.9rem;transition:all .2s}
"@

Write-Host "Generating style pages..." -ForegroundColor Yellow

foreach ($s in $styles) {
    $num = [int]$s.id
    $nav = Get-Nav $s.id 50
    $file = Join-Path $OutputDir "$($s.id).html"
    $html = $null

    # Each case builds a unique HTML demo
    switch ($num) {
        # NOTE: Due to script size, we call sub-generators
        default {
            # Template-based generation with style-specific customization
            $html = & "$PSScriptRoot\generate_style.ps1" -StyleId $s.id -StyleEn $s.en -StyleZh $s.zh -StyleCat $s.cat -NavHtml $nav -NavCSS $navCSS
        }
    }

    if ($html) {
        Set-Content -Path $file -Value $html -Encoding UTF8
        Write-Host "  ✅ $($s.id).html - $($s.en)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== Generation Complete! ===" -ForegroundColor Cyan
Write-Host "Open top50-demos/index.html to browse all demos." -ForegroundColor Gray
