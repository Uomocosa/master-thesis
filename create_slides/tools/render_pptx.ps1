# Renders every slide of a .pptx to PNG using PowerPoint COM automation.
# Usage: powershell -File render_pptx.ps1 -PptxPath <file.pptx> [-OutDir <dir>]
param(
    [Parameter(Mandatory = $true)][string]$PptxPath,
    [string]$OutDir = ""
)

$PptxPath = (Resolve-Path $PptxPath).Path
if ($OutDir -eq "") {
    $OutDir = Join-Path (Split-Path $PptxPath) "renders"
}
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path

$powerpoint = New-Object -ComObject PowerPoint.Application
try {
    $presentation = $powerpoint.Presentations.Open($PptxPath, $true, $true, $false)
    $baseName = [IO.Path]::GetFileNameWithoutExtension($PptxPath)
    foreach ($slide in $presentation.Slides) {
        $outFile = Join-Path $OutDir ("{0}_slide{1:d2}.png" -f $baseName, $slide.SlideIndex)
        $slide.Export($outFile, "PNG", 1920, 1080)
        Write-Output $outFile
    }
    $presentation.Close()
}
finally {
    $powerpoint.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($powerpoint) | Out-Null
}
