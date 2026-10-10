# پرامپت‌های تولید محتوا — فصل‌به‌فصل

مسیر: `tools/chapter_prompts/`

## ساختار
```
tools/chapter_prompts/
  README_FA.md                 ← همین فایل
  _MASTER_PROMPT.md            ← قوانین مشترک JSON
  INDEX.md                     ← فهرست همه فصل‌ها
  priority/                    ← ۴ اولویت فوری
    01_ospf_bgp_redistribution.md
    02_vpn_ipsec_ssl.md
    03_firewall_practical.md
    04_network_troubleshooting.md
  chapters/
    ch01.md … ch67.md          ← پرامپت اختصاصی هر فصل
```

## چطور استفاده کنی
1. فایل `_MASTER_PROMPT.md` + فایل فصل (یا priority) را به ChatGPT بده.
2. JSON خروجی را بگذار در: `tools/packs/chNN_slug/name_pack.json`
3. واردسازی:
```bash
python tools/apply_any_pack.py --db server/data/encyclopedia.db --pack tools/packs/.../file.json --apply
```
4. اندروید: commit + push + Actions → Build Android APK

## چهار اولویت
| فایل | موضوع | فصل هدف |
|------|--------|--------|
| priority/01_… | OSPF+BGP+Redistribution | ۱۴ / ۶۶ |
| priority/02_… | VPN IPsec/SSL | ۲۱ / ۲۴ / ۶۷ |
| priority/03_… | فایروال عملی | ۲۰ / ۲۴ / ۲۵ |
| priority/04_… | عیب‌یابی سیستماتیک | ۶۰ / ۶۲ |

اگر پوشه `chapters/` خالی بود:
```bash
python tools/chapter_prompts/generate_chapter_prompts.py
```
