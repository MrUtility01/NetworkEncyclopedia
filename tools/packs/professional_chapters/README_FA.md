# بسته‌های حرفه‌ای فصل‌محور

این پوشه تکمیل canonical فصل‌های ۳۱–۳۳ و ۴۰–۶۳ را نگه می‌دارد. هر topic پنج سطح L0 تا L4 و UID پایدار دارد؛ سؤال‌ها در `meta.assessment.questions` و پاسخ‌ها فقط در `meta.assessment.answer_key` هستند. محتوای هر درس معماری، روند اجرایی، فرمان‌های نمونه، Lab مجاز، عیب‌یابی مبتنی بر evidence، امنیت، rollback، معیار پذیرش و واژه‌نامه دارد.

## ادغام
- Windows: `server/core/pack_loader.py` بسته‌های فصل‌محور را نسخه مرجع درس‌های canonical می‌شناسد.
- Android: `scripts/merge_content_packs_into_android.py` بسته‌های این پوشه را در asset دانشنامه merge می‌کند.
- گزارش ممیزی: `docs/CONTENT_AUDIT_31_68_FA.md`.

## محدودیت
JSONها و جدایی سؤال/پاسخ در مرحله تولید بررسی شده‌اند؛ تمام دستورات وابسته به نسخه/محصول نیازمند بازبینی مقصد هستند (`review_required`). آزمایش نهایی دیتابیس Windows و build/install APK جداگانه باید اجرا شود.
