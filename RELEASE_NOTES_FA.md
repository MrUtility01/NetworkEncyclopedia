# نسخه نهایی — دایرةالمعارف شبکه (کتاب‌گونه)

## ویندوز (سرور وب)

```bash
cd ~/NetworkEncyclopedia
git pull
cd server
python -m pip install -r requirements.txt
python app.py
```

- آدرس: `http://127.0.0.1:5050` یا `http://IP-سیستم:5050`
- رمز ورود: `engineerjokar`
- بعد از اولین اجرا یا آپدیت: دکمه **بازسازی** را بزنید تا همه درس‌ها با محتوای کامل seed شوند.

## اندروید (APK)

1. برو به: https://github.com/MrUtility01/NetworkEncyclopedia/actions
2. workflow **Build APK v1** → **Run workflow** (یا صبر برای بیلد خودکار بعد از push)
3. Artifact: **EngineerJokar-APK-v1** را دانلود و نصب کن
4. رمز ورود: `engineerjokar`

در بیلد، اسکریپت `export_android_index.py` حدود **۵۶۶۴ درس** در **۶۸ فصل** را با full_content / commands / examples / notes کتاب‌گونه داخل APK می‌گذارد.

## محتوای هر درس

۱۵ بخش: اهمیت، واژه‌نامه، معماری، نظریه، پیکربندی، دستورات چندسکو (Cisco/MikroTik/FortiGate/Linux/PowerShell)، سناریو، Lab، RCA، امنیت، مقیاس، مصاحبه، ضدالگو، آزمون، چک‌لیست.
