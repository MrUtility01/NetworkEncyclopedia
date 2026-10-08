package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object ScenarioSeeder {
    private const val META = "scenarios_seeded_v4"

    private val TOPICS = listOf(
        Triple("VLAN و سگمنت‌بندی", "Cisco,MikroTik", "کلاینت‌های VLAN10 به سرور VLAN20 دسترسی ندارند؛ ARP ناقص"),
        Triple("STP Loop", "Cisco", "broadcast storm بعد از اتصال لینک جدید؛ CPU سوییچ بالا"),
        Triple("OSPF Area", "Cisco,MikroTik", "مسیر Area1 در Area0 دیده نمی‌شود؛ Neighbor stuck in 2-Way"),
        Triple("BGP Failover", "Cisco,Linux", "قطع لینک ISP1 ولی ترافیک به ISP2 سوییچ نمی‌شود"),
        Triple("ACL اشتباه", "Cisco,FortiGate", "سرویس HTTPS قطع شده بعد از اعمال ACL جدید"),
        Triple("NAT Overload", "Cisco,MikroTik", "کاربران اینترنت یک‌طرفه؛ translation table پر"),
        Triple("VPN IPSec", "FortiGate,Cisco", "Phase1 up ولی Phase2 down"),
        Triple("HA فایروال", "FortiGate", "Failover انجام شد ولی sessionها drop شدند"),
        Triple("DNS Split-Horizon", "Windows,Linux", "نام داخلی از بیرون resolve می‌شود"),
        Triple("DHCP Scope Exhaust", "Windows,Cisco", "کلاینت‌های جدید APIPA می‌گیرند"),
        Triple("AD Site Replication", "Windows", "GPO در سایت فرعی اعمال نمی‌شود"),
        Triple("Kerberos Time Skew", "Windows", "Login با خطای clock skew"),
        Triple("Wi-Fi Roaming", "Cisco WLC", "کلاینت هنگام جابجایی AP قطع می‌شود"),
        Triple("MTU Blackhole", "Cisco,Linux", "TCP بزرگ fail؛ ping کوچک OK"),
        Triple("HSRP Split-Brain", "Cisco", "دو Active هم‌زمان؛ VIP تکراری"),
        Triple("SNMP Storm", "Cisco", "لینک اشباع از trap/poll"),
        Triple("Port Security", "Cisco", "پورت err-disabled بعد از تعویض NIC"),
        Triple("BPDU Guard", "Cisco", "پورت access با دریافت BPDU خاموش شد"),
        Triple("TCP Handshake Fail", "Linux,Windows", "SYN ارسال می‌شود؛ SYN-ACK نمی‌رسد"),
        Triple("Storage Latency", "VMware,Linux", "VM کند؛ IOPS بالا")
    )

    suspend fun ensure(context: Context): Int = withContext(Dispatchers.IO) {
        val db = AppDatabase.get(context)
        val dao = db.scenarioDao()
        val existing = dao.count()
        if (existing > 0 && db.lessonDao().getMeta(META) == "1" && existing >= 40) {
            return@withContext existing
        }

        val items = (1..200).map { i ->
            val (name, vendors, incident) = TOPICS[(i - 1) % TOPICS.size]
            val code = "CAP-%03d".format(i)
            sc(
                code = code,
                title = "$name — سناریوی سازمانی #$i",
                users = 200 + (i * 17) % 3000,
                sites = 1 + (i % 6),
                vendors = vendors,
                business = "سازمان چندسایته با تمرکز روی $name.",
                req = "پایداری سرویس، Verify، capture، Runbook برای $name.",
                constraints = "پنجره Change محدود؛ حداقل قطعی.",
                incident = incident,
                tasks = "1) Scope 2) Evidence 3) Hypothesis 4) Fix+backup 5) Verify 6) Document — $name",
                expected = "سرویس پایدار + Runbook",
                hints = "از L1 شروع؛ بکاپ قبل از change.",
                solution = "RCA: Symptom→Scope→Evidence→Fix→Verify | $vendors",
                verification = "کلاینت واقعی + لاگ + در صورت نیاز pcap"
            )
        }
        dao.upsertAll(items)
        db.lessonDao().putMeta(SyncMetaEntity(META, "1"))
        dao.count()
    }

    private fun sc(
        code: String, title: String, users: Int, sites: Int, vendors: String,
        business: String, req: String, constraints: String,
        incident: String, tasks: String, expected: String,
        hints: String, solution: String, verification: String
    ) = ScenarioEntity(
        code = code, titleFa = title, titleEn = code, category = "Capstone",
        level = "L4", difficulty = "خبره", users = users, sites = sites, vendors = vendors,
        businessContext = business, requirements = req, constraintsText = constraints,
        incident = incident, symptoms = incident, tasks = tasks, expectedResult = expected,
        objectives = "حل end-to-end با capture و مستندسازی",
        hints = hints, solution = solution, verification = verification,
        skillsRequired = vendors, estimatedHours = 6
    )
}
