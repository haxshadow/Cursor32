# Advanced Subdomain Discovery Tool (Pro Edition)

একটি প্রোফেশনাল গ্রেড subdomain enumeration tool যা cutting-edge techniques ব্যবহার করে maximum subdomain discovery করে।

## বৈশিষ্ট্যসমূহ (Features)

### ✅ মূল বৈশিষ্ট্য
- **AI-Powered Subdomain Prediction** - মেশিন লার্নিং ব্যবহার করে subdomain predict করে
- **Multi-threaded DNS Bruteforce** - দ্রুত DNS query করার জন্য threading ব্যবহার
- **Certificate Transparency Logs** - CT logs থেকে subdomain খুঁজে
- **Live Subdomain Verification** - HTTP/HTTPS দিয়ে live subdomain check করে
- **Advanced Error Handling** - robust error handling এবং retry mechanism
- **Multiple Output Formats** - TXT, CSV, JSON ফরম্যাটে ফলাফল save করে
- **Visualization Support** - matplotlib দিয়ে গ্রাফ তৈরি করে

### 🔧 উন্নত বৈশিষ্ট্য
- **Rate Limiting** - API rate limits respect করে
- **Wildcard Detection** - DNS wildcard automatically detect করে
- **Configuration Support** - YAML config file সাপোর্ট
- **Logging System** - বিস্তারিত logging এবং monitoring
- **Resource Management** - proper cleanup এবং resource management

## ইনস্টলেশন (Installation)

### ১. Repository Clone করুন
```bash
git clone <repository-url>
cd advanced-subdomain-finder
```

### ২. Python Dependencies Install করুন
```bash
# সব dependencies install করুন
pip install -r requirements.txt

# অথবা minimal installation এর জন্য
pip install requests dnspython PyYAML
```

### ৩. Optional Dependencies
```bash
# ML features এর জন্য
pip install scikit-learn numpy

# Visualization এর জন্য
pip install matplotlib

# Web scraping এর জন্য
pip install beautifulsoup4 selenium

# User agent randomization এর জন্য
pip install fake-useragent
```

## ব্যবহার (Usage)

### সাধারণ ব্যবহার
```bash
python advanced_subdomain_finder.py example.com
```

### Advanced Options
```bash
# Custom wordlist দিয়ে
python advanced_subdomain_finder.py example.com -w wordlist.txt

# Threads এবং timeout specify করে
python advanced_subdomain_finder.py example.com -t 200 --timeout 15

# Output directory specify করে
python advanced_subdomain_finder.py example.com -o results

# Verbose logging enable করে
python advanced_subdomain_finder.py example.com -v

# Configuration file দিয়ে
python advanced_subdomain_finder.py example.com -c config.yaml
```

### Command Line Arguments
```
positional arguments:
  domain                Target domain (e.g., example.com)

optional arguments:
  -h, --help            Help message দেখান
  -w, --wordlist        Custom wordlist file
  -c, --config          Configuration file (YAML)
  -t, --threads         Number of threads (default: 100)
  --timeout             Timeout in seconds (default: 10)
  -o, --output          Output directory
  --no-ai               AI-powered discovery disable করুন
  -v, --verbose         Verbose logging enable করুন
```

## Configuration

Tool টি `config.yaml` ফাইল দিয়ে configure করা যায়। প্রথমবার রান করলে একটি default config তৈরি হবে।

### Sample Configuration:
```yaml
# DNS resolvers
resolvers:
  - 8.8.8.8
  - 1.1.1.1
  - 9.9.9.9

# Rate limits (requests per second)
rate_limits:
  dns_queries: 50
  http_requests: 30

# Threading
threads: 100
timeout: 10

# Certificate Transparency sources
ct_sources:
  - "https://crt.sh/?q=%.{}&output=json"

# Wordlist categories
wordlists:
  use_categories:
    - common
    - tech
  custom_words: []
```

## Output Formats

Tool টি তিনটি ফরম্যাটে ফলাফল save করে:

### ১. Text Format (`domain_subdomains.txt`)
```
# Advanced Subdomain Discovery Results for example.com
# Generated: 2024-01-01T12:00:00
# Total Found: 25
# Live Subdomains: 15
# Vulnerable: 2

## All Subdomains:
www.example.com
api.example.com
mail.example.com
...
```

### ২. CSV Format (`domain_subdomains.csv`)
```csv
Subdomain,Status,Service,Status Code
www.example.com,Live,,200
api.example.com,Live,,200
old.example.com,DNS Only,,
```

### ৩. JSON Format (`domain_subdomains.json`)
```json
{
  "domain": "example.com",
  "scan_info": {
    "start_time": "2024-01-01T12:00:00",
    "duration": 120.5,
    "threads": 100
  },
  "statistics": {
    "dns_queries": 1500,
    "http_requests": 25,
    "ai_predictions": 100
  },
  "subdomains": {
    "all": ["www.example.com", "api.example.com"],
    "live": ["www.example.com"],
    "vulnerable": []
  }
}
```

## Dependencies

### Core Dependencies (প্রয়োজনীয়)
- `requests` - HTTP requests এর জন্য
- `dnspython` - DNS queries এর জন্য
- `PyYAML` - Configuration file এর জন্য

### Optional Dependencies
- `scikit-learn`, `numpy` - ML features এর জন্য
- `matplotlib` - Visualization এর জন্য
- `beautifulsoup4` - Web scraping এর জন্য
- `selenium` - Browser automation এর জন্য
- `fake-useragent` - User agent randomization এর জন্য

## Performance Tips

### ১. Threads Optimization
```bash
# Fast discovery এর জন্য বেশি threads
python advanced_subdomain_finder.py example.com -t 200

# Stable discovery এর জন্য কম threads
python advanced_subdomain_finder.py example.com -t 50
```

### ২. Rate Limiting
Configuration file এ rate limits adjust করুন:
```yaml
rate_limits:
  dns_queries: 100  # প্রতি সেকেন্ডে DNS queries
  http_requests: 50  # প্রতি সেকেন্দে HTTP requests
```

### ৩. Memory Optimization
বড় domain এর জন্য output directory আলাদা রাখুন:
```bash
python advanced_subdomain_finder.py example.com -o /path/to/large/storage
```

## Error Handling

Tool টিতে comprehensive error handling আছে:

- **DNS Errors**: Invalid resolvers automatically skip হয়
- **HTTP Errors**: Retry mechanism দিয়ে handle করে
- **Timeout Errors**: Configurable timeout settings
- **Memory Errors**: Resource cleanup automatically হয়
- **Interrupt Handling**: Ctrl+C দিয়ে gracefully stop করা যায়

## Troubleshooting

### ১. DNS Resolution সমস্যা
```bash
# Valid DNS resolvers check করুন
nslookup google.com 8.8.8.8
```

### ২. Permission সমস্যা
```bash
# Output directory এর permission check করুন
chmod 755 output_directory
```

### ৩. Memory সমস্যা
```bash
# Threads কমিয়ে run করুন
python advanced_subdomain_finder.py example.com -t 50
```

### ৪. Dependency সমস্যা
```bash
# Missing dependencies install করুন
pip install --upgrade -r requirements.txt
```

## Security Notes

- Tool টি শুধুমাত্র ethical hacking এবং authorized penetration testing এর জন্য ব্যবহার করুন
- Target domain এর উপর permission ছাড়া scan করবেন না
- Rate limiting respect করুন এবং target server এর উপর অতিরিক্ত load দেবেন না

## Contributing

Bug reports এবং feature requests স্বাগত। Issue open করার আগে existing issues check করুন।

## License

এই project MIT License এর অধীনে distributed।

## Support

সাহায্যের জন্য issue open করুন অথবা discussion section ব্যবহার করুন।

