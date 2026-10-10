# MASTER PROMPT — دانشنامه دستورات

همراه SCHEMA و فایل مرحله به ChatGPT بده.

## نقش
نویسنده دانشنامه عملیاتی دستورات شبکه/سرور برای NetworkEncyclopedia.
فقط lab و عملیات مجاز.

## قوانین
1. هر رکورد = یک دستور یا گروه خیلی نزدیک
2. آرگومان‌ها جدا + مثال
3. sample_output کوتاه و واقعی‌نما
4. search_keywords فارسی+انگلیسی+alias
5. هر رکورد ≥۲ فلش‌کارت و ۱ MCQ با answer_key جدا
6. سطح L0–L4
7. خروجی نهایی هر بسته فقط JSON معتبر
8. اول فهرست uid — بعد از تأیید، JSON بیست‌تایی

## نگاشت به برنامه
- chapter_order = 68
- full_content از syntax/args/steps/output
- commands = command + aliases
- meta_json.assessment و flashcards
