@echo off
title Reset Self-Aware AI Agent
echo Reset Self-Aware AI Agent
echo =========================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Change to parent directory (project root)
cd ..\

REM Run the reset script
echo Resetting agent...
python scripts\reset.py

pause