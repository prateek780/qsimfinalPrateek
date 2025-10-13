@echo off
echo Starting Student Snapshot Watcher
echo.
echo Usage: start_snapshot_watcher.bat student_id [interval_seconds]
echo Example: start_snapshot_watcher.bat alice 10
echo.

if "%1"=="" (
    echo ERROR: Please provide student_id
    echo Example: start_snapshot_watcher.bat alice
    exit /b 1
)

set STUDENT_ID=%1
set INTERVAL=%2
if "%INTERVAL%"=="" set INTERVAL=10

echo Watching code changes for: %STUDENT_ID%
echo Snapshot interval: %INTERVAL% seconds
echo.
echo Press Ctrl+C to stop watching
echo.

python watch_student_changes.py %STUDENT_ID% %INTERVAL%

