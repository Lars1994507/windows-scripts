# FixRedWindowsAndTaskbarContext.ps1
# Run as Administrator for best results

Write-Host "Fixing red windows and taskbar right-click issue on Windows 11..." -ForegroundColor Cyan

# 1. Kill and restart Explorer (refreshes taskbar + window chrome)
Write-Host "Restarting Windows Explorer..." -ForegroundColor Yellow
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 2. Restart the Taskbar experience (Win11 specific)
Write-Host "Restarting Taskbar services..." -ForegroundColor Yellow
Get-Process "StartMenuExperienceHost" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process "SearchHost" -ErrorAction SilentlyContinue | Stop-Process -Force

# 3. Reset color settings to system default (fixes red borders)
Write-Host "Resetting color and theme preferences..." -ForegroundColor Yellow

# Force re-apply current theme without red tint
try {
    # Disable any accidental high-contrast or custom accent color that forces red
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\DWM" -Name "AccentColor" -Value "" -ErrorAction SilentlyContinue
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\DWM" -Name "ColorizationColor" -Value "" -ErrorAction SilentlyContinue
    
    # Trigger a theme refresh by toggling color auto-detection
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    Set-ItemProperty -Path $regPath -Name "ColorPrevalence" -Value 1 -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
    Set-ItemProperty -Path $regPath -Name "ColorPrevalence" -Value 0 -ErrorAction SilentlyContinue
}
catch {
    Write-Host "Note: Could not modify color registry (non-critical)." -ForegroundColor DarkYellow
}

# 4. Refresh DWM (Desktop Window Manager) to apply color changes
Write-Host "Refreshing Desktop Window Manager..." -ForegroundColor Yellow
Get-Process "dwm" -ErrorAction SilentlyContinue | ForEach-Object {
    # DO NOT kill dwm directly – it will black screen temporarily.
    # Instead, force a DWM restart via theme change
    $null = [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
    [Microsoft.Win32.SystemEvents]::UserPreferenceChanged.Invoke($null, [Microsoft.Win32.UserPreferenceCategory]::Color)
}

# 5. Final Explorer restart to ensure everything is fresh
Write-Host "Final restart of Windows Shell..." -ForegroundColor Yellow
Start-Process "explorer.exe"
Start-Sleep -Seconds 3

Write-Host "`nFix applied. Testing if issues persist:" -ForegroundColor Green
Write-Host "- Open any folder/Window – title bar/borders should NOT be red now." -ForegroundColor White
Write-Host "- Right-click any icon on your taskbar – context menu SHOULD appear." -ForegroundColor White
Write-Host "- If still red, change Personalization > Colors > Accent color manually once." -ForegroundColor Gray