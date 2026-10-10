<#
    =============================================================================
    Visual Analytics Lab (MACSE603) - Assessments 3 to 8
    Automated Screenshot Capture Utility
    Author: Vedant Nimkar | Reg No: 26MML0045
    =============================================================================

    USAGE:
    ------
    1. List all required screenshots:
       .\capture_qp3_to_qp8.ps1 -List

    2. Capture a single window (Power BI, Browser, or Terminal):
       .\capture_qp3_to_qp8.ps1 -Step qp3_01_slicers
       .\capture_qp3_to_qp8.ps1 -Step qp3_05_service_dashboard

    3. Full-screen capture:
       .\capture_qp3_to_qp8.ps1 -Step qp3_01_slicers -FullScreen

    4. Guided interactive run (walks through an assessment step by step):
       .\capture_qp3_to_qp8.ps1 -Guided QP3
       .\capture_qp3_to_qp8.ps1 -Guided QP4
       .\capture_qp3_to_qp8.ps1 -Guided QP5
       .\capture_qp3_to_qp8.ps1 -Guided QP8
       .\capture_qp3_to_qp8.ps1 -Guided QP7
#>
[CmdletBinding()]
param(
    [string]$Step,
    [ValidateSet('QP3', 'QP4', 'QP5', 'QP7', 'QP8')][string]$Guided,
    [switch]$FullScreen,
    [switch]$List,
    [int]$DelaySeconds = 0
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ShotDir = Join-Path $Root 'screenshots'
if (-not (Test-Path $ShotDir)) { New-Item -ItemType Directory -Path $ShotDir | Out-Null }

# Catalogue of All Screenshots for Assessments 3 to 8
$Steps = [ordered]@{
    # ---- Assessment 3 (QP3) ------------------------------------------------
    'qp3_01_slicers'          = 'QP3 Exp 7 - Power BI Desktop with Date & Category Slicers filtering report'
    'qp3_02_drilldown'        = 'QP3 Exp 7 - Power BI Desktop Drill-down on Category -> Subcategory hierarchy'
    'qp3_03_decomp_tree'      = 'QP3 Exp 7 - Power BI Desktop Decomposition Tree AI visual breakdown'
    'qp3_04_publish_pro'      = 'QP3 Exp 8 - Power BI Desktop Publish dialog to Power BI Pro workspace'
    'qp3_05_service_dashboard'= 'QP3 Exp 8 - Power BI Service (app.powerbi.com) Dashboard with pinned tiles'
    'qp3_06_collaboration'    = 'QP3 Exp 8 - Power BI Service Comments & @mentions collaboration pane'
    'qp3_07_data_alert'       = 'QP3 Exp 8 - Power BI Service Manage Alerts panel on Revenue card'
    'qp3_08_html_dashboard'   = 'QP3 Exp 9 - HTML5 & CSS modern dark-mode Visual Analytics Dashboard'

    # ---- Assessment 4 (QP4) ------------------------------------------------
    'qp4_01_flask_run'        = 'QP4 Exp 11 - PowerShell running Flask API app.py on port 5000'
    'qp4_02_api_json'         = 'QP4 Exp 11 - Browser / Postman showing /api/kpis or /api/sales/monthly JSON'
    'qp4_03_echarts_line'     = 'QP4 Exp 10 - Apache ECharts Time-Series Line Chart with DataZoom'
    'qp4_04_echarts_bar'      = 'QP4 Exp 10 - Apache ECharts Category Revenue & Profit Bar Chart'
    'qp4_05_echarts_donut'    = 'QP4 Exp 10 - Apache ECharts Donut & Scatter Bubble Charts'

    # ---- Assessment 5 (QP5) ------------------------------------------------
    'qp5_01_integrated_dash'  = 'QP5 Exp 12 - Integrated Dashboard with dynamic filters & drill-down'
    'qp5_02_streamlit_home'   = 'QP5 Exp 13 - Streamlit Multipage App Home landing page'
    'qp5_03_streamlit_kpis'   = 'QP5 Exp 13 - Streamlit Executive KPIs page with interactive multiselect'
    'qp5_04_streamlit_subcat' = 'QP5 Exp 13 - Streamlit Category Deep Dive with subcategory drilldown'

    # ---- Assessment 8 (QP8) ------------------------------------------------
    'qp8_01_docker_compose'   = 'QP8 Exp 14 - Terminal showing docker-compose up -d --build output'
    'qp8_02_docker_ps'        = 'QP8 Exp 14 - Terminal showing docker ps with healthy containers'
    'qp8_03_docker_push'      = 'QP8 Exp 14 - Terminal showing push_to_registry.ps1 Docker Hub push'

    # ---- Assessment 7 (QP7) ------------------------------------------------
    'qp7_01_k8s_apply'        = 'QP7 Exp 15 - Terminal showing kubectl apply -f . manifest creation'
    'qp7_02_k8s_pods'         = 'QP7 Exp 15 - Terminal showing kubectl get pods -n visual-analytics'
    'qp7_03_k8s_service_dns'  = 'QP7 Exp 15 - Terminal showing kubectl get svc and describe sql-db-service'
}

if ($List) {
    Write-Host "`nVisual Analytics Lab - Required Screenshots Catalog (Assessments 3-8)" -ForegroundColor Cyan
    Write-Host ('-' * 85)
    foreach ($k in $Steps.Keys) {
        $exists = (Test-Path (Join-Path $ShotDir "$k.png")) -or (Test-Path (Join-Path $Root "figures\$k.png"))
        $mark = if ($exists) { '[READY] ' } else { '[TODO]  ' }
        $col = if ($exists) { 'Green' } else { 'DarkGray' }
        Write-Host ("{0} {1,-26} {2}" -f $mark, $k, $Steps[$k]) -ForegroundColor $col
    }
    Write-Host ""
    return
}

# Win32 Interop to capture active window
if (-not ('Win32Cap' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class Win32Cap {
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
}
'@
}

function Snap-Window([string]$SavePath, [bool]$Full) {
    Start-Sleep -Milliseconds 400
    if ($Full) {
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        $bmp.Save($SavePath, [System.Drawing.Imaging.ImageFormat]::Png)
        $g.Dispose(); $bmp.Dispose()
        return
    }

    $hwnd = [Win32Cap]::GetForegroundWindow()
    $r = New-Object Win32Cap+RECT
    [Win32Cap]::GetWindowRect($hwnd, [ref]$r) | Out-Null
    $w = $r.Right - $r.Left
    $h = $r.Bottom - $r.Top
    if ($w -le 10 -or $h -le 10) {
        Snap-Window $SavePath $true
        return
    }
    $bmp = New-Object System.Drawing.Bitmap $w, $h
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.Left, $r.Top, 0, 0, (New-Object System.Drawing.Size($w, $h)))
    $bmp.Save($SavePath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
}

# Execution
if ($Step) {
    if (-not $Steps.ContainsKey($Step)) {
        Write-Warning "Unknown step '$Step'. Use -List to view catalogue."
        return
    }
    if ($DelaySeconds -gt 0) {
        Write-Host "Waiting $DelaySeconds seconds... switch to target window now!" -ForegroundColor Yellow
        Start-Sleep -Seconds $DelaySeconds
    }
    $targetFile = Join-Path $ShotDir "$Step.png"
    Snap-Window -SavePath $targetFile -Full $FullScreen
    Write-Host "Captured: $targetFile" -ForegroundColor Green
}
elseif ($Guided) {
    Write-Host "`nStarting Guided Screenshot Capture for: $Guided" -ForegroundColor Cyan
    $filterPrefix = $Guided.ToLower()
    foreach ($k in $Steps.Keys) {
        if ($k.StartsWith($filterPrefix)) {
            Write-Host "`nTarget: $($Steps[$k])" -ForegroundColor Yellow
            Write-Host "Position target window on screen and press ENTER to capture (or 's' to skip)..." -ForegroundColor White -NoNewline
            $ans = Read-Host
            if ($ans -ne 's') {
                $targetFile = Join-Path $ShotDir "$k.png"
                Snap-Window -SavePath $targetFile -Full $FullScreen
                Write-Host "-> Saved $k.png" -ForegroundColor Green
            }
        }
    }
    Write-Host "`nGuided capture completed for $Guided!" -ForegroundColor Cyan
}
