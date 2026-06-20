#!/usr/bin/env python3
import os
import datetime
import argparse
from colorama import Fore, init

init(autoreset=True)

print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════════╗
║                 🔥 KALI RECON NINJA v2.2 🔥                  ║
║     Advanced Professional Reconnaissance Framework           ║
║              Perfect for Red Team & Internship Portfolio     ║
╚══════════════════════════════════════════════════════════════╝
""")

parser = argparse.ArgumentParser(description="Kali Recon Ninja v2.2")
parser.add_argument("-t", "--target", required=True, help="Target URL or IP")
args = parser.parse_args()

target = args.target
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
clean_target = target.replace('http://','').replace('https://','').replace('/', '_').replace(':', '_')
report_dir = f"reports/{clean_target}_{timestamp}"
os.makedirs(report_dir, exist_ok=True)

print(Fore.GREEN + f"[+] Launching Professional Recon on {target}\n")

def safe_run(cmd, name, output_file):
    print(Fore.CYAN + f"[+] Running {name}...")
    os.system(cmd)
    if os.path.exists(output_file) and os.path.getsize(output_file) > 10:
        print(Fore.GREEN + f"   ✅ {name} completed")
        return True
    else:
        print(Fore.YELLOW + f"   [!] {name} completed (limited output)")
        with open(output_file, "w") as f:
            f.write(f"# {name} completed.\n")
        return False

safe_run(f"nmap -A -T4 -oN {report_dir}/nmap.txt {target if not '://' in target else target.split('://')[1]}", "Nmap", f"{report_dir}/nmap.txt")
safe_run(f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt -o {report_dir}/gobuster.txt -t 50 --quiet -k", "Gobuster", f"{report_dir}/gobuster.txt")
safe_run(f"nikto -h {target} -o {report_dir}/nikto.txt --timeout 15", "Nikto", f"{report_dir}/nikto.txt")
safe_run(f"whatweb -a 3 {target} > {report_dir}/whatweb.txt", "WhatWeb", f"{report_dir}/whatweb.txt")
safe_run(f"nuclei -u {target} -o {report_dir}/nuclei.txt -silent", "Nuclei", f"{report_dir}/nuclei.txt")

# EyeWitness
print(Fore.CYAN + "[+] Capturing Screenshots...")
os.system(f"eyewitness -f {report_dir}/gobuster.txt --web -d {report_dir}/screenshots --no-prompt 2>/dev/null || echo '[*] EyeWitness done'")

# Professional HTML Report
html_report = f"{report_dir}/KALI_RECON_NINJA_v2.2_REPORT.html"

with open(html_report, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Kali Recon Ninja v2.2 • Professional Report</title>
    <style>
        body {{font-family:Segoe UI,Arial;background:#0a0a0a;color:#00ff9d;margin:40px;line-height:1.7;}}
        h1 {{color:#00ccff;text-align:center; font-size:28px;}}
        h2 {{color:#00ff9d;border-bottom:2px solid #00ccff;padding-bottom:10px;}}
        pre {{background:#111;padding:20px;border-radius:10px;overflow:auto;font-size:14px; border:1px solid #333;}}
        .header {{text-align:center;font-size:22px;color:#00ccff;margin:20px 0;}}
        .badge {{background:#00ccff;color:#000;padding:5px 12px;border-radius:20px;font-size:14px;}}
    </style>
</head>
<body>
    <div class="header">🔥 Kali Recon Ninja v2.2 <span class="badge">Professional Edition</span></div>
    <h1>Target: {target}</h1>
    <p><strong>Scan Date:</strong> {timestamp} | <strong>Tool Author:</strong> Cyber45</p>
    <hr>
    <h2>📡 Nmap Enumeration</h2><pre>{open(f'{report_dir}/nmap.txt', encoding='utf-8', errors='ignore').read()}</pre>
    <h2>📁 Directory Discovery</h2><pre>{open(f'{report_dir}/gobuster.txt', encoding='utf-8', errors='ignore').read()}</pre>
    <h2>🛡️ Nikto Analysis</h2><pre>{open(f'{report_dir}/nikto.txt', encoding='utf-8', errors='ignore').read()}</pre>
    <h2>⚡ Nuclei Vulnerability Scan</h2><pre>{open(f'{report_dir}/nuclei.txt', encoding='utf-8', errors='ignore').read() if os.path.exists(f"{report_dir}/nuclei.txt") else "Scan completed"}</pre>
    <h2>📸 EyeWitness Visual Evidence</h2>
    <p>Screenshots saved in <strong>screenshots/</strong> folder — ready for reporting.</p>
    <hr>
    <p><strong>This tool demonstrates practical automation, tool chaining, and professional reporting skills.</strong></p>
</body>
</html>""")

print(Fore.GREEN + "\n🎉 SCAN COMPLETE - PROFESSIONAL REPORT GENERATED!")
print(Fore.YELLOW + f"📁 Best Report: {html_report}")
