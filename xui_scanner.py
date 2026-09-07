#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🔍 XUI SCANNER PRO v2.0 - 3X-UI Panel Detector 🔍             ║
║           Advanced IP Scanner for Finding Vulnerable 3X-UI Panels           ║
║                                                                              ║
║  Features:                                                                   ║
║  ✓ Multi-Port Scanning (2053, 443, 80, 8443, 2083, 81)                     ║
║  ✓ Bulk IP Support (CIDR, Range, List)                                      ║
║  ✓ Fast Multi-threaded Scanner                                              ║
║  ✓ 3X-UI Fingerprint Detection                                              ║
║  ✓ Version Detection                                                        ║
║  ✓ Vulnerability Assessment                                                 ║
║  ✓ Auto-Export to XUI Cracker Format                                        ║
║  ✓ Beautiful Real-time UI                                                    ║
║  ✓ Proxy Support                                                             ║
║                                                                              ║
║  Author: @mansorkorea84                                                      ║
║  License: MIT - Educational Purposes Only                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import threading
import sys
import json
import re
import time
import os
import socket
import ipaddress
import random
from urllib.parse import urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from queue import Queue
import argparse
import ssl

# ==================== CONFIGURATION ====================
VERSION = "2.0"
AUTHOR = "@mansorkorea84"

# 3X-UI Default Ports (in order of probability)
XUI_DEFAULT_PORTS = [2053, 443, 8443, 2083, 81, 8080, 8888, 9090, 3000, 5000]

# Scan Settings
DEFAULT_TIMEOUT = 5
MAX_THREADS = 100
CONNECTION_TIMEOUT = 3

# ==================== COLORS ====================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;206m'
    PURPLE = '\033[38;5;141m'
    END = '\033[0m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'

# ==================== USER AGENTS ====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

# ==================== 3X-UI FINGERPRINTS ====================
XUI_FINGERPRINTS = [
    # HTML indicators
    r'3x-ui|3xui|x-ui|xui',
    r'xray|Xray|XRAY',
    r'vless|vmess|trojan|shadowsocks',
    r'panel.*login|dashboard.*login',
    # Headers
    r'x-ui',
    # Page titles
    r'<title>.*[Xx][Uu][Ii].*</title>',
    r'<title>.*[Pp]anel.*</title>',
    # Specific paths
    r'/xui/|/panel/',
]

XUI_API_PATHS = ['/xui/panel/api/inbounds/list', '/login', '/xui/']

# ==================== DATA CLASSES ====================
@dataclass
class ScanTarget:
    """Represents a target to scan"""
    ip: str
    port: int
    protocol: str = "https"
    
    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.ip}:{self.port}"
    
    @property
    def key(self) -> str:
        return f"{self.ip}:{self.port}"

@dataclass
class PanelInfo:
    """Information about a found 3X-UI panel"""
    url: str
    ip: str
    port: int
    is_xui: bool = False
    version: Optional[str] = None
    title: Optional[str] = None
    server: Optional[str] = None
    has_csrf: bool = False
    csrf_token: Optional[str] = None
    response_time: float = 0.0
    status_code: int = 0
    vulnerabilities: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    headers: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'ip': self.ip,
            'port': self.port,
            'is_xui': self.is_xui,
            'version': self.version,
            'title': self.title,
            'server': self.server,
            'has_csrf': self.has_csrf,
            'response_time': round(self.response_time, 3),
            'status_code': self.status_code,
            'vulnerabilities': self.vulnerabilities,
            'endpoints': self.endpoints,
        }
    
    @property
    def for_cracker(self) -> str:
        """Format for XUI Cracker input"""
        return f"{self.ip}:{self.port}"

@dataclass
class ScanStats:
    """Scan statistics"""
    total_targets: int = 0
    scanned: int = 0
    found: int = 0
    up: int = 0
    down: int = 0
    errors: int = 0
    start_time: float = field(default_factory=time.time)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def increment(self, stat: str):
        with self._lock:
            if hasattr(self, stat):
                current = getattr(self, stat)
                setattr(self, stat, current + 1)
    
    def get_stats(self) -> dict:
        with self._lock:
            elapsed = time.time() - self.start_time
            return {
                'total': self.total_targets,
                'scanned': self.scanned,
                'found': self.found,
                'up': self.up,
                'down': self.down,
                'errors': self.errors,
                'elapsed': elapsed,
                'speed': self.scanned / elapsed if elapsed > 0 else 0,
                'progress': (self.scanned / self.total_targets * 100) if self.total_targets > 0 else 0
            }

# ==================== PROXY MANAGER ====================
class ProxyManager:
    """Manages proxy rotation"""
    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.index = 0
        self.lock = threading.Lock()
        
    def get(self) -> Optional[Dict]:
        with self.lock:
            if not self.proxies:
                return None
            proxy = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            if not proxy.startswith('http'):
                proxy = f'http://{proxy}'
            return {'http': proxy, 'https': proxy}
    
    @classmethod
    def from_file(cls, filename: str) -> 'ProxyManager':
        proxies = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)
        except:
            pass
        return cls(proxies)

# ==================== PORT SCANNER ====================
class PortScanner:
    """Fast TCP port scanner"""
    
    def __init__(self, timeout: float = CONNECTION_TIMEOUT):
        self.timeout = timeout
        
    def is_open(self, ip: str, port: int) -> bool:
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, ip: str, ports: List[int]) -> List[int]:
        """Scan multiple ports, return open ones"""
        open_ports = []
        for port in ports:
            if self.is_open(ip, port):
                open_ports.append(port)
        return open_ports

# ==================== 3X-UI DETECTOR ====================
class XUIDetector:
    """Detects and fingerprints 3X-UI panels"""
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT, proxy_manager: ProxyManager = None):
        self.timeout = timeout
        self.proxy_manager = proxy_manager
        self.session_cache = {}
        self.lock = threading.Lock()
        
    def _get_session(self, proxy: bool = True) -> requests.Session:
        """Get or create HTTP session"""
        thread_id = threading.current_thread().ident
        with self.lock:
            if thread_id not in self.session_cache:
                session = requests.Session()
                session.headers.update({
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                })
                if proxy and self.proxy_manager:
                    p = self.proxy_manager.get()
                    if p:
                        session.proxies.update(p)
                self.session_cache[thread_id] = session
            return self.session_cache[thread_id]
    
    def detect(self, target: ScanTarget) -> PanelInfo:
        """Detect if target is a 3X-UI panel"""
        info = PanelInfo(
            url=target.url,
            ip=target.ip,
            port=target.port
        )
        
        session = self._get_session()
        
        try:
            start_time = time.time()
            
            # Try HTTPS first, fallback to HTTP
            for protocol in ['https', 'http']:
                target.protocol = protocol
                url = target.url
                
                try:
                    if protocol == 'https':
                        response = session.get(
                            url + "/",
                            timeout=self.timeout,
                            verify=False,
                            allow_redirects=True,
                            headers={'Host': target.ip}
                        )
                    else:
                        response = session.get(
                            url + "/",
                            timeout=self.timeout,
                            allow_redirects=True,
                            headers={'Host': target.ip}
                        )
                    
                    info.response_time = time.time() - start_time
                    info.status_code = response.status_code
                    
                    # Store headers
                    info.headers = dict(response.headers)
                    
                    # Get server header
                    info.server = response.headers.get('Server', 'Unknown')
                    
                    # Check if port is open (any response means it's up)
                    if response.status_code in [200, 301, 302, 307, 401, 403, 500, 502, 503]:
                        info.up = True
                        
                        content = response.text.lower()
                        headers_str = str(response.headers).lower()
                        
                        # Extract title
                        title_match = re.search(r'<title>([^<]+)</title>', response.text, re.IGNORECASE)
                        if title_match:
                            info.title = title_match.group(1).strip()
                        
                        # Check for 3X-UI fingerprints
                        for pattern in XUI_FINGERPRINTS:
                            if re.search(pattern, content, re.IGNORECASE) or \
                               re.search(pattern, headers_str, re.IGNORECASE):
                                info.is_xui = True
                                break
                        
                        # Additional checks for 3X-UI
                        if not info.is_xui:
                            # Check specific paths
                            for path in XUI_API_PATHS:
                                try:
                                    check_url = url + path
                                    check_resp = session.get(
                                        check_url,
                                        timeout=3,
                                        verify=False,
                                        allow_redirects=False
                                    )
                                    if check_resp.status_code in [200, 301, 302, 401, 403]:
                                        info.endpoints.append(path)
                                        if path in ['/xui/', '/xui/panel/api/inbounds/list']:
                                            info.is_xui = True
                                except:
                                    pass
                        
                        # Try to extract CSRF token
                        csrf_patterns = [
                            r'name="csrf_token"\s+value="([^"]+)"',
                            r'csrf-token["\s:]+["\']?([^"\'>\s]+)',
                            r'x-csrf-token["\s:]+["\']?([^"\'>\s]+)',
                        ]
                        for pattern in csrf_patterns:
                            match = re.search(pattern, response.text, re.IGNORECASE)
                            if match:
                                info.csrf_token = match.group(1)
                                info.has_csrf = True
                                break
                        
                        # Try to extract version
                        version_patterns = [
                            r'version["\s:]+(["\']?)([0-9]+\.[0-9]+[^\1]*?)\1',
                            r'v([0-9]+\.[0-9]+\.[0-9]+)',
                            r'Version:\s*([0-9.]+)',
                        ]
                        for pattern in version_patterns:
                            match = re.search(pattern, response.text, re.IGNORECASE)
                            if match:
                                info.version = match.group(2) if match.lastindex >= 2 else match.group(1)
                                break
                        
                        # Check vulnerabilities
                        self._check_vulnerabilities(info, response)
                        
                        # If we got a response, no need to try other protocol
                        break
                        
                except requests.exceptions.SSLError:
                    # SSL error, try HTTP
                    continue
                except requests.exceptions.ConnectionError:
                    continue
                except Exception as e:
                    continue
                    
        except Exception as e:
            info.error = str(e)
            
        return info
    
    def _check_vulnerabilities(self, info: PanelInfo, response: requests.Response):
        """Check for common vulnerabilities"""
        vulns = []
        
        # Missing security headers
        security_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options (Clickjacking possible)',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options',
            'Strict-Transport-Security': 'Missing HSTS header',
            'Content-Security-Policy': 'Missing CSP header',
            'X-XSS-Protection': 'Missing XSS Protection',
        }
        
        for header, msg in security_headers.items():
            if header not in response.headers:
                vulns.append(msg.split('(')[0].strip())
        
        # Server version disclosure
        server = response.headers.get('Server', '')
        if server and server != 'Unknown':
            if any(v in server.lower() for v in ['nginx/', 'apache/', 'cloudflare']):
                vulns.append(f'Server: {server}')
        
        # Debug info
        if 'debug' in response.text.lower() or 'stack trace' in response.text.lower():
            vulns.append('Debug info disclosure')
        
        # Default credentials indicator
        if info.is_xui:
            vulns.append('Potential default creds')
        
        info.vulnerabilities = vulns

# ==================== MAIN SCANNER CLASS ====================
class XUIScannerPro:
    """Main scanner application"""
    
    def __init__(self):
        self.stats = ScanStats()
        self.found_panels: List[PanelInfo] = []
        self.detector = XUIDetector()
        self.port_scanner = PortScanner()
        self.proxy_manager: Optional[ProxyManager] = None
        self.stop_event = threading.Event()
        self.found_lock = threading.Lock()
        
    def set_proxy_manager(self, manager: ProxyManager):
        self.proxy_manager = manager
        self.detector.proxy_manager = manager
        
    def parse_targets(self, input_data: str) -> List[ScanTarget]:
        """Parse various input formats into targets"""
        targets = []
        lines = input_data.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # IP:PORT format (most common)
            if ':' in line and '/' not in line:
                parts = line.rsplit(':', 1)
                ip = parts[0].strip()
                try:
                    port = int(parts[1].strip())
                    targets.append(ScanTarget(ip=ip, port=port))
                except ValueError:
                    # Might be IPv6 or invalid, skip
                    continue
                    
            # URL format
            elif line.startswith('http://') or line.startswith('https://'):
                try:
                    parsed = urlparse(line)
                    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                    targets.append(ScanTarget(
                        ip=parsed.hostname or '',
                        port=port,
                        protocol=parsed.scheme
                    ))
                except:
                    continue
                    
            # CIDR notation
            elif '/' in line:
                try:
                    network = ipaddress.ip_network(line, strict=False)
                    for ip in network.hosts():
                        for port in XUI_DEFAULT_PORTS[:3]:  # Only scan top 3 ports for CIDR
                            targets.append(ScanTarget(ip=str(ip), port=port))
                except:
                    continue
                    
            # Plain IP (scan all default ports)
            else:
                try:
                    ipaddress.ip_address(line)  # Validate IP
                    for port in XUI_DEFAULT_PORTS:
                        targets.append(ScanTarget(ip=line, port=port))
                except:
                    continue
                    
        return targets
    
    def load_from_file(self, filename: str) -> List[ScanTarget]:
        """Load targets from file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return self.parse_targets(content)
        except FileNotFoundError:
            print(f"{Colors.RED}[-] File not found: {filename}{Colors.END}")
            return []
        except Exception as e:
            print(f"{Colors.RED}[-] Error loading file: {e}{Colors.END}")
            return []
    
    def scan_target(self, target: ScanTarget) -> Optional[PanelInfo]:
        """Scan a single target"""
        if self.stop_event.is_set():
            return None
            
        self.stats.increment('scanned')
        
        # Quick port check first
        if not self.port_scanner.is_open(target.ip, target.port):
            self.stats.increment('down')
            return None
            
        self.stats.increment('up')
        
        # Full detection
        info = self.detector.detect(target)
        
        if info.is_xui:
            self.stats.increment('found')
            with self.found_lock:
                self.found_panels.append(info)
            self._print_found(info)
            
        return info
    
    def scan_batch(self, targets: List[ScanTarget], threads: int = 50) -> List[PanelInfo]:
        """Scan multiple targets with progress"""
        self.stats.total_targets = len(targets)
        self.found_panels = []
        self.stats = ScanStats(total_targets=len(targets))
        self.stop_event.clear()
        
        print(f"\n{Colors.CYAN}[*] Starting scan of {len(targets)} targets on {threads} threads...{Colors.END}")
        print(f"{Colors.CYAN}[*] Scanning ports: {', '.join(map(str, set(t.port for t in targets[:10])))}...{Colors.END}\n")
        
        # Start stats display thread
        def show_stats():
            while not self.stop_event.is_set():
                self._display_stats()
                time.sleep(0.5)
        
        stats_thread = threading.Thread(target=show_stats, daemon=True)
        stats_thread.start()
        
        try:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = {executor.submit(self.scan_target, t): t for t in targets}
                
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    try:
                        future.result()
                    except Exception as e:
                        self.stats.increment('errors')
                        
        except KeyboardInterrupt:
            self.stop_event.set()
            print(f"\n\n{Colors.YELLOW}[!] Scan interrupted!{Colors.END}")
        finally:
            self.stop_event.set()
            time.sleep(0.5)
            self._display_stats(final=True)
            
        return self.found_panels
    
    def quick_scan(self, ips: List[str], ports: List[int] = None, threads: int = 50) -> List[PanelInfo]:
        """Quick scan of IPs on specified ports"""
        if ports is None:
            ports = [2053]  # Default 3X-UI port
            
        targets = []
        for ip in ips:
            ip = ip.strip()
            if ip and not ip.startswith('#'):
                for port in ports:
                    targets.append(ScanTarget(ip=ip, port=port))
                    
        return self.scan_batch(targets, threads)
    
    def smart_scan(self, ips: List[str], threads: int = 50) -> List[PanelInfo]:
        """Smart scan - tries default port first, then others if open"""
        targets = []
        for ip in ips:
            ip = ip.strip()
            if ip and not ip.startswith('#'):
                # Always try 2053 first (most common)
                targets.append(ScanTarget(ip=ip, port=2053))
                
        return self.scan_batch(targets, threads)
    
    def _display_stats(self, final: bool = False):
        """Display scan statistics"""
        os.system('cls' if os.name == 'nt' else 'clear')
        self._print_banner()
        
        s = self.stats.get_stats()
        
        print(f"{Colors.BLUE}╔═══════════════════════════════════════════════════════════════════════════╗")
        print(f"{Colors.BLUE}║{Colors.YELLOW}  🔍 XUI SCANNER PRO - LIVE STATISTICS{Colors.BLUE}                                        ║")
        print(f"{Colors.BLUE}╠═══════════════════════════════════════════════════════════════════════════╣")
        print(f"{Colors.BLUE}║{Colors.CYAN}  📊 Total Targets   : {Colors.WHITE}{str(s['total']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.CYAN}  ✅ Scanned         : {Colors.WHITE}{str(s['scanned']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.GREEN}  🎯 3X-UI Found     : {Colors.GREEN}{str(s['found']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.CYAN}  🟢 Hosts Up        : {Colors.WHITE}{str(s['up']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.RED}  🔴 Hosts Down      : {Colors.RED}{str(s['down']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.ORANGE}  💥 Errors          : {Colors.ORANGE}{str(s['errors']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}╠═══════════════════════════════════════════════════════════════════════════╣")
        
        # Progress bar
        progress = s['progress']
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"{Colors.BLUE}║{Colors.PURPLE}  📈 Progress        : {Colors.CYAN}[{bar}] {Colors.WHITE}{progress:.1f}%{' ' * (25 - len(str(int(progress))))}{Colors.BLUE}║")
        
        # Speed and time
        elapsed_min = int(s['elapsed'] // 60)
        elapsed_sec = int(s['elapsed'] % 60)
        print(f"{Colors.BLUE}║{Colors.PURPLE}  ⏱️  Elapsed Time    : {Colors.WHITE}{elapsed_min}m {elapsed_sec}s{' ' * (43 - len(str(elapsed_min)) - len(str(elapsed_sec)))}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.PURPLE}  ⚡ Speed           : {Colors.WHITE}{s['speed']:.1f} targets/sec{' ' * (34 - len(str(int(s['speed']))))}{Colors.BLUE}║")
        print(f"{Colors.BLUE}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.END}")
        
        if final:
            print(f"\n{Colors.GREEN}[+] Scan Complete! Found {s['found']} 3X-UI panels.{Colors.END}")
    
    def _print_found(self, info: PanelInfo):
        """Print found panel info"""
        print(f"\n{Colors.BG_GREEN}{Colors.BLACK}  🎯 3X-UI PANEL FOUND!  {Colors.END}")
        print(f"{Colors.GREEN}  ┌────────────────────────────────────────────────────┐")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  URL       : {Colors.WHITE}{info.url:<38}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  IP:PORT   : {Colors.WHITE}{info.ip}:{info.port:<33}{Colors.GREEN}│")
        if info.version:
            print(f"{Colors.GREEN}  │{Colors.CYAN}  Version   : {Colors.WHITE}{info.version:<38}{Colors.GREEN}│")
        if info.title:
            print(f"{Colors.GREEN}  │{Colors.CYAN}  Title     : {Colors.WHITE}{info.title[:38]:<38}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Response  : {Colors.WHITE}{info.status_code} ({info.response_time:.2f}s){' ' * (26 - len(str(info.status_code)) - len(f'{info.response_time:.2f}'))}{Colors.GREEN}│")
        if info.vulnerabilities:
            vuln_str = ', '.join(info.vulnerabilities[:2])
            print(f"{Colors.GREEN}  │{Colors.YELLOW}  Issues    : {Colors.WHITE}{vuln_str[:38]:<38}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  └────────────────────────────────────────────────────┘{Colors.END}")
    
    def _print_banner(self):
        """Print banner"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                                              ║
{Colors.RED}║{Colors.CYAN}   ███████╗ █████╗ ██╗   ██╗███████╗ ██████╗  ██████╗ ██████╗  {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ██╔════╝██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   █████╗  ███████║██║   ██║█████╗  ██║   ██║██║   ██║██║  ██║ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ██╔══╝  ██╔══██║██║   ██║██╔══╝  ██║   ██║██║   ██║██║  ██║ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ███████╗██║  ██║╚██████╔╝███████║╚██████╔╝╚██████╔╝██████╔╝ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝  {Colors.RED}║
{Colors.RED}║                                                                              ║
{Colors.RED}╠══════════════════════════════════════════════════════════════════════════════╣
{Colors.RED}║{Colors.GREEN}          🔍 XUI SCANNER PRO v{VERSION} 🔍                                  {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}               Advanced 3X-UI Panel Detector                             {Colors.RED}║
{Colors.RED}║{Colors.MAGENTA}                       Author: {AUTHOR}                                   {Colors.RED}║
{Colors.RED}║{Colors.CYAN}                          [{now}]                                  {Colors.RED}║
{Colors.RED}╚══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
    
    def save_results(self, filename: str = None):
        """Save scan results to files"""
        if not self.found_panels:
            print(f"{Colors.YELLOW}[!] No panels found to save.{Colors.END}")
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = filename or f"xui_scan_{timestamp}.json"
        data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'scanner_version': VERSION,
            'total_found': len(self.found_panels),
            'panels': [p.to_dict() for p in self.found_panels]
        }
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}[+] JSON saved: {json_file}{Colors.END}")
        
        # Save TXT (for XUI Cracker)
        txt_file = f"xui_panels_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"# XUI Scanner Pro v{VERSION}\n")
            f.write(f"# Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total Found: {len(self.found_panels)}\n")
            f.write("#" + "=" * 70 + "\n\n")
            for panel in self.found_panels:
                f.write(f"{panel.for_cracker}\n")
        print(f"{Colors.GREEN}[+] Panels list saved: {txt_file}{Colors.END}")
        print(f"{Colors.CYAN}[*] Use this file with XUI Cracker: python3 xui_cracker.py --targets {txt_file}{Colors.END}")
        
        # Save detailed report
        report_file = f"xui_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("XUI SCANNER PRO - DETAILED REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Panels Found: {len(self.found_panels)}\n\n")
            
            for i, panel in enumerate(self.found_panels, 1):
                f.write("-" * 80 + "\n")
                f.write(f"PANEL #{i}\n")
                f.write("-" * 80 + "\n")
                f.write(f"URL: {panel.url}\n")
                f.write(f"IP:Port: {panel.ip}:{panel.port}\n")
                if panel.version:
                    f.write(f"Version: {panel.version}\n")
                if panel.title:
                    f.write(f"Title: {panel.title}\n")
                f.write(f"Response Time: {panel.response_time:.3f}s\n")
                f.write(f"Status Code: {panel.status_code}\n")
                if panel.vulnerabilities:
                    f.write(f"Vulnerabilities:\n")
                    for v in panel.vulnerabilities:
                        f.write(f"  - {v}\n")
                if panel.endpoints:
                    f.write(f"Endpoints: {', '.join(panel.endpoints)}\n")
                f.write("\n")
                
        print(f"{GREEN}[+] Detailed report saved: {report_file}{Colors.END}")
        
        return json_file, txt_file, report_file
    
    def run_interactive(self):
        """Run interactive mode"""
        while True:
            self._print_banner()
            
            menu = f"""
{Colors.CYAN}┌─────────────────────────────────────────────────────────────────────┐
{Colors.CYAN}│{Colors.YELLOW}                         SCAN MODES                                 {Colors.CYAN}│
{Colors.CYAN}├─────────────────────────────────────────────────────────────────────┤
{Colors.CYAN}│                                                                     │
{Colors.CYAN}│{Colors.GREEN}  [1]{Colors.WHITE} Quick Scan (Port 2053)   {Colors.DIM}- Fastest, most common port    {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [2]{Colors.WHITE} Full Port Scan         {Colors.DIM}- All common 3X-UI ports       {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [3]{Colors.WHITE} Smart Scan             {Colors.DIM}- Auto-detect best approach   {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [4]{Colors.WHITE} Custom Ports Scan      {Colors.DIM}- Specify custom ports         {Colors.CYAN}│
{Colors.CYAN}│                                                                     │
{Colors.CYAN}├─────────────────────────────────────────────────────────────────────┤
{Colors.CYAN}│{Colors.YELLOW}  [0] Exit                                                             {Colors.CYAN}│
{Colors.CYAN}└─────────────────────────────────────────────────────────────────────┘{Colors.END}

{Colors.CYAN}[?] Select Mode: {Colors.END}"""
            
            choice = input().strip()
            
            if choice == '0':
                print(f"{Colors.CYAN}[*] Goodbye! 👋{Colors.END}")
                break
                
            elif choice == '1':
                self._mode_quick_scan()
            elif choice == '2':
                self._mode_full_scan()
            elif choice == '3':
                self._mode_smart_scan()
            elif choice == '4':
                self._mode_custom_scan()
            else:
                print(f"{Colors.RED}[-] Invalid choice!{Colors.END}")
                time.sleep(1)
                
            if choice in ['1', '2', '3', '4']:
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
    
    def _mode_quick_scan(self):
        """Quick scan mode - only port 2053"""
        self._print_banner()
        
        ip_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file or IPs (one per line, paste end with empty line): {Colors.END}").strip()
        
        if os.path.isfile(ip_input):
            ips = load_ip_list(ip_input)
        else:
            # Read from stdin
            ips = []
            while True:
                line = input()
                if not line.strip():
                    break
                ips.append(line.strip())
        
        if not ips:
            print(f"{Colors.RED}[-] No IPs provided!{Colors.END}")
            return
            
        threads = input(f"{Colors.CYAN}[?] {Colors.WHITE}Threads (default 50): {Colors.END}").strip()
        try:
            threads = min(100, max(1, int(threads))) if threads else 50
        except:
            threads = 50
            
        found = self.quick_scan(ips, ports=[2053], threads=threads)
        
        if found:
            self.save_results()
    
    def _mode_full_scan(self):
        """Full port scan mode"""
        self._print_banner()
        
        ip_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file or IPs: {Colors.END}").strip()
        
        if os.path.isfile(ip_input):
            ips = load_ip_list(ip_input)
        else:
            ips = [ip_input]
            
        if not ips:
            print(f"{Colors.RED}[-] No IPs provided!{Colors.END}")
            return
            
        threads = input(f"{Colors.CYAN}[?] {Colors.WHITE}Threads (default 30): {Colors.END}").strip()
        try:
            threads = min(100, max(1, int(threads))) if threads else 30
        except:
            threads = 30
            
        # Create targets for all default ports
        targets = []
        for ip in ips:
            for port in XUI_DEFAULT_PORTS:
                targets.append(ScanTarget(ip=ip, port=port))
                
        found = self.scan_batch(targets, threads)
        
        if found:
            self.save_results()
    
    def _mode_smart_scan(self):
        """Smart scan mode"""
        self._print_banner()
        
        ip_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file or IPs: {Colors.END}").strip()
        
        if os.path.isfile(ip_input):
            ips = load_ip_list(ip_input)
        else:
            ips = [ip_input]
            
        if not ips:
            print(f"{Colors.RED}[-] No IPs provided!{Colors.END}")
            return
            
        threads = input(f"{Colors.CYAN}[?] {Colors.WHITE}Threads (default 50): {Colors.END}").strip()
        try:
            threads = min(100, max(1, int(threads))) if threads else 50
        except:
            threads = 50
            
        found = self.smart_scan(ips, threads)
        
        if found:
            self.save_results()
    
    def _mode_custom_scan(self):
        """Custom port scan mode"""
        self._print_banner()
        
        ip_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file or IPs: {Colors.END}").strip()
        ports_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}Ports (comma-separated, e.g., 2053,443,8443): {Colors.END}").strip()
        
        if os.path.isfile(ip_input):
            ips = load_ip_list(ip_input)
        else:
            ips = [ip_input]
            
        # Parse ports
        ports = []
        for p in ports_input.split(','):
            p = p.strip()
            try:
                ports.append(int(p))
            except:
                continue
                
        if not ips or not ports:
            print(f"{Colors.RED}[-] Invalid input!{Colors.END}")
            return
            
        threads = input(f"{Colors.CYAN}[?] {Colors.WHITE}Threads (default 50): {Colors.END}").strip()
        try:
            threads = min(100, max(1, int(threads))) if threads else 50
        except:
            threads = 50
            
        found = self.quick_scan(ips, ports=ports, threads=threads)
        
        if found:
            self.save_results()

# ==================== UTILITY FUNCTIONS ====================
def load_ip_list(filename: str) -> List[str]:
    """Load IP list from file"""
    ips = []
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ips.append(line)
    except Exception as e:
        print(f"{Colors.RED}[-] Error loading {filename}: {e}{Colors.END}")
    return ips

# ==================== CLI INTERFACE ====================
def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description=f'XUI Scanner Pro v{VERSION} - Advanced 3X-UI Panel Detector',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xui_scanner.py                          # Interactive mode
  python xui_scanner.py --scan ips.txt            # Quick scan (port 2053)
  python xui_scanner.py --full-scan ips.txt      # Full port scan
  python xui_scanner.py --ports 2053,443,8443 ips.txt  # Custom ports
  python xui_scanner.py --smart-scan ips.txt      # Smart auto-detect
        """
    )
    
    parser.add_argument('--scan', '-s', help='Quick scan IP file (port 2053)')
    parser.add_argument('--full-scan', '-f', help='Full port scan IP file')
    parser.add_argument('--smart-scan', help='Smart scan IP file')
    parser.add_argument('--ports', '-p', help='Comma-separated ports for custom scan')
    parser.add_argument('--threads', '-t', type=int, default=50, help='Thread count (default: 50)')
    parser.add_argument('--output', '-o', help='Output file prefix')
    parser.add_argument('--proxy-file', help='Proxy list file')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='Request timeout')
    
    args = parser.parse_args()
    
    # Interactive mode if no args
    if len(sys.argv) == 1:
        scanner = XUIScannerPro()
        scanner.run_interactive()
        return
    
    # CLI mode
    scanner = XUIScannerPro()
    scanner.detector.timeout = args.timeout
    
    # Load proxies
    if args.proxy_file:
        scanner.set_proxy_manager(ProxyManager.from_file(args.proxy_file))
    
    try:
        if args.scan:
            ips = load_ip_list(args.scan)
            found = scanner.quick_scan(ips, threads=args.threads)
            
        elif args.full_scan:
            ips = load_ip_list(args.full_scan)
            targets = []
            for ip in ips:
                for port in XUI_DEFAULT_PORTS:
                    targets.append(ScanTarget(ip=ip, port=port))
            found = scanner.scan_batch(targets, args.threads)
            
        elif args.smart_scan:
            ips = load_ip_list(args.smart_scan)
            found = scanner.smart_scan(ips, args.threads)
            
        elif args.ports and len(sys.argv) > 1:
            # Need IPs from positional arg
            if not args.scan:
                print(f"{Colors.RED}[-] IP file required for custom port scan{Colors.END}")
                return
            ips = load_ip_list(args.scan)
            ports = [int(p.strip()) for p in args.ports.split(',')]
            found = scanner.quick_scan(ips, ports=ports, threads=args.threads)
            
        else:
            print(f"{Colors.RED}[-] No scan mode specified{Colors.END}")
            return
            
        # Save results
        if found:
            scanner.save_results(args.output)
            
        print(f"\n{Colors.GREEN}[+] Done! Found {len(found)} 3X-UI panels.{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {e}{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Exited by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[-] Fatal error: {e}{Colors.END}")
