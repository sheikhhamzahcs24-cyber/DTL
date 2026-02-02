@echo off
echo ===================================================
echo   Mental Health Companion - One Click Start
echo ===================================================

echo 1. Starting Backend Server (Port 8000)...
start "Backend API" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

echo 2. Starting Frontend Server (Port 5500)...
start "Frontend Website" cmd /k "cd frontend && python -m http.server 5500"

echo 3. Opening Browser...
timeout /t 3 >nul
explorer "http://localhost:5500"

echo.
echo ===================================================
echo   System Running!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5500
echo.
echo   Do not close the pop-up windows.
echo ===================================================
pause
