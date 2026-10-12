# پر کردن ترتیبی درس‌ها با محتوای واقعی

این پوشه پک‌های JSON واقعی دارد که با `pack_loader` روی درس‌های موجود match می‌شوند.

## اعمال

```bash
cd server
export NETENC_TOKEN=09136555866
python app.py
# یا
curl -X POST http://127.0.0.1:5050/api/apply-packs -H "Authorization: Bearer 09136555866"
```

برای اجبار اعمال مجدد، متای `packs_applied` را پاک کنید یا API را صدا بزنید.

## فایل‌ها
- `ordered_real_lessons_pack.json` — OSI تا امنیت (۲۰ درس)
- `ordered_real_lessons_pack2.json` — پیشرفته‌تر (۱۰ درس)
- پک‌های قبلی در `real_lessons_core` و سایر پوشه‌ها
