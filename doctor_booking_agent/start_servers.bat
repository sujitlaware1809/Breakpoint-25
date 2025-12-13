@echo off
echo Starting Doctor Booking System...
echo.
echo [1/2] Starting Flask Backend on port 5000...
start "Flask Backend" cmd /k "cd /d %~dp0 && ..\venv\Scripts\python.exe hospital_api.py"
timeout /t 3 /nobreak > nul

echo [2/2] Starting Next.js Frontend on port 3000...
cd frontend
start "Next.js Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo Flask Backend: http://localhost:5000
echo Next.js Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to stop all servers...
pause > nul

taskkill /FI "WindowTitle eq Flask Backend*" /T /F
taskkill /FI "WindowTitle eq Next.js Frontend*" /T /F
