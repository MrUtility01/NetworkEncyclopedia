# دانشنامه جامع دستورات — ENGINEER JOKAR

فصل اختصاصی دستورات چندوندر با:
- دسته‌بندی موضوعی و سطح
- توضیح آرگومان‌ها و خروجی مورد انتظار
- جستجوی هوشمند (کلیدواژه / alias / کار مرتبط)
- کارت‌های فلش و سؤال ارزیابی

## محدوده
1. Cisco IOS / IOS-XE
2. MikroTik RouterOS 7
3. فایروال عمومی (مفهوم + pfSense/OPNsense)
4. FortiGate CLI
5. Issabel / Asterisk
6. PowerShell (شبکه و سرور)

## مراحل

| مرحله | خروجی | معیار |
|-------|--------|------|
| ۰ | اسکلت + schema | تأیید شما |
| ۱ | Cisco Switching | ≥۴۰ رکورد |
| ۲ | Cisco Routing/ACL/NAT | ≥۴۰ |
| ۳ | MikroTik | ≥۴۰ |
| ۴ | FortiGate | ≥۳۵ |
| ۵ | Issabel | ≥۲۵ |
| ۶ | PowerShell | ≥۴۰ |
| ۷ | فلش‌کارت + سؤال کامل | هر رکورد ≥۲ کارت |
| ۸ | واردسازی + جستجو | audit |

```
tools/commands_encyclopedia/
  README_FA.md  SCHEMA.md  MASTER_PROMPT.md
  phases/   prompts/
tools/packs/commands_encyclopedia/   ← JSON خروجی
```

هر مرحله را جدا به ChatGPT بده؛ قبل از مرحله بعد JSON را در packs ذخیره کن.
