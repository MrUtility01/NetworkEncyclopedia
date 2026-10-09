# بستهٔ کامل Windows Server برای ENGINEER JOKAR

این بسته محتوای آموزشی را برای **رکوردهای موجود** در فصل‌های ۲۸، ۲۹، ۳۰، ۳۱، ۳۲ و ۳۵ مخزن NetworkEncyclopedia آماده می‌کند. فصل یا درس تازه‌ای ایجاد نمی‌شود و عنوان، ترتیب، شناسه یا UID رکوردهای برنامه نباید تغییر کند.

## محدوده

- فصل ۲۸: Windows Server Core، نصب، role/feature، Server Manager، Windows Admin Center و مدیریت از راه دور
- فصل ۲۹: Active Directory، Forest/Domain/OU، DC، Global Catalog، FSMO، replication، GPO و امنیت AD
- فصل ۳۰: DNS، DHCP، NPS/RADIUS و 802.1X
- فصل ۳۱: SMB، مجوزهای Share و NTFS، DFS/DFSR، Print Server و driver
- فصل ۳۲: Defender، BitLocker، Windows Firewall، AppLocker، security baseline، LAPS، Event Log و EDR
- فصل ۳۵: ابزارهای شبکهٔ CMD، PowerShell، Remoting، Active Directory module، اسکریپت، Task Scheduler و DSC

هر موضوع پنج سطح L0 تا L4 دارد؛ بسته شامل ۷۳ موضوع، ۱۸ زیرفصل و ۳۶۵ درس است. هر درس دارای متن فارسی، فرمان‌های مرتبط، لابراتوار کنترل‌شده، سناریو، عیب‌یابی، نکات امنیتی و چهار سؤال است. پاسخ‌نامه در `meta.assessment.answer_key` جدا از `meta.assessment.questions` نگهداری می‌شود. وضعیت محتوا `review_required` است؛ پیش از استفادهٔ عملیاتی، سازگاری دستورها با نسخه و نقش نصب‌شده بررسی شود.

## فایل‌ها

- `windows_server_complete_curriculum_pack.json`: بستهٔ داده
- `validate_pack.py`: اعتبارسنجی JSON و ساختار بسته
- `apply_content_pack.py`: پیش‌نمایش و به‌روزرسانی رکوردهای موجود SQLite
- `build_pack.py`: بازتولید JSON از کاتالوگ این بسته
- `VALIDATION.txt`: گزارش تست ساختاری و شبیه‌سازی واردسازی

## قرار دادن فایل‌ها روی ویندوز

۱. از ZIP استفاده کنید و پوشهٔ `engineer_jokar_windows_server` را داخل `tools` مخزن قرار دهید. ساختار باید این‌گونه باشد:

```text
NetworkEncyclopedia-main/
  server/
  shared/
  tools/
    engineer_jokar_windows_server/
      windows_server_complete_curriculum_pack.json
      validate_pack.py
      apply_content_pack.py
      README_FA.md
```

۲. در File Explorer به ریشهٔ مخزن بروید، در نوار آدرس `powershell` بنویسید و Enter بزنید.

۳. اعتبارسنجی بسته را اجرا کنید:

```powershell
py -3 .\tools\engineer_jokar_windows_server\validate_pack.py
```

باید `365 lessons / 73 topics / 18 subchapters` را ببینید.

## پیش‌نمایش واردسازی

ابتدا بررسی کنید فایل دیتابیس واقعاً در این مسیر موجود باشد. مسیر زیر با ساختار عمومی فعلی مخزن سازگار است، اما مسیر نسخهٔ محلی شما ممکن است فرق کند:

```powershell
Test-Path .\server\data\encyclopedia.db
```

اگر `True` بود، پیش‌نمایش را اجرا کنید:

```powershell
py -3 .\tools\engineer_jokar_windows_server\apply_content_pack.py --db .\server\data\encyclopedia.db
```

این فرمان فقط گزارش می‌دهد و چیزی را تغییر نمی‌دهد. باید دقیقاً **۳۶۵ تطبیق موقعیت/عنوان** دیده شود و هیچ خطای تطبیق وجود نداشته باشد. اگر مسیر فایل یا گزارش با این انتظار سازگار نیست، اعمال را متوقف کنید.

## اعمال تغییرات

فقط پس از بازبینی پیش‌نمایش، توقف برنامه و تهیهٔ نسخهٔ پشتیبان، اجرا کنید:

```powershell
py -3 .\tools\engineer_jokar_windows_server\apply_content_pack.py --db .\server\data\encyclopedia.db --apply --overwrite
```

ابزار قبل از اعمال از دیتابیس SQLite با Backup API نسخهٔ پشتیبان می‌گیرد. `--overwrite` یعنی متن فعلی همان درس‌های هدف با محتوای این بسته جایگزین می‌شود. رکوردها، ID/UID، عنوان و ترتیب دست‌نخورده می‌مانند و خارج از این شش فصل چیزی نباید تغییر کند.

## نکات بسیار مهم

- **این بسته را به‌عنوان یک پوشه در `tools` قرار دهید؛ JSON را به فایل Python یا دیتابیس تغییرنام ندهید.**
- اگر پیش‌نمایش کمتر یا بیشتر از ۳۶۵ تطبیق نشان داد، `--apply` را اجرا نکنید. نسخهٔ مخزن یا داده‌های محلی احتمالاً تغییر کرده‌اند و باید عنوان‌ها/موقعیت‌ها تطبیق داده شوند.
- اسکریپت فقط رکوردهای SQLite موجود را به‌روزرسانی می‌کند؛ `server/core/full_curriculum.py` را تغییر نمی‌دهد. اگر برنامه از روی کد seed/reseed اجرا شود، ممکن است دادهٔ دیتابیس دوباره ساخته شود. برای نگهداری دائمی در توزیع نرم‌افزار باید بعداً منبع اصلی seed هم با حفظ قرارداد داده به‌روزرسانی شود.
- `content_hash` و فیلدهای device/sync عمداً تغییر نمی‌کنند چون الگوریتم و قرارداد sync را نباید حدس زد. اگر برنامهٔ شما تغییرات محتوا را با hash یا sync چنددستگاهی مدیریت می‌کند، ابتدا کد sync را بررسی کنید و انتشار به کاربران دیگر را تا تأیید روش رسمی برنامه انجام ندهید.
- دستورها برای Windows Server/PowerShell وابسته به نسخه و Role هستند. درس‌های AD، DNS، DHCP، NPS، DFSR، BitLocker، Firewall و Group Policy را در VM یا آزمایشگاه ایزوله بررسی کنید؛ هیچ فرمان تغییر‌دهنده‌ای را بدون backup، پنجرهٔ تغییر و rollback روی سرور واقعی اجرا نکنید.
- محتوای بسته با `review_required` علامت خورده است. اعتبارسنجی ساختاری به معنای اجرای همهٔ دستورها روی همهٔ نسخه‌های Windows Server نیست.

## منابع رسمی پیشنهادی

- Windows Server releases: https://learn.microsoft.com/en-us/windows-server/get-started/windows-server-release-info
- Server Core: https://learn.microsoft.com/en-us/windows-server/administration/server-core/server-core-why-to-install
- Windows Admin Center: https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/overview
- AD DS: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview
- Group Policy: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-overview
- Windows LAPS: https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview
- DNS: https://learn.microsoft.com/en-us/windows-server/networking/dns/dns-top
- DHCP: https://learn.microsoft.com/en-us/windows-server/networking/technologies/dhcp/dhcp-top
- NPS: https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-top
- SMB: https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview
- DFS Namespace: https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/dfs-overview
- PowerShell: https://learn.microsoft.com/en-us/powershell/scripting/overview
- PowerShell Remoting: https://learn.microsoft.com/en-us/powershell/scripting/learn/remoting/overview
