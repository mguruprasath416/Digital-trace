# 🔍 DigitalTrace — Digital Footprint Investigation System

> **SOC / Cybersecurity Portfolio Project**  
> An OSINT aggregation tool for authorized security research and attack surface awareness.

---

## ⚠️ Legal & Ethical Notice

This tool is for:
- **Security professionals** assessing their own organization's footprint
- **Students** learning OSINT concepts in a lab/CTF environment
- **Individuals** researching their own digital presence

**Unauthorized use against real individuals or organizations may violate laws including the CFAA (US), Computer Misuse Act (UK), and IT Act (India). Always obtain written authorization.**

---

## 🧠 Features

| Module | Description | API Required? |
|---|---|---|
| Username Checker | Checks 12+ platforms for a username | ❌ None |
| WHOIS Lookup | Domain registration data | ❌ None |
| IP Intelligence | Geolocation & ASN info | ❌ Free (IPinfo) |
| Breach Check | Email in known data breaches | ✅ HIBP (~$3.50/mo) |
| Dork Generator | Google dork query builder | ❌ None |
| Metadata Extractor | EXIF/doc metadata from local files | ❌ None |
| HTML Report Builder | Compiles all findings into a report | ❌ None |
| Web Dashboard | Flask UI for all modules | ❌ None |

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Configure API keys
Edit `config/settings.py` and add your keys:
- **IPInfo**: https://ipinfo.io/signup (free, 50k/month)
- **HIBP**: https://haveibeenpwned.com/API/Key (paid, ~$3.50/month)

### 3. Run via CLI
```bash
# Check a username
python main.py --username johndoe

# WHOIS a domain
python main.py --domain example.com

# IP lookup
python main.py --ip 8.8.8.8

# Check email breaches
python main.py --email user@example.com

# Generate dorks
python main.py --dorks example.com

# Full investigation + HTML report
python main.py --username johndoe --domain example.com --ip 1.2.3.4 --report

# Launch web dashboard
python main.py --dashboard
```

### 4. Web Dashboard
```bash
python main.py --dashboard
# Open http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
digital-trace/
├── main.py                    # CLI entry point
├── requirements.txt
├── config/
│   ├── settings.py            # API keys & config
│   └── platforms.json         # Platform URL list
├── core/
│   ├── username_checker.py    # Multi-platform username search
│   ├── metadata_extractor.py  # EXIF & document metadata
│   ├── dork_generator.py      # Google dork query builder
│   └── report_builder.py      # HTML report generator
├── modules/
│   ├── whois_lookup.py        # Domain WHOIS
│   ├── ipinfo_lookup.py       # IP geolocation
│   └── haveibeenpwned.py      # Breach database check
├── dashboard/
│   ├── app.py                 # Flask web app
│   └── templates/index.html   # Dashboard UI
├── reports/output/            # Generated reports saved here
└── utils/
    ├── logger.py              # Colored logging
    ├── rate_limiter.py        # Polite request delays
    └── validator.py           # Input sanitization
```

---

## 🔑 SOC Skills Demonstrated

- **OSINT Methodology** — structured intelligence gathering
- **API Integration** — HIBP, IPInfo
- **Input Validation & Sanitization** — XSS/injection prevention
- **Rate Limiting** — ethical, server-respectful requests
- **Audit Logging** — all queries logged
- **Report Generation** — professional HTML output
- **Full-Stack** — Python backend + Flask + HTML/CSS/JS dashboard

---

## 📚 Learning Resources

- [OSINT Framework](https://osintframework.com/)
- [HaveIBeenPwned API Docs](https://haveibeenpwned.com/API/v3)
- [Google Dorking Guide](https://www.exploit-db.com/google-hacking-database)
- [IPInfo Docs](https://ipinfo.io/developers)
