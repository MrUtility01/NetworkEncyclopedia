# ساختار برنامه و استاندارد عمق محتوا

## معماری سه‌لایه (باید حفظ شود)

```
Windows (Flask + SQLite)  ←—Sync LAN—→  Android (Room + assets)
         │                                    │
         └──────── offline-complete ──────────┘
```

1. **ویندوز** بدون گوشی کامل است.
2. **اندروید** بدون PC کامل است (seed از `curriculum_index.json.gz`).
3. **Sync** اختیاری است و قراردادش در `docs/SYNC_PROTOCOL.md` است.

## نقشهٔ پوشه‌ها

| مسیر | نقش |
|------|-----|
| `server/app.py` | API + Sync + health |
| `server/core/full_curriculum.py` | اسکلت ۶۳ فصل |
| `server/core/rich_content.py` | تولید متن غنی هنگام seed |
| `server/core/db.py` | SQLite و seed |
| `server/workspace_routes.py` | کارها/یادداشت/vault (با توکن) |
| `android/.../OfflineSeeder.kt` | بارگذاری فهرست آفلاین |
| `android/.../QuizActivity.kt` | آزمون |
| `android/.../ScenarioSeeder.kt` | لابراتوار/سناریوی Capstone |
| `tools/chapter_prompts/` | پرامپت تولید محتوا |
| `tools/packs/` | JSON بسته‌های غنی |
| `tools/audit_content.py` | ممیزی عمق و ساختار |

## تعداد فصل

| لایه | تعداد |
|------|--------|
| هسته seed (`full_curriculum`) | **۶۳** |
| بسته/افزونه (Git, Security, Routing deep, VPN) | **۶۴–۶۷** پس از merge pack در اندروید |

## تعریف درس «کامل»

1. معرفی و پیش‌نیاز
2. آموزش از صفر + تشبیه سازمانی
3. معماری فنی
4. مثال مرحله‌ای
5. دستورات با خروجی مورد انتظار
6. لابراتوار ایمن (Lab)
7. عیب‌یابی RCA
8. نکات امنیتی
9. خلاصه + واژه‌نامه
10. `meta.assessment.questions` + `answer_key` جدا

آستانه‌های ممیزی (`tools/audit_content.py`):

- **deep:** `full_content ≥ 2000`
- **mid:** ۸۰۰–۱۹۹۹
- **thin:** < ۸۰۰ → نیاز به غنی‌سازی

## آزمون و لابراتوار — وضعیت

| جزء | وضعیت | کار بعدی |
|-----|--------|----------|
| آزمون اندروید | از بانک درس سؤال می‌سازد | ترجیح `meta.assessment` وقتی موجود باشد |
| سناریو Capstone | جدول `scenarios` + ScenarioSeeder | یکسان‌سازی ویندوز/اندروید |
| Lab داخل درس | در `full_content` درس‌های غنی | پر کردن فصل‌های thin |
| بانک سؤال جدا | در پک‌های JSON تخصصی | استاندارد questions/answer_key |

## ترتیب اصولی کار محتوا

1. `python tools/audit_content.py --db server/data/encyclopedia.db`
2. ضعیف‌ترین فصل‌ها از `weakest_chapters`
3. پرامپت `tools/chapter_prompts/`
4. JSON → `tools/packs/` → `apply_any_pack.py`
5. دوباره audit
6. سپس APK

**قانون:** تا فصل‌های حیاتی (۸، ۱۳، ۱۴، ۲۰، ۲۴، ۲۹، ۵۱، ۶۰) از thin خارج نشده‌اند، فصل جدید اضافه نکن.
