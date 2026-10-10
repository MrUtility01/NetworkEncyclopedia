# اولویت ۲ — VPN سازمانی: IPsec + SSL و عیب‌یابی

این پرامپت را **کامل** به ChatGPT بده (همراه `_MASTER_PROMPT.md`).

---

نقش: نویسندهٔ دورهٔ VPN سازمانی برای NetworkEncyclopedia  
ریپو: https://github.com/MrUtility01/NetworkEncyclopedia  
خروجی: JSON استاندارد `lessons`

## محدوده
- chapter_order: **67** و همپوشانی با **21** (MikroTik VPN) و **24** (FortiGate)
- موضوعات:
  1. مفاهیم VPN و رمزنگاری کاربردی
  2. IPsec: IKEv1/IKEv2, Phase1/Phase2, ESP/AH, policy-based vs route-based
  3. Site-to-Site IPsec
  4. Remote Access / SSL VPN portal
  5. Certificate vs PSK
  6. Routing over tunnel و split-tunnel
  7. عیب‌یابی: Phase1 fail, Phase2 fail, SA expire, NAT-T, MTU/MSS
  8. امنیت: cipher مدرن، ریسک split-tunnel ناامن

## سطوح
L0–L4؛ حداقل ۲۵–۳۵ درس.

## سناریوهای اجباری
- دو سایت با IPsec IKEv2
- کاربر دورکار SSL VPN
- Phase1 proposal mismatch
- Phase2 traffic selector mismatch
- Tunnel up ولی route نیست
- NAT-T پشت مودم خانگی
- Certificate expired
- Failover دو ISP (مفهوم)

## دستورات / پنل
- FortiGate (CLI/GUI مفهومی)
- MikroTik IPsec
- مقایسهٔ آموزشی strongSwan/WireGuard فقط با برچسب

## Lab
فقط lab شخصی/شبیه‌ساز؛ بدون دور زدن امنیت سازمان واقعی.

## شروع
فهرست درس‌ها با uid → JSON بسته‌بسته  

## ذخیره
`tools/packs/ch67_vpn_enterprise/vpn_ipsec_ssl_pack.json`
