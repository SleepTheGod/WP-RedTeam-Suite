# WP-RedTeam-Suite

**Advanced WordPress Penetration Testing Suite - Red Team Edition**

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)](https://github.com/SleepTheGod/WP-RedTeam-Suite)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

## 🚀 Overview

WP-RedTeam-Suite is a comprehensive WordPress penetration testing tool designed for red team operations, CTF competitions, and authorized security assessments. With **5000+ endpoints**, **1000+ plugin checks**, and **advanced exploitation modules**, it surpasses traditional tools like WPScan in both speed and coverage.

### 🔥 Key Features

- **📊 5000+ Endpoints** - Comprehensive WordPress endpoint enumeration
- **🔍 1000+ Plugin Checks** - Extensive plugin vulnerability scanning
- **🎨 3000+ Theme Checks** - Complete theme detection and analysis
- **🛡️ Backdoor Detection** - Advanced webshell and backdoor identification
- **💥 Exploit Modules** - Automated exploitation for common vulnerabilities
- **👤 User Enumeration** - REST API and author-based user discovery
- **🔐 Security Auditing** - Header analysis and configuration review
- **⚡ Multi-Threaded** - Fast parallel scanning with adjustable threads
- **📈 Detailed Reporting** - Comprehensive JSON and console reports
- **🌐 HTTP/HTTPS Support** - Full SSL/TLS support with proxy capabilities

---

## 📦 Installation

### Clone the Repository
```bash
git clone https://github.com/SleepTheGod/WP-RedTeam-Suite.git
cd WP-RedTeam-Suite
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Manual Installation
```bash
pip install requests beautifulsoup4 urllib3 colorama
```

---

## 🛠️ Requirements

- Python 3.6+
- requests
- beautifulsoup4
- urllib3
- colorama

---

## 🚀 Quick Start

### Basic Scan
```bash
python wp_redteam.py -u http://target.com
```

### Advanced Scan with Options
```bash
python wp_redteam.py -u http://target.com -c "admin=hash;user=admin" -t 50 -T 10
```

### Through Proxy
```bash
python wp_redteam.py -u http://target.com -p http://127.0.0.1:8080
```

### With Custom User-Agent
```bash
python wp_redteam.py -u http://target.com -a "Mozilla/5.0 (Custom) AppleWebKit/537.36"
```

---

## 📊 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url` | Target WordPress URL (required) | - |
| `-c, --cookies` | Authentication cookies (key=value; key2=value2) | None |
| `-t, --threads` | Number of threads for scanning | 30 |
| `-T, --timeout` | Request timeout in seconds | 5 |
| `-p, --proxy` | Proxy URL (e.g., http://127.0.0.1:8080) | None |
| `-a, --user-agent` | Custom User-Agent | Random |
| `--no-ssl-verify` | Disable SSL verification | False |

---

## 🔍 What It Scans

### Endpoint Categories

#### 1. **Core WordPress**
- Admin directories (`/wp-admin/`, `/wp-admin/network/`, `/wp-admin/user/`)
- Core files (`wp-config.php`, `wp-login.php`, `xmlrpc.php`)
- REST API endpoints (`/wp-json/*`)
- Feed endpoints (`/feed/*`, `/comments/feed/*`)

#### 2. **Plugins (1000+)**
- Popular plugins (Akismet, Yoast SEO, WooCommerce, etc.)
- Security plugins (Wordfence, Sucuri, etc.)
- Backup plugins (UpdraftPlus, BackupBuddy, etc.)
- Custom plugin detection

#### 3. **Themes (3000+)**
- Default themes (Twenty* series)
- Popular themes (Divi, Astra, OceanWP, etc.)
- Premium themes (Avada, Enfold, The7, etc.)
- Custom theme detection

#### 4. **Security & Backup Files**
- Configuration files (`.env`, `wp-config.php`, `settings.php`)
- Backup files (`*.sql`, `*.bak`, `*.backup`)
- Log files (`error_log`, `debug.log`, `*.log`)
- Development files (`.git/`, `.svn/`, `.idea/`)

#### 5. **Vulnerability Checks**
- SQL Injection testing
- XSS testing
- Security header analysis
- CVE database matching
- File upload vulnerabilities
- XML-RPC exploitation

#### 6. **Backdoor Detection**
- Common webshell signatures
- Suspicious PHP functions
- Obfuscated code detection
- Plugin backdoors

---

## 📋 Example Output

```
 ▄█     █▄     ▄███████▄         ▄████████    ▄████████ ████████▄           ███        ▄████████    ▄████████   ▄▄▄▄███▄▄▄▄        
███     ███   ███    ███        ███    ███   ███    ███ ███   ▀███      ▀█████████▄   ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄      
███     ███   ███    ███        ███    ███   ███    █▀  ███    ███         ▀███▀▀██   ███    █▀    ███    ███ ███   ███   ███      
███     ███   ███    ███       ▄███▄▄▄▄██▀  ▄███▄▄▄     ███    ███          ███   ▀  ▄███▄▄▄       ███    ███ ███   ███   ███      
███     ███ ▀█████████▀       ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ███    ███          ███     ▀▀███▀▀▀     ▀███████████ ███   ███   ███      
███     ███   ███             ▀███████████   ███    █▄  ███    ███          ███       ███    █▄    ███    ███ ███   ███   ███      
███ ▄█▄ ███   ███               ███    ███   ███    ███ ███   ▄███          ███       ███    ███   ███    ███ ███   ███   ███      
 ▀███▀███▀   ▄████▀             ███    ███   ██████████ ████████▀          ▄████▀     ██████████   ███    █▀   ▀█   ███   █▀  

                       ▄████████  ▄████████    ▄████████ ███▄▄▄▄   ███▄▄▄▄      ▄████████    ▄████████                             
                      ███    ███ ███    ███   ███    ███ ███▀▀▀██▄ ███▀▀▀██▄   ███    ███   ███    ███                             
                      ███    █▀  ███    █▀    ███    ███ ███   ███ ███   ███   ███    █▀    ███    ███                             
                      ███        ███          ███    ███ ███   ███ ███   ███  ▄███▄▄▄      ▄███▄▄▄▄██▀                             
                    ▀███████████ ███        ▀███████████ ███   ███ ███   ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀                               
                             ███ ███    █▄    ███    ███ ███   ███ ███   ███   ███    █▄  ▀███████████                             
                       ▄█    ███ ███    ███   ███    ███ ███   ███ ███   ███   ███    ███   ███    ███                             
                     ▄████████▀  ████████▀    ███    █▀   ▀█   █▀   ▀█   █▀    ██████████   ███    ███                             
                                                                                            ███    ███  


[+] WordPress detected!
[+] WordPress Version: 5.8.2
[*] Scanning 5200 endpoints...
[+] Found endpoint: http://target.com/wp-admin (Status: 200)
[+] Found endpoint: http://target.com/wp-login.php (Status: 200)
[+] Detected plugin: woocommerce (Version: 4.5.2)
[+] Detected plugin: wordfence (Version: 7.5.0)
[+] Detected theme: twentytwenty (Version: 1.8)
[*] Enumerating users...
[+] Found user: admin (admin) - ID: 1
[+] Found user: test (testuser) - ID: 2
[*] Scanning for backdoors and webshells...
[!] BACKDOOR DETECTED: http://target.com/wp-content/plugins/shell/shell.php
    Signature: system($_GET['cmd'])
[*] Checking for known CVEs...
[!] CVE-2020-4567 found in woocommerce 4.5.2
    Auth Bypass (High)
[*] Testing SQL Injection...
[!] Potential SQL injection at http://target.com/?p=1' OR '1'='1
[*] Generating report...

============================================================
                       SCAN REPORT
============================================================

Scan Target: http://target.com
Scan Start: 2024-01-15 14:30:45
Scan Duration: 2:45:30

                           STATISTICS
------------------------------------------------------------
Total Endpoints Checked: 5200
Endpoints Discovered: 342
Plugins Detected: 15
Themes Detected: 3
Users Enumerated: 2
Total Requests: 15742
Successful Requests: 14891
Failed Requests: 851

                        VULNERABILITIES
------------------------------------------------------------
[!] Missing X-Frame-Options header
[!] Missing Content-Security-Policy header
[!] CVE-2020-4567 - Auth Bypass (High)
[!] Potential SQL injection at /?p=1

                           BACKDOORS
------------------------------------------------------------
[!] http://target.com/wp-content/plugins/shell/shell.php - Backdoor plugin detected

                         CREDENTIALS
------------------------------------------------------------
[!] admin:password123 at http://target.com/wp-login.php

                           FINDINGS
------------------------------------------------------------
Users Found:
  - admin (admin) - ID: 1
  - test (testuser) - ID: 2

Plugins Found:
  - woocommerce: 4.5.2
  - wordfence: 7.5.0
  - akismet: 4.1.7
  - contact-form-7: 5.3.2

Themes Found:
  - twentytwenty: 1.8
  - twentynineteen: 1.9
  - divi: 4.10.0

============================================================
Scan Complete!
============================================================

[+] Results saved to wp_scan_20240115_143045.json
```

---

## 🎯 Use Cases

### 1. **CTF Competitions**
- Rapid WordPress reconnaissance
- Vulnerability exploitation
- Flag capture automation

### 2. **Penetration Testing**
- Authorized security assessments
- Vulnerability identification
- Security posture evaluation

### 3. **Red Team Operations**
- Fast enumeration of WordPress installations
- Credential discovery
- Backdoor identification

### 4. **Security Auditing**
- Configuration review
- Security header analysis
- Plugin/theme vulnerability assessment

---

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is designed for authorized security testing and educational purposes only.

- ✅ **DO** use this tool on systems you own or have explicit permission to test
- ✅ **DO** use this tool for CTF competitions and authorized security assessments
- ✅ **DO** use this tool for educational purposes and security research
- ❌ **DO NOT** use this tool for illegal activities
- ❌ **DO NOT** use this tool without proper authorization
- ❌ **DO NOT** use this tool for any malicious purposes

**Always obtain written permission before testing any system you don't own.**

---

## 🔧 Development

### Project Structure
```
WP-RedTeam-Suite/
├── wp_redteam.py          # Main scanner
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── LICENSE                # MIT License
└── examples/              # Example usage scripts
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

### TODO
- [ ] Add more CVE entries
- [ ] Implement fuzzing module
- [ ] Add WAF detection
- [ ] Improve exploit modules
- [ ] Add support for WordPress MU
- [ ] Implement API for automation

---

## 📚 Similar Tools

| Tool | Features | Language |
|------|----------|----------|
| **WP-RedTeam-Suite** | 5000+ endpoints, Multi-threaded | Python |
| WPScan | 1000+ plugins, API | Ruby |
| WPscan | ~500 endpoints | Python |
| WPSeku | ~300 endpoints | Python |
| WPForce | ~200 endpoints | Python |

---

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/SleepTheGod/WP-RedTeam-Suite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SleepTheGod/WP-RedTeam-Suite/discussions)
- **Security**: [Security Policy](SECURITY.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- WordPress Security Team
- CTF Community
- WPScan Team
- Security Researchers

---

## ⭐ Star History

If you find this tool useful, please consider giving it a ⭐ on [GitHub](https://github.com/SleepTheGod/WP-RedTeam-Suite)!

---

**Built with ❤️ by SleepTheGod**
