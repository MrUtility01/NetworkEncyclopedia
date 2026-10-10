# ادغام cisco_switching در اندروید

فایل شما اعتبارسنجی شد: **۱۳۲۳ دستور**.

اسکریپت `scripts/merge_content_packs_into_android.py` آن‌ها را به **فصل ۶۸** تبدیل می‌کند.

## روی ویندوز / Git Bash

```bash
cd ~/NetworkEncyclopedia
git pull
python scripts/merge_content_packs_into_android.py
# باید ببینید: ch68 commands 1323
git add android/app/src/main/assets/curriculum_index.json.gz
git add scripts/merge_content_packs_into_android.py
git commit -m "content: embed cisco_switching commands as chapter 68"
git push
```

سپس GitHub → Actions → **Build Android APK** → Run workflow.

بعد از نصب APK: Settings → Clear data برنامه تا seed v12 فصل ۶۸ را بار کند.

## ویندوز سرور (SQLite)

فعلاً `apply_any_pack` برای `commands[]` به‌صورت مستقیم درس insert نمی‌کند؛ اولویت اندروید asset است. برای ویندوز در مرحله بعد importer اختصاصی اضافه می‌شود.
