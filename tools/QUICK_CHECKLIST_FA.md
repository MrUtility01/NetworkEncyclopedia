# چک‌لیست عملی Git — نسخه جیبی

## چرخه امن روزانه

```bash
git status --short
git switch -c feature/descriptive-name
# edit files
git diff
git add path/to/selected-file
git diff --staged
git commit -m "fix: explain the change"
git fetch origin
git log --graph --oneline --decorate --all -20
git push -u origin feature/descriptive-name
```

## پیش از هر عملیات پرخطر

- [ ] مسیر مخزن درست است: `git rev-parse --show-toplevel`
- [ ] شاخه فعلی و وضعیت کاری بررسی شده‌اند.
- [ ] مقصد remote بررسی شده است: `git remote -v`
- [ ] diff و فایل‌هایی که قرار است تغییر کنند مشخص‌اند.
- [ ] اگر تاریخچه بازنویسی می‌شود، آیا commit قبلاً منتشر شده؟
- [ ] اگر secret افشا شده، credential rotate شده است؛ فقط حذف فایل کافی نیست.

## تفاوت دستورات بازگردانی

| دستور | اثر اصلی | ریسک |
|---|---|---|
| `git restore file` | دور ریختن تغییر unstaged یک فایل از روی Index | بالا؛ تغییر محلی ممکن است از دست برود |
| `git restore --staged file` | خارج‌کردن فایل از Stage | کم؛ Working Tree معمولاً حفظ می‌شود |
| `git reset --soft HEAD~1` | جابه‌جایی HEAD؛ تغییرها staged می‌مانند | متوسط؛ تاریخچه شاخه تغییر می‌کند |
| `git reset HEAD~1` | جابه‌جایی HEAD و بازنشانی Index | متوسط تا بالا |
| `git reset --hard ...` | بازنشانی HEAD، Index و Working Tree | بسیار بالا |
| `git revert <commit>` | ساخت commit معکوس و حفظ تاریخچه | معمولاً گزینه مناسب‌تر برای شاخه مشترک |
| `git reflog` | پیدا کردن referenceهای قبلی محلی | ابزار بازیابی؛ دائمی نیست |

## قاعده انتشار

هرگز قبل از بازبینی `git diff --staged`، بررسی `.gitignore` و کنترل secretها commit/push نکنید. `git add` انتشار در GitHub نیست؛ `commit` نیز به‌تنهایی چیزی را به remote نمی‌فرستد.
