<#
.SYNOPSIS
    將 1024x1024 的正方形卡片主圖裁切為目標長寬比。

.DESCRIPTION
    CardGen 後處理腳本。接受 AI 生成的 1024x1024 正方形 PNG，
    依卡片類型置中裁切為直式 (5:7) 或橫式 (8.56:5.4)。

.PARAMETER InputPath
    原始 1024x1024 圖片的絕對路徑。

.PARAMETER OutputPath
    裁切後圖片的輸出絕對路徑。

.PARAMETER Orientation
    卡片方向：'portrait'（直式，5:7）或 'landscape'（橫式，信用卡比例）。

.EXAMPLE
    .\crop_card.ps1 -InputPath ".\images\cb_007.png" -OutputPath ".\images\cb_007_cropped.png" -Orientation portrait
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,
    [Parameter(Mandatory = $true)]
    [ValidateSet('portrait', 'landscape')]
    [string]$Orientation
)

Add-Type -AssemblyName System.Drawing

$source = [System.Drawing.Image]::FromFile((Resolve-Path $InputPath).Path)
$srcWidth = $source.Width
$srcHeight = $source.Height

if ($Orientation -eq 'portrait') {
    [int]$targetWidth = [math]::Round($srcHeight * 5 / 7)
    [int]$targetHeight = $srcHeight
    [int]$cropX = [math]::Round(($srcWidth - $targetWidth) / 2)
    [int]$cropY = 0
}
else {
    [int]$targetWidth = $srcWidth
    [int]$targetHeight = [math]::Round($srcWidth * 5.4 / 8.56)
    [int]$cropX = 0
    [int]$cropY = [math]::Round(($srcHeight - $targetHeight) / 2)
}

Write-Host "Source: ${srcWidth}x${srcHeight}"
Write-Host "Target: ${targetWidth}x${targetHeight} ($Orientation)"
Write-Host "Crop offset: X=$cropX, Y=$cropY"

$cropRect = New-Object System.Drawing.Rectangle($cropX, $cropY, $targetWidth, $targetHeight)
$cropped = New-Object System.Drawing.Bitmap($targetWidth, $targetHeight)
$graphics = [System.Drawing.Graphics]::FromImage($cropped)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

$destRect = New-Object System.Drawing.Rectangle(0, 0, $targetWidth, $targetHeight)
$graphics.DrawImage($source, $destRect, $cropRect, [System.Drawing.GraphicsUnit]::Pixel)

$outputDir = Split-Path $OutputPath -Parent
if ($outputDir -and (-not (Test-Path $outputDir))) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $resolvedOutput = $OutputPath
}
else {
    $resolvedOutput = Join-Path (Get-Location) $OutputPath
}

$cropped.Save($resolvedOutput, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$cropped.Dispose()
$source.Dispose()

Write-Host "Cropped image saved to: $resolvedOutput"
