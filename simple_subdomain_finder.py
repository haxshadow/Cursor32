#!/usr/bin/env python3
"""
Simple Subdomain Discovery Tool (Minimal Edition)
===============================================
এটি একটি সরল subdomain enumeration tool যা minimal dependencies দিয়ে কাজ করে।
শুধুমাত্র Python built-in modules ব্যবহার করে।

Features:
- Basic DNS bruteforce
- Certificate Transparency search
- Simple wordlist support
- Basic HTTP verification
- Text output format
"""

import json
import re
import threading
import time
import socket
import argparse
import sys
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv
from datetime import datetime
import logging
from collections import defaultdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Colors:
    """Terminal color codes"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SimpleSubdomainFinder:
    def __init__(self, domain, threads=50, timeout=10, output_dir=None):
        self.domain = domain.lower().strip()
        self.threads = min(threads, 100)  # Limit threads
        self.timeout = max(timeout, 5)    # Minimum timeout
        self.found_subdomains = set()
        self.live_subdomains = set()
        self.scanned_subdomains = set()
        self.progress = 0
        self.total_tasks = 0
        self.start_time = time.time()
        
        # Statistics
        self.stats = {
            'dns_queries': 0,
            'http_requests': 0,
            'ct_queries': 0,
            'errors': defaultdict(int),
            'start_time': self.start_time
        }
        
        # Setup output directory
        self.output_dir = Path(output_dir) if output_dir else Path(f"results_{domain}")
        try:
            self.output_dir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            logger.error(f"Could not create output directory: {e}")
            self.output_dir = Path(".")

    def print_banner(self):
        """Tool banner প্রিন্ট করে"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║              SIMPLE SUBDOMAIN FINDER                          ║
    ║              Minimal Dependencies Edition                     ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.YELLOW}Target Domain: {Colors.GREEN}{self.domain}{Colors.END}
{Colors.YELLOW}Threads: {Colors.GREEN}{self.threads}{Colors.END}
{Colors.YELLOW}Timeout: {Colors.GREEN}{self.timeout}s{Colors.END}
{Colors.YELLOW}Output Dir: {Colors.GREEN}{self.output_dir}{Colors.END}
"""
        print(banner)

    def load_wordlist(self, wordlist_file=None):
        """Load wordlist from file or generate default"""
        if wordlist_file and Path(wordlist_file).exists():
            try:
                logger.info(f"Loading wordlist from {wordlist_file}")
                with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                    wordlist = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                logger.info(f"Loaded {len(wordlist)} words from file")
                return wordlist
            except Exception as e:
                logger.error(f"Error loading wordlist file: {e}")
                
        # Default wordlist
        logger.info("Using default wordlist")
        return [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2',
            'cpanel', 'whm', 'autodiscover', 'autoconfig', 'ns3', 'm', 'imap', 'test', 'ns', 'blog',
            'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns4', 'mail2', 'new', 'mysql',
            'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql',
            'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img',
            'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1',
            'ns5', 'upload', 'client', 'bb', 'chat', 'irc', 'live', 'search', 'ftp2',
            'archive', 'mc', 'herald', 'gis', 'monitor', 'login', 'backup', 'alerts', 'admin2',
            'panel', 'server', 'ns6', 'staging', 'app', 'git', 'svn', 'help', 'jenkins', 'ftp',
            'mailadmin', 'databases', 'ssh', 'postgres', 'phpmyadmin', 'admins', 'cpanelwebmail',
            'control', 'webmaster', 'mail1', 'server1', 'ns7', 'direct', 'mailman', 'development'
        ]

    def dns_lookup(self, subdomain):
        """Simple DNS lookup using socket"""
        if subdomain in self.scanned_subdomains:
            return False
            
        self.scanned_subdomains.add(subdomain)
        full_domain = f"{subdomain}.{self.domain}"
        
        try:
            # Simple DNS resolution using socket
            socket.gethostbyname(full_domain)
            self.found_subdomains.add(full_domain)
            self.stats['dns_queries'] += 1
            logger.info(f"Found subdomain: {full_domain}")
            print(f"{Colors.GREEN}[+] Found: {full_domain}{Colors.END}")
            return True
        except socket.gaierror:
            # DNS resolution failed
            pass
        except Exception as e:
            self.stats['errors']['dns'] += 1
            logger.error(f"DNS lookup error for {full_domain}: {e}")
        
        return False

    def run_dns_bruteforce(self, wordlist_file=None):
        """Multi-threaded DNS bruteforce"""
        logger.info(f"Starting DNS bruteforce with {self.threads} threads...")
        print(f"{Colors.YELLOW}[*] Starting DNS bruteforce with {self.threads} threads...{Colors.END}")
        
        wordlist = self.load_wordlist(wordlist_file)
        self.total_tasks += len(wordlist)
        logger.info(f"Using {len(wordlist)} words in wordlist")
        print(f"{Colors.YELLOW}[*] Using {len(wordlist)} words in wordlist{Colors.END}")
        
        try:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                futures = [executor.submit(self.dns_lookup, word) for word in wordlist]
                for future in as_completed(futures):
                    self.progress += 1
                    if self.progress % 50 == 0:
                        self.print_progress()
        except Exception as e:
            logger.error(f"DNS bruteforce error: {e}")

    def certificate_transparency(self):
        """Search Certificate Transparency logs"""
        logger.info("Searching Certificate Transparency logs...")
        print(f"{Colors.YELLOW}[*] Searching Certificate Transparency logs...{Colors.END}")
        
        ct_url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        
        try:
            # Create request with proper headers
            req = urllib.request.Request(
                ct_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.stats['ct_queries'] += 1
                
                if isinstance(data, list):
                    for cert in data:
                        if 'name_value' in cert:
                            domains = cert['name_value'].split('\n')
                            for domain in domains:
                                domain = domain.strip().lower()
                                if (domain.endswith(f".{self.domain}") and 
                                    domain not in self.found_subdomains and
                                    '*' not in domain):
                                    self.found_subdomains.add(domain)
                                    logger.info(f"CT Log found: {domain}")
                                    print(f"{Colors.GREEN}[+] CT Log: {domain}{Colors.END}")
                                    
        except Exception as e:
            self.stats['errors']['ct'] += 1
            logger.error(f"CT search error: {e}")
            print(f"{Colors.RED}[!] CT search error: {e}{Colors.END}")

    def verify_live_subdomains(self):
        """Check if subdomains are live via HTTP"""
        logger.info("Verifying live subdomains...")
        print(f"{Colors.YELLOW}[*] Verifying live subdomains...{Colors.END}")
        
        def check_live(subdomain):
            try:
                for protocol in ['https', 'http']:
                    try:
                        url = f"{protocol}://{subdomain}"
                        req = urllib.request.Request(
                            url,
                            headers={
                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                            }
                        )
                        
                        with urllib.request.urlopen(req, timeout=self.timeout) as response:
                            self.stats['http_requests'] += 1
                            if response.getcode() < 400:
                                self.live_subdomains.add(subdomain)
                                logger.info(f"Live subdomain: {url} [{response.getcode()}]")
                                print(f"{Colors.GREEN}[+] Live: {url} [{response.getcode()}]{Colors.END}")
                                return True
                    except Exception:
                        continue
                        
            except Exception as e:
                self.stats['errors']['live_check'] += 1
                logger.error(f"Live check error for {subdomain}: {e}")
            
            return False
        
        if self.found_subdomains:
            self.total_tasks += len(self.found_subdomains)
            try:
                with ThreadPoolExecutor(max_workers=min(self.threads, 20)) as executor:
                    futures = [executor.submit(check_live, subdomain) for subdomain in self.found_subdomains]
                    for future in as_completed(futures):
                        self.progress += 1
                        if self.progress % 10 == 0:
                            self.print_progress()
            except Exception as e:
                logger.error(f"Live verification error: {e}")

    def print_progress(self):
        """Print current progress"""
        elapsed = time.time() - self.start_time
        progress_percent = (self.progress / self.total_tasks) * 100 if self.total_tasks > 0 else 0
        
        progress_msg = (f"Progress: {self.progress}/{self.total_tasks} ({progress_percent:.1f}%) - "
                       f"Elapsed: {elapsed:.1f}s - Found: {len(self.found_subdomains)}")
        
        logger.info(progress_msg)
        print(f"{Colors.BLUE}[*] {progress_msg}{Colors.END}")

    def save_results(self, filename=None):
        """Save results in multiple formats"""
        if not filename:
            filename = f"{self.domain}_subdomains"
        
        try:
            # Text format
            txt_file = self.output_dir / f"{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"# Simple Subdomain Discovery Results for {self.domain}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n")
                f.write(f"# Total Found: {len(self.found_subdomains)}\n")
                f.write(f"# Live Subdomains: {len(self.live_subdomains)}\n\n")
                
                f.write("## All Subdomains:\n")
                for subdomain in sorted(self.found_subdomains):
                    f.write(f"{subdomain}\n")
                
                f.write("\n## Live Subdomains:\n")
                for subdomain in sorted(self.live_subdomains):
                    f.write(f"{subdomain}\n")
            
            # CSV format
            csv_file = self.output_dir / f"{filename}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Subdomain', 'Status'])
                
                for subdomain in sorted(self.found_subdomains):
                    status = "Live" if subdomain in self.live_subdomains else "DNS Only"
                    writer.writerow([subdomain, status])
            
            # JSON format
            json_file = self.output_dir / f"{filename}.json"
            results = {
                'domain': self.domain,
                'scan_info': {
                    'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration': time.time() - self.start_time,
                    'threads': self.threads,
                    'timeout': self.timeout
                },
                'statistics': dict(self.stats),
                'results': {
                    'total_subdomains': len(self.found_subdomains),
                    'live_subdomains': len(self.live_subdomains)
                },
                'subdomains': {
                    'all': sorted(self.found_subdomains),
                    'live': sorted(self.live_subdomains)
                }
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {txt_file}, {csv_file}, {json_file}")
            print(f"{Colors.GREEN}[+] Results saved to:{Colors.END}")
            print(f"    - Text: {txt_file}")
            print(f"    - CSV: {csv_file}")
            print(f"    - JSON: {json_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            print(f"{Colors.RED}[!] Error saving results: {e}{Colors.END}")

    def print_summary(self):
        """Print final summary"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}=" * 60)
        print("                    DISCOVERY SUMMARY")
        print("=" * 60 + Colors.END)
        
        print(f"{Colors.YELLOW}Target Domain:{Colors.END} {self.domain}")
        print(f"{Colors.YELLOW}Total Subdomains Found:{Colors.END} {len(self.found_subdomains)}")
        print(f"{Colors.YELLOW}Live Subdomains:{Colors.END} {len(self.live_subdomains)}")
        print(f"{Colors.YELLOW}Scan Duration:{Colors.END} {time.time() - self.start_time:.2f} seconds")
        
        print(f"\n{Colors.BLUE}Statistics:{Colors.END}")
        print(f"  DNS Queries: {self.stats.get('dns_queries', 0)}")
        print(f"  HTTP Requests: {self.stats.get('http_requests', 0)}")
        print(f"  CT Queries: {self.stats.get('ct_queries', 0)}")
        
        if self.stats.get('errors'):
            print(f"\n{Colors.YELLOW}Errors encountered:{Colors.END}")
            for error_type, count in self.stats['errors'].items():
                print(f"  {error_type}: {count}")
        
        logger.info(f"Scan completed. Found {len(self.found_subdomains)} subdomains, "
                   f"{len(self.live_subdomains)} live")

    def run(self, wordlist_file=None):
        """Main execution method"""
        try:
            self.print_banner()
            
            # Basic validation
            if not self.domain or len(self.domain) < 3:
                logger.error("Invalid domain provided")
                print(f"{Colors.RED}[!] Invalid domain provided{Colors.END}")
                return
            
            logger.info(f"Starting subdomain discovery for {self.domain}")
            
            # Step 1: DNS Bruteforce
            self.run_dns_bruteforce(wordlist_file)
            
            # Step 2: Certificate Transparency
            self.certificate_transparency()
            
            # Step 3: Live Verification
            if self.found_subdomains:
                self.verify_live_subdomains()
            
            # Step 4: Results
            self.print_summary()
            self.save_results()
            
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            print(f"\n{Colors.YELLOW}[!] Process interrupted by user{Colors.END}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

def main():
    parser = argparse.ArgumentParser(description='Simple Subdomain Discovery Tool (Minimal Edition)')
    parser.add_argument('domain', help='Target domain (e.g., example.com)')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds (default: 10)')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Domain validation
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$', args.domain):
        print(f"{Colors.RED}[!] Invalid domain format{Colors.END}")
        sys.exit(1)
    
    try:
        finder = SimpleSubdomainFinder(
            args.domain,
            threads=args.threads,
            timeout=args.timeout,
            output_dir=args.output
        )
        
        finder.run(wordlist_file=args.wordlist)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Process interrupted by user{Colors.END}")
    except Exception as e:
        logger.error(f"Main execution error: {e}")
        print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()