# نصب و همگام‌سازی

## ۱) ویندوز (میزبان)

```bat
git clone https://github.com/MrUtility01/NetworkEncyclopedia.git
cd NetworkEncyclopedia\server
python -m pip install -r requirements.txt
python app.py
```

یا از پوشه `windows\start.bat`.

خروجی کنسول چیزی شبیه:
```text
LAN: http://192.168.1.10:5050
Local: http://127.0.0.1:5050
```

مرورگر: همان آدرس Local  
اندروید: همان آدرس LAN

### فایل‌های هسته (curriculum)
اگر `server/core/full_curriculum.py` و `phase_a.py` و `db.py` کامل نبودند، از بسته محلی `NetworkEncyclopediaWeb` کپی کنید داخل `server/core/`.

## ۲) اندروید

1. Android Studio → Open → پوشه `android/`
2. Sync Gradle
3. روی گوشی (همان Wi‑Fi) Run
4. IP ویندوز را وارد کنید → **اتصال** → **همگام‌سازی**

## ۳) API Sync

| متد | مسیر |
|-----|------|
| GET | `/api/sync/hello` |
| GET | `/api/sync/manifest?since=` |
| POST | `/api/sync/pull` `{uids:[]}` |
| POST | `/api/sync/push` `{records:[]}` |

قانون تعارض: **Last-Write-Wins** روی `last_updated` + `content_hash`

توکن اختیاری: متغیر محیطی `NETENC_TOKEN` و هدر `X-NetEnc-Token`
