#!/usr/bin/env python3
"""
Configuration file for Advanced Subdomain Discovery Tool
"""

import yaml
import random

# Extended DNS resolvers
EXTENDED_DNS_RESOLVERS = [
    '8.8.8.8',      # Google
    '1.1.1.1',      # Cloudflare
    '9.9.9.9',      # Quad9
    '208.67.222.222', # OpenDNS
    '8.26.56.26',   # Comodo
    '64.6.64.6',    # Verisign
    '77.88.8.8',    # Yandex
    '156.154.70.1', # Neustar
]

# Advanced wordlists
ADVANCED_WORDLISTS = {
    'common': [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2',
        'cpanel', 'whm', 'autodiscover', 'autoconfig', 'ns3', 'm', 'imap', 'test', 'ns', 'blog',
        'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns4', 'mail2', 'new', 'mysql',
        'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql',
        'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img',
        'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1',
        'ns5', 'upload', 'client', 'forum', 'bb', 'chat', 'irc', 'live', 'search', 'ftp2',
        'archive', 'mc', 'herald', 'gis', 'monitor', 'login', 'backup', 'alerts', 'admin2',
        'panel', 'server', 'ns6', 'staging', 'app', 'git', 'svn'
    ],
    'tech': [
        'api', 'app', 'staging', 'dev', 'test', 'prod', 'production', 'beta', 'alpha',
        'demo', 'sandbox', 'preview', 'canary', 'edge', 'master', 'main', 'develop',
        'feature', 'hotfix', 'release', 'build', 'ci', 'cd', 'jenkins', 'gitlab',
        'github', 'docker', 'k8s', 'kubernetes', 'helm', 'terraform', 'ansible'
    ],
    'services': [
        'mail', 'email', 'smtp', 'pop3', 'imap', 'webmail', 'exchange', 'outlook',
        'calendar', 'contacts', 'tasks', 'notes', 'files', 'drive', 'storage',
        'backup', 'sync', 'share', 'docs', 'wiki', 'kb', 'help', 'support',
        'ticket', 'issue', 'bug', 'crm', 'erp', 'hr', 'finance', 'accounting'
    ]
}

# Numeric patterns
NUMERIC_PATTERNS = {
    'simple_numbers': list(range(1, 21)),
    'years': list(range(2010, 2025)),
    'ports': [80, 443, 8080, 8443, 3000, 5000, 8000, 9000],
    'versions': ['v1', 'v2', 'v3', 'v4', 'v5']
}

# Permutation patterns
PERMUTATION_PATTERNS = [
    '{}-dev', 'dev-{}', '{}-test', 'test-{}', '{}-staging', 'staging-{}',
    '{}-prod', 'prod-{}', '{}-api', 'api-{}', '{}-app', 'app-{}',
    '{}-1', '{}-2', '{}-01', '{}-02', 'new-{}', 'old-{}',
    '{}-backup', 'backup-{}', '{}-db', 'db-{}', '{}-web', 'web-{}'
]

# Certificate Transparency sources
CT_SOURCES = [
    "https://crt.sh/?q=%.{}&output=json",
    "https://api.certspotter.com/v1/issuances?domain={}&include_subdomains=true&expand=dns_names"
]

# Subdomain takeover signatures
TAKEOVER_SIGNATURES = {
    'github.io': [
        'There isn\'t a GitHub Pages site here.',
        'For root URLs (like http://example.com/) you must provide an index.html file'
    ],
    'heroku': [
        'No such app',
        'herokucdn.com/error-pages/no-such-app.html'
    ],
    'amazonaws.com': [
        'NoSuchBucket',
        'The specified bucket does not exist'
    ],
    'shopify': [
        'Sorry, this shop is currently unavailable.',
        'Shopify\\s{0,5}Will be back soon'
    ],
    'fastly': [
        'Fastly error: unknown domain'
    ],
    'azurewebsites.net': [
        'Web site not found',
        'Error 404 - Web app not found'
    ]
}

# DNS record types
DNS_RECORD_TYPES = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA']

# User agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
]

# Rate limits (requests per second)
RATE_LIMITS = {
    'dns_queries': 50,
    'http_requests': 30,
    'api_requests': 10
}

# Advanced patterns for AI prediction
ADVANCED_PATTERNS = [
    '{}-internal', 'internal-{}', '{}-external', 'external-{}',
    '{}-secure', 'secure-{}', '{}-public', 'public-{}',
    '{}-private', 'private-{}', '{}-corp', 'corp-{}',
    '{}-admin', 'admin-{}', '{}-user', 'user-{}',
    '{}-guest', 'guest-{}', '{}-vpn', 'vpn-{}',
    '{}-proxy', 'proxy-{}', '{}-cache', 'cache-{}',
    '{}-load', 'load-{}', '{}-balance', 'balance-{}'
]

# AI patterns
AI_PATTERNS = [
    'ai', 'ml', 'data', 'analytics', 'bigdata', 'spark', 'hadoop',
    'tensorflow', 'pytorch', 'sklearn', 'jupyter', 'notebook',
    'model', 'prediction', 'inference', 'training', 'pipeline'
]

# Blockchain domains
BLOCKCHAIN_DOMAINS = [
    '.crypto', '.zil', '.eth', '.luxe', '.kred', '.xyz', '.art'
]

# IoT patterns
IOT_PATTERNS = [
    'iot.{}', 'devices.{}', 'sensors.{}', 'gateway.{}',
    'hub.{}', 'controller.{}', 'monitor.{}', 'tracker.{}'
]

# Cloud patterns
CLOUD_PATTERNS = [
    'aws.{}', 'azure.{}', 'gcp.{}', 'cloud.{}',
    's3.{}', 'ec2.{}', 'rds.{}', 'lambda.{}',
    'cloudfront.{}', 'cdn.{}', 'storage.{}'
]

# Passive DNS sources
PASSIVE_DNS_SOURCES = [
    {
        'name': 'VirusTotal',
        'url': 'https://www.virustotal.com/vtapi/v2/domain/report',
        'api_key_required': True,
        'parser': 'virustotal_parser'
    },
    {
        'name': 'AlienVault OTX',
        'url': 'https://otx.alienvault.com/api/v1/indicators/domain/{}/passive_dns',
        'api_key_required': False,
        'parser': 'otx_parser'
    },
    {
        'name': 'HackerTarget',
        'url': 'https://api.hackertarget.com/hostsearch/?q={}',
        'api_key_required': False,
        'parser': 'hackertarget_parser'
    }
]

# Selenium configuration
SELENIUM_CONFIG = {
    'enabled': False,
    'headless': True,
    'timeout': 30,
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
}

# Netlas configuration
NETLAS_CONFIG = {
    'enabled': False,
    'api_key': 'YOUR_NETLAS_API_KEY',
    'base_url': 'https://app.netlas.io/api'
}

def get_comprehensive_wordlist():
    """সম্পূর্ণ wordlist return করে"""
    wordlist = []
    for category in ADVANCED_WORDLISTS.values():
        wordlist.extend(category)
    
    # Add numeric patterns
    for pattern_list in NUMERIC_PATTERNS.values():
        wordlist.extend([str(p) for p in pattern_list])
    
    # Remove duplicates and sort
    return sorted(list(set(wordlist)))

def get_category_wordlist(category):
    """নির্দিষ্ট category এর wordlist return করে"""
    return ADVANCED_WORDLISTS.get(category, [])

def generate_permutations(base_word):
    """একটি base word এর জন্য permutation generate করে"""
    permutations = []
    for pattern in PERMUTATION_PATTERNS:
        if '{}' in pattern:
            permutations.append(pattern.format(base_word))
    return permutations

def create_default_config():
    """Default configuration file তৈরি করে"""
    config = {
        'resolvers': EXTENDED_DNS_RESOLVERS[:4],  # First 4 resolvers
        'rate_limits': RATE_LIMITS,
        'threads': 100,
        'timeout': 10,
        'wordlists': {
            'use_categories': ['common', 'tech'],
            'custom_words': []
        },
        'ct_sources': CT_SOURCES,
        'takeover_signatures': TAKEOVER_SIGNATURES,
        'passive_dns_sources': PASSIVE_DNS_SOURCES,
        'selenium_config': SELENIUM_CONFIG,
        'netlas_config': NETLAS_CONFIG,
        'advanced_patterns': ADVANCED_PATTERNS[:10],  # First 10 patterns
        'ai_patterns': AI_PATTERNS,
        'blockchain_domains': BLOCKCHAIN_DOMAINS,
        'iot_patterns': IOT_PATTERNS,
        'cloud_patterns': CLOUD_PATTERNS,
        'permutation_patterns': PERMUTATION_PATTERNS[:6]  # First 6 patterns
    }
    
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("Default config.yaml file created successfully!")
    return config