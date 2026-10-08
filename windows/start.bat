@echo off
chcp 65001 >nul
title NetworkEncyclopedia — Engineer Jokar
cd /d "%~dp0..\server"

REM رمز پیش‌فرض همگام‌سازی LAN (قابل تغییر)
if not defined NETENC_TOKEN set NETENC_TOKEN=09136555866
if not defined NETENC_DEVICE set NETENC_DEVICE=%COMPUTERNAME%
if not defined PORT set PORT=5050
if not defined HOST set HOST=0.0.0.0

echo ============================================
echo  NetworkEncyclopedia Server
echo  Token : %NETENC_TOKEN%
echo  Port  : %PORT%
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python پیدا نشد. از python.org نصب کنید.
  pause
  exit /b 1
)

python -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo [WARN] نصب وابستگی‌ها با هشدار — ادامه...
)

echo.
echo در حال seed و اجرای سرور...
echo مرورگر: http://127.0.0.1:%PORT%
echo اندروید: همان Wi-Fi + Token بالا
echo.
python app.py
pause
