# NetworkEncyclopedia

دایرةالمعارف جامع شبکه و زیرساخت IT — **۶۳ فصل** · L0–L4 · Capstone سازمانی

## معماری

```
shared/          هسته مشترک (پروتکل Sync + Schema)
server/          سرور وب + API همگام‌سازی (ویندوز/میزبان LAN)
windows/         لانچر ویندوز (اتصال به server محلی)
android/         کلاینت اندروید (Sync روی Wi‑Fi)
docs/            مستندات پروتکل
```

## همگام‌سازی حرفه‌ای (LAN)

- هر رکورد: `uid` + `last_updated` + `content_hash`
- فقط **دلتا** رد و بدل می‌شود
- قانون تعارض: **Last-Write-Wins** (با نمایش conflict برای ویرایش همزمان)
- کشف peer: IP دستی یا mDNS (`_netenc._tcp`)

جزئیات: [`docs/SYNC_PROTOCOL.md`](docs/SYNC_PROTOCOL.md)

## اجرای سریع (میزبان ویندوز)

```bat
cd server
python -m pip install -r requirements.txt
python app.py
```

باز کردن: `http://127.0.0.1:5050`  
از اندروید روی همان Wi‑Fi: `http://IP-ویندوز:5050` و دکمه **همگام‌سازی**

## اندروید

پروژه Kotlin در `android/` — Android Studio → Open → Sync Gradle → Run.

## وضعیت

| بخش | وضعیت |
|-----|--------|
| ساختار ۶۳ فصل | ✅ |
| وب RTL + بارگذاری تنبل | ✅ |
| API Sync حرفه‌ای | ✅ |
| لانچر ویندوز | ✅ |
| اسکلت اندروید + Sync Client | ✅ |
| محتواى عمیق AI | 🔜 |
