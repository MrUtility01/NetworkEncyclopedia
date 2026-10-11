# نصب و اجرای ویندوز روی کل شبکه داخلی

## رمز برنامه / توکن Sync

```
09136555866
```

## ۱) نصب Python (یک‌بار)

PowerShell به‌عنوان Administrator:

```text
winget install Python.Python.3.12
```

تیک **Add to PATH** را بزن. پنجره‌ها را ببند و دوباره باز کن.

```text
python --version
```

## ۲) کلون / به‌روز

```text
cd %USERPROFILE%
git clone https://github.com/MrUtility01/NetworkEncyclopedia.git
cd NetworkEncyclopedia
git pull
```

## ۳) فایروال (یک‌بار، PowerShell Admin)

```powershell
New-NetFirewallRule -DisplayName "NetEnc 5050" -Direction Inbound -Protocol TCP -LocalPort 5050 -Action Allow
```

## ۴) اجرا

دوبار کلیک روی:

```text
windows\START_LAN.bat
```

یا:

```text
cd server
set NETENC_TOKEN=09136555866
set NETENC_HOST=0.0.0.0
set NETENC_PORT=5050
python -m pip install -r requirements.txt
python app.py
```

## ۵) آدرس‌ها

| کجا | آدرس |
|-----|------|
| همین سیستم | http://127.0.0.1:5050 |
| گوشی / سیستم دیگر در LAN | http://IP-سیستم:5050 |

IP را ببین:

```text
ipconfig
```

مثال: `http://192.168.1.50:5050`

## ۶) اندروید Sync

- آدرس سرور: `http://IP-سیستم:5050`
- توکن: `09136555866`

## فصل‌ها

با `seed_full` فصل‌های **۱ تا ۶۸** ساخته می‌شوند. اگر دیتابیس قدیمی است:

```text
del server\data\encyclopedia.db
```

بعد دوباره `python app.py`.
