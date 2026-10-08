package com.netenc.app.data

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/** ۲۰۰ سناریوی سازمانی Capstone */
object ScenarioSeeder {
    private const val META = "scenarios_seeded_v2"

    private val TOPICS = listOf(
        "VLAN و سگمنت‌بندی", "STP Loop", "OSPF Area", "BGP Failover", "ACL اشتباه",
        "NAT Overload", "VPN IPSec", "HA فایروال", "DNS Split-Horizon", "DHCP Scope Exhaust",
        "AD Site Replication", "Kerberos Time Skew", "GPO نیمه‌اعمال", "Wi-Fi Roaming",
        "VoIP QoS", "SPAN Capture", "MTU Blackhole", "Asymmetric Routing", "HSRP Split-Brain",
        "Certificate Expiry", "Proxy Auth", "WAF False Positive", "Backup Restore Fail",
        "Storage Latency", "VM HA Admission", "NPS RADIUS", "SNMP Storm", "NTP Drift",
        "IPv6 Dual-Stack", "SD-WAN Brownout", "Container Network Policy", "Zero Trust Policy",
        "Packet Header Anomaly", "TCP Handshake Fail", "UDP Loss", "QoS Remark",
        "Port Security", "Storm Control", "BPDU Guard", "Root Guard"
    )
    private val VENDORS = listOf("Cisco", "MikroTik", "FortiGate", "Windows", "Linux", "VMware", "Mixed")

    suspend fun ensure(context: Context): Int = withContext(Dispatchers.IO) {
        val db = AppDatabase.get(context)
        val dao = db.scenarioDao()
        if (db.lessonDao().getMeta(META) == "1" && dao.count() >= 150) return@withContext dao.count()

        val items = (1..200).map { i ->
            val t = TOPICS[(i - 1) % TOPICS.size]
            val v = VENDORS[(i - 1) % VENDORS.size]
            val code = "CAP-%03d".format(i)
            sc(
                code = code,
                title = "$t — سناریوی سازمانی #$i",
                users = 200 + (i * 17) % 3000,
                sites = 1 + (i % 6),
                vendors = v,
                business = "سازمان با تمرکز عملیاتی روی $t.",
                req = "پایداری، Verify، capture و مستندسازی $t.",
                constraints = "پنجره Change محدود؛ حداقل قطعی.",
                incident = "علائم $t در سگمنت/سایت نمونه.",
                tasks = "Scope→Capture/Header→Route/Policy/Identity→Fix→Verify ($t)",
                expected = "سرویس پایدار + Runbook + نمونه پکت مستند"
            )
        }
        dao.upsertAll(items)
        db.lessonDao().putMeta(SyncMetaEntity(META, "1"))
        dao.count()
    }

    private fun sc(
        code: String, title: String, users: Int, sites: Int, vendors: String,
        business: String, req: String, constraints: String,
        incident: String, tasks: String, expected: String
    ) = ScenarioEntity(
        code = code, titleFa = title, titleEn = code, category = "Capstone",
        level = "L4", difficulty = "خبره", users = users, sites = sites, vendors = vendors,
        businessContext = business, requirements = req, constraintsText = constraints,
        incident = incident, symptoms = incident, tasks = tasks, expectedResult = expected,
        objectives = "حل end-to-end با capture و مستند",
        hints = "هدر/پکت را در نقطه درست بگیرید؛ از L1 تا Identity بالا بروید.",
        solution = "Symptom→Scope→Evidence→RootCause→Fix→Verify→Document",
        verification = "کلاینت + لاگ + capture",
        skillsRequired = vendors, estimatedHours = 6
    )
}
