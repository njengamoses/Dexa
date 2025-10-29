# Dexa - Offensive Security Toolkit

Modules:
- core/scanner.py : nmap wrapper
- core/recon.py   : whois wrapper
- core/report.py  : simple report saver
- utils/logger.py : basic logging
- cli.py          : command-line interface

Ensure system tools are installed: sudo apt update && sudo apt install nmap whois -y
Run: python3 -m dexa.cli scan <target>  OR  python3 -m dexa.cli recon <domain>
