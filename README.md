# NetRecon: Multi-Threaded Port Scanner & Banner Grabber

A fast, lightweight, and modular network reconnaissance tool written in Python using raw sockets.

**NetRecon** goes beyond basic port scanning by actively capturing banners, analyzing protocol signatures, and parsing HTTP/HTTPS service headers to identify active services and potential server disclosures—all without relying on bulky third-party dependencies like **Nmap**.

---

##  Key Features

-  **High-Speed Scanning**
  - Utilizes Python's `ThreadPoolExecutor` for concurrent scanning, handling massive port ranges in seconds.

-  **Adaptive Banner Grabbing**
  - Sends targeted payloads depending on the port configuration (e.g., crafting specific HTTP headers for web ports) to prompt a detailed response from the service.

-  **Signature-Based Service Detection**
  - Matches raw socket responses against an internal database of known protocols (SSH, FTP, SMTP, HTTP) instead of relying solely on common port numbers.

-  **Web Header Analysis**
  - Extracts important server details and HTTP headers such as:
    - `Server`
    - `X-Powered-By`
    - `Set-Cookie`

-  **Clean CLI & Logging**
  - Supports:
    - Custom thread counts
    - Single ports, comma-separated ports, and port ranges
    - Saving structured scan results to a local text file

---

##  Architecture Overview

Instead of simply checking whether a TCP handshake succeeds, **NetRecon** actively communicates with open services to collect useful metadata.

### Scanning Workflow

1. **Port Identification**
   - Fast TCP connect sweep using `socket.connect_ex()`.

2. **Protocol Triggering**
   - Sends adaptive probes to encourage the service to respond.

3. **Fingerprinting & Intelligence**
   - Parses responses for:
     - Service banners
     - Version strings
     - HTTP headers
     - Protocol signatures

---

##  Installation

No external dependencies are required.

NetRecon relies entirely on Python's standard library.

```bash
git clone https://github.com/ahbkr/Network-Security-Toolkit.git
cd Network-Security-Toolkit
```

---

##  Usage

```bash
python NetRecon.py <target> [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `target` | Target IP address or domain name (e.g., `192.168.1.1` or `example.com`) |

### Options

| Option | Description |
|--------|-------------|
| `-p`, `--ports` | Ports to scan. Supports single ports, comma-separated values, or ranges. **Default:** `1-1024` |
| `-t`, `--threads` | Number of concurrent threads. **Default:** `100` |
| `-o`, `--output` | Save structured scan results to a local text file |

---

##  Examples

### Basic Scan (Top 1024 Ports)

```bash
python NetRecon.py 192.168.1.50 -t 150
```

### Scan Specific Ports

```bash
python NetRecon.py example.com -p 22,80,443,8080
```

### Full Port Scan with Output File

```bash
python NetRecon.py 10.0.0.1 -p 1-65535 -t 200 -o local_scan_report.txt
```

---

##  Sample Output

```text
============================================================
[*] Starting Scan on Target: 192.168.1.131
[*] Total Ports to Scan   : 5
[*] Thread Count          : 100
============================================================

[+] Port 22   | Service: SSH     | Status: OPEN | Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5

[+] Port 80   | Service: HTTP    | Status: OPEN
              | Info: Server: Apache/2.4.41 (Ubuntu)
              |       Set-Cookie: PHPSESSID=...

[+] Port 443  | Service: HTTPS   | Status: OPEN
              | Banner: HTTPS (Encrypted)

[+] Port 3306 | Service: MySQL   | Status: OPEN
              | Banner: No response

[*] Scan completed successfully.
```

---

##  Disclaimer

This project is intended **strictly for educational purposes, authorized penetration testing, and local network auditing**.

The author is **not responsible** for any misuse, unauthorized network scanning, or illegal activities performed using this tool.
