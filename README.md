# NetRecon: Multi-Threaded Port Scanner & Banner Grabber

A fast, lightweight, and modular network reconnaissance tool written in Python using raw sockets. NetRecon goes beyond basic port scanning by actively capturing banners, analyzing protocol signatures, and parsing HTTP/HTTPS service headers to identify active services and potential server disclosures—all without relying on bulky third-party dependencies like Nmap.

## Key Features

* **High-Speed Scanning:** Utilizes Python's `ThreadPoolExecutor` for concurrent scanning, handling massive port ranges in seconds.
* **Adaptive Banner Grabbing:** Sends targeted payloads depending on the port configuration (e.g., crafting specific HTTP headers for web ports) to prompt a detailed response from the service.
* **Signature-Based Service Detection:** Matches raw socket responses against an internal database of known protocols (SSH, FTP, SMTP, HTTP) rather than guessing services based strictly on port numbers.
* **Web Header Analysis:** Extracts critical server details and configuration headers (`Server`, `X-Powered-By`, `Set-Cookie`) during HTTP scans.
* **Clean CLI & Logging:** Supports customizable thread counts, specific port/range inputs, and outputs clean structured results to a local text file.

---

## Architecture Overview

Instead of just checking if a TCP handshake completes, NetRecon interacts with open ports to extract service metadata:

1. **Port Identification:** Fast TCP connect sweep (`socket.connect_ex`).
2. **Protocol Triggering:** Sends adaptive probes to nudge the daemon into responding.
3. **Fingerprinting & Intelligence:** Parses the buffer for known version strings and extracts HTTP header telemetry.

---

## Installation & Setup

No `pip install` required. NetRecon relies entirely on standard Python libraries.

```bash
git clone [https://github.com/ahbkr/Network-Security-Toolkit.git](https://github.com/ahbkr/Network-Security-Toolkit.git)
cd Network-Security-Toolkit
