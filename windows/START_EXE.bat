@echo off
setlocal EnableExtensions
chcp 65001 >nul
title NetworkEncyclopedia - Engineer Jokar
cd /d "%~dp0"
if not exist "NetworkEncyclopedia.exe" (
  echo [ERROR] NetworkEncyclopedia.exe was not found in this folder.
  echo Extract the complete Windows ZIP and rerun this launcher.
  pause
  exit /b 2
)
if not defined NETENC_TOKEN set /p "NETENC_TOKEN=Enter a strong private sync token: "
if not defined NETENC_TOKEN (
  echo [ERROR] NETENC_TOKEN must not be empty.
  pause
  exit /b 3
)
if not defined NETENC_HOST set "NETENC_HOST=0.0.0.0"
if not defined NETENC_PORT set "NETENC_PORT=5050"
if not defined NETENC_DEVICE set "NETENC_DEVICE=%COMPUTERNAME%"
echo.
echo NetworkEncyclopedia - Engineer Jokar
echo Local URL: http://127.0.0.1:%NETENC_PORT%
echo Port: %NETENC_PORT%
echo Token: hidden
echo Keep this window open while the server is running.
echo For LAN access, allow the port only on trusted Private networks.
echo.
start "" /min cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:%NETENC_PORT%"
"NetworkEncyclopedia.exe"
set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo NetworkEncyclopedia stopped with exit code %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
