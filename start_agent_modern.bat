@echo off
title Self-Aware AI Agent - Modern
echo Self-Aware AI Agent - Modern Startup
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Choose startup mode:
echo 1. Web Server Mode (default)
echo 2. Interactive CLI Mode
echo 3. Autonomous Mode
echo 4. Heartbeat Mode
echo.

set /p choice="Enter choice (1-4, default=1): "

if "%choice%"=="2" (
    echo Starting interactive CLI mode...
    python -m agent.main --mode interactive
) else if "%choice%"=="3" (
    echo Starting autonomous mode...
    python -m agent.main --mode autonomous
) else if "%choice%"=="4" (
    echo Starting heartbeat mode...
    python -m agent.main --mode heartbeat
) else (
    echo Starting web server...
    python agent_server.py
)

pause