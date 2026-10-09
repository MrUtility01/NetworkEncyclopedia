package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * سناریوهای سازمانی غنی و ملموس — هر کدام با داستان واقعی، علائم، وظایف گام‌به‌گام،
 * شواهد، راه‌حل و معیار Verify.
 */
object ScenarioSeeder {
    private const val META = "scenarios_seeded_v5_rich"

    data class RichScenario(
        val name: String,
        val vendors: String,
        val incident: String,
        val business: String,
        val symptoms: String,
        val tasks: String,
        val solution: String,
        val verification: String,
        val hints: String,
        val difficulty: String = "خبره",
        val hours: Int = 6,
    )

    private val RICH = listOf(
        RichScenario(
            name = "VLAN و سگمنت‌بندی — دسترسی بین VLAN قطع",
            vendors = "Cisco,MikroTik",
            incident = "کلاینت‌های VLAN10 (کاربران) به سرور فایل در VLAN20 پینگ نمی‌زنند؛ ARP گاهی ناقص است.",
            business = "شرکت با ۴ طبقه، VLAN جدا برای Users / Servers / VoIP / Guest. فایل‌سرور حیاتی حسابداری روی VLAN20 است. حدود ۴۰۰ کاربر در شیفت صبح.",
            symptoms = "• پینگ داخل VLAN10 OK\n• پینگ به gateway VLAN10 OK\n• پینگ به 10.20.20.10 (فایل‌سرور) timeout\n• روی سوییچ: MAC سرور در VLAN20 دیده می‌شود\n• traceroute در اولین hop می‌ماند",
            tasks = "1) Scope: فقط بین VLAN یا همه؟\n2) Evidence: show vlan brief, show ip interface brief, show ip route, show arp\n3) Hypothesis: SVI؟ inter-VLAN routing؟ ACL؟ trunk allowed؟\n4) Fix با backup\n5) Verify از کلاینت واقعی\n6) Document",
            solution = "معمولاً یکی از این‌هاست:\n• SVI VLAN20 یا VLAN10 down/بدون IP\n• ip routing غیرفعال\n• ACL روی SVI\n• trunk بین access و distribution، VLAN20 را allow نکرده\nرفع: اصلاح trunk/SVI + Verify پینگ دوطرفه + تست دسترسی SMB.",
            verification = "از کلاینت VLAN10: ping فایل‌سرور + باز شدن share. show vlan + show ip route پایدار.",
            hints = "اول لایه ۲ را تمیز کن (VLAN/trunk) بعد لایه ۳ (SVI/ACL).",
        ),
        RichScenario(
            name = "STP Loop — broadcast storm بعد از کابل backup",
            vendors = "Cisco",
            incident = "بعد از وصل کابل backup بین دو سوییچ access، CPU سوییچ‌ها ۱۰۰٪، تلفن‌ها و دوربین‌ها قطع.",
            business = "ساختمان اداری ۳ طبقه. تیم کابل‌کشی یک uplink اضافه برای redundancy گذاشت بدون هماهنگی با شبکه.",
            symptoms = "• LED پورت‌ها دیوانه‌وار چشمک\n• show processes cpu = 99%\n• ping داخل همان سوییچ هم timeout\n• لاگ: %SW_MATM-4-MACFLAP",
            tasks = "1) فوراً کابل مشکوک را بکش (مهار آسیب)\n2) show spanning-tree — Root کیست؟ کدام پورت Block باید باشد؟\n3) آیا STP روی آن VLAN اصلاً فعال است؟\n4) PortFast اشتباه روی uplink؟\n5) بعد از پایدار شدن: طراحی صحیح redundancy با EtherChannel یا STP درست",
            solution = "کابل را جدا کن → storm می‌خوابد. سپس:\n• spanning-tree mode rapid-pvst\n• Root را روی distribution ثابت کن\n• BPDU Guard روی access\n• برای redundancy واقعی: EtherChannel نه دو لینک مستقل بدون STP.",
            verification = "CPU زیر ۲۰٪، show spanning-tree یک Root پایدار، یک پورت Blocking روی لینک backup، تلفن‌ها و دوربین‌ها online.",
            hints = "در طوفان اول کابل را بکش؛ بعد تحلیل کن. PortFast فقط روی کلاینت.",
            hours = 4,
        ),
        RichScenario(
            name = "OSPF — مسیر Area فرعی در هسته نیست",
            vendors = "Cisco,MikroTik",
            incident = "مسیرهای Area1 (سایت فرعی) در Area0 دیده نمی‌شوند؛ Neighbor در 2-Way گیر کرده.",
            business = "دفتر مرکزی (Area0) و کارخانه (Area1) با لینک اختصاصی. کاربران کارخانه به ERP مرکزی دسترسی ندارند.",
            symptoms = "• show ip ospf neighbor → 2-Way\n• show ip route ospf → مسیر Area1 نیست\n• پینگ بین روترها OK\n• MTU و timer یکسان به نظر می‌رسد",
            tasks = "1) show ip ospf interface — نوع شبکه؟ DR/BDR؟\n2) آیا هر دو سمت یک Area و یک process؟\n3) Authentication؟\n4) آیا ABR به‌درستی LSA نوع ۳ می‌فرستد؟\n5) Fix + clear ip ospf process (با احتیاط در production)",
            solution = "در multi-access اگر DR انتخاب نشود یا network type ناسازگار باشد (broadcast vs point-to-point) در 2-Way می‌ماند.\nرفع رایج: ip ospf network point-to-point روی لینک اختصاصی، یکسان‌سازی timer/auth، بررسی ABR.",
            verification = "Neighbor = Full، مسیرهای Area1 در Area0، پینگ end-to-end از کلاینت کارخانه به ERP.",
            hints = "2-Way روی لینک p2p طبیعی نیست؛ network-type را چک کن.",
        ),
        RichScenario(
            name = "BGP Failover — ISP1 قطع شد ترافیک نرفت ISP2",
            vendors = "Cisco,Linux",
            incident = "لینک ISP1 down شد ولی ترافیک خروجی به ISP2 سوییچ نشد؛ اینترنت سازمان قطع.",
            business = "دو ISP فعال (dual-homed). SLA با کسب‌وکار: حداکثر ۵ دقیقه قطعی اینترنت.",
            symptoms = "• show ip bgp summary → peer ISP1 Idle/down\n• مسیرهای default هنوز next-hop ISP1 را نشان می‌دهند یا اصلاً default از ISP2 نیست\n• traceroute از داخل به ۸.۸.۸.۸ fail",
            tasks = "1) آیا default route از ISP2 دریافت و نصب شده؟\n2) local-preference / weight / AS-path prepending؟\n3) prefix-list خروجی/ورودی؟\n4) آیا FEC یا static float دارید؟\n5) بعد از رفع: تست قطع عمدی ISP1 در پنجره نگهداری",
            solution = "معمولاً local-pref بالاتر برای ISP1 باقی مانده یا ISP2 اصلاً default نفرستاده / فیلتر شده.\nرفع: تنظیم local-pref یا weight، اطمینان از دریافت 0.0.0.0/0 از هر دو، تست failover کنترل‌شده.",
            verification = "قطع ISP1 → حداکثر چند ثانیه اختلال → ترافیک از ISP2. show ip bgp + traceroute تأیید.",
            hints = "قبل از production، failover را در Lab یا پنجره کوتاه تست کن.",
            hours = 8,
        ),
        RichScenario(
            name = "ACL اشتباه — HTTPS بعد از change قطع",
            vendors = "Cisco,FortiGate",
            incident = "بعد از اعمال ACL برای محدود کردن RDP، سرویس HTTPS داخلی هم قطع شد.",
            business = "تیم امنیت می‌خواست RDP فقط از jump-server باشد. change در ساعت کاری انجام شد.",
            symptoms = "• مرورگر به https://app.corp.local timeout\n• RDP واقعاً محدود شده (هدف اصلی)\n• hit count روی ACL خط deny بالا می‌رود\n• از jump-server هم HTTPS کار نمی‌کند",
            tasks = "1) Backup قبلی را پیدا کن\n2) show access-lists با hit count\n3) ترتیب ruleها — آیا deny عمومی قبل از permit HTTPS است؟\n4) object/group اشتباه؟\n5) Rollback فوری اگر لازم، بعد اصلاح دقیق",
            solution = "ACL از بالا به پایین match می‌شود. یک deny ip any any یا object اشتباه قبل از permit 443 باعث این می‌شود.\nرفع: permit صریح tcp any host APP eq 443 قبل از deny، یا اصلاح object. همیشه review دو نفره.",
            verification = "HTTPS از کلاینت عادی OK، RDP فقط از jump-server، hit count منطقی.",
            hints = "هیچ‌وقت deny any any را بدون permitهای لازم بالای آن نگذار.",
        ),
        RichScenario(
            name = "NAT Overload — کاربران اینترنت یک‌طرفه",
            vendors = "Cisco,MikroTik",
            incident = "کاربران به اینترنت وصل می‌شوند ولی صفحه‌ها کامل لود نمی‌شوند؛ translation table پر است.",
            business = "حدود ۶۰۰ کاربر پشت یک PAT. امروز صبح اوج مصرف.",
            symptoms = "• show ip nat translations → تعداد نزدیک سقف\n• بعضی sessionها timeout\n• از بیرون به داخل (اگر لازم) کار نمی‌کند\n• CPU روتر متوسط رو به بالا",
            tasks = "1) سقف translations چقدر است؟\n2) آیا entryهای stale پاک می‌شوند؟\n3) آیا چند public IP در pool هست؟\n4) timeoutهای NAT مناسب‌اند؟\n5) راه‌حل کوتاه‌مدت و بلندمدت",
            solution = "کوتاه‌مدت: clear ip nat translation * (با احتیاط) + افزایش timeout مناسب.\nبلندمدت: pool چند آدرسه، یا CGNAT آگاهانه، یا شکستن به چند edge.",
            verification = "تعداد translations زیر سقف، کاربران بدون شکایت، مانیتور ۳۰ دقیقه پایدار.",
            hints = "قبل از clear در production، نمونه بگیر و تأثیر را بسنج.",
        ),
        RichScenario(
            name = "VPN IPSec — Phase1 up Phase2 down",
            vendors = "FortiGate,Cisco",
            incident = "تونل Site-to-Site Phase1 سبز است ولی Phase2 نمی‌آید؛ ترافیک بین دو سایت برقرار نیست.",
            business = "اتصال دفتر مرکزی به انبار. اپلیکیشن انبار به دیتابیس مرکزی وابسته است.",
            symptoms = "• show crypto isakmp sa = QM_IDLE (Phase1 OK)\n• show crypto ipsec sa = خالی یا 0 packet\n• interesting traffic تعریف شده به نظر می‌رسد",
            tasks = "1) مقایسه transform-set / PFS / lifetime دو طرف\n2) proxy-id / interesting traffic یکسان؟\n3) routing برگشت از سایت مقابل؟\n4) NAT وسط مسیر؟\n5) لاگ Phase2",
            solution = "ناسازگاری PFS یا ACL جفت (proxy-id) شایع‌ترین علت است.\nرفع: یکسان‌سازی Phase2 proposal، mirror کردن interesting traffic، بررسی routing و NAT-T.",
            verification = "show crypto ipsec sa با encaps/decaps افزایش‌یابنده، پینگ و دسترسی اپلیکیشن بین سایت‌ها.",
            hints = "Phase1 سبز فقط نصف راه است؛ همیشه Phase2 و شمارنده پکت را ببین.",
        ),
        RichScenario(
            name = "HA فایروال — Failover با drop شدن sessionها",
            vendors = "FortiGate",
            incident = "Failover انجام شد ولی همه sessionهای بانکی drop شدند؛ کاربران باید دوباره لاگین کنند.",
            business = "فایروال HA Active-Passive جلو دیتاسنتر. انتظار session-sync برای اپلیکیشن‌های حساس.",
            symptoms = "• HA status بعد از failover درست است\n• session table روی واحد جدید خالی یا ناقص\n• لاگ: session sync issue یا لینک HA",
            tasks = "1) وضعیت session-pickup / session-sync\n2) لینک HA و heartbeat\n3) نسخه firmware دو طرف یکسان؟\n4) آیا اپلیکیشن به source-port حساس است؟\n5) تست failover برنامه‌ریزی‌شده",
            solution = "فعال‌سازی و تأیید session sync، بررسی کابل/پورت HA، یکسان‌سازی نسخه، تست در پنجره نگهداری.",
            verification = "Failover آزمایشی بدون قطع sessionهای تست، مانیتور session count دو طرف.",
            hints = "HA بدون session-sync فقط دستگاه را جابه‌جا می‌کند نه تجربه کاربر را.",
            hours = 8,
        ),
        RichScenario(
            name = "DNS Split-Horizon — نام داخلی از بیرون resolve می‌شود",
            vendors = "Windows,Linux",
            incident = "از اینترنت می‌توان نام‌های داخلی مثل dc01.corp.local را resolve کرد؛ ساختار AD لو رفته.",
            business = "سرور DNS داخلی هم به اینترنت recursion می‌دهد یا zone داخلی روی public قرار گرفته.",
            symptoms = "• dig @public-ip dc01.corp.local از بیرون جواب می‌دهد\n• در داخل هم کار می‌کند\n• هیچ view یا split-horizon تعریف نشده",
            tasks = "1) کدام سرور authoritative است؟\n2) آیا recursion برای همه باز است؟\n3) جداسازی internal/external view\n4) بستن recursion از بیرون\n5) بررسی نشت اطلاعات دیگر",
            solution = "پیاده‌سازی Split-Horizon (view در BIND یا policy در Windows DNS)، بستن recursion برای منبع خارجی، جدا کردن zone عمومی از خصوصی.",
            verification = "از بیرون: نام داخلی NXDOMAIN یا timeout. از داخل: resolve صحیح. تست با dig از دو نقطه.",
            hints = "هیچ‌وقت DNS داخلی را مستقیم به اینترنت expose نکن.",
        ),
        RichScenario(
            name = "DHCP Scope Exhaust — کلاینت‌ها APIPA می‌گیرند",
            vendors = "Windows,Cisco",
            incident = "کلاینت‌های جدید در یک طبقه همه 169.254.x.x می‌گیرند.",
            business = "صبح روز کاری، طبقه ۳. حدود ۸۰ لپ‌تاپ جدید برای کارآموزان اضافه شده.",
            symptoms = "• ipconfig → APIPA\n• Scope همان VLAN در وضعیت 100% depleted\n• Relay روی SVI تنظیم است\n• سرور DHCP خودش سالم است",
            tasks = "1) کدام Scope؟ چند lease آزاد؟\n2) leaseهای قدیمی/stale؟\n3) آیا می‌توان محدوده را گسترش داد؟\n4) Reservationهای غیرضروری؟\n5) راه‌حل موقت و دائم",
            solution = "موقت: کاهش lease time + آزاد کردن reservationهای بلااستفاده.\nدائم: گسترش Scope یا /23 به‌جای /24، یا VLAN جدا برای مهمان/کارآموز.",
            verification = "کلاینت جدید IP معتبر + gateway + DNS، تعداد free address > ۲۰٪.",
            hints = "قبل از گسترش Scope، از خالی نبودن آدرس در استفاده دستی مطمئن شو.",
        ),
        RichScenario(
            name = "AD — Kerberos Time Skew",
            vendors = "Windows",
            incident = "کاربران سایت فرعی خطای clock skew هنگام لاگین می‌گیرند.",
            business = "یک DC در سایت فرعی. ارتباط WAN گاهی ناپایدار. بیش از ۵ دقیقه اختلاف ساعت.",
            symptoms = "• Event log: time difference\n• w32tm /query /status → منبع زمان اشتباه یا offset بزرگ\n• لاگین با حساب محلی کار می‌کند",
            tasks = "1) منبع زمان DC فرعی و PDC؟\n2) UDP 123 باز است؟\n3) VM time sync با host تداخل ندارد؟\n4) همگام‌سازی اجباری\n5) مانیتور ماندگار",
            solution = "تنظیم سلسله‌مراتب زمان (PDC از NTP معتبر، بقیه از PDC)، باز بودن فایروال NTP، غیرفعال کردن time sync هایپرویزور اگر تداخل دارد.",
            verification = "w32tm /stripchart نشان‌دهنده offset زیر ۱ ثانیه، لاگین کاربران بدون خطا.",
            hints = "Kerberos بیش از ۵ دقیقه اختلاف را نمی‌بخشد.",
        ),
        RichScenario(
            name = "Wi-Fi Roaming — قطع هنگام جابجایی بین AP",
            vendors = "Cisco WLC",
            incident = "کلاینت هنگام حرکت بین دو طبقه چند ثانیه قطع می‌شود؛ تماس VoIP می‌پرد.",
            business = "بیمارستان، تلفن‌های Wi-Fi روی ترالی‌ها. نیاز به roaming سریع.",
            symptoms = "• log کلاینت: re-auth کامل به‌جای fast roam\n• FT / 802.11r غیرفعال یا ناسازگار\n• قدرت سیگنال در مرز طبقات ضعیف",
            tasks = "1) آیا 802.11r / OKC فعال است؟\n2) همان SSID و security روی هر دو AP؟\n3) قدرت و channel planning؟\n4) تست با یک کلاینت و capture",
            solution = "فعال‌سازی Fast Transition، یکسان‌سازی SSID/security، بهینه‌سازی power و channel، تست با گوشی واقعی.",
            verification = "جابجایی بین AP بدون قطع شنیداری تماس، زمان roam زیر ۵۰–۱۰۰ms در حالت ایده‌آل.",
            hints = "VoIP روی Wi-Fi بدون fast roam practically دردسر است.",
            hours = 8,
        ),
        RichScenario(
            name = "MTU Blackhole — TCP بزرگ fail پینگ کوچک OK",
            vendors = "Cisco,Linux",
            incident = "اپلیکیشن روی VPN فایل بزرگ نمی‌فرستد؛ ping 32 بایتی OK است.",
            business = "ارتباط Site-to-Site. کاربران از کندی و timeout شکایت دارند.",
            symptoms = "• ping -l 32 OK\n• ping -l 1472 fail یا fragmentation needed و کسی جواب نمی‌دهد\n• TCP handshake گاهی OK ولی data بزرگ نه",
            tasks = "1) Path MTU Discovery کار می‌کند؟\n2) ICMP unreachable توسط فایروال بسته نشده؟\n3) MTU تونل (VPN overhead)؟\n4) clamp MSS؟",
            solution = "کاهش MTU روی تونل یا اینترفیس، یا ip tcp adjust-mss، باز کردن ICMP type 3 code 4 در مسیر.",
            verification = "انتقال فایل بزرگ موفق، ping با اندازه نزدیک MTU OK.",
            hints = "اگر ICMP را کامل بستید، PMTUD می‌میرد.",
        ),
        RichScenario(
            name = "HSRP Split-Brain — دو Active هم‌زمان",
            vendors = "Cisco",
            incident = "دو روتر هم‌زمان Active شده‌اند؛ VIP تکراری و ترافیک ناپایدار.",
            business = "gateway کاربران با HSRP. لینک heartbeat یا L2 بین دو روتر قطع شده.",
            symptoms = "• show standby روی هر دو: State Active\n• کاربران گاهی وصل گاهی نه\n• CAM table سوییچ MAC VIP را جابه‌جا می‌کند",
            tasks = "1) لینک L2 بین دو روتر؟\n2) اولویت و preempt؟\n3) authentication HSRP؟\n4) بازیابی لینک و یک Active کردن",
            solution = "رفع لینک بین روترها، تأیید authentication، تنظیم اولویت واضح، در صورت نیاز preempt با delay.",
            verification = "فقط یک Active، VIP پایدار، پینگ gateway بدون قطعی.",
            hints = "Split-brain یعنی هر دو فکر می‌کنند تنها هستند — معمولاً مشکل L2 است.",
        ),
        RichScenario(
            name = "Port Security — err-disabled بعد از تعویض NIC",
            vendors = "Cisco",
            incident = "پورت کاربر بعد از تعویض کارت شبکه err-disabled شد.",
            business = "لپ‌تاپ حسابداری. Port-Security با maximum 1 و violation shutdown.",
            symptoms = "• show interfaces status → err-disabled\n• show port-security interface → violation count\n• MAC جدید با MAC قدیمی فرق دارد",
            tasks = "1) تأیید violation\n2) clear port-security sticky / errdisable recovery\n3) آیا maximum را باید ۲ کرد (dock + laptop)؟\n4) آموزش به کاربر/میز خدمت",
            solution = "shutdown/no shutdown یا errdisable recovery، در صورت نیاز sticky MAC جدید، یا maximum 2 برای سناریوهای dock.",
            verification = "پورت up، کلاینت IP و دسترسی، show port-security بدون violation جدید.",
            hints = "قبل از تعویض NIC در سازمان‌های سخت‌گیر، به شبکه خبر بده.",
            difficulty = "ادمین",
            hours = 2,
        ),
        RichScenario(
            name = "BPDU Guard — پورت access با BPDU خاموش شد",
            vendors = "Cisco",
            incident = "پورت access کاربر err-disabled شد چون BPDU دریافت کرد.",
            business = "کاربر یک سوییچ رومیزی ارزان به پورت زده یا کابل loop ساخته.",
            symptoms = "• err-disabled\n• لاگ: BPDU Guard\n• show spanning-tree interface → inconsistency",
            tasks = "1) کابل و دستگاه انتهایی را بررسی کن\n2) BPDU Guard را عمداً روی access گذاشته‌اید؟ (درست است)\n3) بازیابی پورت بعد از رفع علت",
            solution = "جدا کردن سوییچ غیرمجاز، آموزش کاربر، errdisable recovery cause bpduguard با interval مناسب.",
            verification = "پورت up فقط با کلاینت عادی، بدون دریافت BPDU.",
            hints = "BPDU Guard دوست شماست؛ علت را پاک کن نه ویژگی را.",
            difficulty = "ادمین",
            hours = 2,
        ),
        RichScenario(
            name = "TCP Handshake Fail — SYN می‌رود SYN-ACK برنمی‌گردد",
            vendors = "Linux,Windows,Cisco",
            incident = "کلاینت به سرور SYN می‌فرستد ولی SYN-ACK نمی‌رسد؛ سرویس از جای دیگر OK است.",
            business = "اپلیکیشن جدید روی سرور VLAN دیگر. فایروال و ACL در مسیر.",
            symptoms = "• tcpdump سمت کلاینت: فقط SYN\n• سمت سرور: SYN می‌رسد ولی جواب خارج نمی‌شود یا برنمی‌گردد\n• پینگ گاهی OK (ICMP جداست)",
            tasks = "1) capture دو طرفه\n2) ACL/firewall در مسیر برگشت؟\n3) reverse path / uRPF؟\n4) routing برگشت؟\n5) Windows Firewall روی سرور؟",
            solution = "باز کردن protos/ports در هر دو جهت، اصلاح routing، بررسی uRPF، استثنای فایروال میزبان.",
            verification = "handshake کامل در pcap، اتصال اپلیکیشن موفق.",
            hints = "همیشه هر دو جهت را capture کن؛ یک‌طرفه دیدن فریبنده است.",
        ),
        RichScenario(
            name = "Storage Latency — VMها کند با IOPS بالا",
            vendors = "VMware,Linux",
            incident = "VMها کند شده‌اند؛ CPU/RAM عادی، latency دیسک بالا، یک آرایه RAID در حال rebuild.",
            business = "دیتاسنتر کوچک، datastore مشترک. یک دیسک خراب و rebuild شروع شده.",
            symptoms = "• esxtop / iostat: await بالا\n• RAID controller: rebuild in progress\n• لاگ: disk predictive failure قبلاً هشدار داده بود",
            tasks = "1) تأیید rebuild و درصد پیشرفت\n2) آیا دیسک hot-spare درست عمل کرد؟\n3) آیا می‌توان VMهای غیرحیاتی را جابه‌جا کرد؟\n4) برنامه‌ریزی تعویض دیسک و جلوگیری از double-fault",
            solution = "صبوری کنترل‌شده حین rebuild، جابجایی بار اگر ممکن، تعویض دیسک مشکوک بعدی، بررسی سياسة hot-spare.",
            verification = "بعد از اتمام rebuild: latency عادی، vmها responsive، وضعیت آرایه Optimal.",
            hints = "در حین rebuild، بار اضافی نگذار؛ double disk failure = فاجعه.",
            hours = 10,
        ),
        RichScenario(
            name = "SNMP Storm — لینک اشباع از trap/poll",
            vendors = "Cisco",
            incident = "لینک management اشباع شده؛ ترافیک SNMP غیرعادی بالا.",
            business = "نرم‌افزار مانیتورینگ جدید با interval خیلی کوتاه و تعداد زیاد OID.",
            symptoms = "• interface counters: ترافیک management بالا\n• CPU متوسط\n• snmp walkهای موازی زیاد",
            tasks = "1) منبع poll کجاست؟\n2) interval و تعداد OID\n3) جداسازی management VRF/ VLAN؟\n4) rate-limit SNMP؟",
            solution = "افزایش interval، محدود کردن OID، management VRF، ACL برای SNMP، در صورت نیاز rate-limit.",
            verification = "ترافیک management عادی، مانیتورینگ همچنان داده کافی دارد.",
            hints = "مانیتورینگ نباید خودش شبکه را خراب کند.",
            hours = 3,
        ),
        RichScenario(
            name = "GPO در سایت فرعی اعمال نمی‌شود",
            vendors = "Windows",
            incident = "GPO map درایو در سایت فرعی اعمال نمی‌شود؛ در مرکزی OK است.",
            business = "تغییر سیاست برای همه سایت‌ها. کاربران فرعی هنوز درایو قدیمی می‌بینند.",
            symptoms = "• gpresult /r → GPO در لیست نیست یا Denied\n• replication بین DCها؟\n• امنیته لینک یا WMI filter؟",
            tasks = "1) gpupdate /force + gpresult\n2) بررسی replication (repadmin)\n3) لینک GPO به OU درست؟\n4) فیلتر امنیتی و WMI\n5) لاگ Operational GroupPolicy",
            solution = "رفع replication، تأیید لینک و فیلتر، حذف تداخل، تست با کاربر آزمایشی.",
            verification = "gpresult نشان‌دهنده GPO، درایو map شده بعد از logoff/logon.",
            hints = "اول replication را سالم کن؛ بعد GPO.",
        ),
    )

    suspend fun ensure(context: Context): Int = withContext(Dispatchers.IO) {
        val db = AppDatabase.get(context)
        val dao = db.scenarioDao()
        val existing = dao.count()
        if (existing > 0 && db.lessonDao().getMeta(META) == "1" && existing >= RICH.size) {
            return@withContext existing
        }

        val items = RICH.mapIndexed { idx, r ->
            val i = idx + 1
            val code = "CAP-%03d".format(i)
            sc(
                code = code,
                title = r.name,
                users = 200 + (i * 37) % 2800,
                sites = 1 + (i % 5),
                vendors = r.vendors,
                business = r.business,
                req = "پایداری سرویس، جمع‌آوری شواهد، Fix با backup، Verify از کلاینت واقعی، Runbook.",
                constraints = "پنجره Change محدود؛ حداقل قطعی؛ هماهنگی با تیم‌های وابسته.",
                incident = r.incident,
                symptoms = r.symptoms,
                tasks = r.tasks,
                expected = "سرویس پایدار + مستند RCA + Runbook قابل استفاده توسط شیفت بعد",
                hints = r.hints,
                solution = r.solution,
                verification = r.verification,
                difficulty = r.difficulty,
                hours = r.hours,
            )
        }
        val expanded = (1..maxOf(40, RICH.size)).map { i ->
            val base = items[(i - 1) % items.size]
            if (i <= items.size) base
            else base.copy(
                code = "CAP-%03d".format(i),
                titleFa = base.titleFa + " — واریانت #$i",
                users = 150 + (i * 23) % 3200,
            )
        }
        dao.upsertAll(expanded)
        db.lessonDao().putMeta(SyncMetaEntity(META, "1"))
        dao.count()
    }

    private fun sc(
        code: String, title: String, users: Int, sites: Int, vendors: String,
        business: String, req: String, constraints: String,
        incident: String, symptoms: String, tasks: String, expected: String,
        hints: String, solution: String, verification: String,
        difficulty: String, hours: Int,
    ) = ScenarioEntity(
        code = code, titleFa = title, titleEn = code, category = "Capstone",
        level = "L4", difficulty = difficulty, users = users, sites = sites, vendors = vendors,
        businessContext = business, requirements = req, constraintsText = constraints,
        incident = incident, symptoms = symptoms, tasks = tasks, expectedResult = expected,
        objectives = "حل end-to-end با evidence، capture در صورت نیاز، و مستندسازی قابل تحویل",
        hints = hints, solution = solution, verification = verification,
        skillsRequired = vendors, estimatedHours = hours,
    )
}
