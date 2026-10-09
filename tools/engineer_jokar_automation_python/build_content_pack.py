# -*- coding: utf-8 -*-
"""Generate a schema-compatible Persian curriculum pack for Python and IT automation."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import date

OUT = Path(__file__).with_name('automation_python_curriculum_pack.json')
LEVELS = [
    ('L0', 'آشنایی', 'Intro', 'درک شهودی و واژگان پایه'),
    ('L1', 'مقدماتی', 'Junior', 'اجرای کار پایه در محیط کنترل‌شده'),
    ('L2', 'ادمین', 'Admin', 'اجرای عملیاتی همراه با اعتبارسنجی و ثبت گزارش'),
    ('L3', 'مهندس', 'Senior', 'طراحی مقاوم، idempotency، تست، مشاهده‌پذیری و بازیابی'),
    ('L4', 'خبره', 'Architect', 'معماری سازمانی، حاکمیت، مقیاس‌پذیری و کنترل blast radius'),
]

# Each topic contains distinct, topic-specific content. Shared pedagogical scaffolding is
# expanded according to L0-L4 while all questions and answer keys remain separate in meta.
TOPICS = [
# Chapter 21 — RouterOS automation (chapter 21, subsection 4)
 dict(ch=21, sub=4, topic='Scheduler', en='Scheduler', domain='MikroTik RouterOS',
      summary='اجرای زمان‌بندی‌شدهٔ کارهای مدیریتی در RouterOS با کنترل دسترسی، ثبت نتیجه و امکان بازیابی.',
      why='Scheduler برای کارهایی مناسب است که باید در زمان مشخص یا با فاصلهٔ زمانی اجرا شوند؛ مانند تهیهٔ خروجی وضعیت، بررسی دوره‌ای سلامت و پاک‌سازی کنترل‌شدهٔ داده‌های موقت.',
      concepts='زمان شروع (start-time)، فاصلهٔ تکرار (interval)، رویداد اجرا (on-event)، سیاست دسترسی اسکریپت و تفاوت اجرای دستی با اجرای زمان‌بندی‌شده.',
      mechanism='Scheduler یک رویداد زمان‌دار ایجاد می‌کند و در زمان سررسید، دستور یا اسکریپت را با زمینهٔ دسترسی خودش اجرا می‌کند. ساعت و منطقهٔ زمانی دستگاه، وضعیت فعال/غیرفعال بودن رکورد و مجوزهای اسکریپت بر نتیجه اثر دارند.',
      commands='''/system scheduler print detail
/system scheduler add name=lab-status interval=1h start-time=startup on-event="/system resource print" comment="LAB ONLY"
/system scheduler disable [find name="lab-status"]
/system scheduler remove [find name="lab-status"]''',
      example='یک کار آزمایشی فقط وضعیت منابع را چاپ می‌کند. در دستگاه عملیاتی، اول فرمان را دستی آزمایش کنید، سپس زمان‌بندی را فعال کنید و بعد از مشاهدهٔ لاگ، حذف یا غیرفعال‌سازی را تمرین کنید.',
      lab='در روتر آزمایشی یا CHR یک Scheduler با نام یکتا بسازید که هر ساعت یک دستور فقط‌خواندنی را اجرا کند؛ از /system scheduler print detail و /log print برای اعتبارسنجی استفاده کنید؛ سپس آن را disable و remove کنید.',
      issues='اگر کار اجرا نمی‌شود، فعال بودن رکورد، start-time/interval، زمان سیستم، syntax رشتهٔ on-event، لاگ‌ها و permission context را به‌ترتیب بررسی کنید. اجرای دستی موفق لزوماً به معنی اجرای موفق تحت Scheduler نیست.',
      security='اصل حداقل دسترسی را رعایت کنید؛ برای تغییرات شبکه‌ای برنامهٔ rollback و پنجرهٔ نگهداری داشته باشید؛ رمزها را داخل متن on-event یا comment قرار ندهید؛ اجرای دوره‌ای پرتکرار می‌تواند CPU و log را بی‌جهت مصرف کند.',
      advanced='برای عملیات غیرقابل‌تکرار، قفل منطقی یا شرط پیش‌نیاز بگذارید. هم‌زمانی jobها، تغییر ساعت و reboot را در طراحی لحاظ کنید. قبل از ارتقا، سازگاری syntax را با نسخهٔ RouterOS هدف بیازمایید.',
      glossary='Scheduler: زمان‌بند؛ on-event: دستور هنگام رویداد؛ interval: فاصلهٔ اجرا؛ permission context: زمینهٔ مجوز اجرا؛ rollback: بازگردانی تغییر.',
      question='کدام بررسی قبل از فعال‌کردن یک job دوره‌ای از همه مهم‌تر است؟', answer='ابتدا دستور را دستی و در محیط آزمایش اجرا کنید، سپس مجوزها و خروجی/لاگ را بررسی کنید و تازه بعد از تعیین دوره و مسیر بازگشت آن را فعال کنید.', distractors=['فعال کردن آن روی همهٔ روترها بدون تست','گذاشتن رمز مدیر در comment برای عیب‌یابی','حذف لاگ‌ها برای کم‌کردن حجم']),
 dict(ch=21, sub=4, topic='Netwatch', en='Netwatch', domain='MikroTik RouterOS',
      summary='پایش در دسترس‌بودن یک میزبان و اجرای رویدادهای کنترل‌شده بر مبنای تغییر وضعیت آن.',
      why='Netwatch برای تشخیص up/down بودن endpointهای منتخب مفید است؛ اما ping موفق فقط دسترسی ICMP را نشان می‌دهد و به‌تنهایی سلامت برنامه یا مسیر کامل سرویس را تضمین نمی‌کند.',
      concepts='host هدف، نوع آزمون، interval، timeout، وضعیت up/down، رویدادهای up-script/down-script و hysteresis/debounce برای جلوگیری از نوسان.',
      mechanism='Netwatch آزمون تعریف‌شده را در بازه‌های زمانی انجام می‌دهد و هنگام تغییر وضعیت، رویداد متناظر را اجرا می‌کند. فایروال، rate limit، route و سیاست ICMP مقصد می‌توانند نتیجه را تغییر دهند.',
      commands='''/tool netwatch print detail
/tool netwatch add host=192.0.2.10 interval=30s timeout=2s comment="LAB ONLY"
/tool netwatch disable [find comment="LAB ONLY"]
/tool netwatch remove [find comment="LAB ONLY"]''',
      example='از TEST-NET-1 یعنی 192.0.2.0/24 در مثال مستنداتی استفاده شده؛ برای لابراتوار واقعی، IP یک میزبان آزمایشیِ تحت کنترل خودتان را جایگزین کنید. up/down script را ابتدا خالی یا فقط log-only نگه دارید.',
      lab='یک endpoint آزمایشی در شبکهٔ خصوصی خود انتخاب کنید، رکورد Netwatch بدون script مخرب بسازید، وضعیت را در دو حالت reachable/unreachable بررسی کنید و سپس record را حذف کنید.',
      issues='هدف پاسخ نمی‌دهد: route، ACL، ICMP و timeout را بررسی کنید. تغییرات پی‌درپی up/down: timeout/interval را متناسب کنید و شرط تأیید چندباره یا منطق debounce اضافه کنید. وضعیت up است اما سرویس خراب است: health-check لایهٔ برنامه لازم است.',
      security='از Netwatch به‌عنوان مکانیسم اجرای فرمان دلخواه با امتیاز بالا استفاده نکنید. مقصدهای پایش را محدود کنید، فرمان‌های رویداد را ساده و قابل‌ثبت نگه دارید و برای قطع لینک اصلی از روش تأیید دوم استفاده کنید.',
      advanced='پایش چند مقصد مستقل از یک مقصد واحد، احتمال false positive را کم می‌کند. هنگام اجرای failover، از بازگشت سریع و نوسان route جلوگیری کنید و وضعیت واقعی data plane را پس از تغییر verify کنید.',
      glossary='Endpoint: نقطهٔ پایانی؛ health check: آزمون سلامت؛ false positive: هشدار نادرست؛ debounce: جلوگیری از واکنش به نوسان کوتاه.',
      question='چرا پاسخ‌دادن ping برای اعلام سالم‌بودن کامل یک برنامه کافی نیست؟', answer='چون ICMP فقط پاسخ‌گویی شبکه‌ای مقصد را نشان می‌دهد؛ پورت، فرایند، وابستگی‌ها یا درخواست کاربردی می‌توانند همچنان خراب باشند.', distractors=['چون ping همیشه TCP استفاده می‌کند','چون Netwatch فقط DNS را بررسی می‌کند','چون پاسخ ICMP ثابت می‌کند برنامه و پایگاه داده سالم‌اند']),
 dict(ch=21, sub=4, topic='Script', en='Script', domain='MikroTik RouterOS',
      summary='نوشتن اسکریپت‌های RouterOS برای تکرارپذیرکردن عملیات، با کنترل خطا، دسترسی و قابلیت بازگردانی.',
      why='اسکریپت کوتاه می‌تواند عملیات تکراری را استاندارد کند؛ اما هر اسکریپتی که تنظیمات را تغییر می‌دهد باید با ورودی مشخص، پیش‌شرط، خروجی قابل‌ردیابی و روش بازگشت طراحی شود.',
      concepts='متغیر، شرط، حلقه، دستور print/find/set، بلوک on-error در نسخه‌های پشتیبانی‌شده، scope، permission و ذخیره‌سازی script در Script repository.',
      mechanism='RouterOS اسکریپت را در interpreter داخلی اجرا می‌کند. context اجرا، scope متغیرها و مجوزهای اسکریپت بر دسترسی به منوها اثر دارند؛ syntax آن با Python/Bash یکی نیست.',
      commands='''/system script print detail
/system script add name=lab-readonly source=":put [/system identity get name]" comment="LAB ONLY"
/system script run lab-readonly
/system script remove [find name="lab-readonly"]''',
      example='نمونهٔ read-only نام هویت روتر را چاپ می‌کند. قبل از استفاده از /set، /remove یا تغییر firewall، خروجی find را محدود و تعداد رکوردهای هدف را کنترل کنید.',
      lab='در CHR اسکریپتی بسازید که فقط identity و resource را بخواند؛ آن را دستی اجرا کنید، لاگ و خروجی را بررسی کنید، و سپس حذف کنید. تمرین تغییر تنظیمات در همان لاب فقط پس از snapshot انجام شود.',
      issues='خطای syntax: عبارت‌ها را کوچک و مرحله‌ای اجرا کنید. خطای permission: context و policyهای script را بررسی کنید. نتیجهٔ غیرمنتظرهٔ find: شرط جست‌وجو را print کنید و پیش از تغییر، تعداد نتایج را اعتبارسنجی کنید.',
      security='اسکریپت‌های دانلودشده یا کپی‌شده را بدون بازبینی اجرا نکنید. policyهای حساس را فقط در صورت نیاز فعال کنید، اسرار را در source ننویسید، و دستورات مخرب مثل حذف bulk را با تأیید و backup محافظت کنید.',
      advanced='برای اجرای چندبارهٔ امن، idempotency طراحی کنید: اگر وضعیت درست است، تغییری ندهد. عملیات را به read/plan و apply جدا کنید و خروجی قبل/بعد را نگه دارید.',
      glossary='Interpreter: مفسر؛ scope: دامنهٔ متغیر؛ idempotency: نتیجهٔ یکسان در اجرای تکراری؛ precondition: پیش‌شرط؛ source: متن اسکریپت.',
      question='منظور از idempotent بودن یک اسکریپت عملیاتی چیست؟', answer='اجرای دوباره با همان ورودی، وضعیت را دوباره و دوباره به همان حالت مطلوب می‌رساند بدون آنکه تغییرات اضافه یا ناخواسته تولید کند.', distractors=['هر اجرا حتماً یک رکورد جدید بسازد','هر اجرا تمام پیکربندی را پاک کند','اسکریپت فقط یک بار قابل اجرا باشد']),
 dict(ch=21, sub=4, topic='API Automation', en='API Automation', domain='MikroTik RouterOS',
      summary='اتصال برنامهٔ بیرونی به RouterOS از مسیرهای مدیریتی مجاز، با احراز هویت، timeout، حداقل دسترسی و اعتبارسنجی خروجی.',
      why='API اتوماسیون را از ورود دستی به روتر جدا می‌کند و امکان خواندن وضعیت یا اعمال پیکربندی تکرارپذیر را می‌دهد؛ خود API جایگزین طراحی دسترسی و کنترل تغییر نیست.',
      concepts='RouterOS API بومی، REST API در نسخه‌ها/پیکربندی‌های پشتیبانی‌شده، TLS، حساب اختصاصی، timeout، retry محدود، schema اعتبارسنجی و audit log.',
      mechanism='کلاینت به سرویس مدیریتی فعال‌شده وصل می‌شود، احراز هویت می‌کند، درخواست را می‌فرستد و پاسخ را parse می‌کند. پورت باز بودن به‌تنهایی موفقیت پروتکل، مجوز یا سازگاری endpoint را تضمین نمی‌کند.',
      commands='''# بررسی دسترسی از میزبان مجاز (نمونهٔ پایتون با Requests برای REST)
import os, requests
base = os.environ["ROUTEROS_REST_URL"]  # مانند https://router.example/rest
user = os.environ["ROUTEROS_USER"]
password = os.environ["ROUTEROS_PASSWORD"]
r = requests.get(f"{base}/system/resource", auth=(user, password), timeout=(3, 10), verify=True)
r.raise_for_status()
print(r.json())''',
      example='در نمونه، URL و credentials از متغیر محیطی گرفته می‌شوند، timeout اجباری است و اعتبارسنجی TLS خاموش نشده است. endpoint و دسترسی REST باید با نسخهٔ RouterOS و تنظیمات همان دستگاه تأیید شود.',
      lab='در یک RouterOS CHR جدا از شبکهٔ تولید، فقط حساب آزمایشی کم‌دسترسی و endpoint خواندنی بسازید؛ یک درخواست GET بفرستید، پاسخ/کد HTTP را ثبت کنید، خطای 401/403/timeout را عمداً آزمایش و سپس حساب را حذف کنید.',
      issues='Connection refused: سرویس/پورت/مسیر شبکه را بررسی کنید. Timeout: ACL، مسیر و زمان timeout را بررسی کنید. 401/403: credentials و policy. خطای TLS: نام میزبان/CA را اصلاح کنید؛ verify=False راه‌حل عملیاتی امن نیست. JSON نامتوقع: نسخه و endpoint را بررسی کنید.',
      security='API را روی اینترنت عمومی باز نگذارید؛ ترجیحاً از شبکهٔ مدیریت یا VPN استفاده کنید، گواهی معتبر داشته باشید، حساب اختصاصی کم‌دسترسی بسازید، credential را در Git/لاگ ننویسید و فرمان‌های write را با approval و backup محافظت کنید.',
      advanced='Retry فقط برای خطاهای موقت و با سقف/backoff انجام شود. به‌طور خودکار عملیات write را پس از timeout کورکورانه تکرار نکنید؛ ممکن است درخواست اول انجام شده باشد. قبل/بعد را بخوانید و نتیجه را با وضعیت مطلوب مقایسه کنید.',
      glossary='API: رابط برنامه‌نویسی؛ endpoint: مسیر سرویس؛ TLS: رمزنگاری انتقال؛ timeout: حد انتظار؛ backoff: افزایش تدریجی فاصلهٔ retry.',
      question='چرا پس از timeout نباید بدون بررسی، درخواست تغییردهندهٔ تنظیمات را فوراً تکرار کرد؟', answer='زیرا سرور ممکن است تغییر را اعمال کرده باشد ولی پاسخ به کلاینت نرسیده باشد؛ تکرار کور می‌تواند عملیات غیرتکرارپذیر را دوبار انجام دهد.', distractors=['چون HTTP هرگز timeout ندارد','چون REST فقط از ICMP استفاده می‌کند','چون پاسخ timeout ثابت می‌کند روتر خاموش است']),
 dict(ch=21, sub=4, topic='SNMP', en='SNMP', domain='Monitoring',
      summary='جمع‌آوری شاخص‌های دستگاه از طریق OID/MIB برای مانیتورینگ ظرفیت، سلامت و رخدادها.',
      why='SNMP برای poll کردن counters و دریافت traps/notifications از تجهیزات استفاده می‌شود. SNMP جای ابزارهای پیکربندی امن را نمی‌گیرد و اعداد counter باید به نرخ/بازهٔ زمانی تبدیل شوند.',
      concepts='manager، agent، OID، MIB، GET/GETNEXT/GETBULK، counter، gauge، trap/inform، SNMPv2c و SNMPv3 authPriv.',
      mechanism='سامانهٔ مدیریت یک OID را از agent می‌خواند یا agent رخداد را به manager می‌فرستد. Counterهای 64-bit برای نرخ‌های پرسرعت مناسب‌ترند؛ wrap و reboot باید در محاسبهٔ delta لحاظ شوند.',
      commands='''# ابزارهای Net-SNMP؛ نام interface/OID را برای تجهیز خود بررسی کنید
snmpget -v3 -l authPriv -u monitor -a SHA -A "$SNMP_AUTH" -x AES -X "$SNMP_PRIV" 192.0.2.20 sysUpTime.0
snmpwalk -v3 -l authPriv -u monitor -a SHA -A "$SNMP_AUTH" -x AES -X "$SNMP_PRIV" 192.0.2.20 IF-MIB::ifName''',
      example='192.0.2.20 یک آدرس مستنداتی است و باید با آدرس دستگاه آزمایشی جایگزین شود. شناسهٔ الگوریتم‌ها و گزینه‌ها را با نسخهٔ ابزار و سیاست امنیتی محیط تطبیق دهید و رمزها را در history پوسته ننویسید.',
      lab='در آزمایشگاه فقط یک agent تحت مدیریت را با SNMPv3 فعال کنید، OID زمان uptime و نام رابط‌ها را بخوانید، مقدارها را با CLI دستگاه تطبیق دهید و سپس دسترسی SNMP را از میزبان‌های غیرمجاز مسدود کنید.',
      issues='No response: ACL/UDP 161، نسخه، credential و context را بررسی کنید. Unknown OID: MIB/OID معتبر نیست. counter صفر: نوع counter، پورت اشتباه یا پشتیبانی agent. نمودار جهشی: reboot، wrap یا فاصلهٔ poll را بررسی کنید.',
      security='در صورت امکان SNMPv3 authPriv را به communityهای ساده ترجیح دهید؛ UDP 161/162 را به سامانه‌های مدیریت محدود کنید؛ دسترسی write را حذف کنید مگر نیاز روشن و کنترل‌شده وجود داشته باشد؛ secrets را rotate کنید.',
      advanced='polling پرتکرار و walk گسترده می‌تواند بار مدیریتی بسازد. از GETBULK با محدودیت اندازه، discovery کنترل‌شده و برچسب‌گذاری استاندارد برای چندفروشنده‌ای استفاده کنید.',
      glossary='OID: شناسهٔ شیء؛ MIB: تعریف ساختار داده؛ agent: عامل روی تجهیز؛ manager: سامانهٔ مدیریت؛ counter: شمارنده؛ trap: پیام رخداد یک‌طرفه.',
      question='برای مانیتورینگ امن و خواندن شاخص‌ها، کدام گزینه معمولاً مناسب‌تر است؟', answer='SNMPv3 با احراز هویت و رمزنگاری (authPriv)، محدودشده به managerهای مجاز و فقط با مجوزهای موردنیاز.', distractors=['SNMPv2c با community برابر public در همهٔ VLANها','فعال‌کردن write برای همهٔ OIDها بدون نیاز','بازکردن UDP 161 به اینترنت']),
 dict(ch=21, sub=4, topic='Traffic Flow', en='Traffic Flow', domain='Flow telemetry',
      summary='صدور رکوردهای جریان ترافیک برای مشاهدهٔ الگوهای ارتباطی و تحلیل مصرف، نه ثبت کامل payload بسته‌ها.',
      why='Flow telemetry تصویری از مبدأ، مقصد، پورت‌ها، پروتکل و حجم/زمان جریان می‌دهد و برای capacity planning و تحلیل الگو مفید است؛ این داده با packet capture تفاوت دارد.',
      concepts='flow، exporter، collector، NetFlow/IPFIX format، sampling، active/inactive timeout، template و محدودیت ترافیک hardware-offloaded.',
      mechanism='روتر جریان‌ها را بر اساس ویژگی‌های بسته گروه‌بندی کرده و رکوردها را به collector می‌فرستد. در RouterOS، Traffic-Flow همهٔ ترافیک hardware-offloaded را الزاماً نمی‌بیند؛ محدودیت مسیر پردازش باید در تفسیر داده لحاظ شود.',
      commands='''/ip traffic-flow print
/ip traffic-flow set enabled=yes
/ip traffic-flow target print detail
# در لابراتوار، collector و target را مطابق نسخهٔ RouterOS تنظیم و سپس با ترافیک کنترل‌شده بررسی کنید.''',
      example='پس از فعال‌سازی exporter، یک اتصال آزمایشی به سرویس داخلی ایجاد و مشاهده کنید آیا رکورد به collector می‌رسد. وجود byte count به معنی ذخیره‌شدن محتوای کامل (payload) نیست.',
      lab='در CHR و collector آزمایشی، یک target مستندشده تنظیم کنید؛ با یک جریان TCP کنترل‌شده رکورد ایجاد کنید؛ آدرس/پورت/بایت را با انتظار مقایسه کنید و در پایان export را خاموش کنید.',
      issues='رکورد نمی‌رسد: مقصد، UDP port، route/firewall، format و clock را بررسی کنید. بخشی از ترافیک دیده نمی‌شود: offload/sampling/interface را بررسی کنید. تعداد جریان‌ها زیاد است: timeout و ظرفیت collector را بسنجید.',
      security='رکوردها می‌توانند الگوی رفتار کاربران و سرویس‌ها را افشا کنند؛ دسترسی و retention را محدود کنید، ترافیک telemetry را جدا کنید و اطلاعات را با اصل کمینه‌سازی نگه دارید.',
      advanced='برای تخمین حجم کل با sampling، ضریب نمونه‌گیری را صریح لحاظ کنید. قبل از تصمیم ظرفیت، شمارنده‌های اینترفیس را با flow records مقایسه کنید و احتمال missing flows را مستند کنید.',
      glossary='Exporter: فرستندهٔ جریان؛ collector: گیرنده/تحلیل‌گر؛ IPFIX: قالب تبادل جریان؛ sampling: نمونه‌گیری؛ payload: محتوای بسته.',
      question='تفاوت اصلی Flow telemetry و packet capture چیست؟', answer='Flow معمولاً metadata و آمار جریان را ثبت می‌کند؛ packet capture می‌تواند بسته‌های خام و در صورت نبود رمزنگاری payload را هم داشته باشد و از نظر حجم/حریم خصوصی پرهزینه‌تر است.', distractors=['Flow همیشه تمام payload رمزگشایی‌شده را ذخیره می‌کند','Packet capture فقط شمارندهٔ بایت دارد','این دو مفهوم کاملاً یکسان‌اند']),
 dict(ch=21, sub=4, topic='Graphing', en='Graphing', domain='Monitoring',
      summary='نمایش روند زمانی شاخص‌های تجهیز برای دیدن ظرفیت، الگوهای دوره‌ای و تغییرات غیرعادی.',
      why='نمودار یک مقدار لحظه‌ای را به روند تبدیل می‌کند؛ برای تشخیص اشباع لینک، افزایش تدریجی حافظه، افت availability یا اثر تغییر مفید است، اما کیفیت آن وابسته به بازهٔ نمونه‌گیری و نگهداری داده است.',
      concepts='metric، sampling interval، aggregation، retention، baseline، unit، counter rate، percentile و correlation زمانی.',
      mechanism='سامانه مقدارها را در بازه‌های زمانی نمونه‌برداری می‌کند، در صورت نیاز aggregate می‌کند و بر اساس retention نگه می‌دارد. نمودار counter باید معمولاً نرخ/اختلاف زمانی را نشان دهد، نه مقدار تجمعی خام را.',
      commands='''/tool graphing interface print
/tool graphing resource print
/tool graphing queue print
# syntax و دسترسی از WebFig/Winbox را مطابق نسخه و پیکربندی RouterOS بررسی کنید.''',
      example='اگر counter بایت در ۶۰ ثانیه ۶۰۰,۰۰۰,۰۰۰ بایت افزایش یابد، نرخ متوسط حدود ۸۰ Mbps است: 600,000,000 × 8 ÷ 60 = 80,000,000 bit/s.',
      lab='برای یک رابط آزمایشی نمودار بسازید یا مانیتورینگ موجود را بررسی کنید؛ ترافیک مصنوعی کنترل‌شده ایجاد کنید؛ نرخ نمودار را با counter و بازهٔ زمانی مقایسه کنید و بعد از آزمایش تنظیمات را بازگردانید.',
      issues='نمودار خالی: ویژگی/رابط انتخابی، سطح دسترسی و سرویس را بررسی کنید. قله‌های غیرواقعی: reboot، wrap counter، reset یا فاصلهٔ نمونه‌گیری را بررسی کنید. نمودار هموار اما incident کوتاه: resolution زمانی کافی نیست.',
      security='صفحهٔ graphing می‌تواند اطلاعات شبکه را آشکار کند؛ پنل‌های مدیریتی را محدود و دسترسی راه دور را امن کنید. retention را بر اساس نیاز عملیاتی و سیاست حریم خصوصی تنظیم کنید.',
      advanced='برای ظرفیت‌سنجی از baseline زمان اوج و روند بلندمدت استفاده کنید؛ میانگین به‌تنهایی قله‌ها را مخفی می‌کند. correlation با logها و تغییرات کمک می‌کند علت را از هم‌بستگی صرف جدا کنید.',
      glossary='Baseline: وضعیت مرجع؛ retention: مدت نگهداری؛ aggregation: تجمیع؛ resolution: تفکیک‌پذیری زمانی؛ correlation: هم‌بستگی.',
      question='چرا رسم مستقیم مقدار تجمعی counter به‌عنوان نرخ ترافیک می‌تواند گمراه‌کننده باشد؟', answer='counter تجمعی معمولاً با زمان افزایش می‌یابد؛ برای نرخ باید اختلاف counterها بر مدت زمان تقسیم شود و reboot/wrap نیز بررسی شود.', distractors=['چون counter همیشه واحد دما دارد','چون نرخ با تقسیم اختلاف بر زمان به دست می‌آید اما واحد اهم دارد','چون نمودار نمی‌تواند دادهٔ عددی نشان دهد']),
# Chapter 35 — PowerShell automation (chapter 35, subsection 3)
 dict(ch=35, sub=3, topic='Remoting', en='PowerShell Remoting', domain='Windows PowerShell',
      summary='اجرای فرمان یا تبادل داده با سیستم‌های Windows راه دور تحت سیاست احراز هویت و دسترسی سازمان.',
      why='PowerShell Remoting مدیریت چند سرور را بدون ورود تعاملی به هر میزبان ممکن می‌کند؛ پیش‌نیازهای WinRM، احراز هویت، firewall و policy باید پیش از اجرای فرمان بررسی شوند.',
      concepts='WinRM، WS-Management، PSSession، Invoke-Command، Kerberos، TrustedHosts در سناریوهای محدود، JEA و session configuration.',
      mechanism='کلاینت با endpoint راه دور احراز هویت می‌کند و فرمان را در session طرف مقابل اجرا می‌کند. در دامنهٔ Active Directory، Kerberos معمولاً از Basic/TrustedHosts امن‌تر و ساده‌تر برای هویت میزبان استفاده می‌کند؛ double-hop نیازمند طراحی جداگانه است.',
      commands='''# روی کلاینت مجاز
Test-WSMan -ComputerName server01.contoso.com
$session = New-PSSession -ComputerName server01.contoso.com -Authentication Kerberos
Invoke-Command -Session $session -ScriptBlock { Get-Service -Name WinRM }
Remove-PSSession $session''',
      example='نام server01.contoso.com نمونه است. ابتدا از endpoint و حساب مجاز استفاده کنید و یک فرمان خواندنی اجرا کنید؛ از فعال‌کردن گستردهٔ TrustedHosts یا Basic authentication برای حل فوری خطا پرهیز کنید.',
      lab='دو VM در یک شبکهٔ آزمایشی دامنه‌ای یا محیط محلی کنترل‌شده بسازید؛ WinRM را طبق راهنمای رسمی فعال کنید؛ Test-WSMan و سپس Get-Service را راه دور اجرا کنید؛ session را ببندید و logهای امنیتی را بررسی کنید.',
      issues='Access denied: عضویت گروه/endpoint policy را چک کنید. Cannot connect: DNS، WinRM listener، firewall و service. Kerberos error: ساعت، SPN و FQDN. double-hop: delegation یا طراحی امن انتقال credential را بررسی کنید.',
      security='از اجرای دستورات با Domain Admin برای همهٔ کارها پرهیز کنید. از JEA، حساب مدیریتی اختصاصی، TLS/ Kerberos، محدودسازی firewall و logging استفاده کنید؛ credential را در script یا transcript افشا نکنید.',
      advanced='برای چندمیزبانی، fan-out و throttle را محدود کنید، timeout بگذارید و نتایج هر میزبان را مستقل ثبت کنید. فرمان‌ها را idempotent کنید و پیش از change از inventory و canary استفاده کنید.',
      glossary='PSSession: نشست PowerShell؛ WinRM: سرویس مدیریت راه دور؛ Kerberos: پروتکل احراز هویت؛ JEA: Just Enough Administration؛ double-hop: دسترسی از سرور واسط به منبع دوم.',
      question='در یک محیط دامنه‌ای، برای Remoting معمولاً چرا استفاده از FQDN و Kerberos از اتصال مبتنی بر IP و TrustedHosts بهتر است؟', answer='FQDN به شناسایی سرویس/SPN و اعتبارسنجی هویت میزبان کمک می‌کند و Kerberos احراز هویت دامنه‌ای را فراهم می‌کند؛ TrustedHosts جایگزین عمومی اعتماد به هویت نیست.', distractors=['چون Kerberos رمز عبور را در متن ساده می‌فرستد','چون IP همیشه نام SPN را به صورت خودکار دارد','چون TrustedHosts همهٔ میزبان‌ها را به‌طور امن امضا می‌کند']),
 dict(ch=35, sub=3, topic='AD Module', en='Active Directory PowerShell Module', domain='Windows identity automation',
      summary='مدیریت خواندنی یا کنترل‌شدهٔ کاربران، گروه‌ها، OUها و ویژگی‌های Active Directory با cmdletهای استاندارد.',
      why='ماژول ActiveDirectory کارهای تکراری هویتی مانند گزارش عضویت گروه‌ها و ایجاد تغییرات دسته‌ای را استاندارد می‌کند؛ انتخاب اشتباه دامنه/OU یا فیلتر گسترده می‌تواند پیامدهای سازمانی داشته باشد.',
      concepts='Get-ADUser، Get-ADGroupMember، SearchBase، LDAP filter، Distinguished Name، WhatIf/Confirm، replication و delegation.',
      mechanism='Cmdletها درخواست‌های directory را از طریق AD Web Services/LDAP path پشتیبانی‌شده انجام می‌دهند و اشیاء را به صورت PowerShell object برمی‌گردانند. replication می‌تواند باعث تفاوت موقت بین DCها شود.',
      commands='''Import-Module ActiveDirectory
Get-ADUser -Filter * -SearchBase "OU=Lab,DC=example,DC=com" -Properties Enabled | Select-Object SamAccountName,Enabled
# قبل از تغییر دسته‌ای از -WhatIf استفاده کنید؛ پشتیبانی WhatIf به cmdlet وابسته است.''',
      example='example.com و OU=Lab دامنهٔ نمونه‌اند. گزارش را ابتدا در OU آزمایشگاهی بسازید و دامنه/بحث انتخابی را صریح کنید؛ عبارت -Filter * بدون SearchBase می‌تواند دامنهٔ بزرگی را برگرداند.',
      lab='یک OU و چند کاربر آزمایشی ایجاد کنید؛ فهرست کاربران Enabled را استخراج کنید؛ خروجی CSV را با تعداد مورد انتظار تطبیق دهید؛ تمرین تغییر وضعیت فقط روی حساب‌های lab و با WhatIf/بازبینی انجام شود.',
      issues='Module not found: RSAT/ویژگی ابزار مدیریتی و نسخهٔ سیستم. Access denied: delegation و scope. کاربر پیدا نشد: SearchBase/Filter/replication. نتیجهٔ زیاد: فیلتر دامنه و OU را محدود کنید.',
      security='از اصل کمترین امتیاز، OUهای جدا، تأیید تغییر گروه‌های حساس و ثبت ممیزی استفاده کنید. رمز عبور را در history/log ننویسید؛ عملیات انبوه را ابتدا به CSV خروجی و بازبینی محدود کنید.',
      advanced='تغییرات دسته‌ای را با دو مرحلهٔ plan/apply طراحی کنید: فهرست هدف‌ها را در فایل بازبینی‌شده تهیه و hash/تعداد آن را ثبت کنید؛ سپس اجرای تدریجی و verification بر اساس object GUID انجام دهید.',
      glossary='OU: واحد سازمانی؛ DN: Distinguished Name؛ LDAP filter: شرط جست‌وجوی directory؛ RSAT: ابزارهای مدیریت راه دور؛ DC: Domain Controller.',
      question='چرا برای گزارش یا تغییر دسته‌ای AD بهتر است SearchBase و فیلتر محدود داشته باشیم؟', answer='دامنهٔ عملیات را کاهش می‌دهد، از خواندن/تغییر ناخواستهٔ اشیای خارج از محدوده جلوگیری می‌کند و بازبینی نتایج را ممکن می‌سازد.', distractors=['زیرا SearchBase تمام کنترل‌های دسترسی را لغو می‌کند','چون فیلتر محدود replication را متوقف می‌کند','چون -Filter * همیشه فقط یک کاربر برمی‌گرداند']),
 dict(ch=35, sub=3, topic='Network Scripts', en='PowerShell Network Scripts', domain='Windows operations',
      summary='ساخت اسکریپت‌های شبکه برای جمع‌آوری پیکربندی، آزمون دسترسی و تولید گزارش قابل‌تکرار.',
      why='اسکریپت‌های PowerShell می‌توانند ipconfigهای دستی، تست پورت و گزارش DNS را به فرایندی تکرارپذیر با timestamp، خطایابی و خروجی CSV/JSON تبدیل کنند.',
      concepts='cmdlet، pipeline، object، Test-Connection، Test-NetConnection، Resolve-DnsName، Get-NetIPConfiguration، try/catch و structured output.',
      mechanism='PowerShell اشیاء .NET را میان cmdletها منتقل می‌کند؛ این با پردازش متن خام در batch متفاوت است. خروجی را بهتر است تا پایان به‌صورت object نگه دارید و سپس به CSV/JSON تبدیل کنید.',
      commands='''Get-NetIPConfiguration
Test-NetConnection -ComputerName example.com -Port 443
Resolve-DnsName example.com
Get-NetRoute -AddressFamily IPv4 | Sort-Object RouteMetric''',
      example='example.com برای نمایش است. Test-NetConnection -Port آزمون TCP است و معادل ping یا اثبات سلامت کامل وب‌اپلیکیشن نیست. برای گزارش سازمانی، timestamp و computername را همراه نتیجه ذخیره کنید.',
      lab='در Windows VM آدرس/route را استخراج کنید، DNS یک دامنهٔ آزمایشی را resolve کنید، اتصال TCP به پورت مجاز را بسنجید و نتیجه را به CSV بنویسید؛ سپس یک hostname اشتباه وارد و مدیریت خطا را اعتبارسنجی کنید.',
      issues='DNS failure: resolver و suffix. TCP fail: route/firewall/listener. نتیجهٔ نامعتبر: نام میزبان یا IPv4/IPv6. script متوقف می‌شود: try/catch، ErrorAction و بررسی nullها را طراحی کنید.',
      security='اسکن شبکه را فقط با مجوز محدوده انجام دهید؛ خروجی ممکن است شامل IP داخلی/نام میزبان باشد. ابزارهای تشخیصی destructive را به‌صورت پیش‌فرض اجرا نکنید و ورودی‌های کاربر را validate کنید.',
      advanced='مجموعه‌های چندصد میزبان نیازمند throttle، timeout، cancellation و خروجی یک نتیجه برای هر target هستند. جداسازی جمع‌آوری داده از تصمیم‌گیری remediate خطر اقدام کور را کم می‌کند.',
      glossary='Pipeline: زنجیرهٔ cmdletها؛ object: دادهٔ دارای ویژگی/متد؛ route metric: هزینهٔ مسیر؛ structured output: خروجی ساخت‌یافته؛ remediation: اصلاح.',
      question='آیا موفقیت Test-NetConnection روی پورت 443 ثابت می‌کند وب‌سایت کاملاً سالم است؟', answer='خیر؛ فقط برقراری اتصال TCP به مقصد/پورت را می‌سنجد؛ TLS، HTTP status، احراز هویت، backend و تجربهٔ کاربر آزمون‌های جدا دارند.', distractors=['بله، TCP موفق همهٔ لایه‌های برنامه را تأیید می‌کند','خیر، زیرا این cmdlet فقط DNS انجام می‌دهد','بله، حتی اگر DNS مقصد متفاوت باشد']),
 dict(ch=35, sub=3, topic='Scheduled Jobs', en='PowerShell Scheduled Jobs', domain='Windows automation',
      summary='اجرای دوره‌ای اسکریپت‌ها با Task Scheduler یا قابلیت‌های مناسب PowerShell، همراه با هویت اجرا و مانیتورینگ.',
      why='Job زمان‌بندی‌شده برای گزارش دوره‌ای، backup verify و health check مفید است؛ context اجرا با جلسهٔ تعاملی متفاوت است و مسیرها، credential، environment و دسترسی‌ها باید صریح شوند.',
      concepts='Task Scheduler، trigger، action، principal، working directory، execution policy، transcript/log، retry و exit code.',
      mechanism='Scheduler در زمان trigger برنامه/اسکریپت را با principal و تنظیمات مشخص اجرا می‌کند. فرایند زمان‌بندی‌شده معمولاً profile/driveهای map‌شدهٔ جلسهٔ کاربر را ندارد.',
      commands='''# مشاهدهٔ Taskها
Get-ScheduledTask | Select-Object TaskName,TaskPath,State
# اجرای دستی یک task آزمایشی
Start-ScheduledTask -TaskName "Lab-NetworkReport"
Get-ScheduledTaskInfo -TaskName "Lab-NetworkReport"''',
      example='نام task فقط نمونه است و باید در محیط آزمایش وجود داشته باشد. در Task Scheduler از مسیر مطلق powershell.exe، script path، working directory و log path استفاده کنید.',
      lab='یک task روزانه برای اجرای اسکریپت گزارش read-only در Windows VM بسازید؛ با Run دستی آزمایش کنید؛ LastRunTime/LastTaskResult و فایل log را بررسی کنید؛ سپس task را disable و حذف کنید.',
      issues='به صورت دستی کار می‌کند اما schedule نه: working directory، account، permissions، network credential، execution policy و environment را بررسی کنید. نتیجهٔ task: از Task Scheduler history و event log کمک بگیرید.',
      security='از ذخیرهٔ رمز در argument خط فرمان پرهیز کنید؛ اجرای task را با حساب service کم‌دسترسی انجام دهید؛ ACL اسکریپت و log را محدود کنید و روی رخدادهای شکست alert بگذارید.',
      advanced='از lock یا فایل marker برای جلوگیری از اجرای هم‌زمان استفاده کنید؛ timeout و exit code تعریف کنید؛ تغییرات را اول در staging/canary انجام دهید و schedule را در تقویم تغییرات ثبت کنید.',
      glossary='Trigger: محرک زمان‌بندی؛ principal: حساب اجرا؛ working directory: مسیر جاری؛ exit code: کد پایان؛ overlap: هم‌پوشانی اجرا.',
      question='چرا اسکریپت موفق در پنجرهٔ تعاملی ممکن است در Task Scheduler شکست بخورد؟', answer='زیرا حساب اجرا، مسیر جاری، profile، متغیرهای محیطی، credentialهای شبکه یا policy متفاوت‌اند؛ باید این موارد صریح و در log ثبت شوند.', distractors=['چون Task Scheduler فقط فایل‌های CSV را اجرا می‌کند','چون اجرای زمان‌بندی‌شده هیچ هویتی ندارد','چون PowerShell در task نمی‌تواند فایل بخواند']),
 dict(ch=35, sub=3, topic='DSC مقدماتی', en='Desired State Configuration', domain='Windows configuration management',
      summary='تعریف حالت مطلوب پیکربندی و سنجش/اعمال آن به‌جای اجرای مجموعه‌ای از تغییرات دستی غیرقابل‌ردیابی.',
      why='DSC و ابزارهای configuration management به استانداردسازی حالت سرورها کمک می‌کنند؛ syntax و موتور DSC بسته به نسل Windows PowerShell DSC یا مدل‌های جدید متفاوت است.',
      concepts='desired state، resource، configuration document، test/set/get، drift، MOF در DSC کلاسیک، و پیکربندی مبتنی بر agent/endpoint در نسخه‌های جدید.',
      mechanism='پیکربندی، وضعیت مورد انتظار را توصیف می‌کند؛ resource آن را با وضعیت فعلی مقایسه و در صورت مجاز بودن اصلاح می‌کند. نباید syntax کلاسیک DSC را بدون بررسی به نسخه/موتور جدید تعمیم داد.',
      commands='''# بررسی موتور/ماژول‌های موجود پیش از اجرای نمونه
$PSVersionTable
Get-Module -ListAvailable PSDesiredStateConfiguration
Get-Command -Module PSDesiredStateConfiguration -ErrorAction SilentlyContinue''',
      example='این نمونه عمداً read-only است و برای شناسایی نسخه و ماژول استفاده می‌شود. پیکربندی تغییردهنده را فقط با نسخهٔ مستندشده، resourceهای نصب‌شده و VM snapshot آزمایش کنید.',
      lab='در Windows VM نسخهٔ PowerShell و ماژول DSC را شناسایی کنید؛ یک resource رسمی و سازگار را در lab انتخاب کنید؛ ابتدا test/preview یا equivalent تشخیصی اجرا کنید؛ اعمال را پس از snapshot و ثبت rollback انجام دهید.',
      issues='Resource پیدا نمی‌شود: نسخه/ماژول. syntax معتبر نیست: موتور DSC متفاوت. drift مداوم: resource یا dependency با ابزار دیگری در حال تغییر است. نتیجه ناپایدار: حالت مطلوب دقیق یا idempotence ناقص است.',
      security='پیکربندی باید secret را از فایل عمومی جدا کند، دسترسی به اسناد/خروجی‌ها را محدود کند و تغییرهای امنیتی را با آزمون و rollback اعمال کند. پیکربندی سراسری بدون canary پرخطر است.',
      advanced='DSC را به‌عنوان حلقهٔ کنترل تنظیمات ببینید: declare → test → set → verify → report. مالکیت هر ویژگی را مشخص کنید تا دو automation engine برای یک setting وارد جنگ نشوند.',
      glossary='Desired state: حالت مطلوب؛ resource: واحد مدیریت تنظیم؛ drift: فاصلهٔ وضعیت واقعی از مطلوب؛ idempotence: اجرای تکراری بدون تغییر اضافی؛ canary: نمونهٔ کم‌ریسک.',
      question='اگر دو سامانهٔ خودکار یک setting را با مقدارهای متفاوت مدیریت کنند، چه اتفاقی محتمل است؟', answer='configuration drift و نوسان پیکربندی ایجاد می‌شود؛ باید برای هر setting مالک واحد تعریف یا سیاست ادغام روشن داشته باشیم.', distractors=['هر دو مقدار هم‌زمان ذخیره می‌شوند بدون تعارض','سرور به‌طور خودکار امن‌ترین مقدار را حدس می‌زند','DSC تمام ابزارهای دیگر را غیرفعال می‌کند']),
# Chapter 51.1 — Python network libraries
 dict(ch=51, sub=1, topic='Paramiko', en='Paramiko', domain='Python SSH',
      summary='استفاده از SSH در Python برای اتصال مدیریتی، اجرای فرمان و انتقال فایل با کنترل host key و timeout.',
      why='Paramiko پیاده‌سازی SSH برای Python است و امکان ساخت ابزارهای سفارشی را می‌دهد؛ برای عملیات چندفروشنده‌ای شبکه معمولاً باید parsing، paging و اختلاف CLI را خود برنامه مدیریت کند.',
      concepts='SSHClient، Transport، host key، known_hosts، authentication، channel، timeout، SFTP و مدیریت exception.',
      mechanism='کلاینت مذاکرهٔ SSH انجام می‌دهد، هویت سرور را با host key بررسی می‌کند، احراز هویت می‌شود و فرمان را از طریق channel اجرا می‌کند. خاموش‌کردن بررسی host key ریسک MITM می‌سازد.',
      commands='''python -m pip install paramiko
python - <<'PY'
import paramiko
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
client.connect("192.0.2.10", username="netops", key_filename="~/.ssh/id_ed25519", timeout=5, banner_timeout=5, auth_timeout=5)
stdin, stdout, stderr = client.exec_command("show version", timeout=10)
print(stdout.read().decode(errors="replace"))
print(stderr.read().decode(errors="replace"))
client.close()
PY''',
      example='دستور show version مثال روتر است و در همهٔ سیستم‌ها وجود ندارد؛ «192.0.2.10» آدرس مستنداتی است. host key را قبلاً از کانال مورداعتماد ثبت کنید و از AutoAddPolicy در اسکریپت عملیاتی استفاده نکنید مگر workflow اعتماد به میزبان به‌درستی مدیریت شده باشد.',
      lab='ابتدا به یک Linux VM شخصی با کلید SSH وصل شوید و hostname را بخوانید؛ بعد در صورت داشتن روتر lab، command read-only سازنده را اجرا کنید؛ خطای host key و timeout را کنترل‌شده بیازمایید و اتصال را در finally ببندید.',
      issues='Host key mismatch: تغییر واقعی یا حملهٔ احتمالی است؛ fingerprint را از کانال مجزا تأیید کنید. Authentication failed: key/agent/username. Hang: timeout برای connect و channel. خروجی خالی: فرمان سازنده یا مجوز را بررسی کنید.',
      security='کلید خصوصی را در repo نگذارید؛ از known_hosts معتبر، کلیدهای مجزا و حساب کم‌دسترسی استفاده کنید. خروجی فرمان ممکن است حاوی secrets باشد؛ logها را redact کنید و sessionها را حتماً ببندید.',
      advanced='برای تعداد زیادی دستگاه، concurrency محدود، backoff، pool مجزا و سقف زمانی کل عملیات را طراحی کنید. SSH CLI خروجی متنی دارد؛ parsing با regex شکننده است و باید نسخه/locale را لحاظ کند.',
      glossary='SSH: پوستهٔ امن؛ host key: کلید هویت سرور؛ MITM: حملهٔ واسط؛ channel: کانال SSH؛ SFTP: انتقال فایل روی SSH.',
      question='چرا RejectPolicy همراه با known_hosts برای اتوماسیون SSH انتخاب امن‌تری از قبول خودکار هر کلید است؟', answer='زیرا فقط میزبان‌هایی که هویت کلیدشان از قبل تأیید شده پذیرفته می‌شوند؛ قبول خودکار می‌تواند اتصال به میزبان جعلی را بدون هشدار بپذیرد.', distractors=['چون RejectPolicy رمزنگاری SSH را غیرفعال می‌کند','چون known_hosts رمز عبور را در متن ساده می‌نویسد','چون کلید میزبان هیچ نقشی در شناسایی سرور ندارد']),
 dict(ch=51, sub=1, topic='Netmiko', en='Netmiko', domain='Python network CLI automation',
      summary='ساده‌سازی اتصال SSH به تجهیزات شبکه و تعامل با CLI با درنظرگرفتن driverهای سازندگان.',
      why='Netmiko در مقایسه با SSH خام، الگوهای رایج CLI شبکه مانند ورود به enable mode، ارسال فرمان، انتظار prompt و جمع‌آوری خروجی را مدیریت می‌کند؛ سازگاری به device_type و نسخه بستگی دارد.',
      concepts='ConnectHandler، device_type، send_command، send_config_set، prompt matching، session log، global_delay_factor/timeoutهای نسخه‌محور و config mode.',
      mechanism='Netmiko بر لایه SSH تکیه می‌کند، prompt را شناسایی و فرمان را ارسال می‌کند؛ خروجی همچنان متن است و تغییرات CLI میان vendor/نسخه تفاوت دارد.',
      commands='''python -m pip install netmiko
'''
      , example='''from netmiko import ConnectHandler
from getpass import getpass

device = {
    "device_type": "cisco_ios",
    "host": "192.0.2.20",
    "username": "netops",
    "password": getpass("Password: "),
    "conn_timeout": 5,
}
with ConnectHandler(**device) as conn:
    output = conn.send_command("show version", read_timeout=20)
    print(output)''',
      lab='روی یک simulator/virtual lab یا دستگاه خودتان، ابتدا فقط فرمان show/version را اجرا کنید؛ session log را در فایل با دسترسی محدود ذخیره کنید؛ تغییر config را تنها در lab و پس از backup آزمایش کنید.',
      issues='Authentication/prompt mismatch: device_type، login banner و prompt. خروجی ناقص: read_timeout/paging. خطای enable: مجوز و enable secret. config ناقص: بررسی حالت CLI و نتیجهٔ هر فرمان.',
      security='رمز را در سورس ثابت ننویسید؛ password را با secret store/environment یا prompt بگیرید؛ خروجی session ممکن است محرمانه باشد؛ برای تغییرات از dry-run/تأیید و backup استفاده کنید.',
      advanced='برای عملیات fleet، به دستگاه‌ها دسته‌های کوچک بدهید، اتصال‌های موازی را محدود کنید و اولویت‌بندی fail-fast/canary داشته باشید. config push باید پس از اعمال با فرمان‌های show قابل راستی‌آزمایی شود.',
      glossary='Driver/device_type: پروفایل رفتار دستگاه؛ prompt: نشانگر ورودی CLI؛ paging: صفحه‌بندی خروجی؛ config mode: حالت پیکربندی؛ session log: گزارش نشست.',
      question='کدام کار Netmiko را از اجرای مستقیم یک رشته با SSH خام متمایز می‌کند؟', answer='پروفایل دستگاه و مدیریت تعامل‌های معمول CLI مانند prompt، config mode و ارسال فرمان را ساده می‌کند؛ با این حال خروجی هنوز متن است و نیاز به اعتبارسنجی دارد.', distractors=['Netmiko همهٔ مدل‌های دستگاه را بدون تعیین نوع خودکار می‌شناسد','Netmiko به SSH یا شبکه نیاز ندارد','Netmiko صحت تغییرات شبکه را بدون verification تضمین می‌کند']),
 dict(ch=51, sub=1, topic='NAPALM', en='NAPALM', domain='Multi-vendor network automation',
      summary='رابط یکپارچه برای برخی عملیات شبکه بین سیستم‌عامل‌های پشتیبانی‌شده، از جمله گرفتن facts، خواندن وضعیت و مدیریت candidate configuration.',
      why='NAPALM برای abstraction چندفروشنده‌ای و workflowهای config compare/commit مفید است؛ قابلیت‌ها و عملیات دقیق به driver، پلتفرم و نسخه وابسته‌اند و همهٔ سازندگان/فرمان‌ها برابر پوشش داده نمی‌شوند.',
      concepts='driver، get_facts، get_interfaces، get_config، load_merge_candidate، compare_config، commit_config، discard_config و rollback.',
      mechanism='کد driver متناسب با NOS انتخاب می‌شود و متدهای مشترک را از طریق transportهای مختلف پیاده‌سازی می‌کند. در محیطی که candidate config واقعی پشتیبانی نمی‌شود، رفتار و امکان rollback را باید جدا بررسی کرد.',
      commands='''python -m pip install napalm
''',
      example='''from napalm import get_network_driver
from getpass import getpass

driver = get_network_driver("ios")
device = driver(host="192.0.2.20", username="netops", password=getpass(), optional_args={})
try:
    device.open()
    facts = device.get_facts()
    print(facts.get("hostname"), facts.get("os_version"))
finally:
    device.close()''',
      lab='یک driver که صریحاً از دستگاه آزمایشی شما پشتیبانی می‌کند انتخاب کنید؛ ابتدا فقط get_facts/get_interfaces اجرا کنید؛ سپس در lab از config candidate استفاده و compare_config را قبل از commit بررسی کنید؛ rollback را عملاً آزمایش کنید.',
      issues='Driver not found: نام driver/extra package. Unsupported operation: بررسی support matrix. اتصال: transport/credentials. تفاوت config: normalize/replace-vs-merge و پشتیبانی device را بررسی کنید.',
      security='اعتبارنامه و دسترسی‌ها را محدود کنید؛ پیش از commit خروجی compare را بازبینی کنید؛ backup و session logs محرمانه‌اند. فرض نکنید commit یا rollback روی همه driverها رفتار یکسان دارد.',
      advanced='قابلیت abstraction را با ماتریس پوشش مشخص کنید: متدها، transport، مدل دستگاه و نسخهٔ NOS. برای تغییرات حیاتی از staged rollout، canary و verification مستقل از خود API استفاده کنید.',
      glossary='NOS: سیستم‌عامل شبکه؛ driver: پیاده‌سازی مخصوص پلتفرم؛ candidate config: پیکربندی پیشنهادی؛ commit: اعمال تغییر؛ rollback: بازگشت به وضعیت پیشین.',
      question='چرا باید پشتیبانی driver و روش commit/rollback را پیش از اتکای سازمانی به NAPALM بررسی کرد؟', answer='زیرا API یکپارچه الزاماً به معنی پوشش یکسان قابلیت‌ها نیست؛ متدها و transactional behavior به driver و پلتفرم بستگی دارند.', distractors=['چون NAPALM صرفاً برای مانیتورینگ CPU است','چون همهٔ driverها دقیقاً همهٔ قابلیت‌ها را پیاده‌سازی می‌کنند','چون rollback همیشه حتی روی تغییرات خارج از NAPALM تضمین است']),
 dict(ch=51, sub=1, topic='Scrapli', en='Scrapli', domain='Python network CLI automation',
      summary='تعامل CLI شبکه از Python با پشتیبانی از transportها و driverهای مناسب برای برخی پلتفرم‌ها.',
      why='Scrapli برای اتصال‌های CLI سریع و کنترل‌پذیر و الگوهای synchronous/asynchronous مفید است؛ انتخاب core/network driver و transport باید با دستگاه واقعی سازگار باشد.',
      concepts='Scrapli، platform driver، transport، channel، authentication، timeout_socket/transport/ops، response، privilege level و AsyncScrapli.',
      mechanism='کتابخانه نشست را از طریق transport ایجاد کرده، prompt/privilege را مدیریت می‌کند و responseهای فرمان را برمی‌گرداند. driver خاص شبکه معمولاً رفتار CLI را بهتر از generic driver می‌شناسد.',
      commands='''python -m pip install scrapli
''',
      example='''from getpass import getpass
from scrapli.driver.core import IOSXEDriver

device = {
    "host": "192.0.2.20", "auth_username": "netops",
    "auth_password": getpass(), "auth_strict_key": True,
    "transport": "system", "timeout_socket": 5,
}
with IOSXEDriver(**device) as conn:
    response = conn.send_command("show version")
    print(response.result)''',
      lab='روی شبیه‌ساز/روتر آزمایشی و driver دقیق همان NOS یک دستور read-only اجرا کنید؛ strict host key را حفظ کنید؛ timeout کوتاه را امتحان کنید و پاسخ/failed status را ذخیره کنید.',
      issues='Driver mismatch: platform/NOS version. host-key failure: fingerprint. command times out: prompt/paging/timeout. پشتیبانی transport: system/paramiko/ssh2 extras نصب‌شده را بررسی کنید.',
      security='auth_strict_key را بدون دلیل خاموش نکنید؛ secrets را در کد commit نکنید؛ پکیج‌ها را pin و update کنید؛ برای async هزاران اتصال را هم‌زمان باز نکنید.',
      advanced='Async می‌تواند throughput را افزایش دهد، اما محدودیت دستگاه، CPU، file descriptor و rate-limit را حذف نمی‌کند. semaphore، batch و per-host timeout بگذارید و نتایج را مستقل ذخیره کنید.',
      glossary='Transport: حامل ارتباط؛ async: اجرای ناهمگام؛ semaphore: سقف هم‌زمانی؛ response result: متن پاسخ؛ strict host key: الزام اعتبارسنجی هویت میزبان.',
      question='مزیت اجرای ناهمگام Scrapli چه چیزی را تضمین نمی‌کند؟', answer='می‌تواند زمان انتظار برای I/O چند دستگاه را بهتر مدیریت کند، اما تضمین نمی‌کند خود دستگاه ظرفیت اتصال نامحدود دارد یا تغییرات بدون verification امن‌اند.', distractors=['نیاز به محدودکردن هم‌زمانی را حذف می‌کند','احراز هویت را غیرضروری می‌کند','باعث می‌شود همهٔ فرمان‌ها در تمام vendorها یکسان باشند']),
 dict(ch=51, sub=1, topic='Requests API', en='Requests API', domain='Python HTTP APIs',
      summary='مصرف APIهای HTTP با Requests شامل timeout، بررسی status، TLS verification، JSON، session و مدیریت خطا.',
      why='بخش بزرگی از اتوماسیون از REST APIها استفاده می‌کند؛ کلاینت قابل‌اعتماد باید خطاهای HTTP/شبکه را تفکیک کند، timeout داشته باشد و صحت پاسخ را اعتبارسنجی کند.',
      concepts='GET/POST/PUT/PATCH/DELETE، status code، headers، JSON، Session، timeout connect/read، TLS certificate verification، retry و idempotent method.',
      mechanism='Requests روی HTTP/HTTPS کار می‌کند و پاسخ را شامل status، headers و body ارائه می‌دهد. `raise_for_status()` خطاهای HTTP 4xx/5xx را به exception تبدیل می‌کند ولی schema بدنه را باید جدا validate کرد.',
      commands='''python -m pip install requests
''',
      example='''import requests

with requests.Session() as session:
    response = session.get(
        "https://api.github.com/repos/psf/requests",
        timeout=(3.05, 10), verify=True,
    )
    response.raise_for_status()
    data = response.json()
    print(data.get("full_name"), response.status_code)''',
      lab='یک API عمومی یا endpoint در lab بخوانید؛ timeout را اجباری کنید؛ با URL نامعتبر و status خطا رفتار exception را بررسی کنید؛ برای API دارای احراز هویت از token آزمایشی با scope کم و environment استفاده کنید.',
      issues='Connect timeout: DNS/route/firewall. Read timeout: سرور کند. SSLError: CA/hostname; گواهی را خاموش نکنید. 401/403: scope و token. JSONDecodeError: پاسخ HTML/بدنهٔ خالی. 429: rate limit.',
      security='از HTTPS و verify=True استفاده کنید؛ token را در URL یا log ننویسید؛ redirectها را در endpoint حساس بررسی کنید؛ timeout و سقف پاسخ را تعیین کنید؛ retry در POST را بدون idempotency key طراحی نکنید.',
      advanced='برای APIهای پرترافیک Session، connection pooling و backoff با jitter مفید است. محدودیت نرخ، pagination، ETag و idempotency key را رعایت کنید و schema پاسخ را validate کنید.',
      glossary='REST: الگوی API مبتنی بر HTTP؛ status code: وضعیت پاسخ؛ Session: نشست با connection pooling؛ 429: Too Many Requests؛ pagination: صفحه‌بندی نتایج.',
      question='کدام مجموعهٔ کنترل برای درخواست HTTP عملیاتی مناسب‌تر است؟', answer='timeout، اعتبارسنجی گواهی TLS، بررسی status با raise_for_status، اعتبارسنجی محتوا و نگهداری امن token.', distractors=['timeout ندادن و retry نامحدود','غیرفعال‌کردن verify برای حل تمام TLS errorها','قرار دادن API token در query string و log کردن URL']),
# Chapter 51.2 — Infrastructure as Code
 dict(ch=51, sub=2, topic='Ansible Playbook', en='Ansible Playbook', domain='Network automation / IaC',
      summary='تعریف کارهای پیکربندی و اعتبارسنجی به‌شکل playbookهای تکرارپذیر، قابل‌بازبینی و قابل‌نسخه‌بندی.',
      why='Ansible کنترل‌نودمحور و معمولاً بدون agent برای بسیاری از عملیات شبکه و سیستم مناسب است؛ ماژول‌های شبکه با ماژول‌های Linux/Windows متفاوت‌اند و باید collection و connection plugin درست انتخاب شوند.',
      concepts='control node، managed node، inventory، play، task، module، collection، vars، handlers، check mode، diff و vault.',
      mechanism='Ansible inventory را می‌خواند، taskها را به ترتیب اجرا و خروجی هر host را گزارش می‌کند. برای تجهیزات شبکه معمولاً اتصال SSH/HTTPS و ماژول اختصاصی پلتفرم لازم است؛ idempotency به خود ماژول و طراحی task وابسته است.',
      commands='''ansible --version
ansible-inventory -i inventory.yml --list
ansible-playbook -i inventory.yml site.yml --syntax-check
ansible-playbook -i inventory.yml site.yml --check --diff''',
      example='''# playbook نمونهٔ read-only؛ ماژول دقیق را با collection پلتفرم تطبیق دهید
- name: Collect network facts
  hosts: lab_routers
  gather_facts: false
  tasks:
    - name: Query device facts
      ansible.builtin.debug:
        msg: "اجرای واقعی facts به ماژول پلتفرم وابسته است"''',
      lab='یک inventory با یک دستگاه آزمایشی بسازید؛ ابتدا ansible-inventory و syntax-check را اجرا کنید؛ سپس یک task فقط‌خواندنی اجرا کنید؛ اگر --check برای ماژول هدف پشتیبانی می‌شود، خروجی plan را پیش از تغییر واقعی بررسی کنید.',
      issues='Unreachable: transport/credential/ACL. module not found: collection نصب یا FQCN اشتباه. Variable undefined: scope نامناسب. تغییر ناخواسته: check mode محدودیت دارد و پشتیبانی ماژول باید بررسی شود.',
      security='اسرار را در Ansible Vault یا secret manager نگه دارید؛ inventory و playbook به‌عنوان کد حساس review شوند؛ privilege escalation و host pattern را محدود کنید؛ --limit و canary را پیش از fleet-wide change به کار ببرید.',
      advanced='نقش‌ها و collectionها را pin کنید؛ ساختار role/defaults/vars را جدا کنید؛ handlerها و serial/max_fail_percentage را برای کاهش blast radius طراحی کنید؛ نتیجه را با ابزار مستقل verify کنید.',
      glossary='Playbook: تعریف کارها؛ inventory: فهرست میزبان؛ collection: بستهٔ ماژول‌ها/roleها؛ FQCN: نام کامل ماژول؛ check mode: شبیه‌سازی پشتیبانی‌شده؛ blast radius: دامنهٔ اثر خرابی.',
      question='آیا `--check --diff` تضمین می‌کند هیچ تغییری اعمال نمی‌شود و همهٔ ماژول‌ها را به‌درستی شبیه‌سازی می‌کند؟', answer='خیر؛ check mode به پشتیبانی ماژول و task وابسته است و ممکن است همهٔ اثرها را مدل نکند. باید مستندات ماژول و خروجی را بررسی و در staging آزمایش کرد.', distractors=['بله، در هر ماژول و هر نسخه کامل و قطعی است','بله، چون check mode دسترسی به inventory را می‌بندد','خیر، زیرا Ansible اصلاً حالت check ندارد']),
 dict(ch=51, sub=2, topic='Inventory', en='Ansible Inventory', domain='Automation source of truth',
      summary='مدل‌کردن دستگاه‌ها، گروه‌ها، متغیرهای اتصال و محدودهٔ اجرای playbook به‌صورت inventory ساخت‌یافته.',
      why='Inventory مرکز کنترل دامنهٔ اجراست: گروه‌بندی بر اساس platform, site و environment امکان اجرای یک workflow روی تجهیزات منتخب را می‌دهد و اشتباه در group/host pattern می‌تواند کل ناوگان را تغییر دهد.',
      concepts='INI/YAML inventory، hosts، children، group_vars، host_vars، ansible_host، ansible_connection، ansible_network_os و ansible-vault.',
      mechanism='Ansible inventory را به گرافی از hostها و گروه‌ها تبدیل می‌کند و متغیرها از سطوح مختلف ادغام می‌شوند. precedence متغیرها مهم است؛ نام گروه و الگوی هدف را قبل از apply فهرست کنید.',
      commands='''ansible-inventory -i inventory.yml --graph
ansible-inventory -i inventory.yml --host lab-sw1
ansible all -i inventory.yml --list-hosts
ansible-playbook -i inventory.yml site.yml --list-hosts''',
      example='''all:
  children:
    lab_routers:
      hosts:
        rtr-lab-01:
          ansible_host: 192.0.2.21
          ansible_connection: ansible.netcommon.network_cli
          ansible_network_os: cisco.ios.ios
''',
      lab='inventory YAML را برای یک دستگاه ساختگی/آزمایشگاهی بسازید؛ graph و --list-hosts را اجرا کنید؛ با تغییر یک group pattern بررسی کنید دامنه دقیقاً چه hostهایی است؛ secrets را از فایل ساده جدا کنید.',
      issues='Host not found: ساختار YAML/indentation. اتصال به IP غلط: ansible_host. متغیر نادیده گرفته شده: precedence، spelling یا سطح group_vars. اجرای بیش‌ازحد: pattern و children را قبل از command بررسی کنید.',
      security='رمزها را در inventory plaintext نگذارید؛ vault/secret manager استفاده کنید؛ فایل inventory را مثل فهرست asset حساس حفاظت کنید؛ محیط‌های dev/stage/prod را جدا و محدودیت در pipeline اعمال کنید.',
      advanced='برای ناوگان بزرگ از dynamic inventory با source قابل‌اعتماد، cache محدود و validation استفاده کنید. دسته‌بندی را هم بر اساس پلتفرم و هم مکان/محیط طراحی کنید و تغییرات inventory را در Git review کنید.',
      glossary='Host pattern: انتخاب میزبان؛ group_vars: متغیر گروه؛ host_vars: متغیر میزبان؛ dynamic inventory: تولید خودکار فهرست؛ precedence: اولویت اعمال متغیر.',
      question='چرا اجرای `ansible-playbook` بدون کنترل فهرست میزبان‌ها قبل از تغییر پرخطر است؟', answer='زیرا inventory و pattern تعیین می‌کنند چند و کدام دستگاه‌ها هدف قرار می‌گیرند؛ اشتباه در گروه‌ها می‌تواند تغییر را به production گسترش دهد.', distractors=['چون inventory فقط نام نمایشی دارد و بر اجرا اثری ندارد','چون pattern هیچ‌وقت گروه‌ها را گسترش نمی‌دهد','چون Ansible همیشه فقط اولین host را تغییر می‌دهد']),
 dict(ch=51, sub=2, topic='Terraform State', en='Terraform State', domain='Infrastructure as Code',
      summary='درک فایل/بک‌اند state به‌عنوان پیوند بین resourceهای تعریف‌شده و منابع واقعی، همراه با قفل، دسترسی و بازیابی.',
      why='Terraform state به Terraform کمک می‌کند resourceهای پیکربندی را به resourceهای واقعی نگاشت کند و تصمیم بگیرد چه تغییراتی لازم است؛ گم‌شدن یا افشای state می‌تواند باعث drift، دوباره‌سازی یا افشای secret شود.',
      concepts='resource address، state mapping، local/remote backend، locking، workspace، plan/apply، import، state list/show/pull و state backup.',
      mechanism='Terraform وضعیت resourceها و شناسه‌های آن‌ها را در state نگه می‌دارد. backend ممکن است locking و همکاری تیمی فراهم کند؛ فایل state را دستی ویرایش نکنید و از دستورات `terraform state` استفاده کنید.',
      commands='''terraform init
terraform validate
terraform plan
terraform state list
terraform state show 'example_resource.demo'
# دستورات بالا را فقط در دایرکتوری پیکربندی آزمایشی اجرا کنید.''',
      example='`terraform plan` تغییر پیشنهادی را پیش از `apply` نمایش می‌دهد. آدرس `example_resource.demo` صرفاً الگو است و باید با resource واقعی پیکربندی جایگزین شود.',
      lab='یک پروژه Terraform آزمایشگاهی با resource محلی یا provider تمرینی بسازید؛ init/validate/plan را اجرا کنید؛ state list/show را بخوانید؛ برای backend remote، locking/ACL/backup را طبق راهنمای backend بررسی کنید.',
      issues='State lock: عملیات هم‌زمان یا lock قدیمی را با تشخیص مالکیت بررسی کنید؛ هرگز کورکورانه force-unlock نکنید. Resource drift: plan و refresh رفتار نسخه را بررسی کنید. State missing: از backend/backup مطمئن و recovery plan استفاده کنید.',
      security='state ممکن است secret و دادهٔ حساس داشته باشد؛ آن را در Git یا storage بدون ACL/locking قرار ندهید. دسترسی محدود، encryption، backup و audit ضروری‌اند؛ دستورات state modify باید review شوند.',
      advanced='برای تیم، remote backend با کنترل دسترسی و locking را بر فایل مشترک ترجیح دهید. import و state mv/rm فقط بر اساس نقشهٔ دقیق resource address و backup باید اجرا شود.',
      glossary='State: نگاشت وضعیت؛ backend: محل ذخیره state؛ locking: جلوگیری از تغییر هم‌زمان؛ drift: اختلاف واقعیت با کد؛ import: اتصال resource موجود به مدیریت Terraform.',
      question='چرا نباید فایل `terraform.tfstate` را مستقیم ویرایش یا در مخزن عمومی commit کرد؟', answer='ویرایش مستقیم می‌تواند نگاشت داخلی را خراب کند؛ فایل state ممکن است دادهٔ حساس داشته باشد و مخزن عمومی خطر افشا ایجاد می‌کند. از فرمان‌های state و backend امن استفاده کنید.', distractors=['چون state فقط متن توضیحی است و اهمیت ندارد','چون Terraform هیچ‌وقت state را نمی‌خواند','چون Git از هر نوع secret در فایل به‌طور خودکار محافظت می‌کند']),
 dict(ch=51, sub=2, topic='Git Workflow', en='Git Workflow for Automation', domain='Version control',
      summary='مدیریت تغییرات اسکریپت، inventory و playbook با commitهای کوچک، review، branch و نسخه‌بندی قابل‌ردیابی.',
      why='زیرساخت به‌عنوان کد نیازمند provenance و امکان مقایسه/بازگردانی است. Git تاریخچهٔ تغییر را نگه می‌دارد ولی backup از secret یا اعتبارسنجی صحت اجرا را به‌تنهایی انجام نمی‌دهد.',
      concepts='repository، working tree، staging، commit، branch، merge/pull request، tag، diff، revert، ignore و secret scanning.',
      mechanism='تغییرها در diff مرور می‌شوند و commitها نقطهٔ قابل‌ارجاع برای pipeline و گزارش تغییر می‌سازند. branch policy و code review به‌ویژه قبل از اتصال pipeline به تجهیزات production اهمیت دارد.',
      commands='''git status
git diff --check
git diff --staged
git switch -c change/lab-snmp
git add playbooks/ inventory/
git commit -m "Add read-only lab network check"
git log --oneline --decorate -10''',
      example='قبل از `git add` فایل‌های شامل credential یا state را بررسی کنید. `.gitignore` مانع commit فایل‌های از قبل tracked نمی‌شود و پاک‌کردن secret از آخرین commit لزوماً آن را از تاریخچه حذف نمی‌کند.',
      lab='یک repository محلی بسازید، یک inventory آزمایشی بدون secret commit کنید، تغییر کوچک انجام دهید، diff و commit را بازبینی و سپس revert را در branch تمرینی آزمایش کنید.',
      issues='Secret accidentally committed: credential را revoke/rotate کنید و history remediation انجام دهید. Merge conflict: conflict markers را حل و تست کنید. Diff خالی: فایل tracked/ignore را بررسی کنید.',
      security='secret را هرگز با صرفاً اضافه‌کردن به .gitignore ایمن فرض نکنید. secret scanning، protected branch، حداقل reviewer و دسترسی repo را فعال کنید؛ لاگ CI نیز ممکن است secret را چاپ کند.',
      advanced='commit را با issue/change ticket پیوند دهید؛ artifactهای build را reproducible و نسخه‌های dependency را pin کنید؛ tag/commit hash اجراشده را در گزارش استقرار نگه دارید.',
      glossary='Working tree: فایل‌های درحال‌تغییر؛ staging: آماده‌سازی commit؛ revert: commit جبرانی؛ branch protection: سیاست محافظت branch؛ provenance: منشأ قابل‌ردیابی.',
      question='پس از commit شدن یک token واقعی، چرا فقط حذف آن از فایل کافی نیست؟', answer='چون token ممکن است در تاریخچهٔ Git، cloneها، cache و logها باقی بماند؛ باید token را revoke/rotate و تاریخچه/کپی‌ها را طبق رویهٔ سازمانی پاکسازی کرد.', distractors=['چون Git فقط نسخهٔ فعلی فایل را نگه می‌دارد','چون .gitignore به‌طور خودکار تمام تاریخچه را رمز می‌کند','چون token پس از commit خودبه‌خود منقضی می‌شود']),
 dict(ch=51, sub=2, topic='CI برای شبکه', en='CI for Network Automation', domain='CI/CD',
      summary='اجرای خودکار lint، تست، اعتبارسنجی inventory و بررسی تغییرات پیش از اجازهٔ استقرار شبکه.',
      why='CI می‌تواند خطاهای syntax و قرارداد داده را پیش از رسیدن به دستگاه کشف کند. pipeline موفق، به‌تنهایی صحت پیکربندی روی تجهیزات و دسترس‌پذیری کسب‌وکار را تضمین نمی‌کند.',
      concepts='pipeline، trigger، runner، lint، unit/integration test، artifact، secret store، approval gate، environment protection و deployment stage.',
      mechanism='تغییر Git یک job را trigger می‌کند؛ runner ابزارهای ثابت‌شده را اجرا کرده و گزارش تولید می‌کند. Secret و دسترسی deployment باید فقط به job/branch مجاز داده شود و تست‌های destructive در runner ایزوله باشند.',
      commands='''python -m compileall -q scripts/
python -m unittest discover -s tests -v
ansible-playbook -i inventory/lab.yml site.yml --syntax-check
terraform -chdir=infra/lab validate''',
      example='فرمان Terraform فقط وقتی اجراشدنی است که دایرکتوری مذکور پیکربندی مناسب داشته باشد؛ syntax-check و validate را در lab نگه دارید و `apply` خودکار را بدون approval، state locking و scope محدود به production وصل نکنید.',
      lab='pipeline محلی/CI بسازید که compileall، unit test، inventory validation و syntax check را اجرا کند؛ یک خطای عمدی syntax ایجاد کنید و شکست pipeline را ببینید؛ deployment واقعی در این آزمایش غیرفعال بماند.',
      issues='Runner lacks dependencies: نسخه و cache پکیج. Secret missing: scope/environment. False green: assertion ضعیف یا test skip. Flaky tests: race/target mutable. Pipeline broad privileges: token/runner scope را بررسی کنید.',
      security='runner را با مجوز حداقلی و ترجیحاً ephemeral اجرا کنید؛ secretها را در logs mask کنید؛ pull request غیرقابل‌اعتماد را به credential production وصل نکنید؛ approval و protected environments را برای apply اعمال کنید.',
      advanced='تفکیک validate → plan → approval → staged deploy → verify → rollback را پیاده کنید. خروجی plan، commit SHA، نسخهٔ toolchain و تغییر هدف را artifact کنید و شکست هر مرحله را alert بدهید.',
      glossary='CI: یکپارچه‌سازی پیوسته؛ runner: عامل اجرای job؛ artifact: خروجی ذخیره‌شده؛ gate: شرط عبور؛ flaky test: تست ناپایدار؛ ephemeral: موقت و دورریختنی.',
      question='کدام مرحله باید پیش از اعمال تغییر شبکه در production قرار بگیرد؟', answer='اعتبارسنجی، بازبینی plan/diff، تأیید مالک تغییر، استقرار مرحله‌ای و بررسی مستقل خروجی؛ pipeline سبز به تنهایی برای apply بی‌قیدوشرط کافی نیست.', distractors=['اجرای apply روی تمام دستگاه‌ها بلافاصله پس از هر push','حذف تست‌ها برای سریع‌ترشدن pipeline','دادن secret دائمی production به همهٔ runnerها']),
# Chapter 51.3 — AI for IT
 dict(ch=51, sub=3, topic='ChatOps', en='ChatOps', domain='AI-assisted operations',
      summary='طراحی رابط چت برای اجرای فرمان‌های عملیاتی کنترل‌شده با احراز هویت، مجوز، تأیید و ثبت ممیزی.',
      why='ChatOps می‌تواند دسترسی به runbook و مشاهدهٔ وضعیت را آسان کند، اما پیام چت نباید مستقیماً به فرمان shell/router تبدیل شود؛ هر عملیات باید از catalog ازپیش‌تعریف‌شده عبور کند.',
      concepts='chat adapter، identity mapping، command catalog، authorization، approval workflow، audit trail، idempotency key و policy enforcement.',
      mechanism='پیام کاربر به intent محدود/ساخت‌یافته تبدیل می‌شود؛ هویت و scope بررسی می‌شود؛ برای action حساس تأیید گرفته می‌شود؛ worker مجاز action را اجرا می‌کند و نتیجه/شناسهٔ رخداد ثبت می‌شود. مدل زبانی منبع authority نیست.',
      commands='''# الگوی امن: API عملیاتی از پیش‌تعریف‌شده، نه اجرای متن آزاد shell
POST /ops/v1/health-check
Content-Type: application/json
{"target":"lab-router-01","action":"read_only_health","request_id":"change-123"}''',
      example='«وضعیت روتر آزمایشگاه را نشان بده» می‌تواند به action ثابت `read_only_health` نگاشت شود. درخواست «هرچه لازم است firewall را تغییر بده» باید رد یا به گردش‌کار تأییدشده تبدیل شود.',
      lab='یک prototype محلی بسازید که فقط دو action read-only از catalog می‌پذیرد؛ هویت ساختگی کاربر، مجوز ردشده، approval و audit log را آزمایش کنید؛ اجرای shell آزاد و اتصال به دستگاه واقعی غیرفعال باشد.',
      issues='Action اشتباه: intent به allowlist محدود شود. Replay: request_id/idempotency. بدون هویت: fail closed. پاسخ غلط مدل: منبع نتیجهٔ ماشینی و timestamp را جدا نشان دهید؛ مدل را مرجع حقیقت ندانید.',
      security='هیچ secret یا command آزاد را از پیام مدل عبور ندهید؛ prompt injection را فرض محتمل بدانید؛ کمترین دسترسی، allowlist، rate limit، human approval و audit لازم است. پیام‌های چت ممکن است دادهٔ حساس نگه دارند.',
      advanced='policy enforcement را خارج از مدل زبانی نگه دارید؛ مدل فقط پیشنهاد یا پارامترهای schema شده تولید کند. approval باید با هویت و hash دقیق plan پیوند بخورد تا بین preview و apply تغییر رخ ندهد.',
      glossary='ChatOps: عملیات از طریق چت؛ allowlist: فهرست مجاز؛ prompt injection: دستکاری ورودی مدل؛ fail closed: رد در صورت ابهام؛ audit trail: سابقهٔ ممیزی.',
      question='در یک سامانه ChatOps، چه چیزی باید اختیار نهایی اجرای تغییر را داشته باشد؟', answer='موتور policy، هویت/مجوز، allowlist عملیات و workflow تأیید؛ مدل زبان می‌تواند پیشنهاد بدهد اما نباید به‌تنهایی اختیار اجرای action پرخطر را داشته باشد.', distractors=['صرفاً متن پاسخ مدل زبانی','هر کاربری که بتواند به کانال چت پیام بدهد','محتوای خروجی لاگ بدون بررسی هویت']),
 dict(ch=51, sub=3, topic='RAG روی مستندات', en='RAG for IT Documentation', domain='Retrieval-augmented generation',
      summary='بازیابی قطعه‌های مرتبط از اسناد داخلی و استفاده از آن‌ها در پاسخ مدل، همراه با citation و کنترل دسترسی.',
      why='RAG به مدل کمک می‌کند پاسخ را به runbookها، استانداردها و اسناد سازمانی متصل کند؛ کیفیت وابسته به retrieval، تازگی سند، صلاحیت منبع و ACL است و retrieval به‌خودی‌خود حقیقت را تضمین نمی‌کند.',
      concepts='ingestion، chunking، embedding، vector index، metadata filter، retrieval، reranking، grounding، citation، freshness و access control.',
      mechanism='سند به قطعه‌ها تقسیم و نمایه‌سازی می‌شود؛ query کاربر به قطعه‌های مرتبط بازیابی می‌شود؛ مدل پاسخ را با زمینهٔ بازیابی‌شده می‌سازد. مجوز باید پیش از بازگرداندن قطعه اعمال شود، نه فقط بعد از تولید پاسخ.',
      commands='''# طرح سادهٔ pipeline
1. ingest approved documents
2. preserve source_id, version, timestamp, ACL metadata
3. retrieve authorized chunks for query
4. generate answer with citations to chunk IDs
5. validate citations and refuse when evidence is missing''',
      example='پاسخ «چگونه VPN سایت را بازیابی کنم؟» باید به نسخهٔ مصوب runbook و تاریخ آن ارجاع دهد و هر مرحلهٔ پرخطر را از متن بازیابی‌شده جدا و نیازمند تأیید نشان دهد.',
      lab='سه سند آزمایشی با version و ACL متفاوت بسازید؛ سؤال مجاز و غیرمجاز بپرسید؛ بررسی کنید نتیجه citation سند، نسخه و بخش داشته باشد؛ یک سؤال بدون مدرک بسازید و رفتار abstain را کنترل کنید.',
      issues='پاسخ بدون citation: grounding validator. اسناد قدیمی: freshness/retention. نشت سند محدود: ACL در retrieval. chunk نامرتبط: اندازه و overlap/metadata. hallucination: abstention و cross-check منبع.',
      security='متن سند ممکن است prompt injection مخرب داشته باشد؛ اسناد را دادهٔ غیرقابل‌اعتماد تلقی کنید. ACL، tenant separation، redaction داده‌های حساس و ثبت منبع الزامی است.',
      advanced='ارزیابی offline برای recall/precision retrieval، صحت citation و نرخ abstention طراحی کنید. versioning و حذف tombstone اسناد قدیمی را مدیریت کنید و retrieval و generation را جدا اندازه بگیرید.',
      glossary='RAG: تولید تقویت‌شده با بازیابی؛ embedding: نمایش برداری؛ chunk: قطعه سند؛ grounding: اتکا به منبع؛ reranking: رتبه‌بندی دوباره؛ abstention: امتناع هنگام نبود شواهد.',
      question='چرا باید مجوز سند قبل از تحویل قطعه به مدل اعمال شود؟', answer='زیرا اگر سند غیرمجاز وارد زمینه شود، مدل می‌تواند اطلاعات آن را افشا کند؛ پنهان‌کردن citation در خروجی نشت داده را برطرف نمی‌کند.', distractors=['چون ACL فقط ظاهر نتیجه را تغییر می‌دهد','چون embeddingها همیشه داده را ناشناس می‌کنند','چون مدل هرگز متن بازیابی‌شده را بازگو نمی‌کند']),
 dict(ch=51, sub=3, topic='Ollama محلی', en='Local Ollama Models', domain='Local AI operations',
      summary='اجرای مدل‌های زبانی محلی از طریق Ollama برای کارهای آزمایشی/سازمانی، همراه با کنترل منابع و داده.',
      why='اجرای محلی می‌تواند ارسال prompt به یک سرویس خارجی را کاهش دهد، اما لزوماً خطر حریم خصوصی را صفر یا پاسخ را دقیق نمی‌کند؛ مدل، کتابخانه، prompt، log و endpoint باید مدیریت شوند.',
      concepts='model tag، pull/run، local HTTP API، context length، quantization، GPU/CPU RAM، concurrency، model provenance و network binding.',
      mechanism='سرویس محلی مدل را مدیریت و درخواست‌های HTTP را به inference runtime می‌دهد. منابع مورد نیاز به اندازه/quantization/context بستگی دارد؛ مدل محلی همچنان ممکن است prompt injection را بپذیرد یا hallucinate کند.',
      commands='''ollama --version
ollama list
ollama pull llama3.2
ollama run llama3.2
# نام مدل نمونه است؛ نیازمندی، مجوز و hash/tag مدل را قبل از استفاده بررسی کنید.''',
      example='پس از pull کردن مدل مجاز، یک prompt بدون دادهٔ حساس اجرا کنید؛ نسخهٔ مدل و زمان پاسخ را ثبت کنید؛ endpoint مدیریت را به شبکهٔ عمومی bind نکنید.',
      lab='روی رایانهٔ آزمایشی Ollama نصب و نسخه را ثبت کنید؛ یک مدل مناسب منابع را pull کنید؛ prompt کوچک و غیرحساس بفرستید؛ CPU/RAM/زمان را بسنجید؛ اتصال شبکه‌ای غیرضروری را مسدود کنید.',
      issues='Out of memory: مدل کوچک‌تر یا context کوتاه‌تر. API unavailable: سرویس/port. پاسخ کند: CPU/GPU, parallel requests. مدل پیدا نیست: tag. خروجی نادرست: ارزیابی و citation؛ صرف local بودن تضمین صحت نیست.',
      security='مدل و وابستگی‌ها را از منبع معتبر دریافت کنید؛ API محلی ممکن است احراز هویت پیش‌فرض نداشته باشد، پس دسترسی bind/firewall را محدود کنید؛ prompt/log شامل اسرار نشود و لایسنس مدل را بررسی کنید.',
      advanced='برای مقایسهٔ مدل‌ها کیفیت وظیفه، latency، حافظه، مصرف انرژی و license را بسنجید. نسخه و checksum/provenance را pin کنید و مدل را از ابزارهای عملیاتی حساس جدا نگه دارید.',
      glossary='Inference: تولید خروجی؛ quantization: کاهش دقت عددی برای کاهش منابع؛ context length: پنجره زمینه؛ model tag: شناسه نسخه مدل؛ provenance: منشأ مدل.',
      question='کدام جمله دربارهٔ مدل محلی درست‌تر است؟', answer='مدل محلی می‌تواند نیاز به ارسال داده به سرویس بیرونی را کاهش دهد، اما به‌خودی‌خود صحت، امنیت endpoint، مجوز مدل یا عدم ثبت log را تضمین نمی‌کند.', distractors=['اجرای محلی hallucination را ناممکن می‌کند','API محلی همیشه به‌صورت پیش‌فرض احراز هویت و TLS دارد','هر مدل محلی برای استفادهٔ تجاری مجوز نامحدود دارد']),
 dict(ch=51, sub=3, topic='Anomaly Detection مانیتورینگ', en='Anomaly Detection for Monitoring', domain='Observability and data analysis',
      summary='شناسایی رفتار غیرمعمول متریک‌ها با baseline، آستانه‌های پویا و روش‌های آماری، همراه با کنترل false positive.',
      why='دادهٔ متریک شبکه فصل‌پذیر، پرنویز و دارای تغییرات برنامه‌ریزی‌شده است. تشخیص anomaly باید context عملیاتی، کیفیت داده و هزینهٔ مثبت/منفی کاذب را در نظر بگیرد.',
      concepts='baseline، moving average، standard deviation، seasonality، change point، false positive/negative، precision/recall و alert fatigue.',
      mechanism='داده timestamp و labelدار پاکسازی می‌شود؛ baseline آموزش/محاسبه شده و score یا residual با آستانه مقایسه می‌شود؛ رخداد به alert/triage متصل می‌شود. مفهوم anomaly به معنی incident قطعی نیست.',
      commands='''# حداقل تحلیل قابل‌تکرار در Python
import statistics
values = [22, 24, 23, 25, 24, 80]  # دادهٔ ساختگی
baseline = statistics.mean(values[:-1])
print("baseline:", baseline, "latest:", values[-1], "delta:", values[-1] - baseline)''',
      example='در نمونه، 80 نسبت به مشاهدات قبلی بالاتر است، اما قبل از ایجاد Incident باید بدانیم متریک چیست، واحد آن چیست، آیا maintenance بوده و آیا data gap وجود داشته است.',
      lab='CSV ساختگی دارای timestamp و metric بسازید؛ مقدارهای گمشده/تکراری را پاکسازی کنید؛ baseline ساده و آستانه را محاسبه کنید؛ چند incident ساختگی و maintenance window اضافه کنید و precision/false positive را بشمارید.',
      issues='هشدارهای زیاد: فصل‌پذیری و threshold. anomaly گم‌شده: sampling/data quality. تغییر schema: label/unit. baseline آلوده به رخداد: training window را بازبینی کنید. مدل drift: دورهٔ ارزیابی مجدد تعریف کنید.',
      security='از دادهٔ مانیتورینگ ممکن است نام میزبان/کاربر/توپولوژی افشا شود؛ دسترسی، retention و masking را کنترل کنید. تصمیم خودکار مخرب را صرفاً از anomaly score نگیرند.',
      advanced='نسبت به threshold ثابت، seasonality، robust statistics و مدل change-point را ارزیابی کنید. معیار ارزیابی را روی رخدادهای برچسب‌خورده و با هزینهٔ alert تعیین کنید؛ model drift و data drift جدا سنجیده شوند.',
      glossary='Anomaly: ناهنجاری؛ baseline: خط مبنا؛ seasonality: الگوی فصلی؛ precision: سهم هشدارهای درست؛ recall: سهم رخدادهای پیدا شده؛ drift: تغییر توزیع داده.',
      question='چرا افزایش ناگهانی یک متریک نباید به‌طور خودکار باعث restart یا تغییر تنظیمات شود؟', answer='چون ناهنجاری فقط سیگنال برای بررسی است و ممکن است ناشی از maintenance، خطای سنجش یا بار واقعی مجاز باشد؛ ابتدا شواهد و تأثیر بررسی و سپس با policy محدود عمل شود.', distractors=['چون متریک‌ها هیچ ارزش عملیاتی ندارند','چون همهٔ anomalyها مثبت کاذب هستند','چون restart همیشه بی‌خطر است']),
 dict(ch=51, sub=3, topic='تولید Runbook با AI', en='AI-assisted Runbook Authoring', domain='Operational knowledge engineering',
      summary='کمک‌گرفتن از AI برای پیش‌نویس runbook با ورودی‌های تأییدشده، مراحل verification، rollback و بازبینی انسانی.',
      why='AI می‌تواند مستندات را ساختاربندی کند اما ممکن است دستور نادرست، خطرناک یا ناسازگار با نسخه بسازد؛ runbook باید منبع، دامنه، پیش‌شرط و معیار توقف داشته باشد.',
      concepts='runbook، prerequisite، impact assessment، command allowlist، verification step، rollback plan، version applicability، human review و change record.',
      mechanism='مستندات معتبر و زمینهٔ محدود وارد prompt می‌شوند؛ مدل draft می‌سازد؛ validator ساختار و ارجاع‌ها را می‌سنجد؛ مهندس با دستگاه/نسخهٔ آزمایشی دستورها را verify و پس از review منتشر می‌کند.',
      commands='''# قالب پیشنهادی هر اقدام در runbook
- هدف و دامنه
- پیش‌شرط/نسخه/سطح دسترسی
- backup و pre-check
- دستور با placeholderهای واضح
- خروجی مورد انتظار و verify
- شرط توقف/rollback
- evidence و timestamp''',
      example='پیش‌نویس برای «عیب‌یابی DNS» باید فرمان‌های خواندنی مثل nslookup/Resolve-DnsName را از تغییر DNS server جدا کند؛ هر تغییر باید دستور بازگشت، مقصد دقیق و معیار قبولی داشته باشد.',
      lab='یک runbook غیرمخرب برای جمع‌آوری DNS و route از دو سیستم‌عامل ایجاد کنید؛ مدل فقط draft تولید کند؛ هر دستور را دستی اعتبارسنجی، نسخه و output مورد انتظار را مشخص و دستورات write را حذف یا جداگانه review کنید.',
      issues='دستور نسخه‌نامعتبر: مستند رسمی/version target. placeholder گمراه‌کننده: schema و lint. rollback ناقص: آزمون روی snapshot. citation ساختگی: بررسی لینک. runbook مبهم: شرط قبولی/توقف اضافه کنید.',
      security='هیچ‌گاه مدل را مستقیم به shell یا دستگاه وصل نکنید؛ credential و آدرس حساس را حذف کنید؛ متن خروجی را کد غیرقابل‌اعتماد فرض کنید؛ human review و تغییرات کنترل‌شده الزامی‌اند.',
      advanced='runbook را به ساختار داده‌ای مانند YAML/JSON با step type، risk level، required role، preconditions و validation تبدیل کنید. test خودکار می‌تواند وجود rollback/citation/owner/version را الزام کند.',
      glossary='Runbook: دستورالعمل عملیاتی؛ pre-check: بررسی پیش از اجرا؛ rollback: بازگردانی؛ placeholder: مقدار جایگزین؛ change record: سابقهٔ تغییر؛ validation: اعتبارسنجی.',
      question='کدام شرط برای انتشار یک runbook تولیدشده توسط AI ضروری است؟', answer='بازبینی انسانی، اعتبارسنجی منابع/نسخه، آزمایش دستورها در محیط کنترل‌شده، وجود معیار verify و rollback و ثبت مالک/تاریخچه.', distractors=['انتشار مستقیم چون متن روان است','حذف مراحل verification برای کوتاه‌ترشدن','اعتماد به لینک‌هایی که مدل تولید کرده بدون بازکردن آنها']),
]

LEVEL_GUIDANCE = {
 'L0': ('مفهومی و شهودی', 'با واژه‌های پایه و یک خروجی قابل مشاهده شروع کنید؛ هنوز تغییر روی سامانهٔ واقعی ندهید.', 'تشخیص مفهوم اصلی، توضیح کاربرد با زبان ساده و اجرای تمرین read-only.'),
 'L1': ('تمرین مقدماتی', 'یک نمونهٔ کوتاه را در VM یا دستگاه آزمایشگاهی اجرا کنید؛ ورودی و خروجی را یادداشت کنید.', 'اجرای موفق تمرین پایه، توضیح آرگومان‌های اصلی و تشخیص دست‌کم یک خطای ساده.'),
 'L2': ('عملیات ادمین', 'اجرای قابل تکرار با ورودی معتبر، timeout، ثبت لاگ، کنترل مجوز و اعتبارسنجی نتیجه طراحی کنید.', 'ساخت یک روند عملیاتی محدود، مدیریت خطا و ارائهٔ شواهد قبل/بعد.'),
 'L3': ('مهندسی و پایداری', 'تست واحد/یکپارچه، idempotency، کنترل هم‌زمانی، rollout مرحله‌ای و برنامهٔ rollback را در طراحی لحاظ کنید.', 'طراحی فرایند مقاوم، تحلیل failure mode، اندازه‌گیری و مستندسازی Runbook.'),
 'L4': ('معماری سازمانی', 'چند محیط و چند تیم را با RBAC، secrets management، approval gate، audit، ظرفیت، DR و سیاست نسخه‌بندی مدیریت کنید.', 'ارائهٔ طرح معماری با trade-off روشن، blast-radius محدود و معیار پذیرش قابل‌اندازه‌گیری.'),
}

SOURCE_MAP = {
 'MikroTik RouterOS': ['https://manual.mikrotik.com/docs/'],
 'Monitoring': ['https://www.rfc-editor.org/rfc/rfc3411', 'https://www.rfc-editor.org/rfc/rfc2863'],
 'Flow telemetry': ['https://help.mikrotik.com/docs/spaces/ROS/pages/21102653/Traffic+Flow', 'https://www.rfc-editor.org/rfc/rfc7011'],
 'Windows PowerShell': ['https://learn.microsoft.com/powershell/scripting/learn/remoting/'],
 'Windows identity automation': ['https://learn.microsoft.com/powershell/module/activedirectory/'],
 'Windows operations': ['https://learn.microsoft.com/powershell/module/nettcpip/'],
 'Windows automation': ['https://learn.microsoft.com/powershell/module/scheduledtasks/'],
 'Windows configuration management': ['https://learn.microsoft.com/powershell/dsc/overview?view=dsc-1.1'],
 'Python SSH': ['https://docs.paramiko.org/en/stable/'],
 'Python network CLI automation': ['https://ktbyers.github.io/netmiko/', 'https://docs.scrapli.dev/en/latest/'],
 'Multi-vendor network automation': ['https://napalm.readthedocs.io/en/latest/'],
 'Python HTTP APIs': ['https://requests.readthedocs.io/en/latest/'],
 'Network automation / IaC': ['https://docs.ansible.com/ansible/latest/network/getting_started/index.html'],
 'Automation source of truth': ['https://docs.ansible.com/projects/ansible/latest/network/getting_started/first_inventory.html'],
 'Infrastructure as Code': ['https://developer.hashicorp.com/terraform/language/state'],
 'Version control': ['https://git-scm.com/docs'],
 'CI/CD': ['https://docs.github.com/actions'],
 'AI-assisted operations': ['https://owasp.org/www-project-top-10-for-large-language-model-applications/'],
 'Retrieval-augmented generation': ['https://owasp.org/www-project-top-10-for-large-language-model-applications/'],
 'Local AI operations': ['https://ollama.com/'],
 'Observability and data analysis': ['https://prometheus.io/docs/introduction/overview/'],
 'Operational knowledge engineering': ['https://www.nist.gov/cyberframework'],
}


def uid_for(t: dict, lesson_order: int) -> str:
    return f"lesson:ch{t['ch']:02d}:lv{t['sub']:03d}:l{lesson_order:04d}"


def code_block(text: str) -> str:
    return '```text\n' + text.strip() + '\n```'


def explain_distractor(option: str, t: dict) -> str:
    """Return an option-specific reason; avoid generic answer-key filler."""
    text = option.strip()
    low = text.casefold()
    if any(word in low for word in ('رمز', 'گذرواژه', 'password', 'credential', 'secret')):
        reason = 'قرار دادن اطلاعات محرمانه در متن یا comment آن‌ها را در معرض مشاهده، نسخه‌برداری و ثبت ناخواسته قرار می‌دهد؛ از secret store یا متغیر محیطی محافظت‌شده استفاده کنید.'
    elif any(word in low for word in ('بدون تست', 'بدون آزمایش', 'همهٔ روترها', 'همه روترها', 'همهٔ دستگاه', 'همه دستگاه', 'production')):
        reason = 'دامنهٔ تغییر را پیش از آزمون و سنجش اثر گسترش می‌دهد؛ ابتدا روی محیط آزمایش یا یک canary محدود اعتبارسنجی کنید.'
    elif any(word in low for word in ('حذف لاگ', 'پاک‌کردن لاگ', 'پاک کردن لاگ', 'حذف گزارش')):
        reason = 'شواهد لازم برای عیب‌یابی، ممیزی و بازسازی خط زمانی رخداد را از بین می‌برد؛ لاگ را نگه دارید و retention را اصولی مدیریت کنید.'
    elif 'ping همیشه tcp' in low or ('ping' in low and 'tcp' in low and 'استفاده' in low):
        reason = 'ping معمولاً از ICMP استفاده می‌کند، نه TCP؛ ضمن آنکه پاسخ ICMP سلامت برنامه یا پایگاه‌داده را ثابت نمی‌کند.'
    elif 'ثابت می‌کند' in low or ('سالم‌اند' in low and 'icmp' in low):
        reason = 'پاسخ ICMP تنها یک نشانهٔ محدود از دسترس‌پذیری شبکه است و سلامت سرویس، پورت، وابستگی‌ها و منطق برنامه را اثبات نمی‌کند.'
    elif 'رکورد جدید' in low or 'تمام پیکربندی' in low or 'فقط یک بار قابل اجرا' in low:
        reason = 'این رفتار با idempotency سازگار نیست؛ اجرای تکراری باید وضعیت مطلوب را بدون ایجاد تغییر اضافه یا حذف ناخواسته حفظ کند.'
    else:
        reason = f'این پیشنهاد با هدف درس هم‌خوانی ندارد: {t["why"]} راه درست باید معیار موفقیت و محدودیت فنی را صریح بررسی کند.'
    return f'گزینهٔ «{text}» نادرست است؛ {reason}'


def build_assessment(t: dict, level: str, level_index: int):
    # Questions are deliberately stored without answers; answers/rationales are separate.
    distractors = list(t['distractors'])
    correct = t['answer']
    choices = [correct] + distractors
    # deterministic rotation avoids always placing the correct choice first
    shift = (level_index + len(t['topic'])) % len(choices)
    choices = choices[shift:] + choices[:shift]
    correct_index = choices.index(correct)
    letters = ['الف', 'ب', 'ج', 'د']
    q1 = {
        'id': 'Q1', 'type': 'multiple_choice',
        'difficulty': 'easy' if level_index <= 1 else ('medium' if level_index == 2 else 'hard'),
        'question': t['question'],
        'options': [{'id': letters[i], 'text': option} for i, option in enumerate(choices)],
    }
    q2 = {
        'id': 'Q2', 'type': 'short_answer',
        'difficulty': 'easy' if level_index == 0 else 'medium',
        'question': f'با بیان خود توضیح دهید «{t["topic"]}» چه مسئله‌ای را حل می‌کند و یک محدودیت آن چیست؟',
    }
    q3 = {
        'id': 'Q3', 'type': 'practical',
        'difficulty': 'medium' if level_index <= 2 else 'hard',
        'question': f'در محیط آزمایشگاهی، یک اجرای محدود برای «{t["topic"]}» طراحی کنید. پیش‌نیاز، فرمان/کد، خروجی مورد انتظار و روش پاک‌سازی یا بازگشت را بنویسید.',
    }
    q4 = {
        'id': 'Q4', 'type': 'scenario',
        'difficulty': 'medium' if level_index <= 2 else 'hard',
        'question': f'سناریو: عملیات «{t["topic"]}» نتیجهٔ مورد انتظار را نداده است. قبل از تغییر مجدد، چگونه محدودهٔ مشکل، شواهد، علت ریشه‌ای و اعتبارسنجی پس از اصلاح را مشخص می‌کنید؟',
    }
    answers = [
        {'question_id': 'Q1', 'correct_option_id': letters[correct_index], 'answer': correct,
         'rationale': f'این گزینه با سازوکار و محدودیت واقعی موضوع سازگار است: {t["why"]}',
         'distractor_rationales': [{'option_id': letters[i], 'why_wrong': explain_distractor(option, t)} for i, option in enumerate(choices) if option != correct]},
        {'question_id': 'Q2', 'answer': t['why'], 'rubric': ['تعریف درست هدف', 'ذکر یک محدودیت واقعی', 'پرهیز از ادعای تضمین مطلق']},
        {'question_id': 'Q3', 'answer': f"نمونهٔ راه‌حل باید از تمرین آزمایشگاهی این درس پیروی کند: {t['lab']} ابزار/نسخه و مقصد واقعی باید مشخص و خروجی ثبت شود.",
         'rubric': ['محیط کنترل‌شده و کم‌خطر', 'ورودی و فرمان دقیق', 'خروجی/معیار قبولی', 'بازگشت یا پاک‌سازی']},
        {'question_id': 'Q4', 'answer': f"ابتدا محدوده و زمان شروع را ثبت کنید؛ سپس شواهد مرتبط را جمع کنید؛ موارد زیر را به‌ترتیب بررسی کنید: {t['issues']} پس از اصلاح، همان آزمون را دوباره اجرا کنید و نتیجه را با وضعیت مورد انتظار مقایسه کنید.",
         'rubric': ['مشخص‌کردن scope', 'شواهد قبل از تغییر', 'آزمودن فرضیه به‌جای حدس', 'verification پس از اصلاح']},
    ]
    return {'questions': [q1, q2, q3, q4], 'answer_key': answers}


def make_lesson(t: dict, order: int, level_info: tuple, level_index: int):
    level, fa, en, capability = level_info
    skill, guardrail, exit_criteria = LEVEL_GUIDANCE[level]
    title_fa = f"[{level}] {t['topic']} — {fa}"
    title_en = f"[{level}] {t['en']} — {en}"
    prerequisites = {
        'L0': 'آشنایی عمومی با کامپیوتر و هدف مدیریتی مورد بحث؛ هیچ تغییر روی محیط تولید لازم نیست.',
        'L1': 'مفاهیم L0، دسترسی به محیط آزمایشگاهی، و توانایی خواندن خروجی فرمان/کد نمونه.',
        'L2': 'مبانی پروتکل/سیستم‌عامل مرتبط، مدیریت حساب‌ها و مجوزها، و توانایی اجرای تمرین L1.',
        'L3': 'تجربهٔ عملیات L2، کار با لاگ و تست، نسخه‌بندی و تهیهٔ backup یا snapshot.',
        'L4': 'درک معماری و عملیات سطح L3، الزامات کسب‌وکار، سیاست تغییر و کنترل‌های امنیتی سازمان.',
    }[level]
    intro = {
        'L0': f"تصور کنید این کار را هر روز باید چند بار تکرار کنید. «{t['topic']}» روشی برای تبدیل آن کار به فرایندی قابل فهم و قابل کنترل است: {t['why']}",
        'L1': f"در سطح مقدماتی، هدف این است که بدون اتکا به حدس، یک مسیر اجرا را از ابتدا تا انتها انجام دهید. موضوع «{t['topic']}» را با مثال read-only شروع می‌کنیم و هر پارامتر را با اثر آن می‌سنجیم.",
        'L2': f"در سطح ادمین، صرف اجرا کافی نیست؛ باید ورودی، هویت اجرا، timeout، خطا، خروجی و روش verification مدیریت شوند. در این درس «{t['topic']}» در قالب یک workflow کنترل‌شده بررسی می‌شود.",
        'L3': f"در سطح مهندسی، مسئله فقط یک اجرای موفق نیست. باید اجرا در شرایط خرابی، تعداد دستگاه زیاد، تغییر نسخه و تکرار ناخواسته نیز رفتار قابل پیش‌بینی داشته باشد. موضوع «{t['topic']}» را به عنوان بخشی از چرخهٔ عملیاتی می‌بینیم.",
        'L4': f"در سطح معماری، «{t['topic']}» باید درون یک سامانهٔ کنترل تغییر، هویت، مشاهده‌پذیری و بازیابی قرار گیرد. خروجی خوب، فقط کد نیست؛ حدود اختیار، شواهد، SLA/SLO، rollout و مسئولیت‌پذیری را نیز تعریف می‌کند.",
    }[level]
    command_section = t['commands']
    if level_index == 0:
        command_section += '\n\nنکته: ابتدا فقط فرمان/کد خواندنی را اجرا کنید؛ خروجی را قبل از ادامه توضیح دهید.'
    elif level_index == 1:
        command_section += '\n\nقبل از اجرای واقعی، مقصد و حساب را با یک محیط آزمایشگاهی تطبیق دهید و هر گزینه را جداگانه بررسی کنید.'
    elif level_index == 2:
        command_section += '\n\nبرای اجرای عملیاتی، timeout، مدیریت exception، log بدون secret و validation خروجی را به wrapper اضافه کنید.'
    elif level_index == 3:
        command_section += '\n\nنسخهٔ مهندسی باید تست، کنترل تعداد هدف‌ها، concurrency limit، idempotency و راهکار rollback داشته باشد.'
    else:
        command_section += '\n\nدر محیط سازمانی این نمونه را در plan → approval → canary → rollout → verification تقسیم کنید و دسترسی prod را از validation job جدا نگه دارید.'
    workplace = {
        'L0': f"مثال کاری: تیم IT می‌خواهد {t['topic']} را بفهمد و یک وضعیت پایه ثبت کند. نتیجهٔ موفق باید قابل توضیح باشد، نه فقط یک پیام سبز.",
        'L1': f"مثال کاری: کارشناس شیفت یک هدف آزمایشی را با «{t['topic']}» بررسی می‌کند و خروجی را در تیکت ضمیمه می‌کند؛ هنوز مجاز به تغییر گروهی نیست.",
        'L2': f"مثال کاری: ادمین یک workflow برای چند مقصد مجاز اجرا می‌کند؛ هر مقصد نتیجهٔ مستقل، timestamp و کد وضعیت دارد و خطای یک مقصد کل گزارش را محو نمی‌کند.",
        'L3': f"مثال کاری: مهندس تغییر را ابتدا روی canary اجرا می‌کند، اختلاف قبل/بعد را می‌سنجد، در شکست rollout را متوقف می‌کند و شواهد را به change ticket متصل می‌کند.",
        'L4': f"مثال کاری: معمار، این قابلیت را با RBAC، محیط‌های dev/stage/prod، secret manager، approval، telemetry و recovery plan در یک پلتفرم مشترک قرار می‌دهد.",
    }[level]
    steps = {
        'L0': ['هدف را با یک جمله تعریف کنید.', 'اصطلاحات کلیدی را از خروجی نمونه پیدا کنید.', 'ورودی، مقصد و خروجی مورد انتظار را ثبت کنید.', 'توضیح دهید این آزمایش چه چیزی را اثبات نمی‌کند.'],
        'L1': ['محیط آزمایشگاهی و مجوز را بررسی کنید.', 'نمونهٔ کم‌خطر را با مقصد آزمایشی اجرا کنید.', 'خروجی واقعی را با خروجی مورد انتظار مقایسه کنید.', 'یک خطای ساده را ثبت و علت آن را توضیح دهید.'],
        'L2': ['ورودی را validate و مقصدها را allowlist کنید.', 'timeout و کنترل خطا را فعال کنید.', 'نتیجه و timestamp را بدون secret ثبت کنید.', 'پس از اجرا با معیار مستقل وضعیت را verify کنید.'],
        'L3': ['پیش‌شرط و snapshot/backup را بررسی کنید.', 'تست و dry-run/plan قابل استفاده را اجرا کنید.', 'ابتدا روی یک canary با concurrency محدود اجرا کنید.', 'در صورت عبور معیار، مرحله‌ای گسترش دهید؛ در شکست، توقف/rollback و ثبت evidence انجام دهید.'],
        'L4': ['SLO، مالک سرویس و دامنهٔ تغییر را تعریف کنید.', 'RBAC، secrets، rate limit و approval را در طراحی بیاورید.', 'معیارهای ورود/توقف rollout و مسیر rollback را بنویسید.', 'نتایج، هزینه، audit و برنامهٔ بازبینی دوره‌ای را ثبت کنید.'],
    }[level]
    troubleshooting = '\n'.join(f"- {part.strip()}" for part in t['issues'].split('. ') if part.strip())
    safety_lab = 'این آزمایش را روی VM، CHR، simulator یا endpointی که صریحاً تحت مدیریت شماست انجام دهید. هیچ رمز واقعی یا دادهٔ حساس را در فایل نمونه، history یا log قرار ندهید.'
    full_content = f"""# {title_fa}\n\n## عنوان انگلیسی\n{title_en}\n\n## خلاصه\n{t['summary']}\n\n## اهداف یادگیری\nپس از پایان درس، دانشجو باید بتواند: \n- هدف و محدودیت «{t['topic']}» را توضیح دهد.\n- واژگان و اجزای فنی اصلی را تشخیص دهد.\n- نمونهٔ کنترل‌شده را اجرا و خروجی را تفسیر کند.\n- خطاهای پایه را بر اساس شواهد تفکیک کند.\n- ملاحظات سطح {level} را در کار عملی پیاده کند.\n\n## پیش‌نیازها\n{prerequisites}\n\n## مقدمهٔ مفهومی\n{intro}\n\n## مفاهیم اصلی\n{t['concepts']}\n\n## سازوکار داخلی و معماری\n{t['mechanism']}\n\n## مثال مرحله‌به‌مرحله و ابزارها\n{command_section}\n\nتفسیر: ابتدا مشخص کنید ابزار به کدام میزبان/سرویس وصل می‌شود، با چه هویتی اجرا می‌شود و کدام معیار موفقیت را گزارش می‌کند. exit code یا پاسخ موفقِ transport همیشه به معنی سالم بودن سرویس نهایی نیست؛ نتیجهٔ کاربردی باید جدا اعتبارسنجی شود.\n\n## مثال محیط کار\n{workplace}\n{t['example']}\n\n## آزمایشگاه عملی\n**هدف:** تمرین «{t['topic']}» در سطح {level}.\n\n**پیش‌نیاز و ابزار:** {prerequisites} ابزار/نسخهٔ متناسب با محیط خود را پیش از اجرا ثبت کنید.\n\n**ایمنی:** {safety_lab}\n\n**مراحل:**\n""" + '\n'.join(f"{i+1}. {step}" for i, step in enumerate(steps)) + f"""\n\n**روش اعتبارسنجی:** {t['lab']}\n\n**نتیجهٔ مورد انتظار:** اجرای قابل توضیح با شواهد؛ خطاهای مورد انتظار ثبت شده‌اند و پس از تمرین هیچ تغییر آزمایشی ناخواسته باقی نمانده است.\n\n## عیب‌یابی مرحله‌ای\nروش عمومی: Symptom → Scope → Evidence → Hypothesis → Test → Fix → Verify → Document. ابتدا scope و زمان شروع را ثبت کنید و قبل از تغییر، شواهد جمع‌آوری کنید.\n\n{troubleshooting}\n\n## امنیت، محدودیت‌ها و اشتباهات رایج\n{t['security']}\n\nاشتباه‌های متداول: اجرای مستقیم روی production، hardcode کردن credential، اعتماد به یک خروجی بدون verification، نبود timeout، و تکرار درخواست تغییردهنده پس از خطای مبهم. در سطح {level} این موارد را با روش زیر کنترل کنید: {guardrail}\n\n## نکات پیشرفته\n{t['advanced']}\n\n## جمع‌بندی\n{t['summary']}\n\n**مهارت مورد انتظار پس از این سطح:** {exit_criteria}\n\n## واژه‌نامه\n{t['glossary']}\n\n## ارجاع ساختاری\nشناسهٔ درس: `{uid_for(t, order)}`؛ فصل {t['ch']}، زیرفصل {t['sub']}، ترتیب درس {order}. سؤالات ابتدا بدون پاسخ ارائه می‌شوند؛ کلید پاسخ و منطق نمره‌دهی فقط در `meta.assessment.answer_key` نگهداری می‌شود.\n"""
    objectives = [
        f"تعریف هدف و محدودیت {t['topic']}",
        f"توضیح سازوکار {t['topic']} در حوزهٔ {t['domain']}",
        'اجرای تمرین کم‌خطر و تفسیر خروجی واقعی',
        'تشخیص خطا بر اساس شواهد و اجرای verification پس از اصلاح',
        f"اعمال کنترل‌های متناسب با سطح {level}: {skill}",
    ]
    meta = {
        'level': level,
        'learning_objectives': objectives,
        'prerequisites': [prerequisites],
        'keywords_fa': [t['topic'], t['domain'], 'اتوماسیون', 'عیب‌یابی'],
        'keywords_en': [t['en'], 'automation', 'troubleshooting', 'verification'],
        'vendors': ['MikroTik'] if t['domain'] == 'MikroTik RouterOS' else [],
        'protocols': [], 'standards': [],
        'command_categories': ['read', 'configure', 'troubleshoot', 'security', 'automation'],
        'verification_steps': [
            'اجرای آزمایش در محیط کنترل‌شده',
            'مقایسهٔ نتیجه با معیار قبولی مشخص',
            'ثبت timestamp، نسخه و شواهد بدون secret',
        ],
        'troubleshooting_steps': [
            'تعریف symptom و scope', 'جمع‌آوری evidence پیش از تغییر',
            'آزمودن یک فرضیه در هر مرحله', 'verify پس از اصلاح و مستندسازی root cause',
        ],
        'security_notes': [t['security']], 'hardening_notes': [guardrail],
        'monitoring_notes': ['موفقیت transport را از سلامت سرویس نهایی جدا کنید؛ برای شکست، alert و evidence تعریف کنید.'],
        'automation_notes': [t['advanced']],
        'runbook_ref': '', 'scenario_ref': '', 'source_status': 'review_required',
        'official_sources': SOURCE_MAP.get(t['domain'], []),
        'ai_search_prompt': f"برای {t['topic']} در سطح {level} فقط مستندات رسمی و نسخه‌محور را بررسی کن؛ syntax را قبل از توصیه تأیید کن.",
        'ai_teach_prompt': f"موضوع {t['topic']}، سطح {level}: مفهوم، معماری، مثال حل‌شده، آزمایشگاه ایمن، عیب‌یابی و امنیت را آموزش بده.",
        'ai_troubleshoot_prompt': f"برای {t['topic']} از مسیر Symptom→Scope→Evidence→RootCause→Fix→Verify استفاده کن و قبل از تغییر پرخطر هشدار بده.",
        'ai_quiz_prompt': f"چهار سؤال سطح {level} بساز؛ پاسخ‌ها را فقط در answer_key جداگانه قرار بده.",
        'engineering_loop': ['Learn', 'Configure', 'Verify', 'Monitor', 'Break', 'Troubleshoot', 'Secure', 'Automate', 'Document', 'Design'],
        'content_status': 'curated_draft_review_required',
        'content_quality_checks': ['questions_separate_from_answers', 'stable_uid', 'topic_specific_lab', 'safe_lab', 'level_specific_depth'],
        'assessment': build_assessment(t, level, level_index),
    }
    return {
        'uid': uid_for(t, order), 'entity': 'lesson',
        'chapter_order': t['ch'], 'subchapter_order': t['sub'], 'lesson_order': order,
        'topic': t['topic'], 'domain': t['domain'], 'level': level,
        'title_fa': title_fa, 'title_en': title_en, 'tags': level,
        'summary': t['summary'], 'full_content': full_content,
        'commands': command_section, 'examples': t['example'],
        'notes': f"عیب‌یابی: {t['issues']}\n\nامنیت: {t['security']}\n\nپیشرفته: {t['advanced']}\n\nواژه‌نامه: {t['glossary']}",
        'search_query': f"{t['topic']} {t['en']} {t['domain']} official documentation {level}",
        'learning_objectives': objectives,
        'meta': meta,
        'source_status': 'review_required',
    }


def build_pack():
    lessons = []
    for topic in TOPICS:
        for idx, level in enumerate(LEVELS):
            order = TOPICS_TOPIC_INDEX[(topic['ch'], topic['sub'], topic['topic'])] * len(LEVELS) + idx + 1
            lessons.append(make_lesson(topic, order, level, idx))
    return {
        'package_schema_version': 1,
        'project': 'ENGINEER JOKAR / NetworkEncyclopedia',
        'generated_on': date.today().isoformat(),
        'purpose': 'محتوای تکمیلی سطح L0-L4 برای پایتون شبکه و اتوماسیون؛ سازگار با جدول lessons در SQLite مخزن.',
        'scope': [
            {'chapter_order': 21, 'subchapter_order': 4, 'title': '۲۱.۴ اتوماسیون مانیتور MikroTik', 'topics': 7},
            {'chapter_order': 35, 'subchapter_order': 3, 'title': '۳۵.۳ اتوماسیون PowerShell', 'topics': 5},
            {'chapter_order': 51, 'subchapter_order': 1, 'title': '۵۱.۱ Python شبکه', 'topics': 5},
            {'chapter_order': 51, 'subchapter_order': 2, 'title': '۵۱.۲ Infrastructure as Code', 'topics': 5},
            {'chapter_order': 51, 'subchapter_order': 3, 'title': '۵۱.۳ AI در IT', 'topics': 5},
        ],
        'compatibility': {
            'database_table': 'lessons',
            'uid_pattern': 'lesson:ch{chapter_order:02d}:lv{subchapter_order:03d}:l{lesson_order:04d}',
            'updated_columns': ['summary', 'full_content', 'commands', 'examples', 'notes', 'search_query', 'learning_objectives', 'meta_json', 'source_status', 'last_updated', 'content_hash'],
            'preserved': ['chapters', 'levels', 'lessons.id', 'lessons.uid', 'titles', 'tags', 'scenarios', 'study/progress data', 'all non-target records'],
            'answer_separation': 'meta.assessment.questions contains no answers; meta.assessment.answer_key contains answers and rubrics.',
        },
        'lessons': lessons,
    }

# Each topic position is its relative position within its subsection, matching full_curriculum.py.
TOPICS_TOPIC_INDEX = {}
_positions = {}
for _t in TOPICS:
    key = (_t['ch'], _t['sub'])
    _positions[key] = _positions.get(key, 0)
    TOPICS_TOPIC_INDEX[(_t['ch'], _t['sub'], _t['topic'])] = _positions[key]
    _positions[key] += 1

if __name__ == '__main__':
    pack = build_pack()
    OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote {OUT} with {len(pack["lessons"])} lessons and {len(TOPICS)} topics.')
