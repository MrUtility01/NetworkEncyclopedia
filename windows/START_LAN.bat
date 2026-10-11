@echo off
chcp 65001 >nul
cd /d "%~dp0\..\server"

echo ============================================
echo  NetworkEncyclopedia / ENGINEER JOKAR
echo  LAN mode - password/token: 09136555866
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found.
  echo Install: winget install Python.Python.3.12
  echo Enable: Add python.exe to PATH
  pause
  exit /b 1
)

echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo pip failed
  pause
  exit /b 1
)

set NETENC_TOKEN=09136555866
set NETENC_HOST=0.0.0.0
set NETENC_PORT=5050

echo.
echo Starting server on 0.0.0.0:5050 ...
echo From this PC:  http://127.0.0.1:5050
echo From LAN phone/PC: http://YOUR-IP:5050
echo Token/password: 09136555866
echo.

python app.py
pause
