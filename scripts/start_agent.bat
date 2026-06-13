@echo off
title Self-Aware AI Agent
echo Self-Aware AI Agent Startup
echo ==========================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if Ollama is available
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is not installed or not in PATH
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)

REM Change to parent directory (project root)
cd ..\n
REM Start the agent server
echo Starting agent server...
python agent_server.py

pause