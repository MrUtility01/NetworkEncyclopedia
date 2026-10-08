@echo off
chcp 65001 >nul
cd /d "%~dp0..\server"
echo Installing deps...
python -m pip install -r requirements.txt
echo.
echo Starting NetworkEncyclopedia server (0.0.0.0:5050)...
echo Open http://127.0.0.1:5050
echo From Android on same Wi-Fi use the LAN IP shown in console.
python app.py
pause
