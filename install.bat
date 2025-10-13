@echo off
REM Simple launcher that runs PowerShell script with admin privileges
REM This allows running with one command from Cursor terminal

echo ========================================================================
echo   LAUNCHING INSTALLER WITH ADMIN PRIVILEGES
echo ========================================================================
echo.
echo This will open a new window with administrator privileges.
echo Please click YES on the UAC prompt that appears.
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to launch installer
    echo Please run as administrator manually
    pause
)

