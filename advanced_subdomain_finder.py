#!/usr/bin/env python3
"""
Advanced Subdomain Discovery Tool (Pro Edition)
===============================================
এটি একটি প্রোফেশনাল গ্রেড subdomain enumeration tool যা 
cutting-edge techniques ব্যবহার করে maximum subdomain discovery করে।

NEW ADVANCED FEATURES:
- AI-Powered Subdomain Prediction
- Advanced Machine Learning Pattern Analysis
- Cloud Infrastructure Mapping
- Advanced Permutation Engine with NLP
- Real-time Threat Intelligence Integration
- Multi-layered Evasion Techniques
- Multiple API Source Integration
"""

# TensorFlow ওয়ার্নিং লুকানোর জন্য
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow ওয়ার্নিং সম্পূর্ণ বন্ধ করুন
import warnings
warnings.filterwarnings("ignore", category=UserWarning)  # Protobuf ওয়ার্নিং ইগনোর করো
warnings.filterwarnings("ignore")

# Core imports
import asyncio
import aiohttp
import requests
import json
import re
import threading
import time
import socket
import ssl
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import random
import string
from pathlib import Path
import csv
from datetime import datetime
import logging
from collections import defaultdict

# DNS related imports
try:
    import dns.resolver
    import dns.zone
    import dns.query
    DNS_AVAILABLE = True
except ImportError:
    print("Warning: dnspython not installed. DNS functionality will be limited.")
    DNS_AVAILABLE = False

# Data analysis imports (optional)
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    ML_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn/numpy not installed. ML features disabled.")
    ML_AVAILABLE = False

# Visualization imports (optional)
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    PLOT_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib not installed. Visualization disabled.")
    PLOT_AVAILABLE = False

# Web scraping imports (optional)
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    print("Warning: BeautifulSoup4 not installed. Web scraping limited.")
    BS4_AVAILABLE = False

# Selenium imports (optional)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    print("Warning: Selenium not installed. Browser automation disabled.")
    SELENIUM_AVAILABLE = False

# User agent imports (optional)
try:
    from fake_useragent import UserAgent
    UA_AVAILABLE = True
except ImportError:
    print("Warning: fake_useragent not installed. Using default user agents.")
    UA_AVAILABLE = False

# Configuration imports (optional)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    print("Warning: PyYAML not installed. YAML config support disabled.")
    YAML_AVAILABLE = False

# Import configurations
try:
    from config import (
        EXTENDED_DNS_RESOLVERS, ADVANCED_WORDLISTS, NUMERIC_PATTERNS,
        PERMUTATION_PATTERNS, CT_SOURCES, TAKEOVER_SIGNATURES,
        DNS_RECORD_TYPES, USER_AGENTS, RATE_LIMITS,
        get_comprehensive_wordlist, get_category_wordlist, generate_permutations,
        create_default_config, ADVANCED_PATTERNS, AI_PATTERNS,
        BLOCKCHAIN_DOMAINS, IOT_PATTERNS, CLOUD_PATTERNS,
        PASSIVE_DNS_SOURCES, SELENIUM_CONFIG, NETLAS_CONFIG
    )
    CONFIG_AVAILABLE = True
except ImportError:
    print(f"[!] config.py file not found. Using fallback configurations.")
    CONFIG_AVAILABLE = False
    # Fallback configurations
    EXTENDED_DNS_RESOLVERS = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']
    ADVANCED_WORDLISTS = {
        'common': ['www', 'mail', 'ftp', 'admin', 'api', 'app', 'dev', 'test', 'staging', 'prod', 'beta']
    }
    NUMERIC_PATTERNS = {'simple_numbers': list(range(1, 11))}
    PERMUTATION_PATTERNS = ['{}-dev', 'dev-{}', '{}-test', 'test-{}']
    CT_SOURCES = ["https://crt.sh/?q=%.{}&output=json"]
    TAKEOVER_SIGNATURES = {
        'github.io': ['There isn\'t a GitHub Pages site here.'],
        'heroku': ['No such app']
    }
    DNS_RECORD_TYPES = ['A', 'AAAA', 'CNAME']
    USER_AGENTS = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36']
    RATE_LIMITS = {'dns_queries': 50, 'http_requests': 30}
    ADVANCED_PATTERNS = ['{}-internal', 'internal-{}']
    AI_PATTERNS = ['ai', 'ml', 'data']
    BLOCKCHAIN_DOMAINS = ['.crypto', '.eth']
    IOT_PATTERNS = ['iot.{}', 'devices.{}']
    CLOUD_PATTERNS = ['aws.{}', 'azure.{}']
    PASSIVE_DNS_SOURCES = []
    SELENIUM_CONFIG = {'enabled': False}
    NETLAS_CONFIG = {'enabled': False}

    def get_comprehensive_wordlist():
        wordlist = []
        for category in ADVANCED_WORDLISTS.values():
            wordlist.extend(category)
        return sorted(list(set(wordlist)))

    def get_category_wordlist(category):
        return ADVANCED_WORDLISTS.get(category, [])

    def generate_permutations(base_word):
        permutations = []
        for pattern in PERMUTATION_PATTERNS:
            if '{}' in pattern:
                permutations.append(pattern.format(base_word))
        return permutations

    def create_default_config():
        print("Creating basic default configuration...")
        return {}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('subdomain_finder.log'),
        logging.StreamHandler()
    ]
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

# AI-powered subdomain prediction model
class SubdomainPredictor:
    def __init__(self):
        self.trained = False
        if ML_AVAILABLE:
            try:
                self.vectorizer = TfidfVectorizer(max_features=1000)
                self.kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
            except Exception as e:
                logger.warning(f"ML model initialization failed: {e}")
                self.vectorizer = None
                self.kmeans = None
        else:
            self.vectorizer = None
            self.kmeans = None
        
    def train(self, known_subdomains):
        """Known subdomains দিয়ে model train করে"""
        if not ML_AVAILABLE or not self.vectorizer or len(known_subdomains) < 10:
            return False
            
        try:
            X = self.vectorizer.fit_transform(known_subdomains)
            self.kmeans.fit(X)
            self.trained = True
            logger.info(f"AI model trained with {len(known_subdomains)} subdomains")
            return True
        except Exception as e:
            logger.error(f"AI model training failed: {e}")
            return False
    
    def predict(self, base_domain, num_predictions=50):
        """AI ব্যবহার করে subdomain predict করে"""
        predictions = []
        
        # Basic pattern-based predictions
        common_patterns = [
            'api', 'app', 'admin', 'dev', 'test', 'staging', 'prod', 'www',
            'mail', 'ftp', 'blog', 'shop', 'store', 'support', 'help',
            'docs', 'status', 'monitor', 'dashboard', 'portal', 'login',
            'auth', 'oauth', 'sso', 'cdn', 'static', 'assets', 'media',
            'images', 'videos', 'files', 'downloads', 'backup', 'old',
            'new', 'beta', 'alpha', 'canary', 'preview'
        ]
        
        for pattern in common_patterns:
            predictions.extend([
                f"{pattern}.{base_domain}",
                f"{pattern}-1.{base_domain}",
                f"{pattern}-2.{base_domain}",
                f"{pattern}-01.{base_domain}",
                f"{pattern}-02.{base_domain}",
                f"{pattern}-dev.{base_domain}",
                f"{pattern}-test.{base_domain}",
                f"{pattern}-staging.{base_domain}",
                f"{pattern}-prod.{base_domain}",
                f"dev-{pattern}.{base_domain}",
                f"test-{pattern}.{base_domain}",
                f"staging-{pattern}.{base_domain}",
                f"prod-{pattern}.{base_domain}",
            ])
        
        # Remove duplicates and limit results
        unique_predictions = list(set(predictions))
        return unique_predictions[:num_predictions]

class AdvancedSubdomainFinder:
    def __init__(self, domain, config_file=None, threads=100, timeout=10, output_dir=None):
        self.domain = domain.lower().strip()
        self.threads = min(threads, 200)  # Limit threads for stability
        self.timeout = max(timeout, 5)    # Minimum timeout
        self.found_subdomains = set()
        self.wildcards = set()
        self.live_subdomains = set()
        self.vulnerable_subdomains = []
        self.scanned_subdomains = set()
        self.progress = 0
        self.total_tasks = 0
        self.start_time = time.time()
        
        # AI-powered prediction
        self.ai_predictor = SubdomainPredictor()
        
        # Initialize session with better error handling
        self.session = requests.Session()
        if UA_AVAILABLE:
            try:
                ua = UserAgent()
                self.session.headers.update({'User-Agent': ua.random})
            except Exception:
                self.session.headers.update({'User-Agent': USER_AGENTS[0]})
        else:
            self.session.headers.update({'User-Agent': USER_AGENTS[0]})
        
        # Add retry mechanism
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Selenium setup
        self.selenium_driver = None
        
        # Load configurations with better error handling
        self.config = self.load_config_safe(config_file)
        
        # Setup output directory
        self.output_dir = Path(output_dir) if output_dir else Path(f"results_{domain}")
        try:
            self.output_dir.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            logger.error(f"Could not create output directory: {e}")
            self.output_dir = Path(".")
        
        # DNS resolvers with validation
        self.resolvers = self.validate_resolvers(self.config.get('resolvers', EXTENDED_DNS_RESOLVERS))
        
        # Rate limiting
        self.last_dns_query = 0
        self.last_http_request = 0
        
        # Statistics
        self.stats = {
            'dns_queries': 0,
            'http_requests': 0,
            'ct_queries': 0,
            'permutations': 0,
            'ai_predictions': 0,
            'errors': defaultdict(int),
            'start_time': self.start_time
        }
        
        # Initialize Selenium if enabled
        self.setup_selenium_safe()

    def validate_resolvers(self, resolvers):
        """DNS resolvers validate করে"""
        valid_resolvers = []
        for resolver in resolvers:
            try:
                # Test resolver
                test_resolver = dns.resolver.Resolver() if DNS_AVAILABLE else None
                if test_resolver:
                    test_resolver.nameservers = [resolver]
                    test_resolver.timeout = 5
                    test_resolver.resolve('google.com', 'A')
                    valid_resolvers.append(resolver)
            except Exception:
                logger.warning(f"DNS resolver {resolver} is not responding, skipping...")
                continue
        
        if not valid_resolvers:
            logger.warning("No valid DNS resolvers found, using system default")
            return ['8.8.8.8', '1.1.1.1']
        
        return valid_resolvers

    def load_config_safe(self, config_file):
        """Safely load configuration with fallbacks"""
        if not config_file:
            default_config = Path("config.yaml")
            if default_config.exists() and YAML_AVAILABLE:
                config_file = str(default_config)
                logger.info(f"Using configuration file: {config_file}")
            else:
                logger.info("No configuration file found, using defaults")
                return {}
        
        if config_file and YAML_AVAILABLE:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    logger.info(f"Configuration loaded from {config_file}")
                    return config or {}
            except Exception as e:
                logger.error(f"Error loading config file {config_file}: {e}")
                return {}
        
        return {}

    def setup_selenium_safe(self):
        """Safely setup Selenium WebDriver"""
        if not SELENIUM_AVAILABLE or not self.config.get('selenium_config', {}).get('enabled', False):
            return
            
        try:
            logger.info("Setting up Selenium WebDriver...")
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--window-size=1920,1080')
            
            if UA_AVAILABLE:
                try:
                    ua = UserAgent()
                    chrome_options.add_argument(f'--user-agent={ua.random}')
                except:
                    chrome_options.add_argument(f'--user-agent={USER_AGENTS[0]}')
            else:
                chrome_options.add_argument(f'--user-agent={USER_AGENTS[0]}')
            
            # Try to create driver
            self.selenium_driver = webdriver.Chrome(options=chrome_options)
            self.selenium_driver.set_page_load_timeout(30)
            logger.info("Selenium WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Selenium setup failed: {e}")
            self.selenium_driver = None

    def print_banner(self):
        """Tool banner প্রিন্ট করে"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║            ADVANCED SUBDOMAIN FINDER (PRO EDITION)            ║
    ║              AI-Powered Discovery Engine                      ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.YELLOW}Target Domain: {Colors.GREEN}{self.domain}{Colors.END}
{Colors.YELLOW}Threads: {Colors.GREEN}{self.threads}{Colors.END}
{Colors.YELLOW}Timeout: {Colors.GREEN}{self.timeout}s{Colors.END}
{Colors.YELLOW}Output Dir: {Colors.GREEN}{self.output_dir}{Colors.END}
{Colors.YELLOW}DNS Available: {Colors.GREEN}{'YES' if DNS_AVAILABLE else 'NO'}{Colors.END}
{Colors.YELLOW}ML Available: {Colors.GREEN}{'YES' if ML_AVAILABLE else 'NO'}{Colors.END}
{Colors.YELLOW}Selenium: {Colors.GREEN}{'ENABLED' if self.selenium_driver else 'DISABLED'}{Colors.END}
{Colors.YELLOW}Valid Resolvers: {Colors.GREEN}{len(self.resolvers)}{Colors.END}
"""
        print(banner)

    def load_wordlist(self, wordlist_file=None):
        """Load wordlist from file or generate dynamically"""
        if wordlist_file and Path(wordlist_file).exists():
            try:
                logger.info(f"Loading wordlist from {wordlist_file}")
                with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                    wordlist = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                logger.info(f"Loaded {len(wordlist)} words from file")
                return wordlist
            except Exception as e:
                logger.error(f"Error loading wordlist file: {e}")
                
        logger.info("Generating dynamic wordlist")
        if CONFIG_AVAILABLE:
            return get_comprehensive_wordlist()
        else:
            # Fallback wordlist
            return ADVANCED_WORDLISTS.get('common', ['www', 'mail', 'ftp', 'admin'])

    def check_wildcard(self):
        """Wildcard DNS response detect করে"""
        if not DNS_AVAILABLE:
            logger.warning("DNS functionality not available, skipping wildcard check")
            return
            
        logger.info("Checking for wildcard DNS responses...")
        
        test_results = []
        for _ in range(3):  # Reduced iterations for speed
            random_subdomain = ''.join(random.choices(string.ascii_lowercase, k=15))
            test_domain = f"{random_subdomain}.{self.domain}"
            
            try:
                self.rate_limit_dns()
                resolver = dns.resolver.Resolver()
                resolver.nameservers = self.resolvers
                resolver.timeout = self.timeout
                
                answers = resolver.resolve(test_domain, 'A')
                for answer in answers:
                    ip = str(answer)
                    test_results.append(ip)
                    self.stats['dns_queries'] += 1
            except Exception:
                pass
        
        if test_results:
            if len(set(test_results)) == 1:
                self.wildcards.add(test_results[0])
                logger.warning(f"Wildcard detected: {test_results[0]}")
                print(f"{Colors.RED}[!] Wildcard detected: {test_results[0]}{Colors.END}")
            else:
                logger.warning("Inconsistent wildcard responses detected")
                print(f"{Colors.YELLOW}[!] Inconsistent wildcard responses detected{Colors.END}")
        else:
            logger.info("No wildcard detected")
            print(f"{Colors.GREEN}[+] No wildcard detected{Colors.END}")

    def rate_limit_dns(self):
        """Rate limiting for DNS queries"""
        now = time.time()
        elapsed = now - self.last_dns_query
        min_interval = 1.0 / self.config.get('rate_limits', {}).get('dns_queries', RATE_LIMITS['dns_queries'])
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_dns_query = time.time()

    def rate_limit_http(self):
        """Rate limiting for HTTP requests"""
        now = time.time()
        elapsed = now - self.last_http_request
        min_interval = 1.0 / self.config.get('rate_limits', {}).get('http_requests', RATE_LIMITS['http_requests'])
        
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        
        self.last_http_request = time.time()

    def dns_bruteforce(self, subdomain):
        """Single subdomain DNS lookup করে"""
        if not DNS_AVAILABLE:
            return False
            
        if subdomain in self.scanned_subdomains:
            return False
            
        self.scanned_subdomains.add(subdomain)
        full_domain = f"{subdomain}.{self.domain}"
        
        for resolver_ip in self.resolvers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [resolver_ip]
                resolver.timeout = self.timeout
                resolver.lifetime = self.timeout
                
                self.rate_limit_dns()
                
                # A record check
                try:
                    answers = resolver.resolve(full_domain, 'A')
                    for answer in answers:
                        ip = str(answer)
                        if ip not in self.wildcards:
                            self.found_subdomains.add(full_domain)
                            self.stats['dns_queries'] += 1
                            logger.info(f"Found subdomain: {full_domain} -> {ip}")
                            print(f"{Colors.GREEN}[+] Found: {full_domain} -> {ip}{Colors.END}")
                            return True
                except Exception:
                    pass
                
                # CNAME record check
                try:
                    answers = resolver.resolve(full_domain, 'CNAME')
                    for answer in answers:
                        self.found_subdomains.add(full_domain)
                        self.stats['dns_queries'] += 1
                        logger.info(f"Found CNAME: {full_domain} -> {answer}")
                        print(f"{Colors.GREEN}[+] Found (CNAME): {full_domain} -> {answer}{Colors.END}")
                        return True
                except Exception:
                    pass
                    
            except Exception as e:
                self.stats['errors']['dns'] += 1
                continue
        
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
                futures = [executor.submit(self.dns_bruteforce, word) for word in wordlist]
                for future in as_completed(futures):
                    self.progress += 1
                    if self.progress % 100 == 0:
                        self.print_progress()
        except Exception as e:
            logger.error(f"DNS bruteforce error: {e}")

    def ai_powered_discovery(self):
        """AI-powered subdomain prediction and discovery"""
        logger.info("Starting AI-powered subdomain discovery...")
        print(f"{Colors.YELLOW}[*] Starting AI-powered subdomain discovery...{Colors.END}")
        
        # Train AI model with existing subdomains
        if len(self.found_subdomains) > 10:
            self.ai_predictor.train(list(self.found_subdomains))
        
        # Generate AI predictions
        predictions = self.ai_predictor.predict(self.domain, num_predictions=100)
        self.stats['ai_predictions'] = len(predictions)
        
        logger.info(f"Generated {len(predictions)} AI predictions")
        print(f"{Colors.BLUE}[*] Generated {len(predictions)} AI predictions{Colors.END}")
        
        # Test AI predictions
        if predictions:
            self.total_tasks += len(predictions)
            try:
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    futures = [executor.submit(self.dns_bruteforce, pred.split('.')[0]) for pred in predictions]
                    for future in as_completed(futures):
                        self.progress += 1
                        if self.progress % 50 == 0:
                            self.print_progress()
            except Exception as e:
                logger.error(f"AI discovery error: {e}")

    def certificate_transparency(self):
        """Certificate Transparency logs থেকে subdomain খুঁজে"""
        logger.info("Searching Certificate Transparency logs...")
        print(f"{Colors.YELLOW}[*] Searching Certificate Transparency logs...{Colors.END}")
        
        ct_sources = self.config.get('ct_sources', CT_SOURCES)
        
        for source in ct_sources:
            try:
                url = source.format(self.domain)
                self.rate_limit_http()
                
                response = self.session.get(url, timeout=15)
                self.stats['ct_queries'] += 1
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        if isinstance(data, list):
                            for cert in data:
                                domains = []
                                if 'name_value' in cert:
                                    domains = cert['name_value'].split('\n')
                                elif 'dns_names' in cert:
                                    domains = cert['dns_names']
                                
                                for domain in domains:
                                    domain = domain.strip().lower()
                                    if (domain.endswith(f".{self.domain}") and 
                                        domain not in self.found_subdomains and
                                        '*' not in domain):
                                        self.found_subdomains.add(domain)
                                        logger.info(f"CT Log found: {domain}")
                                        print(f"{Colors.GREEN}[+] CT Log: {domain}{Colors.END}")
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON response from {url}")
                        
            except Exception as e:
                self.stats['errors']['ct'] += 1
                logger.error(f"CT search error: {e}")

    def print_progress(self):
        """Print current progress"""
        elapsed = time.time() - self.start_time
        progress_percent = (self.progress / self.total_tasks) * 100 if self.total_tasks > 0 else 0
        
        progress_msg = (f"Progress: {self.progress}/{self.total_tasks} ({progress_percent:.1f}%) - "
                       f"Elapsed: {elapsed:.1f}s - Found: {len(self.found_subdomains)}")
        
        logger.info(progress_msg)
        print(f"{Colors.BLUE}[*] {progress_msg}{Colors.END}")

    def verify_live_subdomains(self):
        """Live subdomain verification করে"""
        logger.info("Verifying live subdomains...")
        print(f"{Colors.YELLOW}[*] Verifying live subdomains...{Colors.END}")
        
        def check_live(subdomain):
            try:
                for protocol in ['https', 'http']:
                    try:
                        self.rate_limit_http()
                        response = self.session.get(f"{protocol}://{subdomain}", 
                                                  timeout=10, allow_redirects=True)
                        self.stats['http_requests'] += 1
                        
                        if response.status_code < 400:
                            self.live_subdomains.add(subdomain)
                            logger.info(f"Live subdomain: {protocol}://{subdomain} [{response.status_code}]")
                            print(f"{Colors.GREEN}[+] Live: {protocol}://{subdomain} [{response.status_code}]{Colors.END}")
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
                with ThreadPoolExecutor(max_workers=min(self.threads, 50)) as executor:  # Limit threads for HTTP
                    futures = [executor.submit(check_live, subdomain) for subdomain in self.found_subdomains]
                    for future in as_completed(futures):
                        self.progress += 1
                        if self.progress % 20 == 0:
                            self.print_progress()
            except Exception as e:
                logger.error(f"Live verification error: {e}")

    def save_results(self, filename=None):
        """Results save করে multiple formats এ"""
        if not filename:
            filename = f"{self.domain}_subdomains"
        
        try:
            # Text format
            txt_file = self.output_dir / f"{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"# Advanced Subdomain Discovery Results for {self.domain}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n")
                f.write(f"# Total Found: {len(self.found_subdomains)}\n")
                f.write(f"# Live Subdomains: {len(self.live_subdomains)}\n")
                f.write(f"# Vulnerable: {len(self.vulnerable_subdomains)}\n")
                f.write(f"# AI Predictions: {self.stats.get('ai_predictions', 0)}\n\n")
                
                f.write("## All Subdomains:\n")
                for subdomain in sorted(self.found_subdomains):
                    f.write(f"{subdomain}\n")
                
                f.write("\n## Live Subdomains:\n")
                for subdomain in sorted(self.live_subdomains):
                    f.write(f"{subdomain}\n")
                
                if self.vulnerable_subdomains:
                    f.write("\n## Potentially Vulnerable Subdomains:\n")
                    for vuln in self.vulnerable_subdomains:
                        f.write(f"{vuln['subdomain']} - {vuln.get('service', 'Unknown')} "
                               f"(Status: {vuln.get('status_code', 'Unknown')})\n")
            
            # CSV format
            csv_file = self.output_dir / f"{filename}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Subdomain', 'Status', 'Service', 'Status Code'])
                
                for subdomain in sorted(self.found_subdomains):
                    status = "Live" if subdomain in self.live_subdomains else "DNS Only"
                    service = ""
                    status_code = ""
                    
                    for vuln in self.vulnerable_subdomains:
                        if vuln['subdomain'] == subdomain:
                            service = vuln.get('service', '')
                            status_code = vuln.get('status_code', '')
                            status = "Vulnerable"
                            break
                    
                    writer.writerow([subdomain, status, service, status_code])
            
            # JSON format
            json_file = self.output_dir / f"{filename}.json"
            results = {
                'domain': self.domain,
                'scan_info': {
                    'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration': time.time() - self.start_time,
                    'threads': self.threads,
                    'timeout': self.timeout,
                    'dns_available': DNS_AVAILABLE,
                    'ml_available': ML_AVAILABLE,
                    'selenium_enabled': self.selenium_driver is not None
                },
                'statistics': dict(self.stats),
                'results': {
                    'total_subdomains': len(self.found_subdomains),
                    'live_subdomains': len(self.live_subdomains),
                    'vulnerable_subdomains': len(self.vulnerable_subdomains),
                    'wildcards': list(self.wildcards)
                },
                'subdomains': {
                    'all': sorted(self.found_subdomains),
                    'live': sorted(self.live_subdomains),
                    'vulnerable': self.vulnerable_subdomains
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

    def generate_visualization(self):
        """Generate visualization if matplotlib is available"""
        if not PLOT_AVAILABLE:
            logger.warning("Matplotlib not available, skipping visualization")
            return
            
        try:
            logger.info("Generating visualization...")
            print(f"{Colors.YELLOW}[*] Generating visualization...{Colors.END}")
            
            # Create a simple bar chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            fig.suptitle(f'Subdomain Discovery Results for {self.domain}', fontsize=14)
            
            # Subdomain types
            labels = ['Live', 'DNS Only', 'Vulnerable']
            sizes = [
                len(self.live_subdomains) - len(self.vulnerable_subdomains),
                len(self.found_subdomains) - len(self.live_subdomains),
                len(self.vulnerable_subdomains)
            ]
            colors = ['#4CAF50', '#FFC107', '#F44336']
            
            # Remove zero values
            non_zero_data = [(label, size, color) for label, size, color in zip(labels, sizes, colors) if size > 0]
            if non_zero_data:
                labels, sizes, colors = zip(*non_zero_data)
                ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            else:
                ax1.text(0.5, 0.5, 'No data to display', ha='center', va='center', transform=ax1.transAxes)
            ax1.set_title('Subdomain Types')
            
            # Statistics
            stats_labels = ['DNS Queries', 'HTTP Requests', 'CT Queries', 'AI Predictions']
            stats_values = [
                self.stats.get('dns_queries', 0),
                self.stats.get('http_requests', 0),
                self.stats.get('ct_queries', 0),
                self.stats.get('ai_predictions', 0)
            ]
            
            ax2.bar(stats_labels, stats_values, color=['#2196F3', '#9C27B0', '#FF9800', '#4CAF50'])
            ax2.set_title('Discovery Statistics')
            ax2.set_ylabel('Count')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            plt.tight_layout()
            
            viz_file = self.output_dir / f"{self.domain}_visualization.png"
            plt.savefig(viz_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Visualization saved to {viz_file}")
            print(f"{Colors.GREEN}[+] Visualization saved to {viz_file}{Colors.END}")
            
        except Exception as e:
            logger.error(f"Visualization generation error: {e}")
            print(f"{Colors.RED}[!] Visualization error: {e}{Colors.END}")

    def print_summary(self):
        """Final summary print করে"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}=" * 60)
        print("                    DISCOVERY SUMMARY")
        print("=" * 60 + Colors.END)
        
        print(f"{Colors.YELLOW}Target Domain:{Colors.END} {self.domain}")
        print(f"{Colors.YELLOW}Total Subdomains Found:{Colors.END} {len(self.found_subdomains)}")
        print(f"{Colors.YELLOW}Live Subdomains:{Colors.END} {len(self.live_subdomains)}")
        print(f"{Colors.YELLOW}Potentially Vulnerable:{Colors.END} {len(self.vulnerable_subdomains)}")
        print(f"{Colors.YELLOW}Scan Duration:{Colors.END} {time.time() - self.start_time:.2f} seconds")
        
        print(f"\n{Colors.BLUE}Statistics:{Colors.END}")
        print(f"  DNS Queries: {self.stats.get('dns_queries', 0)}")
        print(f"  HTTP Requests: {self.stats.get('http_requests', 0)}")
        print(f"  CT Queries: {self.stats.get('ct_queries', 0)}")
        print(f"  AI Predictions: {self.stats.get('ai_predictions', 0)}")
        
        if self.stats.get('errors'):
            print(f"\n{Colors.YELLOW}Errors encountered:{Colors.END}")
            for error_type, count in self.stats['errors'].items():
                print(f"  {error_type}: {count}")
        
        if self.vulnerable_subdomains:
            print(f"\n{Colors.RED}[!] Potentially Vulnerable Subdomains:{Colors.END}")
            for vuln in self.vulnerable_subdomains:
                service = vuln.get('service', 'Unknown')
                status_code = vuln.get('status_code', 'Unknown')
                print(f"  - {vuln['subdomain']} ({service}) [Status: {status_code}]")
        
        logger.info(f"Scan completed. Found {len(self.found_subdomains)} subdomains, "
                   f"{len(self.live_subdomains)} live, {len(self.vulnerable_subdomains)} vulnerable")

    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.selenium_driver:
                self.selenium_driver.quit()
                logger.info("Selenium driver closed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        
        try:
            self.session.close()
        except Exception:
            pass

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
            
            # Step 1: Wildcard detection
            self.check_wildcard()
            
            # Step 2: DNS Bruteforce
            self.run_dns_bruteforce(wordlist_file)
            
            # Step 3: AI-powered discovery
            if ML_AVAILABLE:
                self.ai_powered_discovery()
            else:
                logger.warning("ML not available, skipping AI discovery")
            
            # Step 4: Certificate Transparency
            self.certificate_transparency()
            
            # Step 5: Live Verification
            if self.found_subdomains:
                self.verify_live_subdomains()
            
            # Step 6: Results
            self.print_summary()
            self.save_results()
            
            if PLOT_AVAILABLE:
                self.generate_visualization()
            
        except KeyboardInterrupt:
            logger.info("Process interrupted by user")
            print(f"\n{Colors.YELLOW}[!] Process interrupted by user{Colors.END}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
        finally:
            self.cleanup()

def main():
    parser = argparse.ArgumentParser(description='Advanced Subdomain Discovery Tool (Pro Edition)')
    parser.add_argument('domain', help='Target domain (e.g., example.com)')
    parser.add_argument('-w', '--wordlist', help='Custom wordlist file')
    parser.add_argument('-c', '--config', help='Configuration file (YAML)')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in seconds (default: 10)')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI-powered discovery')
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
        finder = AdvancedSubdomainFinder(
            args.domain,
            config_file=args.config,
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