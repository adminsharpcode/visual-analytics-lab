<#
    Screenshot capture for the Visual Analytics Lab record.

    Captures the Power BI Desktop window (or the full screen) and saves it
    into screenshots\ using the exact filenames the PDF builders look for.

    USAGE
    -----
    Single capture:
        .\capture.ps1 -Step qp1_01_getdata

    Guided run - walks the whole assessment, press Enter at each step:
        .\capture.ps1 -Guided QP1
        .\capture.ps1 -Guided QP2

    List the expected step names:
        .\capture.ps1 -List

    Full screen instead of just the Power BI window:
        .\capture.ps1 -Step qp1_01_getdata -FullScreen
#>
[CmdletBinding()]
param(
    [string]$Step,
    [ValidateSet('QP1', 'QP2')][string]$Guided,
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

# ------------------------------------------------------------ step catalogue
$Steps = [ordered]@{
    # ---- QP1 -------------------------------------------------------------
    'qp1_01_getdata'      = 'QP1 Step 1 - Get data dialog (SQL Server or Text/CSV)'
    'qp1_02_navigator'    = 'QP1 Step 1 - Navigator showing the five tables with preview'
    'qp1_03_raw_preview'  = 'QP1 Step 1 - Raw FactSales preview before cleansing'
    'qp1_04_pq_editor'    = 'QP1 Step 2 - Power Query Editor with the query list'
    'qp1_05_applied_steps'= 'QP1 Step 2 - Applied Steps pane after all cleansing steps'
    'qp1_06_advanced_ed'  = 'QP1 Step 2 - Advanced Editor showing the M script'
    'qp1_07_clean_preview'= 'QP1 Step 2 - Cleansed FactSales preview (5,013 rows)'
    'qp1_08_model_view'   = 'QP1 Step 3 - Model view showing the star schema'
    'qp1_09_relationship' = 'QP1 Step 3 - Edit relationship dialog / Manage relationships'
    'qp1_10_properties'   = 'QP1 Step 3 - Column properties pane (format, summarisation, hidden)'
    'qp1_11_sort_by'      = 'QP1 Step 3 - Sort by column set on MonthName'
    'qp1_12_hierarchies'  = 'QP1 Step 3 - Fields pane showing the four hierarchies'
    # ---- QP2 -------------------------------------------------------------
    'qp2_01_new_column'   = 'QP2 Step 4 - New calculated column in the formula bar'
    'qp2_02_measures'     = 'QP2 Step 4 - Measures created in the Fields pane'
    'qp2_03_core_kpis'    = 'QP2 Step 4 - Card visuals showing the core measure values'
    'qp2_04_top_product'  = 'QP2 Step 4 - Top sold product result'
    'qp2_05_category_avg' = 'QP2 Step 4 - Average sales by product category table'
    'qp2_06_calc_table'   = 'QP2 Step 4 - Calculated table (Product Category Summary)'
    'qp2_07_calculate'    = 'QP2 Step 5 - CALCULATE measure and its result'
    'qp2_08_time_intel'   = 'QP2 Step 5 - Time Intelligence measures (YTD, PY)'
    'qp2_09_yoy_matrix'   = 'QP2 Step 5 - Matrix with Total Sales, Sales PY, YoY Growth %'
    'qp2_10_report_p1'    = 'QP2 Step 6 - Report Page 1 Sales Overview'
    'qp2_11_report_p2'    = 'QP2 Step 6 - Report Page 2 Category and Time Analysis'
    'qp2_12_publish'      = 'QP2 Step 6 - Publish dialog with workspace selection'
    'qp2_13_success'      = 'QP2 Step 6 - Success confirmation with report link'
    'qp2_14_service'      = 'QP2 Step 6 - Published report open at app.powerbi.com'
}

if ($List) {
    Write-Host ''
    Write-Host 'Expected screenshot step names' -ForegroundColor Cyan
    Write-Host ('-' * 78)
    foreach ($k in $Steps.Keys) {
        $exists = Test-Path (Join-Path $ShotDir "$k.png")
        $mark = if ($exists) { '[captured]' } else { '[  todo  ]' }
        $col = if ($exists) { 'Green' } else { 'DarkGray' }
        Write-Host ("{0} {1,-22} {2}" -f $mark, $k, $Steps[$k]) -ForegroundColor $col
    }
    Write-Host ''
    return
}

# ------------------------------------------------------------ win32 interop
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
    public static extern bool ShowWindow(IntPtr hWnd, int n);
    [DllImport("user32.dll")]
    public static extern bool IsIconic(IntPtr hWnd);
}
'@
}

function Get-PowerBIWindow {
    Get-Process PBIDesktop -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowTitle -and $_.MainWindowHandle -ne 0 } |
        Select-Object -First 1
}

function Invoke-Capture {
    param([string]$Name, [string]$Desc)

    $path = Join-Path $ShotDir "$Name.png"

    if ($DelaySeconds -gt 0) {
        Write-Host "  waiting $DelaySeconds s..." -ForegroundColor DarkGray
        Start-Sleep -Seconds $DelaySeconds
    }

    $bounds = $null
    if (-not $FullScreen) {
        $proc = Get-PowerBIWindow
        if ($proc) {
            $h = $proc.MainWindowHandle
            if ([Win32Cap]::IsIconic($h)) { [Win32Cap]::ShowWindow($h, 9) | Out-Null }
            [Win32Cap]::SetForegroundWindow($h) | Out-Null
            Start-Sleep -Milliseconds 700
            $r = New-Object Win32Cap+RECT
            if ([Win32Cap]::GetWindowRect($h, [ref]$r)) {
                $w = $r.Right - $r.Left
                $ht = $r.Bottom - $r.Top
                if ($w -gt 200 -and $ht -gt 200) {
                    $bounds = New-Object System.Drawing.Rectangle($r.Left, $r.Top, $w, $ht)
                }
            }
        }
        else {
            Write-Host '  Power BI Desktop window not found - capturing full screen' -ForegroundColor Yellow
        }
    }
    if (-not $bounds) {
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    }

    $bmp = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $g.Dispose()
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $kb = [math]::Round((Get-Item $path).Length / 1KB)
    $bmp.Dispose()

    Write-Host ("  saved {0}  ({1}x{2}, {3} KB)" -f "screenshots\$Name.png",
        $bounds.Width, $bounds.Height, $kb) -ForegroundColor Green
}

# ------------------------------------------------------------ single
if ($Step) {
    if (-not $Steps.Contains($Step)) {
        Write-Host "Unknown step '$Step'. Run .\capture.ps1 -List" -ForegroundColor Red
        return
    }
    Write-Host ''
    Write-Host $Steps[$Step] -ForegroundColor Cyan
    Invoke-Capture -Name $Step -Desc $Steps[$Step]
    Write-Host ''
    return
}

# ------------------------------------------------------------ guided
if ($Guided) {
    $prefix = $Guided.ToLower()
    $keys = @($Steps.Keys | Where-Object { $_ -like "$prefix*" })

    Write-Host ''
    Write-Host "GUIDED CAPTURE - $Guided  ($($keys.Count) screenshots)" -ForegroundColor Cyan
    Write-Host ('=' * 78)
    Write-Host 'Set up each state in Power BI Desktop, then press Enter here.'
    Write-Host 'Press S to skip a step, Q to quit.' -ForegroundColor DarkGray
    Write-Host ('=' * 78)

    $i = 0
    foreach ($k in $keys) {
        $i++
        Write-Host ''
        Write-Host ("[{0}/{1}] {2}" -f $i, $keys.Count, $k) -ForegroundColor Yellow
        Write-Host ("        {0}" -f $Steps[$k])
        if (Test-Path (Join-Path $ShotDir "$k.png")) {
            Write-Host '        (already captured - Enter overwrites)' -ForegroundColor DarkGray
        }
        $ans = Read-Host '        Enter=capture  S=skip  Q=quit'
        if ($ans -match '^[Qq]') { Write-Host 'Stopped.' -ForegroundColor Yellow; break }
        if ($ans -match '^[Ss]') { Write-Host '        skipped' -ForegroundColor DarkGray; continue }
        Invoke-Capture -Name $k -Desc $Steps[$k]
    }

    $done = @($keys | Where-Object { Test-Path (Join-Path $ShotDir "$_.png") }).Count
    Write-Host ''
    Write-Host ('=' * 78)
    Write-Host ("$Guided captured: $done / $($keys.Count)") -ForegroundColor Cyan
    Write-Host 'Now rebuild the PDFs:' -ForegroundColor Cyan
    Write-Host '    python _04_build_qp1.py'
    Write-Host '    python _04_build_qp2.py'
    Write-Host ''
    return
}

Write-Host ''
Write-Host 'Nothing to do. Try:' -ForegroundColor Yellow
Write-Host '    .\capture.ps1 -List'
Write-Host '    .\capture.ps1 -Guided QP1'
Write-Host '    .\capture.ps1 -Step qp1_08_model_view'
Write-Host ''
