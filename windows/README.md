# Windows Host

## نسخهٔ قابل‌حمل
فایل NetworkEncyclopedia-Windows-x64.zip را از artifact اجرای موفق workflow با نام **Build Windows x64 portable app** دریافت، استخراج و START_EXE.bat را اجرا کن. راهنمای کامل: [INSTALL_EXE_FA.md](INSTALL_EXE_FA.md).

- بستهٔ EXE برای ویندوز x64 ساخته می‌شود و برای اجرا نیاز به نصب جداگانه Python ندارد.
- هنگام نخستین راه‌اندازی، توکن خصوصی را در ورودی محافظت‌شده PowerShell وارد کن.
- پورت پیش‌فرض نسخهٔ قابل‌حمل 5050 است.
- Android و Windows برای همگام‌سازی LAN باید به شبکهٔ مورداعتماد وصل باشند.

## اجرای نسخهٔ سورس
```bat
start.bat
```
نسخهٔ سورس به Python و وابستگی‌های server/requirements.txt نیاز دارد. برای جزئیات، INSTALL_LAN_FA.md را بخوان.
