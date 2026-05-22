# FixAltTab.ps1
# Script to fix Alt+Tab not working on Windows 11



# Run as Administrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Windows 11 Alt+Tab Fix Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
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
Write-Host "Windows Explorer restarted" -ForegroundColor Green
Start-Sleep -Seconds 1

Write-Host ""
Write-Host "Step 2: Resetting Alt+Tab settings in Registry..." -ForegroundColor Yellow

# Backup current AltTab settings
$backupFile = "$env:TEMP\AltTab_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').reg"
try {
    reg export "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer" $backupFile /y 2>$null
    Write-Host "Backup created at: $backupFile" -ForegroundColor Green
}
catch {
    Write-Host "Could not create backup (non-critical)" -ForegroundColor Yellow
}

# Reset AltTabSettings
$altTabPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer"
Set-ItemProperty -Path $altTabPath -Name "AltTabSettings" -Value 1 -Type DWord -ErrorAction SilentlyContinue
Write-Host "AltTabSettings reset to default (1)" -ForegroundColor Green

# Reset MultitaskingViewSettings
$multiTaskPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\MultitaskingView"
if (!(Test-Path $multiTaskPath)) {
    New-Item -Path $multiTaskPath -Force | Out-Null
}
Set-ItemProperty -Path $multiTaskPath -Name "AltTabSettings" -Value 1 -Type DWord -ErrorAction SilentlyContinue
Write-Host "MultitaskingView AltTabSettings reset" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Clearing stuck modifier keys..." -ForegroundColor Yellow

# Use SendKeys to release keys (simpler, no C# needed)
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.SendKeys]::SendWait("{ALT up}")
[System.Windows.Forms.SendKeys]::SendWait("{CTRL up}")
[System.Windows.Forms.SendKeys]::SendWait("{LWIN up}")
[System.Windows.Forms.SendKeys]::SendWait("{RWIN up}")
Write-Host "Stuck modifier keys released" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Restarting Touch Keyboard service..." -ForegroundColor Yellow
try {
    Stop-Service "TabletInputService" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Start-Service "TabletInputService" -ErrorAction SilentlyContinue
    Write-Host "TabletInputService restarted" -ForegroundColor Green
}
catch {
    Write-Host "Could not restart TabletInputService (non-critical)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 5: Resetting Focus Assist settings..." -ForegroundColor Yellow
try {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default`$windows.data.notifications.quiethours\windows.data.notifications.quiethours" -Name "Data" -Value $null -ErrorAction SilentlyContinue
    Write-Host "Focus Assist cache cleared" -ForegroundColor Green
}
catch {
    Write-Host "Focus Assist reset skipped (non-critical)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 6: Refreshing policy settings..." -ForegroundColor Yellow
try {
    gpupdate /target:user /force 2>$null | Out-Null
    Write-Host "Group policy refreshed" -ForegroundColor Green
}
catch {
    Write-Host "Group policy refresh skipped (non-critical)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 7: Final restart of Explorer..." -ForegroundColor Yellow
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process explorer.exe
Write-Host "Windows Explorer restarted" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Alt+Tab Fix Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "If Alt+Tab is still not working, try:" -ForegroundColor Yellow
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Check for Windows updates" -ForegroundColor White
Write-Host "3. Run System File Checker: sfc /scannow" -ForegroundColor White
Write-Host "4. Check third-party overlay software" -ForegroundColor White
Write-Host ""

pause