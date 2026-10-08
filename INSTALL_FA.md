# نصب و همگام‌سازی

## ویندوز (میزبان)

```bat
git clone https://github.com/MrUtility01/NetworkEncyclopedia.git
cd NetworkEncyclopedia
```

### هسته ۶۳ فصل
فایل‌های `server/core/db.py`، `phase_a.py`، `full_curriculum.py` را از بسته محلی
`NetworkEncyclopediaWeb` یا `NetworkEncyclopedia_full_core_for_github.zip` داخل `server/core/` کپی کنید.

همچنین `server/static/app.css` و `app.js` را از همان بسته کپی کنید.

```bat
cd server
python -m pip install -r requirements.txt
python app.py
```

LAN IP در کنسول چاپ می‌شود. اندروید همان IP را می‌زند.

## اندروید

Android Studio → Open → `android/` → Run  
دکمه **اتصال** سپس **همگام‌سازی** (دوطرفه + ذخیره آفلاین JSON)

## Sync

- GET `/api/sync/hello`
- GET `/api/sync/manifest?since=`
- POST `/api/sync/pull`
- POST `/api/sync/push`

تعارض: Last-Write-Wins
