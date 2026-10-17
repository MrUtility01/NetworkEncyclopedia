# وضعیت امکانات برنامه (واقعی)

## برنامه چه می‌کند؟
- دانشنامه آموزشی شبکه/IT (هسته **۶۳ فصل** + پک‌های ۶۴–۶۸)
- مطالعه درس، جستجو، آزمون، فلش‌کارت، سناریو
- ویندوز: Flask + SQLite | اندروید: Kotlin + Room
- همگام‌سازی LAN اختیاری (قرارداد Sync فاز ۲)

## مدیریت کار / نکته / رمز

| قابلیت | ویندوز | اندروید |
|--------|--------|--------|
| فهرست دروس | بله | بله |
| آزمون / فلش‌کارت | مطالعه/وب | بله |
| سناریو | جدول scenarios | ScenarioSeeder |
| کارها (Tasks) | `/workspace` + توکن | جزئی / ناقص |
| یادداشت | `/workspace` | جزئی |
| گاوصندوق رمز | sealed در workspace | **کامل نیست** |
| قفل ورود اپ (PIN) | توکن API/Workspace | **هنوز هم‌سطح نیست** |

**جمع‌بندی:** کار و یادداشت روی ویندوز هست؛ اندروید هنوز به همان سطح نرسیده. رمز ورود یکسان رسمی برای هر دو به‌عنوان PIN اپ کامل پیاده نشده.

## آیا اندروید = ویندوز؟
**خیر، ۱۰۰٪ یکی نیست.** هسته آموزش و فهرست درس نزدیک است؛ Workspace/Vault/وب مدیریتی روی ویندوز قوی‌تر است. Sync بعد از هم‌ترازی API باید هر دو را نزدیک کند.

## مسیرهای ورود محتوا
1. Seed داخلی (`full_curriculum` + `rich_content`)
2. JSON pack → `python tools/apply_any_pack.py --db ... --pack ... --apply`
3. پوشه‌های `tools/engineer_jokar_*`
4. Sync pull از سرور
5. Asset اندروید `curriculum_index.json.gz` هنگام نصب/seed

## پرامپت فصل‌ها
- قالب: `tools/chapter_prompts/_MASTER_PROMPT.md`
- هر فصل: `tools/chapter_prompts/chXX/PROMPT.md`
- اولویت: `tools/chapter_prompts/priority/`
- دستورات: `tools/commands_encyclopedia/`
- بسته‌های حرفه‌ای canonical برای فصل‌های ۳۱–۳۳ و ۴۰–۶۳ در `tools/packs/professional_chapters/` اضافه شده‌اند؛ نتیجه بررسی ساختاری و محدودیت‌های آزمون محیط در [گزارش ممیزی فصل‌های ۳۱ تا ۶۸](CONTENT_AUDIT_31_68_FA.md) ثبت شده است.

## آیکون
درخواست عکس کاربر ثبت شده؛ فقط بعد از build سبز Actions و نصب APK جدید مطمئن شو همان آیکون است.

## پرامپت ChatGPT شما
ساختار ۱۲بخشی + JSON + جدا بودن سؤال/جواب در MASTER و SCHEMA آمده؛ عین متن طولانی یک‌جا به‌جای همه فایل‌ها نیست، ولی قرارداد خروجی همان است.

## سناریو ۲۰×۱۰
پرامپت: `tools/scenarios_200/PROMPT_20x10.md`


## ممیزی و غنی‌سازی فصل‌های ۳۱ تا ۶۸

گزارش تفصیلی: [docs/CONTENT_AUDIT_31_68_FA.md](CONTENT_AUDIT_31_68_FA.md). بسته‌های فصل‌محور جدید با عنوان canonical از اسکلت `server/core/full_curriculum.py` استفاده می‌کنند. برای ممیزی دیتابیس عملی بعد از دریافت تغییرات، اجرا کنید:

```bash
python tools/audit_content.py --db server/data/encyclopedia.db --json docs/content_audit_local.json
```

ممیزی دادهٔ واقعی SQLite و آزمون نهایی APK تا اجرای دستور در محیط مقصد تأییدشده محسوب نمی‌شود.
