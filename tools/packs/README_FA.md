# tools/packs — تنها محل JSON نهایی

## موجودی فعلی (پس از مرتب‌سازی)

| پوشه | محتوا | فصل هدف |
|------|--------|--------|
| `commands_encyclopedia/cisco_switching.json` | دستورات Cisco SW | 68 |
| `commands_encyclopedia/mikrotik.json` | MikroTik (پس از rename) | 68 |
| `routing_deep/chapter_68_cisco_routing_1600.json` | Routing commands (نام فایل تاریخی) | 68 |
| `switching_routing/*` | پک سوییچ/مسیر | merge عنوانی |
| `windows_server/*` | ویندوز سرور | merge |
| `git_chapter64/*` | Git (عمدتاً md) | 64 |
| `vpn_enterprise/` | VPN | 67 |

## قانون

JSON جدید را **فقط اینجا** بگذار. در `commands_encyclopedia/prompts/` نگذار.


## بسته‌های حرفه‌ای Windows/M365 و Linux

| فایل | فصل | درس | آزمون |
|------|------|-----:|------:|
| `windows_admin_professional/ch34_m365_intune_email_professional.json` | ۳۴ — M365، Intune، Conditional Access و ایمیل | ۶۰ | ۱۲۰ |
| `windows_admin_professional/ch35_powershell_cmd_professional.json` | ۳۵ — CMD، PowerShell و اتوماسیون | ۷۵ | ۱۵۰ |
| `linux_services_security/ch36_linux_admin_professional.json` | ۳۶ — مدیریت لینوکس | ۴۵ | ۹۰ |
| `linux_services_security/ch37_linux_network_professional.json` | ۳۷ — شبکه لینوکس | ۴۵ | ۹۰ |
| `linux_services_security/ch38_linux_web_services_professional.json` | ۳۸ — سرویس‌های وب لینوکس | ۴۰ | ۸۰ |
| `linux_services_security/ch39_linux_security_professional.json` | ۳۹ — امنیت لینوکس | ۴۵ | ۹۰ |

هر درس در پنج سطح L0 تا L4 دارای محتوای اجرایی، تمرین lab، عیب‌یابی مبتنی بر شواهد، معیار پذیرش و `meta.assessment.answer_key` جداگانه است. برای فصل‌های Windows/M365، نقش و مجوز، نسخهٔ PowerShell/Module، قابلیت tenant و rollout آزمایشی باید در محیط مقصد بازبینی شود. وضعیت اعتبارسنجی دستورها و قابلیت‌های وابسته به نسخه/tenant: `review_required`.
