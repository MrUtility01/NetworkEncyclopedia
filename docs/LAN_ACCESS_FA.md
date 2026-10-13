# دسترسی از سیستم دیگر به پورت 83

## علت رایج «چیزی نمیاد»
1. فایروال ویندوز پورت 83 را بسته است
2. سرور فقط روی 127.0.0.1 گوش می‌دهد (باید `0.0.0.0` باشد)
3. IP اشتباه زده‌اید (IP واقعی LAN را از `ipconfig` بگیرید)
4. روی ویندوز پورت‌های زیر 1024 گاهی نیاز به **Run as Administrator** دارند

## روی سرور (سیستمی که برنامه اجرا شده)

```bash
cd ~/NetworkEncyclopedia/server
export NETENC_TOKEN=engineerjokar
export NETENC_HOST=0.0.0.0
export NETENC_PORT=83
python app.py
```

پیش‌فرض برنامه هم پورت **83** است؛ اگر تداخل داشت می‌توانید `NETENC_PORT` را عوض کنید.

در کنسول باید خطوطی مثل این ببینید:
```text
NetEnc listening on http://0.0.0.0:83
  LAN URL: http://192.168.x.x:83
```

### باز کردن فایروال ویندوز (PowerShell Admin)

```powershell
New-NetFirewallRule -DisplayName "NetEnc 83" -Direction Inbound -Protocol TCP -LocalPort 83 -Action Allow
```

یا:
```powershell
netsh advfirewall firewall add rule name="NetEnc 83" dir=in action=allow protocol=TCP localport=83
```

### پیدا کردن IP
```powershell
ipconfig
```
آدرس IPv4 کارت LAN/Wi-Fi (مثلاً `192.168.1.50`) را بردارید — نه `127.0.0.1`.

از خود سرور تست:
```text
http://127.0.0.1:83/api/health
http://127.0.0.1:83/api/lan
```

## از سیستم دیگر در همان شبکه
مرورگر:
```text
http://192.168.x.x:83
```

رمز ورود برنامه: **engineerjokar**

## اندروید
در تنظیمات Sync:
```text
http://192.168.x.x:83
```
توکن: `engineerjokar`
