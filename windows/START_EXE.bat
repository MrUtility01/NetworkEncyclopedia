@echo off
setlocal EnableExtensions
chcp 65001 >nul
title NetworkEncyclopedia - Engineer Jokar
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0START_EXE.ps1"
set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo NetworkEncyclopedia launcher exited with code %EXIT_CODE%.
pause
exit /b %EXIT_CODE%
