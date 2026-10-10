# اولویت ۳ — فایروال عملی (Policy / NAT / VPN / HA)

این پرامپت را **کامل** به ChatGPT بده (همراه `_MASTER_PROMPT.md`).

---

نقش: نویسندهٔ دورهٔ فایروال عملی سازمانی برای NetworkEncyclopedia  
ریپو: https://github.com/MrUtility01/NetworkEncyclopedia  
خروجی: JSON استاندارد

## محدوده
- chapter_order: **24** FortiGate ، **20** MikroTik FW ، **25** pfSense/OPNsense
- order هر درس را صریح بنویس.

## محورها
1. Zones و policy از بالا به پایین
2. NAT: SNAT/DNAT/PAT و اشتباهات رایج
3. Object / address group
4. Logging و session
5. VPN روی فایروال (ارجاع به بسته VPN)
6. HA Active-Passive (مفهوم)
7. IPS/AppControl در حد عملیات دفاعی
8. عیب‌یابی: policy miss, implicit deny, NAT error, asymmetric routing

## سطوح
L0–L4؛ حداقل ۳۰ درس.

## سناریوهای اجباری
- اینترنت LAN با NAT
- Publish وب‌سرور (DNAT) امن
- Policy order اشتباه
- دو ISP و policy route مفهومی
- HA failover مفهومی
- پیدا کردن بلاک از روی لاگ
- MikroTik filter forward
- FortiGate policy + address object

## قانون
فقط پیکربندی دفاعی و hardening؛ دستور حمله یا دور زدن فیلتر غیرمجاز ممنوع.

## شروع
فهرست درس‌ها با uid → JSON  

## ذخیره
`tools/packs/firewall_practical/firewall_practical_pack.json`
