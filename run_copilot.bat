@echo off
REM --- Check if the script is running with administrative privileges ---
openfiles >nul 2>&1
if '%errorlevel%' neq '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM --- The script now has admin privileges. ---
REM === CRITICAL FIX: Change directory to the script's location ===
cd /D "%~dp0"

echo.
echo ===============================
echo   AI Copilot -- Running as Admin 
echo   Working Directory: %cd%
echo ===============================
echo.

REM --- Launch GeneXus before starting the Copilot GUI ---
start "" "C:\Program Files (x86)\Artech\GeneXus\GeneXusXEv3\Genexus.exe"

echo Starting the automator...
python main.py

echo.
echo Copilot execution finished.
pause