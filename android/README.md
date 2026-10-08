# Android Client

## باز کردن در Android Studio
1. File → Open → پوشه `android/`
2. Sync Gradle
3. Run روی گوشی/امولاتور (همان Wi‑Fi ویندوز)

## کاربرد
- آدرس سرور: `http://IP-ویندوز:5050`
- دکمه **همگام‌سازی** → `/api/sync/manifest` + pull/push
- قانون تعارض: Last-Write-Wins

## ساختار
```
app/src/main/java/com/netenc/app/
  MainActivity.kt       UI ساده + دکمه Sync
  sync/SyncClient.kt    کلاینت HTTP همگام‌سازی
  sync/SyncModels.kt    مدل‌های JSON
```
