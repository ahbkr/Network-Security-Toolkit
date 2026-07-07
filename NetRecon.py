import socket
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-Proxy"
}

SERVICE_PATTERNS = {
    "HTTP": ["HTTP/1.1", "HTTP/1.0"],
    "SSH": ["SSH-"],
    "FTP": ["220", "FTP"],
    "SMTP": ["SMTP", "HELO", "220"],
}

def detect_service_from_banner(banner_text):
    for service, keys in SERVICE_PATTERNS.items():
        for key in keys:
            if key in banner_text:
                return service
    return None

def parse_http_headers(banner_text):
    headers_info = ['Server:', 'X-Powered-By:', 'Set-Cookie:', 'Location:']
    extracted = []
    lines = banner_text.split('\r\n')
    for line in lines:
        for h in headers_info:
            if h.lower() in line.lower():
                extracted.append(line.strip())
    return " | ".join(extracted) if extracted else ""

def grab_banner(s, target, port):
    try:
        s.settimeout(1.5)
        if port in [80, 8080]:
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n"
            s.send(request.encode('utf-8'))
        else:
            s.send(b'\r\n')
            
        response = s.recv(1024)
        return response.decode(errors="ignore").strip()
    except:
        return ""

def scan_port(target, port, output_file):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0) 
            result = s.connect_ex((target, port))
            
            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")
                
                raw_banner = grab_banner(s, target, port)
                
                detected_service = detect_service_from_banner(raw_banner)
                if detected_service:
                    service = detected_service
                
                extra_info = ""
                if service in ["HTTP", "HTTP-Proxy"] and raw_banner:
                    extra_info = parse_http_headers(raw_banner)
                
                banner_desc = raw_banner.replace('\r\n', ' ') if raw_banner else "No response"
                if len(banner_desc) > 60: banner_desc = banner_desc[:57] + "..."
                
                output_str = f"[+] Port {port:<6} | Service: {service:<12} | Status: OPEN"
                if extra_info:
                    output_str += f" | Info: [{extra_info}]"
                else:
                    output_str += f" | Banner: {banner_desc}"
                    
                print(output_str)
                
                if output_file:
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(output_str + "\n")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Advanced Network Scanner & Banner Grabber")
    parser.add_argument("target", help="Target IP address or Domain name")
    parser.add_argument("-p", "--ports", default="1-1024", help="Ports range (e.g., 20-100 or 80,443,8080) [Default: 1-1024]")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of concurrent threads (default: 100)")
    parser.add_argument("-o", "--output", help="Save results to a text file")
    
    args = parser.parse_args()

    ports_to_scan = []
    if ',' in args.ports:
        ports_to_scan = [int(p) for p in args.ports.split(',')]
    elif '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
        ports_to_scan = range(start, end + 1)
    else:
        ports_to_scan = [int(args.ports)]

    print("\n" + "="*60)
    print(f"[*] Starting Scan on Target: {args.target}")
    print(f"[*] Total Ports to Scan   : {len(ports_to_scan)}")
    print(f"[*] Thread Count           : {args.threads}")
    if args.output:
        print(f"[*] Output File            : {args.output}")
    print("="*60 + "\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for port in ports_to_scan:
            executor.submit(scan_port, args.target, port, args.output)
            
    print("\n[*] Scan completed successfully.")

if __name__ == "__main__":
    main()