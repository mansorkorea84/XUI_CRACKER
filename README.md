# 🔥 XUI SECURITY TOOLKIT v3.0 - ALL-IN-ONE SUITE

<p align="center">
  <img src="https://img.shields.io/badge/Version-3.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8%2B-green?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge" alt="Status">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Purpose-Security%20Testing-orange?style=for-the-badge" alt="Purpose">
  <img src="https://img.shields.io/badge/Target-3X--UI%20Panel-purple?style=for-the-badge" alt="Target">
  <img src="https://img.shields.io/badge/Multi%20Thread-Yes-success?style=for-the-badge" alt="Multi-thread">
  <img src="https://img.shields.io/badge/Scanner-✅-green?style=for-the-badge" alt="Scanner">
  <img src="https://img.shields.io/badge/Cracker-✅-green?style=for-the-badge" alt="Cracker">
</p>

---

## 🎯 What is XUI Security Toolkit?

**XUI Security Toolkit** is a **complete all-in-one security suite** for testing [3X-UI](https://github.com/MHSanaei/3x-ui) panels. It includes:

### 📦 Included Tools:
| Tool | File | Description |
|------|------|-------------|
| **🔍 XUI Scanner Pro** | `xui_scanner.py` | Find & detect 3X-UI panels on any IP |
| **🔓 XUI Cracker Enhanced** | `xui_cracker.py` | Crack panel credentials |
| **⚡ Main Toolkit** | `toolkit.py` | All-in-one launcher with menu |

### ⚠️ Disclaimer

> **This tool is for AUTHORIZED security testing ONLY!**
> 
> ✅ Allowed uses:
> - Penetration Testing (with permission)
> - Security Assessments
> - Educational Purposes
> - Checking your own infrastructure
>
> ❌ Unauthorized access to systems you don't own is **ILLEGAL**

---

## ✨ Features (v3.0 Complete Suite)

### 📡 XUI Scanner Pro v2.0 - NEW!
| Feature | Description |
|---------|-------------|
| **Multi-Port Scanning** | 2053, 443, 8443, 2083, 81, 8080... |
| **Fast TCP Scanner** | Quick port check before HTTP |
| **3X-UI Fingerprinting** | Detects 3X-UI specific patterns |
| **Version Detection** | Extracts panel version |
| **Vulnerability Assessment** | Finds security issues |
| **Auto-Export for Cracker** | One-click export to cracker format |
| **Bulk IP Support** | CIDR, ranges, lists |
| **Beautiful Live UI** | Real-time statistics |

### 🔓 XUI Cracker Enhanced v3.0
| Mode | Description | Speed |
|------|-------------|-------|
| **Standard Brute Force** | Custom wordlist attack | ⚡⚡⚡ |
| **Default Credentials** | Quick check of common creds | ⚡⚡⚡⚡⚡ |
| **Full Auto Attack** | Scan → Default → Brute Force | ⚡⚡⚡ |
| **Scanner Mode** | Identify XUI panels only | ⚡⚡⚡⚡⚡ |
| **API Exploiter** | Extract data from vulnerable panels | ⚡⚡⚡⚡ |

### 🛠️ Advanced Features
- ✅ **Multi-threaded Engine** - Up to 100 concurrent threads
- ✅ **Smart Session Management** - Efficient HTTP session handling
- ✅ **Proxy Support** - Rotate proxies to avoid detection
- ✅ **User-Agent Rotation** - 10+ realistic browser agents
- ✅ **CSRF Token Extraction** - Automatic token handling
- ✅ **Rate Limiting Handling** - Exponential backoff
- ✅ **Beautiful Animated UI** - Real-time statistics
- ✅ **Multiple Output Formats** - TXT, JSON exports
- ✅ **API Data Extraction** - Pull inbounds, users, settings
- ✅ **Vulnerability Detection** - Identify security issues

### 📊 Statistics & Reporting
- Live attack statistics
- Requests per second tracking
- Success/failure rates
- Elapsed time monitoring
- Detailed JSON reports

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/mansorkorea84/XUI_CRACKER.git
cd XUI_CRACKER
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run (Interactive Mode)

```bash
python3 xui_cracker.py
```

### 4. Prepare Your Files

Create or edit these files:
- `ips.txt` - Target list (IP:PORT format)
- `users.txt` - Username wordlist
- `passwords.txt` - Password wordlist

---

## 📖 Usage Examples

### Interactive Mode
```bash
python3 xui_cracker.py
```

### CLI Mode - Full Auto Attack
```bash
python3 xui_cracker.py --mode auto \
    --targets ips.txt \
    --users users.txt \
    -- passwords.txt \
    --threads 20 \
    --output results.json
```

### CLI Mode - Default Credentials Check
```bash
python3 xui_cracker.py --mode default \
    --targets ips.txt \
    --threads 30
```

### CLI Mode - Scan Only
```bash
python3 xui_cracker.py --mode scan \
    --targets ips.txt
```

### CLI Mode - API Exploitation
```bash
python3 xui_cracker.py --mode api \
    --target-url https://target.com:443 \
    --session-token YOUR_TOKEN
```

---

## 📁 Project Structure

```
XUI_CRACKER_ENHANCED/
├── xui_cracker.py          # Main toolkit (2000+ lines)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── docs/
│   └── TUTORIAL_FA.md      # Persian tutorial
├── users.txt               # Default username list
├── passwords.txt           # Default password list
└── ips.txt                 # Sample target list
```

---

## 🎮 Target Format

### IP:PORT Format (Recommended)
```
192.168.1.1:443
10.0.0.1:2053
172.16.0.5:8443
```

### URL Format
```
http://example.com:80
https://example.com:443
http://192.168.1.1:2053
```

### Mixed Format
Both formats work simultaneously!

---

## 📤 Output Files

### xui_good.txt
Found credentials in simple format:
```
https://target.com:443 | admin:admin | 2024-01-15 14:30:00
```

### xui_results.json
Complete results with metadata:
```json
{
  "scan_date": "2024-01-15 14:30:00",
  "total_found": 5,
  "credentials": [...]
}
```

### xui_scan_results.json
Scan mode output with panel details.

### xui_api_exploit.json
API exploitation data.

---

## 🔧 Configuration Options

### Command Line Arguments
| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--mode` | `-m` | Attack mode | interactive |
| `--targets` | `-t` | Target IP file | required |
| `--users` | `-u` | Username file | users.txt |
| `--passwords` | `-p` | Password file | passwords.txt |
| `--threads` | | Thread count | 10 |
| `--proxy-file` | | Proxy list file | none |
| `--output` | `-o` | Output file | auto |
| `--delay` | | Request delay (sec) | 0.1 |
| `--scan-only` | | Scan only, no attack | false |

---

## 🌐 What is 3X-UI?

[3X-UI](https://github.com/MHSanaei/3x-ui) is a popular open-source web panel for managing **Xray-core** proxy servers. It supports:

- **VMess** - V2Ray protocol
- **VLESS** - Lightweight V2Ray protocol  
- **Trojan** - Camouflaged protocol
- **ShadowSocks** - Secure proxy protocol
- And more...

### Why Test 3X-UI Security?

Many 3X-UI deployments have:
- ❌ Default credentials unchanged
- ❌ Weak passwords
- ❌ Exposed admin panels
- ❌ No rate limiting
- ❌ Missing security headers

This tool helps identify these vulnerabilities **before** attackers do!

---

## 🛡️ Security Best Practices for 3X-UI

If you run a 3X-UI panel:

1. **Change default credentials immediately**
2. **Use strong, unique passwords**
3. **Enable firewall rules** (restrict IP access)
4. **Use HTTPS/TLS** always
5. **Keep updated** to latest version
6. **Enable fail2ban** or similar
7. **Don't expose panel** to public internet if possible

---

## 🐛 Bug Reports & Contributions

Found a bug? Want to contribute?

1. Check existing Issues first
2. Create detailed bug report
3. Submit PR with description

---

## 👥 Credits

- **Original Author**: [@cynetx](https://t.me/cynetx) - Base version
- **Enhanced By**: [@mansorkorea84](https://github.com/mansorkorea84) - v3.0
- **Inspiration**: 3X-UI Community

---

## 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

**⚡ POWERED BY XUI CRACKER ENHANCED ⚡**

*Advanced 3X-UI Panel Security Toolkit*

🔗 [Report Bug] · [Request Feature] · [Persian Tutorial](docs/TUTORIAL_FA.md)

**Made with 🔥 by @mansorkorea84**

</div>
