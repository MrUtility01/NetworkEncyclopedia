# بسته‌های حرفه‌ای فصل‌های ۴۰ تا ۴۲

این پوشه بسته‌های محتوایی درس‌محور مطابق ساختار فعلی curriculum را نگه می‌دارد.

| فایل | فصل | درس | موضوع |
|---|---:|---:|---|
| `ch40_vmware_hyperv_professional.json` | 40 | 70 | VMware ESXi/vCenter/vMotion/DRS/HA/FT و Hyper-V |
| `ch41_proxmox_docker_professional.json` | 41 | 55 | Proxmox VE، ZFS، KVM، LXC و Docker |
| `ch42_kubernetes_professional.json` | 42 | 65 | Kubernetes core، networking/security، Helm، monitoring و upgrade |

## توافق محتوایی
- برای هر موضوع سطح‌های L0 تا L4 وجود دارد و عنوان فارسی هر درس بر اساس عنوان رسمی `server/core/full_curriculum.py` ساخته شده است.
- هر درس دارای UID، شماره فصل/زیرفصل/درس، خلاصه، متن Markdown، فرمان‌ها، مثال، لابراتوار، عیب‌یابی ساختاریافته و معیار پذیرش است.
- سؤال‌ها در `meta.assessment.questions` و جواب‌ها فقط در `meta.assessment.answer_key` قرار دارند. پاسخ صحیح داخل گزینه‌های عمومی سؤال منتشر نشده است.
- اسکریپت merge اصلاح شده تا ارزیابی، فلش‌کارت و هدف‌های یادگیری درس‌های match‌شده را در markerهای `notes` حفظ کند.
- `tools/apply_any_pack.py` نیز اصلاح شده تا `meta.assessment` و دیگر metadata ورودی را با حفظ کلیدهای قبلی در ستون `lessons.meta_json` دیتابیس Windows merge کند؛ `source_status` هم ذخیره می‌شود.

## بررسی ساختار JSON
```bash
python -m json.tool tools/packs/virtualization_containers/ch40_vmware_hyperv_professional.json > /dev/null
python -m json.tool tools/packs/virtualization_containers/ch41_proxmox_docker_professional.json > /dev/null
python -m json.tool tools/packs/virtualization_containers/ch42_kubernetes_professional.json > /dev/null
python scripts/merge_content_packs_into_android.py
```

خروجی‌های `title-merge` را برای فصل‌های ۴۰، ۴۱ و ۴۲ بررسی کنید؛ سپس Build اندروید را از GitHub Actions اجرا و محتوای درس، assessment و answer key را در برنامه کنترل کنید.

## نکات عملیاتی
- وضعیت محتوا `review_required` است؛ فرمان‌ها و نمونه پیکربندی‌ها باید با نسخه/edition واقعی تطبیق داده شوند.
- در production عملیات ESXi/Hyper-V/Proxmox/Kubernetes که reboot، failover، تغییر شبکه/storage یا حذف منبع ایجاد می‌کند باید با change window، backup و rollback plan اجرا شود.
- فایل‌های نمونه هیچ credential واقعی ندارند. Secret نباید داخل image، مخزن یا log قرار بگیرد.
- JSON معتبر بودن، به‌تنهایی جایگزین اجرای merge، آزمون اپلیکیشن و Build واقعی نیست.
