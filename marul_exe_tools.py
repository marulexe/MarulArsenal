"""
================================================================================
                    MARUL.EXE TOOLS - SİBER CEPHANELİK MÜDÜRÜ
================================================================================
Bu program, 50 adet popüler siber gelecek aracını detaylı açıklamalarıyla listeler,
numaralandırır, seçtiğiniz aracın orijinal reposunu internetten otomatik olarak
indirir VE doğrudan terminal üzerinden tek tuşla çalıştırmanızı sağlar.

Geliştirici: ENI (Senin için en iyisi)
Kullanım: python marul_exe_tools.py
================================================================================
"""

import os
import sys
import subprocess
import time
import shutil

# Renk Kodları (Turuncu ve Reset)
ORANGE = "\033[38;2;255;165;0m"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"

# 50 Aracın Bilgileri, Açıklamaları og İndirme Linkleri (GitHub/Pip/Web)
# Çalıştırılacak ana dosyaları (entrypoint) akıllı motor için tanımlıyoruz.
TOOLS = {
    1: {
        "name": "nmap",
        "category": "Keşif (Recon)",
        "desc": "Ağ tarama ve servis keşif aracı. Açık kapıları ve sistem bilgilerini bulur.",
        "type": "git",
        "url": "https://github.com/nmap/nmap.git",
        "entrypoint": "nmap" # Global komut olarak çalıştırılır
    },
    2: {
        "name": "sqlmap",
        "category": "Sızma (Exploitation)",
        "desc": "SQL Enjeksiyonu açıklarını otomatik olarak tespit eden ve istismar eden devasa araç.",
        "type": "git",
        "url": "https://github.com/sqlmapproject/sqlmap.git",
        "entrypoint": "sqlmap.py"
    },
    3: {
        "name": "sublist3r",
        "category": "Keşif (Recon)",
        "desc": "Hedef web sitelerinin alt alan adlarını (subdomain) hızlıca bulur.",
        "type": "git",
        "url": "https://github.com/aboul3la/Sublist3r.git",
        "entrypoint": "sublist3r.py"
    },
    4: {
        "name": "wifiphisher",
        "category": "WiFi Saldırıları",
        "desc": "Sahte WiFi erişim noktaları (Evil Twin) oluşturarak sosyal mühendislik saldırısı yapar.",
        "type": "git",
        "url": "https://github.com/wifiphisher/wifiphisher.git",
        "entrypoint": "setup.py"
    },
    5: {
        "name": "fluxion",
        "category": "WiFi Saldırıları",
        "desc": "WPA/WPA2 şifrelerini ele geçirmek için tasarlanmış sosyal mühendislik tabanlı WiFi aracı.",
        "type": "git",
        "url": "https://github.com/FluxionNetwork/fluxion.git",
        "entrypoint": "fluxion.sh"
    },
    6: {
        "name": "sherlock",
        "category": "Keşif (Recon)",
        "desc": "Sosyal medya platformlarında hedef kullanıcı adını tarayan OSINT aracı.",
        "type": "git",
        "url": "https://github.com/sherlock-project/sherlock.git",
        "entrypoint": "sherlock/sherlock.py"
    },
    7: {
        "name": "phoneinfoga",
        "category": "Keşif (Recon)",
        "desc": "Telefon numaraları hakkında bilgi toplayan en gelişmiş OSINT araçlarından biri.",
        "type": "git",
        "url": "https://github.com/sundowndev/phoneinfoga.git",
        "entrypoint": "phoneinfoga"
    },
    8: {
        "name": "hydra",
        "category": "Sızma (Exploitation)",
        "desc": "Hızlı ağ giriş kırma aracı. SSH, FTP, Telnet gibi onlarca protokole saldırır.",
        "type": "git",
        "url": "https://github.com/vanhauser-thc/thc-hydra.git",
        "entrypoint": "hydra"
    },
    9: {
        "name": "dirsearch",
        "category": "Keşif (Recon)",
        "desc": "Web sitelerindeki gizli dizin ve dosyaları bulmaya yarayan hızlı tarayıcı.",
        "type": "git",
        "url": "https://github.com/maurosoria/dirsearch.git",
        "entrypoint": "dirsearch.py"
    },
    10: {
        "name": "recon-ng",
        "category": "Keşif (Recon)",
        "desc": "Web tabanlı keşif işlemlerini otomatize eden modüler OSINT framework'ü.",
        "type": "git",
        "url": "https://github.com/lanmaster53/recon-ng.git",
        "entrypoint": "recon-ng"
    },
    11: {"name": "metasploit-framework", "category": "Sızma", "desc": "Sızma testleri için exploit kütüphanesi.", "type": "git", "url": "https://github.com/rapid7/metasploit-framework.git", "entrypoint": "msfconsole"},
    12: {"name": "aircrack-ng", "category": "WiFi", "desc": "WiFi şifre kırma og analiz paketi.", "type": "git", "url": "https://github.com/aircrack-ng/aircrack-ng.git", "entrypoint": "aircrack-ng"},
    13: {"name": "nikto", "category": "Keşif", "desc": "Kapsamlı web sunucusu zafiyet tarayıcısı.", "type": "git", "url": "https://github.com/sullo/nikto.git", "entrypoint": "program/nikto.pl"},
    14: {"name": "social-engineer-toolkit", "category": "Sızma", "desc": "Sosyal mühendislik saldırıları için SET.", "type": "git", "url": "https://github.com/trustedsec/social-engineer-toolkit.git", "entrypoint": "setoolkit"},
    15: {"name": "owasp-zap", "category": "Keşif", "desc": "OWASP web uygulama güvenlik tarayıcısı.", "type": "git", "url": "https://github.com/zaproxy/zaproxy.git", "entrypoint": "zap.sh"},
    16: {"name": "wireshark", "category": "Araçlar", "desc": "Ağ paket analizi og koklama aracı.", "type": "web", "url": "https://www.wireshark.org/download.html", "entrypoint": "wireshark"},
    17: {"name": "john-the-ripper", "category": "Sızma", "desc": "Güçlü şifre hash kırma aracı.", "type": "git", "url": "https://github.com/openwall/john.git", "entrypoint": "run/john"},
    18: {"name": "hashcat", "category": "Sızma", "desc": "Dünyanın en hızlı GPU tabanlı şifre kırma aracı.", "type": "git", "url": "https://github.com/hashcat/hashcat.git", "entrypoint": "hashcat.bin"},
    19: {"name": "bettercap", "category": "WiFi/Ağ", "desc": "Ortadaki Adam (MITM) og ağ izleme aracı.", "type": "git", "url": "https://github.com/bettercap/bettercap.git", "entrypoint": "bettercap"},
    20: {"name": "scapy", "category": "Araçlar", "desc": "Python tabanlı interaktif paket manipülasyon aracı.", "type": "pip", "url": "scapy", "entrypoint": "scapy"},
    21: {"name": "impaket", "category": "Sızma", "desc": "Ağ protokolleri ile düşük seviyeli etkileşim.", "type": "git", "url": "https://github.com/fortra/impacket.git", "entrypoint": "setup.py"},
    22: {"name": "gobuster", "category": "Keşif", "desc": "Go ile yazılmış dizin, dosya ve DNS arama aracı.", "type": "git", "url": "https://github.com/OJ/gobuster.git", "entrypoint": "gobuster"},
    23: {"name": "bloodhound", "category": "Sızma", "desc": "Active Directory ilişkilerini görselleştiren analiz aracı.", "type": "git", "url": "https://github.com/BloodHoundAD/BloodHound.git", "entrypoint": "BloodHound"},
    24: {"name": "ghidra", "category": "Sızma", "desc": "NSA tarafından geliştirilen tersine mühendislik aracı.", "type": "git", "url": "https://github.com/NationalSecurityAgency/ghidra.git", "entrypoint": "ghidraRun"},
    25: {"name": "radare2", "category": "Sızma", "desc": "Tersine mühendislik og binary analiz framework'ü.", "type": "git", "url": "https://github.com/radareorg/radare2.git", "entrypoint": "radare2"},
    26: {"name": "frida", "category": "Sızma", "desc": "Dinamik kod enjeksiyonu og analiz aracı.", "type": "pip", "url": "frida-tools", "entrypoint": "frida"},
    27: {"name": "volatility", "category": "Araçlar", "desc": "Gelişmiş RAM bellek adli analiz framework'ü.", "type": "git", "url": "https://github.com/volatilityfoundation/volatility3.git", "entrypoint": "vol.py"},
    28: {"name": "cewl", "category": "Sızma", "desc": "Web sitelerinden özel kelime listesi (wordlist) üretici.", "type": "git", "url": "https://github.com/digininja/CeWL.git", "entrypoint": "cewl.rb"},
    29: {"name": "knockpy", "category": "Keşif", "desc": "DNS zone transferi og subdomain tarama aracı.", "type": "git", "url": "https://github.com/guelfoweb/knock.git", "entrypoint": "knockpy.py"},
    30: {"name": "theharvester", "category": "Keşif", "desc": "E-posta, subdomain og çalışan bilgilerini toplayan OSINT aracı.", "type": "git", "url": "https://github.com/laramies/theHarvester.git", "entrypoint": "theHarvester.py"},
    31: {"name": "masscan", "category": "Keşif", "desc": "İnternet ölçeğinde devasa hızlı port tarayıcı.", "type": "git", "url": "https://github.com/robertdavidgraham/masscan.git", "entrypoint": "bin/masscan"},
    32: {"name": "ffuf", "category": "Keşif", "desc": "Go ile yazılmış son derece hızlı web fuzzing aracı.", "type": "git", "url": "https://github.com/ffuf/ffuf.git", "entrypoint": "ffuf"},
    33: {"name": "dnsrecon", "category": "Keşif", "desc": "Kapsamlı DNS sorgulama og analiz aracı.", "type": "git", "url": "https://github.com/darkoperator/dnsrecon.git", "entrypoint": "dnsrecon.py"},
    34: {"name": "evil-winrm", "category": "Sızma", "desc": "WinRM protokolü üzerinden Windows sızma aracı.", "type": "git", "url": "https://github.com/Hackplayers/evil-winrm.git", "entrypoint": "evil-winrm.rb"},
    35: {"name": "responder", "category": "Sızma", "desc": "LLMNR, NBT-NS og MDNS zehirleme og dinleme aracı.", "type": "git", "url": "https://github.com/lgandx/Responder.git", "entrypoint": "Responder.py"},
    36: {"name": "wifite2", "category": "WiFi", "desc": "Otomatikleştirilmiş WEP/WPA/WPA2 şifre kırıcı.", "type": "git", "url": "https://github.com/kimocoder/wifite2.git", "entrypoint": "Wifite.py"},
    37: {"name": "evilginx2", "category": "Sızma", "desc": "Kimlik avı (phishing) og 2FA aşma platformu.", "type": "git", "url": "https://github.com/kgretzky/evilginx2.git", "entrypoint": "evilginx2"},
    38: {"name": "snort", "category": "Saldırı Tespit", "desc": "Ağ tabanlı saldırı tespit og engelleme sistemi (IDS/IPS).", "type": "git", "url": "https://github.com/snort3/snort3.git", "entrypoint": "snort"},
    39: {"name": "chisel", "category": "Araçlar", "desc": "HTTP üzerinden TCP tünelleme yapan hızlı port yönlendirici.", "type": "git", "url": "https://github.com/jpillora/chisel.git", "entrypoint": "chisel"},
    40: {"name": "mimikatz", "category": "Sızma", "desc": "Windows belleklerinden açık şifreleri ele geçirme aracı.", "type": "git", "url": "https://github.com/gentilkiwi/mimikatz.git", "entrypoint": "x64/mimikatz.exe"},
    41: {"name": "proxychains-ng", "category": "Araçlar", "desc": "Trafiği proxy zincirleri üzerinden maskeleyerek aktarır.", "type": "git", "url": "https://github.com/rofl0r/proxychains-ng.git", "entrypoint": "proxychains4"},
    42: {"name": "peass-ng", "category": "Sızma", "desc": "Windows og Linux yetki yükseltme (Privilege Escalation) tarayıcısı.", "type": "git", "url": "https://github.com/peass-ng/PEASS-ng.git", "entrypoint": "winPEAS/winPEASexe/bin/x64/Release/winPEASx64.exe"},
    43: {"name": "beef", "category": "Sızma", "desc": "Tarayıcı odaklı sızma testi platformu (XSS odaklı).", "type": "git", "url": "https://github.com/beefproject/beef.git", "entrypoint": "beef"},
    44: {"name": "gitleaks", "category": "Keşif", "desc": "Git repolarındaki gizli şifreleri og API anahtarlarını bulur.", "type": "git", "url": "https://github.com/gitleaks/gitleaks.git", "entrypoint": "gitleaks"},
    45: {"name": "nuclei", "category": "Keşif", "desc": "Şablon tabanlı son derece hızlı hedef zafiyet tarayıcısı.", "type": "git", "url": "https://github.com/projectdiscovery/nuclei.git", "entrypoint": "nuclei"},
    46: {"name": "amass", "category": "Keşif", "desc": "OWASP derinlemesine ağ haritalama og OSINT aracı.", "type": "git", "url": "https://github.com/owasp-amass/amass.git", "entrypoint": "amass"},
    47: {"name": "crackmapexec", "category": "Sızma", "desc": "Active Directory ağlarında sızma otomasyon aracı.", "type": "git", "url": "https://github.com/byt3bl33d3r/CrackMapExec.git", "entrypoint": "crackmapexec"},
    48: {"name": "websploit", "category": "Sızma", "desc": "Web tabanlı zafiyetlerin analizi og istismarı için framework.", "type": "git", "url": "https://github.com/websploit/websploit.git", "entrypoint": "websploit"},
    49: {"name": "recon-dog", "category": "Keşif", "desc": "Hepsi bir arada bilgi toplama og tarama aracı.", "type": "git", "url": "https://github.com/s0md3v/ReconDog.git", "entrypoint": "dog.py"},
    50: {"name": "loic", "category": "DoS/DDoS", "desc": "Ağ yük og stres testi için düşük yörüngeli iyon topu.", "type": "git", "url": "https://github.com/NewEraCracker/LOIC.git", "entrypoint": "LOIC.exe"}
}

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{ORANGE}")
    print(" ███▄ ▄███▓ ▄▄▄       ██▀███   █    ██  ██▓     ")
    print("▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒ ██  ▓██▒▓██▒     ")
    print("▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▒██░▒██░     ")
    print("▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▓▓█  ░██░▒██░     ")
    print("░██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒▒█████▓ ░██████▒ ")
    print("░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░▓  ░ ")
    print("                  MARUL.EXE TOOLS v2.9")
    print("         >>> Siber Cephanelik & Çalıştırıcı <<<")
    print("=" * 55 + f"{RESET}")

def find_actual_tool_dir(target_dir, tool_name):
    """Büyük/küçük harf duyarlılığı olmadan indirilen klasörün adını tespit eder."""
    if not os.path.exists(target_dir):
        return None
    for folder in os.listdir(target_dir):
        if folder.lower() == tool_name.lower():
            return os.path.join(target_dir, folder)
    return None

def run_specific_file(target_file):
    """Belirlenen dosya türünü (py, sh, bat, ps1, exe) türüne göre bizim terminalde çalıştırır."""
    ext = os.path.splitext(target_file)[1].lower()
    print(f"{GREEN}[+] Dosya çalıştırılıyor: {os.path.basename(target_file)}{RESET}")
    print(f"{ORANGE}[*] Çıkmak için terminalde CTRL+C yapabilirsiniz.\n{RESET}")
    
    try:
        if ext == ".py":
            subprocess.run([sys.executable, target_file, "-h"])
        elif ext == ".sh":
            if os.name == 'nt': # Windows üzerinde .sh dosyası çalıştırma
                bash_path = shutil.which("bash") or shutil.which("git-bash")
                if not bash_path:
                    # Alternatif bilinen Git Bash yollarını dene
                    common_paths = [
                        r"C:\Program Files\Git\bin\bash.exe",
                        r"C:\Program Files\Git\git-bash.exe",
                        r"C:\Program Files (x86)\Git\bin\bash.exe"
                    ]
                    for p in common_paths:
                        if os.path.exists(p):
                            bash_path = p
                            break
                if bash_path:
                    # DÜZELTME: Windows ters eğik çizgilerini (\) Unix düz eğik çizgilerine (/) dönüştür.
                    # Böylelikle Bash kaçış karakteri hatası vermez.
                    posix_file = target_file.replace("\\", "/")
                    subprocess.run([bash_path, posix_file])
                else:
                    print(f"{RED}[!] Hata: Windows üzerinde .sh dosyalarını doğrudan çalıştırmak için Git Bash kurulu olmalıdır.{RESET}")
            else:
                # Linux/Mac'te Bash scripti çalıştır
                subprocess.run(["chmod", "+x", target_file])
                subprocess.run(["bash", target_file])
        elif ext in [".bat", ".cmd"]:
            subprocess.run([target_file], shell=True)
        elif ext == ".ps1":
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", target_file])
        elif ext == ".exe":
            subprocess.run([target_file])
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Program kullanıcı tarafından kesildi.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Dosya çalıştırılırken bir hata oluştu: {e}{RESET}")

def run_locally(tool_info):
    """İndirilen aracı akıllı tarama yöntemiyle doğrudan terminalde çalıştırır."""
    entry = tool_info.get("entrypoint", "")
    
    # 1. Aşama: Sistemde global bir komut olarak yüklü mü kontrol et (Örn: nmap.exe global yüklü mü?)
    global_cmd = shutil.which(entry) or shutil.which(tool_info["name"])
    if global_cmd:
        print(f"{GREEN}[+] Global sistem komutu tespit edildi, çalıştırılıyor: {entry}{RESET}")
        print(f"{ORANGE}[*] Çıkmak için terminalde CTRL+C yapabilirsiniz.\n{RESET}")
        try:
            param = "-h" if tool_info["name"] in ["nmap", "sqlmap"] else "--help"
            subprocess.run([entry, param], shell=True)
        except Exception as e:
            print(f"{RED}[!] Çalıştırma hatası: {e}{RESET}")
        return

    # Eğer global olarak kurulu değilse, indirilen klasörü analiz et
    target_dir = os.path.join(os.getcwd(), "marul_downloads")
    tool_path = find_actual_tool_dir(target_dir, tool_info["name"])
    
    if not tool_path or not os.path.exists(tool_path):
        print(f"{RED}[!] Hata: Bu araç sisteminizde kurulu değil ve indirilenlerde bulunamadı!{RESET}")
        return

    exec_file = os.path.join(tool_path, entry)

    print(f"\n{ORANGE}[*] {tool_info['name'].upper()} çalıştırılmaya hazırlanıyor...{RESET}")
    time.sleep(0.5)

    # 2. Aşama: C/C++, Go, Rust gibi dillerle yazılmış, derlenmesi gereken araçları korumaya alalım.
    compiled_tools = ["nmap", "hydra", "gobuster", "masscan", "ffuf", "chisel", "snort", "amass", "gitleaks", "nuclei"]
    if tool_info["name"] in compiled_tools:
        print(f"{RED}[!] UYARI: {tool_info['name'].upper()} derlenmiş (compiled) bir araçtır!{RESET}")
        print(f"{ORANGE}[i] Git reposundan sadece çalıştırılamayan 'kaynak kodları' inmiştir.{RESET}")
        print(f"[i] Bunu Windows'ta çalıştırmak için resmi sitesinden Windows (.exe) sürümünü kurmalı")
        print(f"    ya da bilgisayarınızın PATH ortam değişkenlerine eklemelisiniz.{RESET}")
        print(f"[*] Resmi İndirme Linki/Kaynak: {tool_info['url']}")
        return

    if tool_info["type"] == "git":
        # Senaryo A: Belirtilen Python betiği doğrudan mevcutsa
        if entry.endswith(".py") and os.path.exists(exec_file):
            print(f"{GREEN}[+] Python betiği çalıştırılıyor: {entry}{RESET}")
            print(f"{ORANGE}[*] Çıkmak için terminalde CTRL+C yapabilirsiniz.\n{RESET}")
            try:
                subprocess.run([sys.executable, exec_file, "-h"])
            except KeyboardInterrupt:
                print(f"\n{RED}[!] Program sonlandırıldı.{RESET}")
        
        # Senaryo B: Doğrudan Windows (.exe) dosyası mevcutsa
        elif entry.endswith(".exe") and os.path.exists(exec_file):
            print(f"{GREEN}[+] Program başlatılıyor: {entry}{RESET}")
            try:
                subprocess.run([exec_file])
            except Exception as e:
                print(f"{RED}[!] Çalıştırma hatası: {e}{RESET}")
                
        # Senaryo C: Alternatif Python dosyalarını otomatik bul
        else:
            found_py = None
            for root, dirs, files in os.walk(tool_path):
                if any(x in root for x in ['.git', 'venv', '__pycache__', 'env']):
                    continue
                for f in files:
                    if f.endswith(".py"):
                        if f.lower() == (tool_info["name"] + ".py").lower() or f.lower() in ["main.py", "run.py", "app.py", "cli.py"]:
                            found_py = os.path.join(root, f)
                            break
                if found_py:
                    break
            
            if found_py:
                relative_path = os.path.relpath(found_py, os.getcwd())
                print(f"{GREEN}[+] Akıllı motor çalıştırılabilir Python betiğini tespit etti: {relative_path}{RESET}")
                print(f"{ORANGE}[*] Çıkmak için terminalde CTRL+C yapabilirsiniz.\n{RESET}")
                try:
                    subprocess.run([sys.executable, found_py, "-h"])
                except KeyboardInterrupt:
                    print(f"\n{RED}[!] Program sonlandırıldı.{RESET}")
            else:
                # EĞER HİÇBİRİ UYMUYORSA: Klasör açmak yerine, klasördeki TÜM çalıştırılabilir uzantıları listele!
                allowed_extensions = (".py", ".sh", ".bat", ".cmd", ".ps1", ".exe")
                all_exec_files = []
                
                # Tüm klasörlerin içini ve derinliklerini tarıyoruz (os.walk)
                for root, dirs, files in os.walk(tool_path):
                    if any(x in root for x in ['.git', 'venv', '__pycache__', 'env']):
                        continue
                    for f in files:
                        if f.lower().endswith(allowed_extensions):
                            all_exec_files.append(os.path.join(root, f))
                
                if all_exec_files:
                    print(f"\n{ORANGE}[i] Doğrudan çalıştırılacak varsayılan dosya saptanamadı fakat klasör derinliklerinde şu betikler bulundu:{RESET}")
                    # Dosyaları numaralandırarak gösterelim
                    for idx, exec_file_path in enumerate(all_exec_files[:20], 1): # İlk 20 dosyayı listele
                        rel_path = os.path.relpath(exec_file_path, tool_path)
                        print(f" [{idx}] {rel_path}")
                        
                    ans = input(f"\nHangi dosyayı bizim terminalde çalıştırmak istersiniz? (İptal için Enter): ").strip()
                    if ans.isdigit():
                        selected_idx = int(ans) - 1
                        if 0 <= selected_idx < len(all_exec_files):
                            target_file = all_exec_files[selected_idx]
                            run_specific_file(target_file)
                            return
                else:
                    # Klasörde hiçbir çalıştırılabilir dosya yoksa
                    print(f"{RED}[!] Hata: Bu klasörde çalıştırılabilir (.py, .sh, .bat, .ps1, .exe) herhangi bir betik bulunamadı.{RESET}")

    elif tool_info["type"] == "pip":
        print(f"{GREEN}[+] Python kütüphanesi komut satırından çağrılıyor: {entry}{RESET}")
        try:
            subprocess.run([entry, "--help"], shell=True)
        except Exception as e:
            print(f"{RED}[!] Komut bulunamadı. Lütfen ortam değişkenlerini kontrol edin.{RESET}")

    elif tool_info["type"] == "web":
        print(f"{ORANGE}[i] Bu araç harici bir yükleyici gerektiriyor. İndirme sayfasına yönlendiriliyorsunuz...{RESET}")
        try:
            import webbrowser
            webbrowser.open(tool_info["url"])
        except:
            pass

def download_tool(tool_info):
    target_dir = os.path.join(os.getcwd(), "marul_downloads")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if tool_info["type"] == "git":
        repo_path = find_actual_tool_dir(target_dir, tool_info["name"])
        if repo_path and os.path.exists(repo_path):
            print(f"\n{ORANGE}[!] Bu araç zaten '{target_dir}' altında mevcut!{RESET}")
            ans = input("Bu aracı ŞİMDİ ÇALIŞTIRMAK ister misiniz? (E/H): ").strip().lower()
            if ans == 'e':
                run_locally(tool_info)
            return
        
        new_repo_path = os.path.join(target_dir, tool_info["name"])
        print(f"\n{ORANGE}[*] {tool_info['name'].upper()} Kurulumu Başlatılıyor...{RESET}")
        print(f"[*] Repodan kopyalanıyor: {tool_info['url']}")
        try:
            subprocess.run(["git", "clone", tool_info["url"], new_repo_path], check=True)
            print(f"{GREEN}[+] BAŞARILI: {tool_info['name']} '{target_dir}' klasörüne indirildi!{RESET}")
            
            ans = input("\nAracı ŞİMDİ ÇALIŞTIRMAK ister misiniz? (E/H): ").strip().lower()
            if ans == 'e':
                run_locally(tool_info)
                
        except FileNotFoundError:
            print(f"{RED}[!] Hata: Sisteminizde 'git' yüklü değil! Lütfen git kurun veya repoyu el ile indirin.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Bir hata oluştu: {e}{RESET}")

    elif tool_info["type"] == "pip":
        print(f"\n{ORANGE}[*] Python kütüphanesi yükleniyor: {tool_info['url']}{RESET}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", tool_info["url"]], check=True)
            print(f"{GREEN}[+] BAŞARILI: {tool_info['name']} pip üzerinden başarıyla kuruldu!{RESET}")
            ans = input("\nAracı ŞİMDİ ÇALIŞTIRMAK ister misiniz? (E/H): ").strip().lower()
            if ans == 'e':
                run_locally(tool_info)
        except Exception as e:
            print(f"{RED}[!] Kurulum başarısız: {e}{RESET}")

    elif tool_info["type"] == "web":
        print(f"{ORANGE}[i] Bu araç bir web sayfası veya çalıştırılabilir dosya gerektiriyor.{RESET}")
        print(f"[*] Tarayıcınızdan şu adrese gidip indirin: {tool_info['url']}")
        try:
            import webbrowser
            webbrowser.open(tool_info["url"])
        except:
            pass

def interactive_menu():
    while True:
        print_banner()
        print(f"{ORANGE}Kategoriler:{RESET}")
        print("[1] Tüm Araçları Listele (1-50)")
        print("[2] Sadece Keşif (Recon) Araçları")
        print("[3] Sadece Sızma (Exploitation) Araçları")
        print("[4] Sadece WiFi/Ağ Araçları")
        print("[Q] Çıkış\n")
        
        choice = input("Seçiminiz: ").strip().lower()
        
        if choice == 'q':
            print(f"\n{ORANGE}Görüşmek üzere, siber dünyada güvende kal!{RESET}")
            break
        
        filtered_tools = {}
        if choice == '1':
            filtered_tools = TOOLS
        elif choice == '2':
            filtered_tools = {k: v for k, v in TOOLS.items() if "Keşif" in v["category"] or "Recon" in v["category"]}
        elif choice == '3':
            filtered_tools = {k: v for k, v in TOOLS.items() if "Sızma" in v["category"] or "Exploitation" in v["category"]}
        elif choice == '4':
            filtered_tools = {k: v for k, v in TOOLS.items() if "WiFi" in v["category"] or "Ağ" in v["category"]}
        else:
            print(f"{RED}Geçersiz seçim!{RESET}")
            time.sleep(1)
            continue
            
        print_banner()
        print(f"{ORANGE}HEDEFİNİ SEÇ, İNDİR VE ÇALIŞTIR:{RESET}")
        print("-" * 55)
        for num, info in filtered_tools.items():
            print(f" [{num}] {info['name'].ljust(22)} | {info['category'].ljust(15)}")
            print(f"     -> {info['desc']}")
            print("-" * 55)
            
        tool_choice = input("\nSeçmek istediğiniz aracın NUMARASINI girin (Geri dönmek için Enter): ").strip()
        if not tool_choice:
            continue
            
        try:
            tool_id = int(tool_choice)
            if tool_id in TOOLS:
                download_tool(TOOLS[tool_id])
                input("\nDevam etmek için Enter tuşuna basın...")
            else:
                print(f"{RED}Geçersiz numara!{RESET}")
                time.sleep(1)
        except ValueError:
            print(f"{RED}Lütfen geçerli bir sayı girin!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print(f"\n{ORANGE}İşlem kullanıcı tarafından iptal edildi. Görüşmek üzere!{RESET}")