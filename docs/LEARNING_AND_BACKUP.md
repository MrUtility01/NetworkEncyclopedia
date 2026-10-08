# یادگیری با کارت + یادآوری + پشتیبان

## کارت‌های یادگیری (SRS ساده)

هر درس وضعیت دارد:

| وضعیت | معنی |
|--------|------|
| new | نخونده |
| learning | در حال یادگیری |
| known | بلدم |
| review | دوباره یادآوری |

دکمه‌ها:
- **مطالعه کردم** → next_review جلو می‌رود
- **دوباره یادآوری کن** → برای مرور بعدی صف می‌شود
- **بلد نیستم** → برمی‌گردد به learning

یادآوری اندروید: هر ساعت یک Notification اگر کارتی due باشد.

## پشتیبان Git

```bat
:: ویندوز — خروجی JSON
curl http://127.0.0.1:5050/api/export > NetEnc_backup.json

git add NetEnc_backup.json
git commit -m "backup content"
git push
```

روی دستگاه دیگر:

```bat
git pull
:: اندروید: فایل را در مسیر Documents بگذارید و Import JSON
```

## پشتیبان Google Drive

1. از اپ **خروجی JSON** بگیرید
2. فایل `NetEnc_export.json` را در Drive آپلود کنید
3. روی دستگاه دیگر دانلود → **ورودی JSON**

فایل دیتابیس ویندوز: `server/data/encyclopedia.db` (می‌توانید همین را هم در Drive بگذارید).

## همگام LAN (مثل قبل)

ویندوز روشن + IP در اندروید + دکمه همگام‌سازی.
