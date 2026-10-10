# اولویت ۴ — عیب‌یابی سیستماتیک شبکه (RCA)

این پرامپت را **کامل** به ChatGPT بده (همراه `_MASTER_PROMPT.md`).

---

نقش: نویسندهٔ متدولوژی عیب‌یابی شبکه برای NetworkEncyclopedia  
ریپو: https://github.com/MrUtility01/NetworkEncyclopedia  
خروجی: JSON استاندارد  
chapter_order پیشنهادی: **60** و/یا **62**

## چارچوب اجباری در هر درس
Symptom → Scope → Evidence → Hypothesis → Fix → Verify → Prevent

## محورها
1. مدل لایه‌ای عیب‌یابی (L1→L7)
2. ابزارها: ping, traceroute, arp, ss/netstat, tcpdump/wireshark (خواندن تشخیصی)
3. مشکلات رایج: duplex, MTU, DNS, gateway, ACL, NAT, VPN, routing loop
4. جمع‌آوری شواهد و timeline
5. ارتباط با NOC و ticket
6. چک‌لیست قبل از تغییر production
7. Post-incident و Runbook

## سطوح
L0 (کاربر) تا L4 (مهندس ارشد NOC)؛ حداقل ۲۵ درس + حداقل ۱۰ سناریوی RCA کامل.

## سناریوهای اجباری (حداقل ۱۰)
- «اینترنت ندارم»
- یک VLAN به DNS نمی‌رسد
- Packet loss متناوب
- traceroute تا وسط می‌میرد
- بعد از ACL سرویس قطع شد
- VPN وصل است ولی اپلیکیشن نه
- DHCP exhaustion مفهومی
- STP topology change
- High CPU سوییچ (مفهوم)
- اشتباه تشخیصی DNS

## قانون
ابزارها فقط تشخیص در lab/محیط مجاز؛ بدون اسکن تهاجمی غیرمجاز.

## شروع
فهرست درس‌ها → JSON بسته‌بسته  

## ذخیره
`tools/packs/ch60_troubleshooting/network_rca_pack.json`
