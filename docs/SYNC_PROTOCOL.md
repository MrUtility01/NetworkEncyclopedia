# پروتکل همگام‌سازی NetworkEncyclopedia v1 (aligned)

## قرارداد API (ویندوز ↔ اندروید)

| عملیات | متد و مسیر | بدنه / پاسخ |
|--------|------------|-------------|
| Hello | `GET /api/sync/hello` | وضعیت + schema |
| Manifest | `GET /api/sync/manifest?since=<iso>` | `{ items: [...] }` |
| Pull | `POST /api/sync/pull` | body `{ "uids": [] }` → `{ "records": [] }` |
| Push | `POST /api/sync/push` | body `{ "records": [] }` |

## احراز هویت

```
Authorization: Bearer <NETENC_TOKEN>
```

یا:

```
X-NetEnc-Token: <NETENC_TOKEN>
```

اگر `NETENC_TOKEN` خالی باشد سرور باز است (فقط dev).

**هشدار:** توکن پیش‌فرض dev را روی LAN عمومی نگذارید:

```bash
set NETENC_TOKEN=یک-رشته-بلند-تصادفی
cd server
python app.py
```

## قانون تعارض (LWW)

```
if client.last_updated > server.last_updated → accept client
elif client.last_updated < server.last_updated → keep server
else if hashes equal → no-op
else → conflict (keep server)
```

## فضای کاری / vault

- `/workspace` با توکن (صفحه login + کوکی) محافظت می‌شود
- رمز vault به‌صورت `enc1:…` ذخیره می‌شود نه متن آشکار
- `GET /api/workspace/export` فقط با توکن

## Health

`GET /api/health` عمومی است و وضعیت ماژول‌ها / تعداد درس را برمی‌گرداند (بدون افشای توکن).

## Schema

`schema_version: 1`
