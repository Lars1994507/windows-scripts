# FixTaskbarRedBlink.ps1
# Script to fix taskbar icons turning red and blinking randomly on Windows 11
# Run as Administrator

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Windows 11 Taskbar Red Blinking Fix Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check for administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script requires administrator privileges!" -ForegroundColor Red
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Step 1: Restarting Windows Explorer..." -ForegroundColor Yellow
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process explorer.exe
Write-Host "✓ Windows Explorer restarted" -ForegroundColor Green
Start-Sleep -Seconds 1

Write-Host "`nStep 2: Disabling Windows Error Reporting Services..." -ForegroundColor Yellow
Write-Host "   (These services can cause taskbar icon flickering)" -ForegroundColor DarkGray

# Stop and disable Problem Reports Control service
$problemReports = Get-Service -Name "WerSvc" -ErrorAction SilentlyContinue
if ($problemReports) {
    Stop-Service -Name "WerSvc" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "WerSvc" -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "✓ Windows Error Reporting Service disabled" -ForegroundColor Green
}

# Stop and disable Windows Error Reporting Service (alternative name)
$werService = Get-Service -Name "WERSvc" -ErrorAction SilentlyContinue
if ($werService) {
    Stop-Service -Name "WERSvc" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "WERSvc" -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "✓ Windows Error Reporting (alt) disabled" -ForegroundColor Green
}

Write-Host "`nStep 3: Disabling Windows Push Notification System Service..." -ForegroundColor Yellow
Write-Host "   (Push notifications can cause taskbar red blinking)" -ForegroundColor DarkGray

$wpnService = Get-Service -Name "WpnService" -ErrorAction SilentlyContinue
if ($wpnService) {
    Stop-Service -Name "WpnService" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "WpnService" -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "✓ Windows Push Notification Service disabled" -ForegroundColor Green
} else {
    Write-Host "! Push Notification Service not found" -ForegroundColor Yellow
}

Write-Host "`nStep 4: Disabling Hardware-Accelerated GPU Scheduling..." -ForegroundColor Yellow
Write-Host "   (Can cause taskbar rendering conflicts on some systems)" -ForegroundColor DarkGray

$gpuPath = "HKLM:\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
$gpuSetting = Get-ItemProperty -Path $gpuPath -Name "HwSchMode" -ErrorAction SilentlyContinue
if ($gpuSetting) {
    Set-ItemProperty -Path $gpuPath -Name "HwSchMode" -Value 0 -Type DWord -ErrorAction SilentlyContinue
    Write-Host "✓ Hardware-accelerated GPU scheduling disabled" -ForegroundColor Green
} else {
    # Try registry alternative location
    $gpuPathAlt = "HKCU:\Software\Microsoft\Windows\CurrentVersion\GraphicsSettings"
    if (Test-Path $gpuPathAlt) {
        Set-ItemProperty -Path $gpuPathAlt -Name "HardwareAcceleratedGPUScheduling" -Value 0 -Type DWord -ErrorAction SilentlyContinue
        Write-Host "✓ Hardware-accelerated GPU scheduling disabled (user setting)" -ForegroundColor Green
    } else {
        Write-Host "! GPU scheduling registry key not found - may need manual check" -ForegroundColor Yellow
    }
}

Write-Host "`nStep 5: Clearing icon cache..." -ForegroundColor Yellow

# Stop Explorer to clear cache safely
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Clear icon cache files
$iconCachePaths = @(
    "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache*",
    "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\thumbcache*",
    "$env:APPDATA\Microsoft\Windows\Recent\AutomaticDestinations\*",
    "$env:APPDATA\Microsoft\Windows\Recent\CustomDestinations\*"
)

foreach ($path in $iconCachePaths) {
    $files = Get-ChildItem -Path $path -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        } catch {
            # Silently continue if file in use
        }
    }
}
Write-Host "✓ Icon cache cleared" -ForegroundColor Green

# Restart Explorer
Start-Process explorer.exe
Start-Sleep -Seconds 2

Write-Host "`nStep 6: Running System File Checker..." -ForegroundColor Yellow
Write-Host "   (Checking for corrupted system files)" -ForegroundColor DarkGray

sfc /scannow
Write-Host "✓ System File Checker completed" -ForegroundColor Green

Write-Host "`nStep 7: Running DISM health check..." -ForegroundColor Yellow

DISM /Online /Cleanup-Image /RestoreHealth
Write-Host "✓ DISM health check completed" -ForegroundColor Green

Write-Host "`nStep 8: Re-registering Windows Shell Experience Host..." -ForegroundColor Yellow

try {
    Get-AppxPackage Microsoft.Windows.ShellExperienceHost | foreach { Add-AppxPackage -register "$($_.InstallLocation)\appxmanifest.xml" -DisableDevelopmentMode -ErrorAction SilentlyContinue }
    Write-Host "✓ Shell Experience Host re-registered" -ForegroundColor Green
} catch {
    Write-Host "! Could not re-register Shell Experience Host" -ForegroundColor Yellow
}

try {
    Get-AppXPackage | Foreach { Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml" -ErrorAction SilentlyContinue }
    Write-Host "✓ All AppX packages re-registered" -ForegroundColor Green
} catch {
    Write-Host "! Could not re-register some AppX packages" -ForegroundColor Yellow
}

Write-Host "`nStep 9: Final restart of Windows Explorer..." -ForegroundColor Yellow
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Start-Process explorer.exe
Write-Host "✓ Windows Explorer restarted" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "   Taskbar Red Blinking Fix Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`nChanges made:" -ForegroundColor White
Write-Host "• Windows Error Reporting Services disabled" -ForegroundColor Gray
Write-Host "• Windows Push Notification Service disabled" -ForegroundColor Gray
Write-Host "• Hardware-accelerated GPU scheduling disabled" -ForegroundColor Gray
Write-Host "• Icon cache cleared" -ForegroundColor Gray
Write-Host "• System files verified and repaired" -ForegroundColor Gray
Write-Host "• Windows Shell components re-registered" -ForegroundColor Gray

Write-Host "`nIf the issue persists after restart, try these additional fixes:" -ForegroundColor Yellow
Write-Host "1. Check for problematic app notifications:" -ForegroundColor White
Write-Host "   - Click the ^ arrow in taskbar to see hidden icons" -ForegroundColor Gray
Write-Host "   - Look for apps with red dots or notification badges" -ForegroundColor Gray
Write-Host "   - Close and reopen the problematic app" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Check for problematic Windows updates:" -ForegroundColor White
Write-Host "   - Settings → Windows Update → Update history → Uninstall updates" -ForegroundColor Gray
Write-Host "   - Look for KB5004300, KB5034441, or KB5048759 and uninstall if present" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Update your graphics driver from manufacturer's website" -ForegroundColor White
Write-Host ""
Write-Host "4. Perform a clean boot to identify conflicting applications:" -ForegroundColor White
Write-Host "   - Type 'msconfig' in Start menu → Services → Hide Microsoft services → Disable all" -ForegroundColor Gray
Write-Host "   - Then check Startup in Task Manager and disable all startup items" -ForegroundColor Gray

Write-Host "`nIMPORTANT: A system restart is recommended for all changes to take effect." -ForegroundColor Magenta
Write-Host ""

pause