#!/usr/bin/env python3
import argparse
from dexa.core import scanner, recon, report
from dexa.utils.logger import log

def cmd_scan(args):
    out = scanner.run_scan(args.target)
    if out:
        fname = report.save_report(out, args.target)
        print(f"Scan saved to {fname}")
    else:
        print("Scan returned no output or failed.")

def cmd_recon(args):
    out = recon.passive_recon(args.target)
    if out:
        fname = report.save_report(out, args.target)
        print(f"Recon saved to {fname}")
    else:
        print("Recon returned no output or failed.")

def main():
    parser = argparse.ArgumentParser(prog="dexa", description="Dexa CLI - Offensive Security Toolkit")
    sub = parser.add_subparsers(dest="command")

    p_scan = sub.add_parser("scan", help="Run nmap scan against target (ip or hostname)")
    p_scan.add_argument("target", help="Target IP/hostname to scan")
    p_scan.set_defaults(func=cmd_scan)

    p_recon = sub.add_parser("recon", help="Run passive recon (whois) for a domain")
    p_recon.add_argument("target", help="Domain to run whois on")
    p_recon.set_defaults(func=cmd_recon)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)

if __name__ == '__main__':
    main()
