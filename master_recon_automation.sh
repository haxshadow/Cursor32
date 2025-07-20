#!/bin/bash

# 🔥 Master Bug Bounty Reconnaissance Automation
# ==================================================
# Complete end-to-end automation framework
# Author: Advanced Bug Bounty Hunter
# Version: 2.0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
THREADS=50
TIMEOUT=10
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"

# Banner
print_banner() {
    echo -e "${CYAN}
 ██████  ██    ██  ██████      ██████   ██████  ██    ██ ███    ██ ████████ ██    ██ 
 ██   ██ ██    ██ ██          ██   ██ ██    ██ ██    ██ ████   ██    ██     ██  ██  
 ██████  ██    ██ ██   ███    ██████  ██    ██ ██    ██ ██ ██  ██    ██      ████   
 ██   ██ ██    ██ ██    ██    ██   ██ ██    ██ ██    ██ ██  ██ ██    ██       ██    
 ██████   ██████   ██████     ██████   ██████   ██████  ██   ████    ██       ██    
                                                                                      
 █████  ██    ██ ████████  ██████  ███    ███  █████  ████████ ██  ██████  ███    ██ 
██   ██ ██    ██    ██    ██    ██ ████  ████ ██   ██    ██    ██ ██    ██ ████   ██ 
███████ ██    ██    ██    ██    ██ ██ ████ ██ ███████    ██    ██ ██    ██ ██ ██  ██ 
██   ██ ██    ██    ██    ██    ██ ██  ██  ██ ██   ██    ██    ██ ██    ██ ██  ██ ██ 
██   ██  ██████     ██     ██████  ██      ██ ██   ██    ██    ██  ██████  ██   ████ 
${NC}"
    echo -e "${GREEN}🚀 Master Bug Bounty Reconnaissance Automation v2.0${NC}"
    echo -e "${YELLOW}📅 $(date)${NC}"
    echo -e "${PURPLE}🎯 Target: $1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

# Notification functions
send_telegram() {
    if [ ! -z "$TELEGRAM_BOT_TOKEN" ] && [ ! -z "$TELEGRAM_CHAT_ID" ]; then
        message="$1"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
             -d chat_id="$TELEGRAM_CHAT_ID" \
             -d text="$message" \
             -d parse_mode="HTML" > /dev/null 2>&1
    fi
}

send_discord() {
    if [ ! -z "$DISCORD_WEBHOOK" ]; then
        message="$1"
        curl -s -H "Content-Type: application/json" \
             -X POST \
             -d "{\"content\": \"$message\"}" \
             "$DISCORD_WEBHOOK" > /dev/null 2>&1
    fi
}

notify() {
    message="$1"
    echo -e "${GREEN}[NOTIFICATION]${NC} $message"
    send_telegram "$message"
    send_discord "$message"
}

# Log function
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$WORKSPACE/automation.log"
}

# Check dependencies
check_dependencies() {
    echo -e "${YELLOW}[+] Checking dependencies...${NC}"
    
    REQUIRED_TOOLS=("subfinder" "httpx" "nuclei" "ffuf" "dnsx" "assetfinder" "gau" "waybackurls" "anew" "jq" "curl" "dig")
    MISSING_TOOLS=()
    
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            MISSING_TOOLS+=("$tool")
        fi
    done
    
    if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
        echo -e "${RED}[-] Missing tools: ${MISSING_TOOLS[*]}${NC}"
        echo -e "${YELLOW}[!] Please install missing tools first${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[✓] All dependencies satisfied${NC}"
}

# Setup workspace
setup_workspace() {
    TARGET="$1"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    WORKSPACE="${TARGET}_${TIMESTAMP}"
    
    echo -e "${YELLOW}[+] Setting up workspace: $WORKSPACE${NC}"
    
    mkdir -p "$WORKSPACE"/{subdomains,recon,scanning,exploitation,reports,logs}
    mkdir -p "$WORKSPACE"/subdomains/{passive,active,permutation,dns,validation}
    mkdir -p "$WORKSPACE"/recon/{http,technologies,content,endpoints}
    mkdir -p "$WORKSPACE"/scanning/{vulnerabilities,ports,ssl}
    
    cd "$WORKSPACE" || exit 1
    
    # Save target and config
    echo "$TARGET" > target.txt
    echo "$WORKSPACE" > workspace.txt
    echo "$(date)" > timestamp.txt
    
    echo -e "${GREEN}[✓] Workspace created: $(pwd)${NC}"
    log "Workspace setup completed for $TARGET"
}

# Phase 1: Passive Subdomain Discovery
passive_subdomain_discovery() {
    echo -e "\n${BLUE}===========================================${NC}"
    echo -e "${CYAN}🕵️  PHASE 1: PASSIVE SUBDOMAIN DISCOVERY${NC}"
    echo -e "${BLUE}===========================================${NC}"
    
    TARGET=$(cat target.txt)
    
    # Multiple passive sources in parallel
    echo -e "${YELLOW}[+] Starting passive subdomain enumeration...${NC}"
    
    # Subfinder with all sources
    echo -e "${PURPLE}[+] Running Subfinder...${NC}"
    subfinder -d "$TARGET" -all -silent -o subdomains/passive/subfinder.txt &
    
    # Assetfinder
    echo -e "${PURPLE}[+] Running Assetfinder...${NC}"
    assetfinder --subs-only "$TARGET" | anew subdomains/passive/assetfinder.txt &
    
    # Certificate Transparency
    echo -e "${PURPLE}[+] Checking Certificate Transparency logs...${NC}"
    curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | jq -r '.[].name_value' 2>/dev/null | grep -v "null" | anew subdomains/passive/crt.txt &
    
    # Historical data
    echo -e "${PURPLE}[+] Collecting historical data...${NC}"
    waybackurls "$TARGET" | unfurl -u domains | grep "$TARGET" | anew subdomains/passive/wayback.txt &
    gau "$TARGET" | unfurl -u domains | grep "$TARGET" | anew subdomains/passive/gau.txt &
    
    # Wait for all background jobs
    wait
    
    # Compile passive results
    cat subdomains/passive/*.txt 2>/dev/null | sort -u > subdomains/passive_all.txt
    PASSIVE_COUNT=$(wc -l < subdomains/passive_all.txt)
    
    echo -e "${GREEN}[✓] Passive discovery completed: $PASSIVE_COUNT subdomains found${NC}"
    log "Passive subdomain discovery: $PASSIVE_COUNT subdomains"
    notify "🔍 Passive Discovery Complete: $PASSIVE_COUNT subdomains found for $TARGET"
}

# Phase 2: Active Subdomain Discovery
active_subdomain_discovery() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${CYAN}🎯 PHASE 2: ACTIVE SUBDOMAIN DISCOVERY${NC}"
    echo -e "${BLUE}========================================${NC}"
    
    TARGET=$(cat target.txt)
    
    # Create comprehensive wordlist
    echo -e "${YELLOW}[+] Creating optimized wordlist...${NC}"
    cat > subdomains/custom_wordlist.txt << 'EOF'
www
mail
ftp
admin
test
dev
staging
prod
api
app
mobile
secure
vpn
portal
dashboard
panel
login
auth
oauth
sso
cdn
static
assets
media
img
images
video
videos
doc
docs
help
support
blog
news
forum
shop
store
payment
pay
billing
account
user
users
member
members
profile
settings
config
db
database
mysql
postgres
redis
elastic
search
solr
kibana
grafana
prometheus
jenkins
gitlab
github
bitbucket
jira
confluence
slack
teams
zoom
meet
calendar
drive
cloud
s3
aws
azure
gcp
docker
k8s
kubernetes
rancher
traefik
nginx
apache
haproxy
loadbalancer
lb
proxy
gateway
firewall
monitor
log
logs
metrics
status
health
ping
trace
debug
staging-api
dev-api
test-api
prod-api
api-dev
api-test
api-staging
api-prod
EOF
    
    # DNS Bruteforcing
    echo -e "${PURPLE}[+] Starting DNS bruteforce...${NC}"
    
    # Create resolvers list
    cat > resolvers.txt << 'EOF'
8.8.8.8
1.1.1.1
208.67.222.222
208.67.220.220
9.9.9.9
149.112.112.112
EOF
    
    # Shuffledns bruteforce
    if command -v shuffledns &> /dev/null; then
        echo -e "${PURPLE}[+] Running Shuffledns...${NC}"
        shuffledns -d "$TARGET" -w subdomains/custom_wordlist.txt -r resolvers.txt -o subdomains/active/shuffledns.txt -silent
    fi
    
    # Puredns bruteforce
    if command -v puredns &> /dev/null; then
        echo -e "${PURPLE}[+] Running Puredns...${NC}"
        puredns bruteforce subdomains/custom_wordlist.txt "$TARGET" -r resolvers.txt -w subdomains/active/puredns.txt
    fi
    
    # Compile active results
    cat subdomains/active/*.txt 2>/dev/null | sort -u > subdomains/active_all.txt
    ACTIVE_COUNT=$(wc -l < subdomains/active_all.txt)
    
    echo -e "${GREEN}[✓] Active discovery completed: $ACTIVE_COUNT new subdomains found${NC}"
    log "Active subdomain discovery: $ACTIVE_COUNT subdomains"
}

# Phase 3: Permutation & Mutation
permutation_discovery() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${CYAN}🔄 PHASE 3: PERMUTATION & MUTATION${NC}"
    echo -e "${BLUE}======================================${NC}"
    
    TARGET=$(cat target.txt)
    
    # Combine all found subdomains
    cat subdomains/passive_all.txt subdomains/active_all.txt 2>/dev/null | sort -u > subdomains/all_found.txt
    
    # Generate permutations
    echo -e "${YELLOW}[+] Generating permutations...${NC}"
    
    # Extract keywords from found subdomains
    cat subdomains/all_found.txt | sed 's/\.'$TARGET'//g' | sed 's/\./ /g' | tr ' ' '\n' | sort -u | grep -v '^$' > subdomains/keywords.txt
    
    # Create permutation script
    python3 << 'EOF'
import sys
import itertools

try:
    # Read keywords
    with open('subdomains/keywords.txt', 'r') as f:
        keywords = [line.strip() for line in f if line.strip() and len(line.strip()) > 1]
    
    # Read target
    with open('target.txt', 'r') as f:
        target = f.read().strip()
    
    common_prefixes = ['dev', 'test', 'stage', 'prod', 'api', 'app', 'admin', 'secure', 'new', 'old', 'beta']
    common_suffixes = ['01', '02', '03', '1', '2', '3', 'new', 'old', 'backup', 'temp', 'dev', 'test', 'bak']
    separators = ['-', '.', '_', '']
    
    permutations = set()
    
    # Generate permutations for each keyword
    for keyword in keywords[:20]:  # Limit to prevent explosion
        # Add original
        permutations.add(keyword)
        
        # Add with prefixes
        for prefix in common_prefixes:
            for sep in separators:
                if sep == '.' and prefix in ['api', 'app']:  # Avoid double dots
                    continue
                permutations.add(f"{prefix}{sep}{keyword}")
        
        # Add with suffixes
        for suffix in common_suffixes:
            for sep in separators:
                permutations.add(f"{keyword}{sep}{suffix}")
    
    # Write permutations to file
    with open('subdomains/permutations.txt', 'w') as f:
        for perm in sorted(permutations):
            if 2 <= len(perm) <= 30:  # Reasonable length
                f.write(f"{perm}\n")
    
    print(f"Generated {len(permutations)} permutations")

except Exception as e:
    print(f"Error generating permutations: {e}")
EOF
    
    # Test permutations if we have them
    if [ -f "subdomains/permutations.txt" ] && [ -s "subdomains/permutations.txt" ]; then
        echo -e "${PURPLE}[+] Testing permutations...${NC}"
        if command -v puredns &> /dev/null; then
            puredns bruteforce subdomains/permutations.txt "$TARGET" -r resolvers.txt -w subdomains/permutation/permutations.txt
        fi
    fi
    
    PERM_COUNT=$(cat subdomains/permutation/*.txt 2>/dev/null | wc -l)
    echo -e "${GREEN}[✓] Permutation discovery completed: $PERM_COUNT subdomains found${NC}"
    log "Permutation discovery: $PERM_COUNT subdomains"
}

# Phase 4: Subdomain Validation & Resolution
validate_subdomains() {
    echo -e "\n${BLUE}=====================================${NC}"
    echo -e "${CYAN}✅ PHASE 4: SUBDOMAIN VALIDATION${NC}"
    echo -e "${BLUE}=====================================${NC}"
    
    # Combine all subdomain sources
    echo -e "${YELLOW}[+] Combining all subdomain sources...${NC}"
    cat subdomains/passive_all.txt subdomains/active_all.txt subdomains/permutation/*.txt 2>/dev/null | sort -u > subdomains/all_subdomains.txt
    
    TOTAL_SUBDOMAINS=$(wc -l < subdomains/all_subdomains.txt)
    echo -e "${CYAN}[+] Total unique subdomains to validate: $TOTAL_SUBDOMAINS${NC}"
    
    # DNS Resolution
    echo -e "${PURPLE}[+] Resolving subdomains...${NC}"
    dnsx -l subdomains/all_subdomains.txt -json -a -aaaa -cname -mx -resp -o subdomains/validation/dns_resolution.json -silent
    
    # Extract resolved subdomains
    cat subdomains/validation/dns_resolution.json 2>/dev/null | jq -r 'select(.a != null or .aaaa != null) | .host' | sort -u > subdomains/validation/resolved.txt
    
    RESOLVED_COUNT=$(wc -l < subdomains/validation/resolved.txt)
    echo -e "${GREEN}[✓] Subdomain validation completed: $RESOLVED_COUNT resolved subdomains${NC}"
    log "Subdomain validation: $RESOLVED_COUNT resolved from $TOTAL_SUBDOMAINS"
    notify "✅ Validation Complete: $RESOLVED_COUNT live subdomains from $TOTAL_SUBDOMAINS total"
}

# Phase 5: HTTP Probing & Service Detection
http_probing() {
    echo -e "\n${BLUE}=====================================${NC}"
    echo -e "${CYAN}🌐 PHASE 5: HTTP PROBING & SERVICES${NC}"
    echo -e "${BLUE}=====================================${NC}"
    
    echo -e "${YELLOW}[+] HTTP/HTTPS probing...${NC}"
    
    # Comprehensive HTTP probing
    httpx -l subdomains/validation/resolved.txt \
          -follow-redirects \
          -status-code \
          -tech-detect \
          -title \
          -server \
          -cdn \
          -method \
          -websocket \
          -pipeline \
          -http2 \
          -json \
          -o recon/http/http_results.json \
          -silent
    
    # Extract live hosts
    cat recon/http/http_results.json 2>/dev/null | jq -r 'select(.status_code) | .url' | sort -u > recon/http/live_hosts.txt
    
    LIVE_COUNT=$(wc -l < recon/http/live_hosts.txt)
    echo -e "${GREEN}[✓] HTTP probing completed: $LIVE_COUNT live web services${NC}"
    log "HTTP probing: $LIVE_COUNT live web services"
    
    # Technology detection summary
    echo -e "${PURPLE}[+] Generating technology summary...${NC}"
    cat recon/http/http_results.json 2>/dev/null | jq -r '.tech[]?' 2>/dev/null | sort | uniq -c | sort -nr > recon/technologies/tech_summary.txt
    
    notify "🌐 HTTP Probing Complete: $LIVE_COUNT live web services detected"
}

# Phase 6: Port Scanning
port_scanning() {
    echo -e "\n${BLUE}==============================${NC}"
    echo -e "${CYAN}🔍 PHASE 6: PORT SCANNING${NC}"
    echo -e "${BLUE}==============================${NC}"
    
    echo -e "${YELLOW}[+] Scanning for web services on non-standard ports...${NC}"
    
    # Port scanning for web services
    naabu -l subdomains/validation/resolved.txt \
          -p 80,443,8080,8443,8000,8888,9000,9443,3000,5000,7000,7001,8001,8002,8008,8009,8081,8082,8083,8084,8090,8091,8092,8093,10000 \
          -json \
          -o scanning/ports/naabu_results.json \
          -silent
    
    # Extract hosts with open ports
    cat scanning/ports/naabu_results.json 2>/dev/null | jq -r '.host + ":" + (.port|tostring)' > scanning/ports/open_ports.txt
    
    PORT_COUNT=$(wc -l < scanning/ports/open_ports.txt)
    echo -e "${GREEN}[✓] Port scanning completed: $PORT_COUNT open ports found${NC}"
    log "Port scanning: $PORT_COUNT open ports"
}

# Phase 7: Content Discovery
content_discovery() {
    echo -e "\n${BLUE}=================================${NC}"
    echo -e "${CYAN}📁 PHASE 7: CONTENT DISCOVERY${NC}"
    echo -e "${BLUE}=================================${NC}"
    
    echo -e "${YELLOW}[+] Starting content discovery...${NC}"
    
    # Limit to top 10 hosts to avoid overwhelming
    head -10 recon/http/live_hosts.txt > recon/content/target_hosts.txt
    
    # Directory discovery
    echo -e "${PURPLE}[+] Directory discovery...${NC}"
    while read -r host; do
        if [ ! -z "$host" ]; then
            clean_host=$(echo "$host" | sed 's/[^a-zA-Z0-9]/_/g')
            echo -e "${CYAN}  [+] Fuzzing: $host${NC}"
            
            # Common directories
            ffuf -w /usr/share/wordlists/dirb/common.txt \
                 -u "$host/FUZZ" \
                 -mc 200,204,301,302,307,401,403 \
                 -ac \
                 -sf \
                 -o "recon/content/${clean_host}_dirs.json" \
                 -t 30 \
                 -timeout $TIMEOUT \
                 -s 2>/dev/null
            
            # API endpoints
            ffuf -w /usr/share/wordlists/dirb/common.txt \
                 -u "$host/api/FUZZ" \
                 -mc 200,204,301,302,307,401,403 \
                 -H "Content-Type: application/json" \
                 -ac \
                 -sf \
                 -o "recon/content/${clean_host}_api.json" \
                 -t 30 \
                 -timeout $TIMEOUT \
                 -s 2>/dev/null
        fi
    done < recon/content/target_hosts.txt
    
    # Common file discovery
    echo -e "${PURPLE}[+] Common file discovery...${NC}"
    httpx -l recon/content/target_hosts.txt \
          -path "/robots.txt,/sitemap.xml,/.well-known/security.txt,/security.txt,/.env,/config.php,/wp-config.php,/database.yml,/package.json,/composer.json" \
          -mc 200 \
          -silent \
          -o recon/content/interesting_files.txt
    
    CONTENT_COUNT=$(find recon/content/ -name "*.json" -type f | wc -l)
    echo -e "${GREEN}[✓] Content discovery completed: $CONTENT_COUNT content files analyzed${NC}"
    log "Content discovery: $CONTENT_COUNT files analyzed"
}

# Phase 8: Vulnerability Scanning
vulnerability_scanning() {
    echo -e "\n${BLUE}====================================${NC}"
    echo -e "${CYAN}🔒 PHASE 8: VULNERABILITY SCANNING${NC}"
    echo -e "${BLUE}====================================${NC}"
    
    echo -e "${YELLOW}[+] Running Nuclei vulnerability scans...${NC}"
    
    # Update nuclei templates
    nuclei -update-templates -silent
    
    # Run nuclei scans
    nuclei -l recon/http/live_hosts.txt \
           -es info \
           -o scanning/vulnerabilities/nuclei_results.txt \
           -json-export scanning/vulnerabilities/nuclei_results.json \
           -silent
    
    VULN_COUNT=$(wc -l < scanning/vulnerabilities/nuclei_results.txt 2>/dev/null || echo 0)
    
    if [ "$VULN_COUNT" -gt 0 ]; then
        echo -e "${RED}[!] Vulnerabilities found: $VULN_COUNT${NC}"
        notify "🚨 VULNERABILITIES FOUND: $VULN_COUNT issues detected!"
        
        # Generate severity summary
        cat scanning/vulnerabilities/nuclei_results.json 2>/dev/null | jq -r '.info.severity' | sort | uniq -c | sort -nr > scanning/vulnerabilities/severity_summary.txt
    else
        echo -e "${GREEN}[✓] No vulnerabilities detected${NC}"
    fi
    
    log "Vulnerability scanning: $VULN_COUNT vulnerabilities found"
}

# Phase 9: Report Generation
generate_report() {
    echo -e "\n${BLUE}==============================${NC}"
    echo -e "${CYAN}📊 PHASE 9: REPORT GENERATION${NC}"
    echo -e "${BLUE}==============================${NC}"
    
    TARGET=$(cat target.txt)
    WORKSPACE=$(cat workspace.txt)
    
    # Count statistics
    PASSIVE_SUBS=$(wc -l < subdomains/passive_all.txt 2>/dev/null || echo 0)
    ACTIVE_SUBS=$(wc -l < subdomains/active_all.txt 2>/dev/null || echo 0)
    RESOLVED_SUBS=$(wc -l < subdomains/validation/resolved.txt 2>/dev/null || echo 0)
    LIVE_HOSTS=$(wc -l < recon/http/live_hosts.txt 2>/dev/null || echo 0)
    OPEN_PORTS=$(wc -l < scanning/ports/open_ports.txt 2>/dev/null || echo 0)
    VULNERABILITIES=$(wc -l < scanning/vulnerabilities/nuclei_results.txt 2>/dev/null || echo 0)
    
    # Generate comprehensive report
    cat > reports/final_report.md << EOF
# 🎯 Bug Bounty Reconnaissance Report

**Target:** $TARGET  
**Date:** $(date)  
**Workspace:** $WORKSPACE  
**Duration:** $(( $(date +%s) - $(stat -c %Y timestamp.txt) )) seconds

---

## 📊 Executive Summary

| Metric | Count |
|--------|-------|
| 🔍 **Passive Subdomains** | $PASSIVE_SUBS |
| 🎯 **Active Subdomains** | $ACTIVE_SUBS |
| ✅ **Resolved Subdomains** | $RESOLVED_SUBS |
| 🌐 **Live Web Services** | $LIVE_HOSTS |
| 🔌 **Open Ports** | $OPEN_PORTS |
| 🚨 **Vulnerabilities** | $VULNERABILITIES |

---

## 🔍 Subdomain Discovery Results

### Passive Sources
\`\`\`
$(head -20 subdomains/passive_all.txt 2>/dev/null || echo "No passive subdomains found")
\`\`\`

### Active Discovery
\`\`\`
$(head -20 subdomains/active_all.txt 2>/dev/null || echo "No active subdomains found")
\`\`\`

### Resolved Subdomains
\`\`\`
$(head -20 subdomains/validation/resolved.txt 2>/dev/null || echo "No resolved subdomains")
\`\`\`

---

## 🌐 Live Web Services

\`\`\`
$(cat recon/http/live_hosts.txt 2>/dev/null || echo "No live hosts found")
\`\`\`

---

## 🔧 Technology Stack

$(cat recon/technologies/tech_summary.txt 2>/dev/null | head -10 || echo "No technology information available")

---

## 🔌 Open Ports

\`\`\`
$(cat scanning/ports/open_ports.txt 2>/dev/null || echo "No open ports found")
\`\`\`

---

## 🚨 Vulnerabilities

$(if [ "$VULNERABILITIES" -gt 0 ]; then
    echo "### Severity Breakdown"
    cat scanning/vulnerabilities/severity_summary.txt 2>/dev/null
    echo ""
    echo "### Vulnerability Details"
    echo "\`\`\`"
    head -20 scanning/vulnerabilities/nuclei_results.txt 2>/dev/null
    echo "\`\`\`"
else
    echo "✅ No vulnerabilities detected by automated scanning"
fi)

---

## 📁 Interesting Files

\`\`\`
$(cat recon/content/interesting_files.txt 2>/dev/null || echo "No interesting files found")
\`\`\`

---

## 🎯 Next Steps

1. **Manual Verification**
   - Verify automated findings
   - Test for false positives

2. **Deep Dive Analysis**
   - Focus on high-value targets
   - Business logic testing

3. **Advanced Testing**
   - Parameter discovery
   - Authentication bypass
   - Authorization issues

4. **Report Preparation**
   - Document findings
   - Create proof-of-concepts
   - Submit reports

---

## 📝 Notes

- All scanning was performed ethically and within scope
- Results should be manually verified before reporting
- Some findings may be false positives
- Additional manual testing recommended

---

*Report generated by Bug Bounty Automation Framework*  
*$(date)*
EOF

    # Generate JSON summary for automation
    cat > reports/summary.json << EOF
{
    "target": "$TARGET",
    "workspace": "$WORKSPACE",
    "timestamp": "$(date -Iseconds)",
    "statistics": {
        "passive_subdomains": $PASSIVE_SUBS,
        "active_subdomains": $ACTIVE_SUBS,
        "resolved_subdomains": $RESOLVED_SUBS,
        "live_hosts": $LIVE_HOSTS,
        "open_ports": $OPEN_PORTS,
        "vulnerabilities": $VULNERABILITIES
    }
}
EOF

    echo -e "${GREEN}[✓] Report generation completed${NC}"
    echo -e "${CYAN}📋 Report saved: reports/final_report.md${NC}"
    log "Report generation completed"
    
    notify "📊 Reconnaissance Complete for $TARGET! Report: $WORKSPACE/reports/final_report.md"
}

# Main execution function
main() {
    if [ $# -eq 0 ]; then
        echo -e "${RED}Usage: $0 <target.com> [options]${NC}"
        echo -e "${YELLOW}Options:${NC}"
        echo -e "  --passive-only    Only run passive reconnaissance"
        echo -e "  --quick          Quick scan (skip content discovery and vuln scanning)"
        echo -e "  --full           Full comprehensive scan (default)"
        exit 1
    fi
    
    TARGET="$1"
    MODE="${2:-full}"
    
    # Validate target
    if [[ ! "$TARGET" =~ ^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$ ]]; then
        echo -e "${RED}[-] Invalid target format. Please provide a valid domain (e.g., example.com)${NC}"
        exit 1
    fi
    
    print_banner "$TARGET"
    check_dependencies
    setup_workspace "$TARGET"
    
    # Execute phases based on mode
    case "$MODE" in
        "--passive-only")
            passive_subdomain_discovery
            validate_subdomains
            http_probing
            generate_report
            ;;
        "--quick")
            passive_subdomain_discovery
            active_subdomain_discovery
            validate_subdomains
            http_probing
            generate_report
            ;;
        "--full"|*)
            passive_subdomain_discovery
            active_subdomain_discovery
            permutation_discovery
            validate_subdomains
            http_probing
            port_scanning
            content_discovery
            vulnerability_scanning
            generate_report
            ;;
    esac
    
    echo -e "\n${GREEN}🎉 Reconnaissance completed successfully!${NC}"
    echo -e "${CYAN}📁 Results saved in: $(pwd)${NC}"
    echo -e "${YELLOW}📋 Report: $(pwd)/reports/final_report.md${NC}"
    
    # Final notification
    notify "🎉 Bug Bounty Reconnaissance COMPLETED for $TARGET! Workspace: $(pwd)"
}

# Script execution
main "$@"