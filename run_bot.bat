@echo off
echo ===============================================
echo    COC Attack Bot - Windows Launcher
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show pyautogui >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo Starting COC Attack Bot...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo Bot exited with error code %errorlevel%
    echo Check the logs folder for more information
)

echo.
echo Bot has stopped.
pause 