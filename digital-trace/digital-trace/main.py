#!/usr/bin/env python3
# main.py — DigitalTrace CLI
"""
DigitalTrace — Digital Footprint Investigation System
For authorized security research and educational use only.

Usage:
  python main.py --username johndoe
  python main.py --domain example.com
  python main.py --ip 8.8.8.8
  python main.py --email user@example.com
  python main.py --dorks example.com
  python main.py --username johndoe --domain example.com --report
  python main.py --dashboard
"""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.logger import get_logger
from utils.validator import sanitize_input

logger = get_logger("main")

BANNER = """
╔══════════════════════════════════════════════════════╗
║          DigitalTrace — OSINT Investigation          ║
║      For authorized / educational use only ⚠        ║
╚══════════════════════════════════════════════════════╝
"""

def confirm_authorization() -> bool:
    print("\n⚠  ETHICS CHECK")
    print("   You must have authorization to investigate this target.")
    print("   Unauthorized OSINT on real individuals may be illegal.\n")
    ans = input("   Do you have authorization? (yes/no): ").strip().lower()
    return ans == "yes"

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="DigitalTrace OSINT Tool")
    parser.add_argument("--username",  help="Username to check across platforms")
    parser.add_argument("--domain",    help="Domain for WHOIS lookup")
    parser.add_argument("--ip",        help="IP address to look up")
    parser.add_argument("--email",     help="Email address to check for breaches")
    parser.add_argument("--dorks",     help="Target for Google dork generation")
    parser.add_argument("--metadata",  help="Path to file for metadata extraction")
    parser.add_argument("--report",    action="store_true", help="Generate HTML report")
    parser.add_argument("--dashboard", action="store_true", help="Launch web dashboard")
    parser.add_argument("--yes",       action="store_true", help="Skip authorization prompt")
    args = parser.parse_args()

    # Launch dashboard mode
    if args.dashboard:
        from dashboard.app import app
        from config.settings import FLASK_HOST, FLASK_PORT
        print(f"🌐 Starting dashboard at http://{FLASK_HOST}:{FLASK_PORT}")
        app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False)
        return

    # Require at least one action
    if not any([args.username, args.domain, args.ip, args.email, args.dorks, args.metadata]):
        parser.print_help()
        return

    # Authorization gate
    if not args.yes and not confirm_authorization():
        print("\n❌ Aborted. Always obtain proper authorization before investigating.\n")
        sys.exit(0)

    findings = {}
    target_label = args.username or args.domain or args.ip or args.email or "target"

    # --- Username check ---
    if args.username:
        from core.username_checker import check_username
        username = sanitize_input(args.username)
        results = check_username(username)
        findings["username"] = results
        found = [r for r in results if r["found"]]
        print(f"\n✅ Username '{username}' found on {len(found)}/{len(results)} platforms")

    # --- WHOIS ---
    if args.domain:
        from modules.whois_lookup import whois_lookup
        domain = sanitize_input(args.domain)
        data = whois_lookup(domain)
        findings["whois"] = data
        if "error" not in data:
            print(f"\n🌐 WHOIS for {domain}:")
            for k, v in data.items():
                if v:
                    print(f"   {k:<20} {v}")

    # --- IP lookup ---
    if args.ip:
        from modules.ipinfo_lookup import ip_lookup
        ip = sanitize_input(args.ip)
        data = ip_lookup(ip)
        findings["ip"] = data
        if "error" not in data:
            print(f"\n📡 IP Info for {ip}:")
            for k, v in data.items():
                if v:
                    print(f"   {k:<15} {v}")

    # --- Breach check ---
    if args.email:
        from modules.haveibeenpwned import check_email_breach
        email = sanitize_input(args.email)
        data = check_email_breach(email)
        findings["breach"] = data
        if "error" in data:
            print(f"\n⚠  Breach check: {data['error']}")
        elif data.get("breached"):
            print(f"\n🚨 {email} found in {data['breach_count']} breach(es)!")
            for b in data["breaches"]:
                print(f"   - {b['name']} ({b['breach_date']}): {', '.join(b['data_types'])}")
        else:
            print(f"\n✅ {email} not found in any known breaches.")

    # --- Dork generator ---
    if args.dorks:
        from core.dork_generator import print_dorks, generate_dorks
        target = sanitize_input(args.dorks)
        print_dorks(target)
        findings["dorks"] = generate_dorks(target)

    # --- Metadata ---
    if args.metadata:
        from core.metadata_extractor import extract_metadata
        data = extract_metadata(args.metadata)
        findings["metadata"] = data
        if "error" not in data:
            print(f"\n📄 Metadata for {args.metadata}:")
            for k, v in data.items():
                print(f"   {k:<30} {v}")

    # --- Report ---
    if args.report and findings:
        from core.report_builder import build_report
        path = build_report(target_label, findings)
        print(f"\n📊 Report saved: {path}")
        print(f"   Open it in your browser to view results.\n")

if __name__ == "__main__":
    main()
