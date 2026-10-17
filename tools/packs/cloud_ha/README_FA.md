# بسته‌های حرفه‌ای فصل‌های ۴۳ و ۴۸

این پوشه دو بستهٔ محتوایی سازگار با ساختار جاری برنامه دارد:

- `ch43_cloud_networking_professional.json`: فصل ۴۳، شبکه ابری؛ ۱۶ موضوع × پنج سطح = ۸۰ درس.
- `ch48_ha_load_balancing_professional.json`: فصل ۴۸، HA و Load Balancing؛ ۱۰ موضوع × پنج سطح = ۵۰ درس.

## سازگاری
- عنوان‌های فارسی/انگلیسی و سطح‌های L0 تا L4 مطابق خروجی `server/core/full_curriculum.py` تولید شده‌اند تا ادغام عنوانی به همان درس موجود برسد.
- هر درس UID پایدار، chapter/subchapter/lesson order، هدف یادگیری، محتوای Markdown، دستورات، مثال، lab، عیب‌یابی و معیار پذیرش دارد.
- هر سؤال در `meta.assessment.questions` است؛ پاسخ صحیح فقط در `meta.assessment.answer_key` نگهداری می‌شود.
- اسکریپت ادغام برای حفظ ارزیابی و هدف‌های یادگیریِ درس‌های match‌شده اصلاح شده است؛ metadata به‌صورت marker در `notes` منتقل می‌شود و رکورد/UID موجود بازنویسی نمی‌شود.

## اعتبارسنجی
پس از checkout شاخه:
```bash
python -m json.tool tools/packs/cloud_ha/ch43_cloud_networking_professional.json > /dev/null
python -m json.tool tools/packs/cloud_ha/ch48_ha_load_balancing_professional.json > /dev/null
python scripts/merge_content_packs_into_android.py
```

پس از اجرای merge، در logها مقدار `title-merge` برای درس‌های هر بسته و شمار درس نهایی را کنترل کنید. سپس Build اندروید را از GitHub Actions اجرا کنید و در APK، عنوان درس‌ها، متن، دستورات و آزمون/answer key را بررسی کنید.

## ایمنی عملیاتی
تمام CLIها و پیکربندی‌های نمونه باید با نسخه و edition محیط شما تطبیق داده شوند. دستورات ساخت منابع ابری، NAT Gateway، circuit/VPN و منابع مدیریت‌شده ممکن است هزینه ایجاد کنند؛ فقط در حساب/محیط مجاز و با بررسی هزینه اجرا شوند. محتوا با وضعیت `review_required` علامت‌گذاری شده است و پیش از production باید توسط مالک فنی بازبینی شود.
