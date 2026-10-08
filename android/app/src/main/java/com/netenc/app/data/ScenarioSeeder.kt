package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/** ۱۰ سناریوی Capstone سازمانی — آفلاین */
object ScenarioSeeder {
    private const val META = "scenarios_seeded_v1"

    suspend fun ensure(context: Context): Int = withContext(Dispatchers.IO) {
        val db = AppDatabase.get(context)
        val dao = db.scenarioDao()
        if (db.lessonDao().getMeta(META) == "1" && dao.count() >= 8) return@withContext dao.count()

        val items = listOf(
            sc("CAPSTONE-01", "سازمان ۳۰۰۰ کاربر — ۴ سایت — Cisco + MikroTik + FortiGate + AD + VMware",
                3000, 4, "Cisco,MikroTik,FortiGate,Microsoft,VMware",
                "سازمان چندسایته با هویت متمرکز، اینترنت دو ISP، VoIP و CCTV.",
                "سگمنت VLAN، HA لبه، AD چندسایت، مانیتورینگ، بکاپ و DR سبک.",
                "بودجه محدود WAN؛ failover زیر ۵ دقیقه.",
                "کاربران سایت ۳ نمی‌توانند authenticate شوند.",
                "بررسی DNS → DC Locator → SRV → Kerberos → Replication → Site/Subnet → Firewall → NTP",
                "بازیابی احراز هویت و مستندسازی Runbook"),
            sc("CAPSTONE-02", "قطع لینک اصلی ISP و Failover BGP/Policy",
                1500, 2, "Cisco,FortiGate",
                "دو ISP با BGP یا Policy Route؛ نیاز به تداوم اینترنت و VPN.",
                "Failover خودکار، حفظ Sessionهای حیاتی، مانیتورینگ لینک.",
                "SLA اینترنت ۹۹.۵٪؛ پنجره تست محدود.",
                "لینک ISP-A قطع شده؛ ترافیک باید به ISP-B برود.",
                "بررسی default route، health-check، NAT، VPN و DNS public.",
                "ترافیک پایدار روی ISP-B و بازگشت کنترل‌شده"),
            sc("CAPSTONE-03", "طراحی Campus با VLAN/STP/Trunk و Core-Distribution",
                800, 1, "Cisco",
                "یک پردیس با چند ساختمان و Access Switch.",
                "VLAN استاندارد، Trunk، STP root، Gateway HSRP/VRRP.",
                "تجهیزات mixed-vendor در Access.",
                "Loop در یک Access و قطعی پراکنده.",
                "بررسی STP state، BPDU guard، trunk allow list، storm control.",
                "پایداری L2 و مستند توپولوژی"),
            sc("CAPSTONE-04", "FortiGate Zone/Policy و بازرسی SSL در لبه",
                2000, 1, "FortiGate",
                "لبه اینترنت با نیاز به Policy دقیق LAN/WAN/DMZ/MGMT.",
                "Zone، Policy، NAT، IPS پایه، لاگ به SIEM.",
                "نباید MGMT از اینترنت باز باشد.",
                "کاربر به یک سرویس DMZ دسترسی ندارد.",
                "Policy hit count، route، DNS، sniffer، certificate.",
                "دسترسی صحیح + Hardening لبه"),
            sc("CAPSTONE-05", "Active Directory Multi-Site و DNS یکپارچه",
                2500, 3, "Microsoft",
                "چند DC در چند سایت با AD-integrated DNS.",
                "Site/Subnet، Replication، GC، Time sync.",
                "یک سایت لینک ضعیف دارد.",
                "Logon کند و Ticket خطا.",
                "nltest، repadmin، dcdiag، DNS SRV، NTP.",
                "Logon پایدار در همه سایت‌ها"),
            sc("CAPSTONE-06", "VMware/Hypervisor HA و Storage حساس",
                1200, 1, "VMware",
                "خوشه مجازی با نیاز به HA و backup.",
                "HA/DRS، Datastore، شبکه VM، snapshot policy.",
                "یک Host از دست می‌رود.",
                "VMهای حیاتی باید جابه‌جا شوند.",
                "vMotion، HA admission، datastore path، NIC teaming.",
                "بازیابی VM و گزارش ظرفیت"),
            sc("CAPSTONE-07", "Wi-Fi سازمانی Roaming و Controller",
                900, 1, "Cisco,Ubiquiti",
                "پوشش انبار و اداری با Roaming.",
                "SSID، VLAN، RF، Controller/Cloud.",
                "تداخل کانال و قدرت نامناسب.",
                "قطع مکالمه VoIP روی Wi-Fi.",
                "کانال، قدرت، DHCP option، QoS، roaming log.",
                "Roaming پایدار و SNR قابل قبول"),
            sc("CAPSTONE-08", "Backup/DR با RPO/RTO تعریف‌شده",
                1800, 2, "Veeam,Windows,Linux",
                "نیاز به بازیابی سرویس‌های حیاتی زیر ۲ ساعت.",
                "Backup 3-2-1، تست restore ماهانه.",
                "بودجه نوار/کلود محدود.",
                "خرابی datastore اصلی.",
                "آخرین backup موفق، restore test، DNS و identity بعد از restore.",
                "سرویس حیاتی با RTO رعایت‌شده بالا می‌آید"),
            sc("CAPSTONE-09", "Automation اولیه با Ansible برای Switchها",
                600, 1, "Cisco,MikroTik,Ansible",
                "پیکربندی تکراری VLAN روی ۲۰ سوئیچ.",
                "Inventory، Playbook، idempotent config، backup قبل از push.",
                "دسترسی SSH فقط از MGMT.",
                "یک سوئیچ بعد از push دسترس‌ناپذیر شد.",
                "rollback از backup، out-of-band، diff قبل از apply.",
                "Playbook پایدار و مستند"),
            sc("CAPSTONE-10", "SOC سبک: لاگ لبه + تشخیص حادثه اولیه",
                2200, 1, "FortiGate,Windows,ELK",
                "نیاز به دید روی تلاش‌های brute-force و policy deny.",
                "جمع‌آوری لاگ، داشبورد، alert ساده.",
                "تیم کوچک؛ بدون SOC کامل.",
                "افزایش login failure روی VPN.",
                "همبستگی IP، geo، time، account lockout.",
                "Alert عملی و Runbook پاسخ"),
        )
        dao.upsertAll(items)
        db.lessonDao().putMeta(SyncMetaEntity(META, "1"))
        dao.count()
    }

    private fun sc(
        code: String, title: String, users: Int, sites: Int, vendors: String,
        business: String, req: String, constraints: String,
        incident: String, tasks: String, expected: String
    ) = ScenarioEntity(
        code = code,
        titleFa = title,
        titleEn = code,
        category = "Capstone",
        level = "L4",
        difficulty = "خبره",
        users = users,
        sites = sites,
        vendors = vendors,
        businessContext = business,
        requirements = req,
        constraintsText = constraints,
        incident = incident,
        symptoms = incident,
        tasks = tasks,
        expectedResult = expected,
        objectives = "حل مسئله سازمانی end-to-end و مستندسازی",
        hints = "از لایه فیزیکی/لینک تا Application و Identity بالا بروید.",
        solution = "مسیر ساخت‌یافته: Scope → Evidence → RootCause → Fix → Verify → Document",
        verification = "تست از کلاینت واقعی + لاگ + وضعیت سرویس وابسته",
        skillsRequired = vendors,
        estimatedHours = 8
    )
}
