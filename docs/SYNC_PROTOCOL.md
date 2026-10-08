# پروتکل همگام‌سازی NetworkEncyclopedia v1

## هدف
همگام‌سازی دو‌طرفه مطالب بین Windows (Host) و Android روی یک LAN، بدون ابر.

## شناسه رکورد

هر موجودیت همگام‌شونده:

| فیلد | توضیح |
|------|--------|
| `uid` | شناسه پایدار سراسری (مثلاً `lesson:ch12:lv3:l004`) |
| `entity` | `lesson` \| `scenario` \| `bookmark` \| `progress` |
| `last_updated` | ISO-8601 UTC |
| `content_hash` | SHA-256 از بدنهٔ معنایی |
| `deleted` | soft-delete |
| `device_id` | آخرین نویسنده |

## جریان Sync

```
1) GET  /api/sync/manifest?since=<iso>
   → فهرست {uid, last_updated, content_hash, deleted}

2) POST /api/sync/pull
   body: { "uids": ["..."] }
   → رکوردهای کامل

3) POST /api/sync/push
   body: { "records": [ {...} ] }
   → اعمال با قانون LWW

4) پاسخ push:
   { applied, conflicts: [{uid, server, client}] }
```

## قانون تعارض (LWW)

```
if client.last_updated > server.last_updated → accept client
elif client.last_updated < server.last_updated → reject, return server
else if hashes equal → no-op
else → conflict (keep server, report both)
```

## کشف دستگاه

1. کاربر IP را دستی وارد می‌کند (ساده و قابل‌اعتماد)
2. اختیاری: mDNS سرویس `_netenc._tcp.local` پورت 5050

## امنیت LAN

- توکن مشترک اختیاری: هدر `X-NetEnc-Token`
- فقط روی شبکه خصوصی
- در نسخه بعدی: pairing با کد ۶ رقمی

## نسخه Schema

`schema_version: 1` در manifest — اگر کلاینت قدیمی‌تر باشد، فقط pull می‌کند.
