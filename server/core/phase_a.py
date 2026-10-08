# -*- coding: utf-8 -*-
"""
فاز A — Enterprise Engineering Layer
- Schema درس غنی‌تر (meta_json + فیلدهای عملیاتی)
- جدول scenarios مستقل
- ۱۰ Capstone سازمانی
- الگوی اجباری L2+: Configure → Verify → Troubleshoot → Document
"""

from __future__ import annotations

import json
from datetime import datetime

# حلقه مهندسی اجباری برای سطح L2 و بالاتر
ENGINEERING_LOOP = [
    "Learn",
    "Configure",
    "Verify",
    "Monitor",
    "Break",
    "Troubleshoot",
    "Secure",
    "Automate",
    "Document",
    "Design",
]

LESSON_META_SCHEMA = {
    "level": "L0-L4",
    "learning_objectives": [],
    "prerequisites": [],
    "keywords_fa": [],
    "keywords_en": [],
    "vendors": [],
    "protocols": [],
    "standards": [],
    "command_categories": ["show", "config", "troubleshoot", "security", "automation"],
    "verification_steps": [],
    "troubleshooting_steps": [],
    "security_notes": [],
    "hardening_notes": [],
    "monitoring_notes": [],
    "automation_notes": [],
    "runbook_ref": "",
    "scenario_ref": "",
    "source_status": "unverified",
    "official_sources": [],
    "ai_search_prompt": "",
    "ai_teach_prompt": "",
    "ai_troubleshoot_prompt": "",
    "ai_quiz_prompt": "",
    "engineering_loop": ENGINEERING_LOOP,
}


def default_meta(title_fa: str, level: str = "L2", vendors=None) -> dict:
    meta = dict(LESSON_META_SCHEMA)
    meta["level"] = level
    meta["vendors"] = vendors or []
    meta["keywords_fa"] = [title_fa]
    meta["learning_objectives"] = [
        f"درک مفهومی {title_fa}",
        "پیکربندی و Verification",
        "عیب‌یابی و مستندسازی Runbook",
    ]
    meta["ai_teach_prompt"] = (
        f"موضوع «{title_fa}» را در سطح {level} آموزش بده. "
        "حتماً بخش‌های Configure، Verify، Troubleshoot و Document را جداگانه بیاور. "
        "دستورات را با توضیح آرگومان بنویس. سناریوی سازمانی مثال بزن."
    )
    meta["ai_search_prompt"] = (
        f"فقط از مستندات رسمی Vendor/RFC برای «{title_fa}» سطح {level} جستجو کن."
    )
    meta["ai_troubleshoot_prompt"] = (
        f"برای مشکل مرتبط با «{title_fa}» مسیر Symptom→Scope→Evidence→RootCause→Fix→Verify را بنویس."
    )
    meta["ai_quiz_prompt"] = (
        f"۵ سؤال سطح {level} درباره «{title_fa}» با پاسخ کوتاه بساز."
    )
    if level in ("L2", "L3", "L4"):
        meta["verification_steps"] = [
            "پیکربندی ذخیره و backup گرفته شود",
            "show/status معادل بررسی شود",
            "تست end-to-end از کلاینت نمونه",
        ]
        meta["troubleshooting_steps"] = [
            "علائم و محدوده را مشخص کن",
            "لایه OSI را ایزوله کن",
            "شواهد (log/capture/counter) جمع کن",
            "فرضیه بساز و تست کن",
            "اصلاح، Verify، مستند کن",
        ]
    return meta


# ---------- ۱۰ Capstone ----------
CAPSTONE_SCENARIOS = [
    {
        "code": "CAPSTONE-01",
        "title_fa": "سازمان ۳۰۰۰ کاربر — ۴ سایت — Cisco + MikroTik + FortiGate + AD + VMware",
        "title_en": "3000-User Multi-Site Enterprise",
        "category": "Capstone",
        "level": "L4",
        "difficulty": "خبره",
        "users": 3000,
        "sites": 4,
        "vendors": "Cisco,MikroTik,FortiGate,Microsoft,VMware",
        "business_context": "سازمان چندسایته با نیاز به هویت متمرکز، اینترنت دو ISP، VoIP و CCTV.",
        "requirements": "سگمنت‌بندی VLAN، HA لبه، AD چندسایت، مانیتورینگ مرکزی، بکاپ و DR سبک.",
        "constraints": "بودجه محدود برای لینک‌های WAN؛ باید failover زیر ۵ دقیقه باشد.",
        "initial_state": "طراحی روی کاغذ؛ هنوز پیاده‌سازی نشده.",
        "incident": "",
        "symptoms": "",
        "objectives": "HLD→LLD→IP Plan→Policy→Verification→Runbookهای حیاتی.",
        "tasks": "1) معماری شبکه و هویت\n2) طرح IP/VLAN\n3) لبه HA\n4) AD Sites\n5) مانیتورینگ\n6) Runbook WAN/AD",
        "hints": "Failure Domain هر سایت را جدا کنید؛ Core مشترک را SPOF نکنید.",
        "expected_result": "سند HLD/LLD + چک‌لیست Verify + ۳ Runbook.",
        "solution": "",
        "verification": "Failover ISP، لاگین AD از سایت دور، پینگ بین سگمنت‌ها.",
        "skills_required": "Routing,FW,AD,Virtualization,Architecture",
        "estimated_hours": 40,
    },
    {
        "code": "CAPSTONE-02",
        "title_fa": "Data Center — Leaf-Spine + EVPN/VXLAN + VMware + Kubernetes",
        "title_en": "DC Leaf-Spine EVPN",
        "category": "Capstone",
        "level": "L4",
        "difficulty": "خبره",
        "users": 0,
        "sites": 1,
        "vendors": "Cisco,VMware,Kubernetes",
        "business_context": "DC جدید برای workload ترکیبی VM و Container.",
        "requirements": "Underlay/Overlay، Multi-Tenancy، HA، مشاهده‌پذیری.",
        "constraints": "تیم کوچک؛ اتوماسیون الزامی است.",
        "initial_state": "رک و برگ‌ها نصب فیزیکی شده‌اند.",
        "incident": "",
        "symptoms": "",
        "objectives": "طراحی و سند عملیاتی DC شبکه.",
        "tasks": "Underlay OSPF/IS-IS، EVPN، vSphere networking، K8s CNI، مانیتورینگ.",
        "hints": "East-West را جدا از North-South ببینید.",
        "expected_result": "توپولوژی + سیاست Multi-Tenant + Runbook لینک Leaf.",
        "solution": "",
        "verification": "vMotion، Pod networking، قطع یک Leaf.",
        "skills_required": "EVPN,VXLAN,VMware,K8s",
        "estimated_hours": 48,
    },
    {
        "code": "CAPSTONE-03",
        "title_fa": "Hybrid Cloud — On-Prem + Azure/AWS",
        "title_en": "Hybrid Cloud Connectivity",
        "category": "Capstone",
        "level": "L4",
        "difficulty": "خبره",
        "users": 1500,
        "sites": 2,
        "vendors": "Azure,AWS,FortiGate,Microsoft",
        "business_context": "انتقال تدریجی سرویس‌ها به ابر با هویت Hybrid.",
        "requirements": "VPN/ExpressRoute، DNS Hybrid، کنترل هویت، امنیت لبه.",
        "constraints": "برخی سرورها نباید به اینترنت مستقیم بروند.",
        "initial_state": "AD on-prem موجود است.",
        "incident": "",
        "symptoms": "",
        "objectives": "اتصال امن و قابل‌مانیتور Hybrid.",
        "tasks": "طراحی شبکه ابر، هویت، مسیریابی، Backup به ابر.",
        "hints": "از Dual-Homed VPN شروع کنید؛ بعد مدار اختصاصی.",
        "expected_result": "نقشه Hybrid + Policy + Runbook قطع تونل.",
        "solution": "",
        "verification": "SSO، وضوح نام DNS، failover تونل.",
        "skills_required": "Cloud Networking,Identity,VPN",
        "estimated_hours": 36,
    },
    {
        "code": "CAPSTONE-04",
        "title_fa": "Ransomware — پاسخ حادثه سراسری",
        "title_en": "Enterprise Ransomware Response",
        "category": "Security Incident",
        "level": "L4",
        "difficulty": "خبره",
        "users": 3000,
        "sites": 4,
        "vendors": "Microsoft,FortiGate,Veeam",
        "business_context": "رمزشدن فایل‌سرورها و انتشار در چند VLAN.",
        "requirements": "ایزوله، حفظ شواهد، بازیابی از Immutable Backup.",
        "constraints": "پرداخت باج ممنوع؛ حداکثر توقف کسب‌وکار ۲۴ساعت برای سرویس حیاتی.",
        "initial_state": "آلرت EDR و شکایت کاربران.",
        "incident": "Ransomware spreading",
        "symptoms": "فایل‌های رمزشده، CPU بالا، ترافیک SMB مشکوک.",
        "objectives": "Contain → Eradicate → Recover → Lessons Learned.",
        "tasks": "ایزوله‌سازی شبکه، غیرفعال‌سازی حساب‌ها، بازیابی، Hardening.",
        "hints": "اول حرکت جانبی را قطع کنید؛ Backup را به شبکه آلوده وصل نکنید.",
        "expected_result": "EOP اجرا شده + گزارش IR + تغییرات کنترلی.",
        "solution": "",
        "verification": "سرویس حیاتی بالا؛ IOC پاک؛ Backup تست‌شده.",
        "skills_required": "IR,Backup,Network Segmentation,AD",
        "estimated_hours": 24,
    },
    {
        "code": "CAPSTONE-05",
        "title_fa": "از دست رفتن کامل Data Center و فعال‌سازی DR",
        "title_en": "DC Total Loss DR",
        "category": "Disaster",
        "level": "L4",
        "difficulty": "خبره",
        "users": 3000,
        "sites": 2,
        "vendors": "VMware,Veeam,FortiGate,Microsoft",
        "business_context": "سایت اصلی از دسترس خارج شده است.",
        "requirements": "اعلام Disaster، فعال‌سازی DR، تغییر DNS، بازیابی هویت.",
        "constraints": "RTO هویت ۴ ساعت؛ RPO داده ۱ ساعت.",
        "initial_state": "DR قبلاً پیکربندی شده اما سالی یک‌بار تست شده.",
        "incident": "DC power/network total failure",
        "symptoms": "قطع کامل سرویس‌های سایت اصلی.",
        "objectives": "اجرای Runbook DR تا Resume کسب‌وکار.",
        "tasks": "Declare → Activate → DNS/Identity/Network/Storage/App → Validate.",
        "hints": "ترتیب وابستگی سرویس‌ها را رعایت کنید.",
        "expected_result": "سرویس‌های حیاتی روی DR؛ سند زمان‌بندی واقعی RTO.",
        "solution": "",
        "verification": "لاگین کاربران، دسترسی فایل، ایمیل، VPN.",
        "skills_required": "DR,DNS,AD,Backup",
        "estimated_hours": 30,
    },
    {
        "code": "CAPSTONE-06",
        "title_fa": "BGP Route Leak / Hijack",
        "title_en": "BGP Route Leak Incident",
        "category": "Security Incident",
        "level": "L4",
        "difficulty": "خبره",
        "users": 0,
        "sites": 1,
        "vendors": "Cisco,ISP",
        "business_context": "ترافیک به مقصد اشتباه می‌رود؛ گزارش‌های بیرونی از Hijack.",
        "requirements": "تشخیص، فیلتر، RPKI/ROA، ارتباط با ISP.",
        "constraints": "دسترسی فقط به لبه سازمانی و لاگ‌ها.",
        "initial_state": "BGP با دو Upstream.",
        "incident": "Route leak/hijack",
        "symptoms": "Latency غیرعادی، Traceroute عجیب، prefixهای ناخواسته.",
        "objectives": "مهار مسیر، Harden فیلترها، مستند کردن.",
        "tasks": "تحلیل جدول BGP، prefix-list، ارتباط ISP، RPKI.",
        "hints": "بogon و prefix خودتان را سخت فیلتر کنید.",
        "expected_result": "مسیر پایدار + سیاست فیلتر به‌روز + Runbook.",
        "solution": "",
        "verification": "show ip bgp؛ رسیدن ترافیک از مسیر درست.",
        "skills_required": "BGP,RPKI,Security",
        "estimated_hours": 16,
    },
    {
        "code": "CAPSTONE-07",
        "title_fa": "خرابی AD / Kerberos / DNS",
        "title_en": "AD Kerberos DNS Failure",
        "category": "Troubleshooting",
        "level": "L3",
        "difficulty": "پیشرفته",
        "users": 3000,
        "sites": 4,
        "vendors": "Microsoft",
        "business_context": "کاربران سایت ۳ نمی‌توانند احراز هویت کنند.",
        "requirements": "پیدا کردن Root Cause در زنجیره DNS→DC Locator→Kerberos→Replication→Time.",
        "constraints": "تغییر بزرگ در ساعت اداری ممنوع مگر Escalate.",
        "initial_state": "سایر سایت‌ها سالم به نظر می‌رسند.",
        "incident": "Auth failure site-3",
        "symptoms": "خطای Trust/Kerberos؛ GPO اعمال نمی‌شود.",
        "objectives": "Ripple را پیدا و رفع کنید؛ Runbook بنویسید.",
        "tasks": "DNS SRV، nltest، repadmin، time skew، فایروال بین سایت.",
        "hints": "اول DNS و زمان را چک کنید.",
        "expected_result": "احراز هویت پایدار + شواهد + Runbook.",
        "solution": "",
        "verification": "logon کاربر تست، اعمال GPO، event بدون خطای مکرر.",
        "skills_required": "AD,DNS,Kerberos",
        "estimated_hours": 12,
    },
    {
        "code": "CAPSTONE-08",
        "title_fa": "بحران کیفیت VoIP",
        "title_en": "VoIP Quality Disaster",
        "category": "Troubleshooting",
        "level": "L3",
        "difficulty": "پیشرفته",
        "users": 500,
        "sites": 2,
        "vendors": "MikroTik,Cisco,Issabel",
        "business_context": "مکالمات قطع‌قطعی وエコー در ساعات اوج.",
        "requirements": "QoS، بررسی WAN، SIP/RTP، بدون مختل کردن اینترنت کاربران.",
        "constraints": "لینک WAN 50Mbps مشترک با اینترنت.",
        "initial_state": "QoS ناقص یا غیرفعال.",
        "incident": "Voice quality degradation",
        "symptoms": "Jitter، Loss، One-way audio.",
        "objectives": "پایدارسازی صوت و Runbook کیفیت.",
        "tasks": "اندازه‌گیری، علامت‌گذاری DSCP، Queue، SIP ALG، VLAN صوت.",
        "hints": "RTP را جدا از مشکل SIP signaling ببینید.",
        "expected_result": "MOS قابل قبول در اوج بار + مستند.",
        "solution": "",
        "verification": "تست مکالمه همزمان چند کانال؛ گراف jitter/loss.",
        "skills_required": "QoS,VoIP,WAN",
        "estimated_hours": 10,
    },
    {
        "code": "CAPSTONE-09",
        "title_fa": "بحران ظرفیت Wi-Fi سازمانی",
        "title_en": "Enterprise Wi-Fi Capacity Disaster",
        "category": "Troubleshooting",
        "level": "L3",
        "difficulty": "پیشرفته",
        "users": 800,
        "sites": 1,
        "vendors": "Cisco,MikroTik",
        "business_context": "در سالن همایش و طبقات شلوغ، وای‌فای از کار می‌افتد.",
        "requirements": "Channel plan، Density، Roaming، جداسازی Guest.",
        "constraints": "خرید AP محدود؛ باید با تنظیمات بهبود داد.",
        "initial_state": "قدرت فرستنده بالا و کانال‌های همپوشان.",
        "incident": "Wi-Fi capacity collapse",
        "symptoms": "ارتباط می‌گیرد ولی اینترنت ندارد؛ روامینگ ضعیف.",
        "objectives": "طراحی مجدد RF و Validation.",
        "tasks": "Survey، کانال، قدرت، band steering، ظرفیت DHCP.",
        "hints": "اول تداخل و تعداد client per AP را بسنجید.",
        "expected_result": "پایداری در تراکم + گزارش قبل/بعد.",
        "solution": "",
        "verification": "تست با تعداد کلاینت بالا؛ roaming صوت روی وای‌فای.",
        "skills_required": "Wireless,RF,DHCP",
        "estimated_hours": 14,
    },
    {
        "code": "CAPSTONE-10",
        "title_fa": "ساخت سازمان از صفر — Business تا Operations",
        "title_en": "Greenfield Enterprise Build",
        "category": "Capstone",
        "level": "L4",
        "difficulty": "خبره",
        "users": 1000,
        "sites": 2,
        "vendors": "Cisco,MikroTik,FortiGate,Microsoft,VMware",
        "business_context": "شرکت جدید؛ هیچ زیرساختی نیست.",
        "requirements": "از نیاز کسب‌وکار تا عملیات پایدار و مستند.",
        "constraints": "زمان ۱۲ هفته؛ باید فازبندی شود.",
        "initial_state": "فقط قرارداد اجاره و تعداد کاربران مشخص است.",
        "incident": "",
        "symptoms": "",
        "objectives": "Business→Requirement→Architecture→HLD→LLD→BOM→Implement→Secure→Monitor→Backup→DR→Docs→Ops",
        "tasks": "تمام زنجیره را سند و نمونه پیکربندی کنید.",
        "hints": "اول سرویس‌های حیاتی (Identity, DNS, DHCP, Internet, Backup).",
        "expected_result": "بسته کامل تحویل پروژه + Runbookها + چک‌لیست NOC.",
        "solution": "",
        "verification": "پذیرش توسط «کارفرما» فرضی بر اساس Acceptance Criteria.",
        "skills_required": "Architecture,Operations,All Domains",
        "estimated_hours": 80,
    },
]


def ensure_phase_a_schema(db):
    """افزودن ستون‌ها و جدول scenarios — بدون حذف داده."""
    cols = [
        ("lessons", "meta_json", "TEXT DEFAULT '{}'"),
        ("lessons", "verification", "TEXT DEFAULT ''"),
        ("lessons", "learning_objectives", "TEXT DEFAULT ''"),
        ("lessons", "prerequisites", "TEXT DEFAULT ''"),
        ("lessons", "source_status", "TEXT DEFAULT 'unverified'"),
        ("lessons", "runbook_ref", "TEXT DEFAULT ''"),
        ("lessons", "scenario_ref", "TEXT DEFAULT ''"),
    ]
    for table, column, definition in cols:
        try:
            db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        except Exception:
            pass

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            title_fa TEXT NOT NULL,
            title_en TEXT,
            category TEXT DEFAULT 'Capstone',
            level TEXT DEFAULT 'L4',
            difficulty TEXT DEFAULT 'خبره',
            users INTEGER DEFAULT 0,
            sites INTEGER DEFAULT 1,
            vendors TEXT DEFAULT '',
            business_context TEXT DEFAULT '',
            requirements TEXT DEFAULT '',
            constraints_text TEXT DEFAULT '',
            initial_state TEXT DEFAULT '',
            incident TEXT DEFAULT '',
            symptoms TEXT DEFAULT '',
            objectives TEXT DEFAULT '',
            tasks TEXT DEFAULT '',
            hints TEXT DEFAULT '',
            expected_result TEXT DEFAULT '',
            solution TEXT DEFAULT '',
            verification TEXT DEFAULT '',
            skills_required TEXT DEFAULT '',
            estimated_hours INTEGER DEFAULT 8,
            is_deleted INTEGER DEFAULT 0,
            last_updated TEXT
        )
        """
    )


def seed_capstone_scenarios(db):
    """درج/به‌روزرسانی ۱۰ Capstone."""
    ensure_phase_a_schema(db)
    now = datetime.now().isoformat()
    added = 0
    updated = 0
    for sc in CAPSTONE_SCENARIOS:
        row = db.fetchone("SELECT id FROM scenarios WHERE code=?", (sc["code"],))
        fields = (
            sc["title_fa"],
            sc["title_en"],
            sc["category"],
            sc["level"],
            sc["difficulty"],
            sc["users"],
            sc["sites"],
            sc["vendors"],
            sc["business_context"],
            sc["requirements"],
            sc["constraints"],
            sc["initial_state"],
            sc["incident"],
            sc["symptoms"],
            sc["objectives"],
            sc["tasks"],
            sc["hints"],
            sc["expected_result"],
            sc["solution"],
            sc["verification"],
            sc["skills_required"],
            sc["estimated_hours"],
            now,
        )
        if row:
            db.execute(
                """UPDATE scenarios SET
                    title_fa=?, title_en=?, category=?, level=?, difficulty=?,
                    users=?, sites=?, vendors=?, business_context=?, requirements=?,
                    constraints_text=?, initial_state=?, incident=?, symptoms=?,
                    objectives=?, tasks=?, hints=?, expected_result=?, solution=?,
                    verification=?, skills_required=?, estimated_hours=?, last_updated=?
                    WHERE code=?""",
                fields + (sc["code"],),
            )
            updated += 1
        else:
            db.execute(
                """INSERT INTO scenarios (
                    code, title_fa, title_en, category, level, difficulty,
                    users, sites, vendors, business_context, requirements,
                    constraints_text, initial_state, incident, symptoms,
                    objectives, tasks, hints, expected_result, solution,
                    verification, skills_required, estimated_hours, last_updated
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (sc["code"],) + fields,
            )
            added += 1
    return {"added": added, "updated": updated, "total": len(CAPSTONE_SCENARIOS)}


def apply_phase_a_meta(db, only_empty=True, limit=None):
    """پر کردن meta_json و پرامپت‌ها برای درس‌ها."""
    ensure_phase_a_schema(db)
    rows = db.fetchall(
        "SELECT id, title_fa, tags, meta_json, search_query FROM lessons WHERE COALESCE(is_deleted,0)=0"
    )
    n = 0
    for r in rows:
        if only_empty and r["meta_json"] and r["meta_json"] not in ("", "{}"):
            continue
        tag = (r["tags"] or "L2").split(",")[0].strip() or "L2"
        meta = default_meta(r["title_fa"], level=tag)
        db.execute(
            """UPDATE lessons SET meta_json=?, search_query=COALESCE(NULLIF(search_query,''), ?),
               learning_objectives=?, source_status=COALESCE(NULLIF(source_status,''), 'unverified')
               WHERE id=?""",
            (
                json.dumps(meta, ensure_ascii=False),
                meta["ai_search_prompt"],
                "\n".join(meta["learning_objectives"]),
                r["id"],
            ),
        )
        n += 1
        if limit and n >= limit:
            break
    return n


def engineering_loop_text(level: str = "L2") -> str:
    if level in ("L0", "L1"):
        return "Learn → مثال ساده → جمع‌بندی"
    return " → ".join(ENGINEERING_LOOP)
