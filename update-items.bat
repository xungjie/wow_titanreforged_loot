@echo off
REM WoW Loot Database - Update Script for Windows
REM Fetches the latest item data from WclBox

echo.
echo ========================================
echo  WoW Loot Database - Update Items
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo.
    echo Please download and install Node.js from:
    echo https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Change to scripts directory
cd /d "%~dp0scripts"

echo Starting item fetch from WclBox...
echo This may take several minutes on first run.
echo.

REM Run the fetch script
node fetch-items-from-wclbox.js

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Fetch failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Update Complete!
echo ========================================
echo.
echo You can now close this window and open index.html in your browser.
echo.
pause
