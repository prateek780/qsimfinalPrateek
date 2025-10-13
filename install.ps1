# Quantum Networking Simulation - PowerShell Installer Launcher
# This script automatically requests admin privileges and runs the installer

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "  REQUESTING ADMINISTRATOR PRIVILEGES" -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This installer needs admin rights to install software."
    Write-Host "A UAC prompt will appear - please click YES to continue."
    Write-Host ""
    Start-Sleep -Seconds 2
    
    # Relaunch as administrator
    try {
        $scriptPath = $MyInvocation.MyCommand.Path
        Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs
        exit
    }
    catch {
        Write-Host "ERROR: Failed to elevate privileges." -ForegroundColor Red
        Write-Host "Please run this script as administrator manually." -ForegroundColor Yellow
        pause
        exit 1
    }
}

# If we're here, we're running as admin
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  RUNNING WITH ADMINISTRATOR PRIVILEGES" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting installer..."
Write-Host ""
Start-Sleep -Seconds 1

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to script directory
Set-Location $scriptDir

# Run the batch installer
& cmd.exe /c "auto_installer_windows.bat"

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  INSTALLATION SCRIPT COMPLETED" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

