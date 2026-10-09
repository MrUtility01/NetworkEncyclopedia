# بسته تکمیل محتوای سوییچینگ و مسیریابی — ENGINEER JOKAR

## دامنه بسته
این بسته برای **تکمیل رکوردهای موجود** این چهار فصل از ساختار عمومی NetworkEncyclopedia ساخته شده است؛ فصل تکراری ایجاد نمی‌کند:

- فصل ۷: اترنت و سوییچینگ پایه — ۱۷ موضوع / ۸۵ درس
- فصل ۱۳: سوییچینگ سیسکو — ۲۹ موضوع / ۱۴۵ درس
- فصل ۱۴: مسیریابی پیشرفته — ۲۸ موضوع / ۱۴۰ درس
- فصل ۲۰: MikroTik Routing / Firewall / NAT — ۲۰ موضوع / ۱۰۰ درس

مجموع: **۹۴ موضوع، ۱۸ زیرفصل و ۴۷۰ درس** (هر موضوع در سطوح L0 تا L4).

## فایل‌ها
- `switching_routing_curriculum_pack.json` — محتوای آموزشی و فهرست محدوده
- `validate_pack.py` — کنترل JSON، تعداد رکوردها، شناسه‌ها، محتوای ضروری و جدابودن پاسخ‌نامه
- `apply_content_pack.py` — ابزار پیش‌نمایش و واردسازی ایمن به SQLite موجود
- `VALIDATION.txt` — نتیجهٔ بررسی بسته و آزمون دیتابیس شبیه‌سازی‌شده

## محتوای هر درس
تعریف و خلاصه، اهداف یادگیری، پیش‌نیاز، توضیح پایه، سازوکار فنی، مثال و فرمان‌های مرتبط، سناریوی محیط کار، لابراتوار کنترل‌شده، مراحل عیب‌یابی، امنیت/تفاوت نسخه‌ها، واژه‌نامه، مهارت نهایی و چهار نوع پرسش ارزیابی. پاسخ‌نامه و معیار ارزیابی در `meta.assessment.answer_key` نگهداری می‌شود و در متن سؤال‌ها درج نشده است.

## واردسازی به دیتابیس واقعی
۱. ابتدا برنامه را طبق روال خودتان متوقف کنید و از دیتابیس واقعی نسخهٔ پشتیبان تهیه کنید.
۲. این پوشه را داخل مخزن قرار دهید؛ وابستگی بیرونی لازم نیست، Python 3 و SQLite استاندارد کافی است.
۳. اعتبارسنجی را اجرا کنید:

```bash
python tools/engineer_jokar_switching_routing/validate_pack.py
```

۴. مسیر دیتابیس را با مسیر واقعی خودتان تطبیق دهید. اجرای بدون `--apply` فقط پیش‌نمایش می‌دهد و هیچ تغییری نمی‌نویسد:

```bash
python tools/engineer_jokar_switching_routing/apply_content_pack.py --db server/data/encyclopedia.db
```

۵. گزارش پیش‌نمایش باید **۴۷۰ تطبیق دقیق** بر اساس شمارهٔ فصل، زیرفصل، ترتیب درس و عنوان فارسی داشته باشد و هیچ mismatch نشان ندهد. برای اعمال واقعی، پرچم‌ها را صریح اضافه کنید:

```bash
python tools/engineer_jokar_switching_routing/apply_content_pack.py --db server/data/encyclopedia.db --apply --overwrite
```

اسکریپت قبل از نوشتن با SQLite Backup API یک نسخهٔ پشتیبان از دیتابیس می‌گیرد، سپس تنها فیلدهای محتوایی درس‌ها را به‌روزرسانی می‌کند. رکورد/فصل/زیرفصل جدید نمی‌سازد، حذف انجام نمی‌دهد و `id`، عنوان، ترتیب، `uid` و ستون‌های sync (`content_hash`, `device_id`, `deleted`) را تغییر نمی‌دهد. اگر حتی یک عنوان یا موقعیت با بسته مطابقت نداشته باشد، کل عملیات قبل از نوشتن متوقف می‌شود.

> **هشدار همگام‌سازی:** اگر این نسخه از برنامه چنددستگاهی و sync دارد، `content_hash` عمداً توسط اسکریپت محاسبه یا تغییر داده نمی‌شود؛ الگوریتم هش و سازوکار انتشار باید با همان نسخهٔ اپ تطبیق داده شود. پس از واردسازی، از مسیر رسمی همگام‌سازی برنامه استفاده کنید و وضعیت کلاینت‌ها را کنترل کنید.

## نکات فنی و عملیاتی
- همهٔ درس‌ها با `source_status=review_required` علامت‌گذاری شده‌اند؛ این نشان می‌دهد محتوای تولیدی هنوز بازبینی فنی نهایی می‌خواهد.
- فرمان‌ها به سازنده/نسخه وابسته‌اند. برای Cisco IOS/IOS XE/NX-OS، FRRouting و MikroTik RouterOS v6/v7، پیش از اجرا با مستندات رسمی همان نسخه تطبیق دهید.
- آزمایش‌های STP، VLAN، route withdrawal، redistribution، firewall/NAT و تغییرات مسیر فقط در شبیه‌ساز یا محیط آزمایشی ایزوله انجام شوند. برای تغییر production باید backup، دسترسی out-of-band، change window، معیار توقف و rollback وجود داشته باشد.
- **از `seed_full(force=True)` یا `rebuild_curriculum_from_scratch` استفاده نکنید**؛ این عملیات‌ها می‌توانند کل محتوای پایگاه داده را حذف و بازسازی کنند.
- فایل دیتابیس محلی کاربر در زمان تولید در دسترس نبود. آزمون واردسازی با دیتابیس ساختگیِ هم‌شکل انجام شده و نتیجه به معنی اعمال موفق روی دیتابیس واقعی کاربر نیست.

## منابع اولیه
- IEEE 802.3 Ethernet: https://standards.ieee.org/standard/802_3-2022.html
- IEEE 802.1Q VLAN: https://standards.ieee.org/standard/802_1Q-2022.html
- IEEE 802.1AX LACP: https://standards.ieee.org/standard/802_1AX-2020.html
- OSPF RFC 2328: https://www.rfc-editor.org/rfc/rfc2328
- BGP RFC 4271: https://www.rfc-editor.org/rfc/rfc4271
- EIGRP RFC 7868: https://www.rfc-editor.org/rfc/rfc7868
- Cisco Catalyst configuration guides: https://www.cisco.com/c/en/us/support/switches/catalyst-9300-series-switches/products-installation-and-configuration-guides-list.html
- MikroTik official documentation: https://help.mikrotik.com/docs/
- MikroTik route selection: https://help.mikrotik.com/docs/spaces/ROS/pages/74678285/Route+Selection+and+Filters
