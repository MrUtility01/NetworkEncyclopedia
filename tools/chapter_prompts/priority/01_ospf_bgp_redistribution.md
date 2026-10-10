# اولویت ۱ — مسیریابی عمیق: OSPF + BGP + Redistribution

این پرامپت را **کامل** به ChatGPT بده (ترجیحاً همراه با `tools/chapter_prompts/_MASTER_PROMPT.md`).

---

نقش: نویسندهٔ دورهٔ تخصصی مسیریابی برای NetworkEncyclopedia (ENGINEER JOKAR)  
ریپو: https://github.com/MrUtility01/NetworkEncyclopedia  
قالب خروجی: JSON با `package_schema_version: 1` و آرایه `lessons`

## محدوده
- chapter_order ترجیحی: **14** (مسیریابی پیشرفته) و در صورت نیاز بسته مکمل با order **66**
- موضوعات:
  1. OSPF: LSA types, Areas (Stub/Totally Stubby/NSSA), DR/BDR, Network types, Cost, SPF
  2. OSPF Multi-Area و Virtual Link (مفهوم + محدودیت)
  3. BGP: ASN, eBGP/iBGP, peering TCP 179, states, path attributes
  4. BGP policy: route-map, prefix-list, AS-path filter, local-pref, MED, communities
  5. Redistribution: seed metric, administrative distance, loop prevention, tags
  6. عیب‌یابی: adjacency down, stuck in EXSTART, missing routes, suboptimal path

## سطوح
برای هر موضوع اصلی L0 تا L4 (حداقل ۲۵–۴۰ درس در کل بسته).

## سناریوهای اجباری (حداقل ۸)
- دو Area OSPF با ABR
- eBGP بین دو ASN سازمانی
- iBGP full-mesh یا Route Reflector (مفهوم)
- Redistribution OSPF↔BGP یک‌طرفه امن
- Peer BGP Idle/Active
- OSPF Neighbor stuck
- Route flap / dampening مفهومی
- مسیر suboptimal به‌خاطر Local Pref

## دستورات
چندوندر با برچسب واضح:
- Cisco IOS/IOS-XE
- MikroTik RouterOS7 (در صورت کاربرد)
- Linux (ip route / FRR) در صورت کاربرد آموزشی

## Lab
فقط توپولوژی شبیه‌سازی (GNS3/EVE-NG/CHR)؛ بدون دسترسی به شبکه واقعی شخص ثالث.

## فیلدهای هر درس
uid, chapter_order, subchapter_order, lesson_order, level (L0–L4), title_fa, title_en, topic, summary, full_content, commands, examples, notes, learning_objectives[], meta.assessment.questions, meta.assessment.answer_key, source_status=review_required

## شروع
1) جدول فهرست درس‌ها (title_fa, level, subchapter, uid)  
2) سپس JSON بسته‌بسته ۲۰ درس  

## ذخیره
`tools/packs/ch14_routing_deep/routing_ospf_bgp_pack.json`
