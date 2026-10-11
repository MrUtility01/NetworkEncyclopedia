@echo off
chcp 65001 >nul
cd /d "%~dp0\..\server"

echo ============================================
echo  NetworkEncyclopedia LAN
echo  Token/password: 09136555866
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found. Run: winget install Python.Python.3.12
  pause
  exit /b 1
)

echo Installing deps (mirror + long timeout)...
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=120
if errorlevel 1 (
  echo Mirror failed, trying default PyPI...
  python -m pip install -r requirements.txt --default-timeout=120
)
if errorlevel 1 (
  echo pip failed - check internet/firewall
  pause
  exit /b 1
)

set NETENC_TOKEN=09136555866
set NETENC_HOST=0.0.0.0
set NETENC_PORT=5050

echo Starting on 0.0.0.0:5050 ...
echo Local:  http://127.0.0.1:5050
echo LAN:    http://YOUR-IP:5050
echo Token:  09136555866
echo.
python app.py
pause
