@echo off
title ISRO Bharatiya Antariksh Station (BAS) - AI HAR System [SIH PS 174]
color 0B

echo ===============================================================================
echo   BHARATIYA ANTARIKSH STATION (BAS) - MODULE BAS-03 SCIENCE RACK
echo   AI HUMAN ACTIVITY RECOGNITION (HAR) SUBSYSTEM [SIH PS 174]
echo ===============================================================================
echo.
echo [1/3] Checking Python 3.14 Environment and Dependencies...
python -c "import fastapi, uvicorn, opencv_python, numpy" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing required on-board dependencies...
    python -m pip install fastapi uvicorn opencv-python pillow websockets
) else (
    echo [OK] All core AI, Computer Vision and WebSocket packages verified.
)

echo.
echo [2/3] Launching Edge AI Telemetry Service on http://localhost:8000 ...
start "" http://localhost:8000

echo.
echo [3/3] Starting High-Performance Uvicorn Server...
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause
