# دسترسی از سیستم دیگر به پورت 5050

## علت رایج «چیزی نمیاد»
1. فایروال ویندوز پورت 5050 را بسته است
2. سرور فقط روی 127.0.0.1 گوش می‌دهد (باید `0.0.0.0` باشد)
3. IP اشتباه زده‌اید (IP واقعی LAN را از `ipconfig` بگیرید)

## روی سرور (سیستمی که برنامه اجرا شده)

```bash
cd ~/NetworkEncyclopedia/server
export NETENC_TOKEN=09136555866
export NETENC_HOST=0.0.0.0
export NETENC_PORT=5050
python app.py
```

در کنسول باید خطوطی مثل این ببینید:
```text
NetEnc listening on http://0.0.0.0:5050
  LAN URL: http://192.168.x.x:5050
```

### باز کردن فایروال ویندوز (PowerShell Admin)

```powershell
New-NetFirewallRule -DisplayName "NetEnc 5050" -Direction Inbound -Protocol TCP -LocalPort 5050 -Action Allow
```

یا:
```powershell
netsh advfirewall firewall add rule name="NetEnc 5050" dir=in action=allow protocol=TCP localport=5050
```

### پیدا کردن IP
```powershell
ipconfig
```
آدرس IPv4 کارت LAN/Wi-Fi (مثلاً `192.168.1.50`) را بردارید — نه `127.0.0.1`.

از خود سرور تست:
```text
http://127.0.0.1:5050/api/health
http://127.0.0.1:5050/api/lan
```

## از سیستم دیگر در همان شبکه
مرورگر:
```text
http://192.168.x.x:5050
```
اگر timeout شد → فایروال یا IP غلط است.  
اگر صفحه آمد ولی فهرست خالی → seed هنوز تمام نشده؛ صبر کنید یا `/api/stats` را چک کنید.

## اندروید
در تنظیمات Sync همان `http://192.168.x.x:5050` و توکن `09136555866` را بگذارید.
