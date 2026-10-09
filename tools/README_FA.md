# پوشه tools — بسته‌های محتوا (Content Packs)

این پوشه **فقط** برای بسته‌های آموزشی JSON و اسکریپت واردسازی است.
برنامهٔ ویندوز از `server/` و اندروید از `android/` اجرا می‌شود؛ اینجا «انبار محتوا» است.

## ساختار درست (همین را حفظ کن)

```text
tools/
  README_FA.md                          ← این راهنما
  AI_CONTENT_PACK_PROMPT.md             ← پرامپت برای دادن به ChatGPT/Claude/Grok
  apply_any_pack.py                     ← واردسازی هر JSON به دیتابیس ویندوز
  reorganize_tools.sh                   ← یک‌بار برای مرتب‌کردن فایل‌های شلخته

  engineer_jokar_automation_python/     ← بسته Auto/Python (فصل ۲۱/۳۵/۵۱)
    automation_python_curriculum_pack.json
    validate_pack.py
    apply_content_pack.py

  engineer_jokar_security_ethical_hacking/  ← فصل ۶۴ امنیت
    security_ethical_hacking_pack.json

  engineer_jokar_wireless_security/     ← امنیت بی‌سیم
    wireless_security_pack.json

  packs/                                ← بسته‌های دیگر (Switching، Windows Server، …)
    switching_routing/
      switching_routing_curriculum_pack.json
    windows_server/
      windows_server_complete_curriculum_pack.json
```

## اگر فایل را در ریشه tools گذاشتی

یک‌بار در Git Bash از ریشهٔ ریپو:

```bash
cd ~/NetworkEncyclopedia
bash tools/reorganize_tools.sh
git add tools
git commit -m "chore: reorganize content packs into folders"
git push
```

## واردسازی به ویندوز (بعد از اجرای سرور حداقل یک‌بار)

```bash
cd ~/NetworkEncyclopedia
python tools/apply_any_pack.py --db server/data/encyclopedia.db --pack tools/engineer_jokar_automation_python/automation_python_curriculum_pack.json --apply
```

یا همهٔ JSONهای داخل tools را یکجا:

```bash
python tools/apply_any_pack.py --db server/data/encyclopedia.db --all --apply
```

## اندروید

بیلد Actions بعد از `export` اسکریپت `merge_content_packs_into_android.py` را اجرا می‌کند و هر بسته‌ای که در مسیرهای شناخته‌شده باشد را ادغام می‌کند.
APK را از Actions بگیر و بعد از نصب **Clear data** بزن.

## تولید بستهٔ جدید با هوش مصنوعی

فایل `AI_CONTENT_PACK_PROMPT.md` را به مدل بده + آدرس گیت:

```text
https://github.com/MrUtility01/NetworkEncyclopedia
```

خروجی باید یک JSON مطابق schema همان پرامپت باشد. آن را در `tools/packs/نام_بسته/` بگذار و با `apply_any_pack.py` وارد کن.
