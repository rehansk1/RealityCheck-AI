@echo off
title RealityCheck AI Launcher

echo ================================
echo     Starting RealityCheck AI
echo ================================
echo.

REM Start Backend
start "Backend" cmd /k "cd /d %~dp0backend && call venv\Scripts\activate && uvicorn app.main:app --reload"

REM Wait for backend
timeout /t 5 >nul

REM Start Frontend
start "Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

REM Wait for Vite
timeout /t 5 >nul

REM Open Browser
start http://localhost:5173

echo.
echo RealityCheck AI Started Successfully!
pause