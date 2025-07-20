#!/bin/bash

# 🔥 Bug Bounty Toolkit Setup Script
# ===================================
# Sets up the complete bug bounty hunting toolkit
# Author: Advanced Bug Bounty Hunter

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_banner() {
    echo -e "${CYAN}"
    echo "🔥 Bug Bounty Toolkit Setup"
    echo "============================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}[✓] $1${NC}"
}

print_info() {
    echo -e "${BLUE}[+] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[!] $1${NC}"
}

print_error() {
    echo -e "${RED}[-] $1${NC}"
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. Some tools may not work properly."
        read -p "Continue anyway? (y/N): " confirm
        if [[ $confirm != [yY] ]]; then
            exit 1
        fi
    fi
}

# Install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."
    
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y curl wget git python3 python3-pip golang-go nodejs npm jq unzip
    elif command -v yum &> /dev/null; then
        sudo yum update -y
        sudo yum install -y curl wget git python3 python3-pip golang nodejs npm jq unzip
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu --noconfirm curl wget git python3 python-pip go nodejs npm jq unzip
    else
        print_error "Unsupported package manager. Please install dependencies manually."
        exit 1
    fi
    
    print_success "System dependencies installed"
}

# Install Go tools
install_go_tools() {
    print_info "Installing Go-based security tools..."
    
    # Set Go environment
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    
    # Add to shell profile
    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
    
    # Install tools
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
    go install -v github.com/projectdiscovery/katana/cmd/katana@latest
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
    go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
    go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
    go install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest
    go install github.com/tomnomnom/assetfinder@latest
    go install github.com/tomnomnom/anew@latest
    go install github.com/tomnomnom/unfurl@latest
    go install github.com/lc/gau/v2/cmd/gau@latest
    go install github.com/tomnomnom/waybackurls@latest
    go install github.com/ffuf/ffuf@latest
    go install github.com/d3mondev/puredns/v2@latest
    
    print_success "Go tools installed"
}

# Install Python tools
install_python_tools() {
    print_info "Installing Python tools..."
    
    pip3 install --user requests beautifulsoup4 urllib3 dnspython
    pip3 install --user markdown weasyprint pygments
    
    # Install dirsearch
    if [ ! -d "$HOME/tools/dirsearch" ]; then
        mkdir -p $HOME/tools
        cd $HOME/tools
        git clone https://github.com/maurosoria/dirsearch.git
        cd dirsearch
        pip3 install -r requirements.txt
        cd -
    fi
    
    print_success "Python tools installed"
}

# Install additional tools
install_additional_tools() {
    print_info "Installing additional tools..."
    
    # Create tools directory
    mkdir -p $HOME/tools
    
    # Install Findomain
    if ! command -v findomain &> /dev/null; then
        curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux
        chmod +x findomain-linux
        sudo mv findomain-linux /usr/local/bin/findomain
    fi
    
    # Install Amass
    if ! command -v amass &> /dev/null; then
        if command -v snap &> /dev/null; then
            sudo snap install amass
        else
            print_warning "Snap not available. Please install Amass manually."
        fi
    fi
    
    # Download SecLists
    if [ ! -d "$HOME/wordlists/SecLists" ]; then
        mkdir -p $HOME/wordlists
        cd $HOME/wordlists
        git clone https://github.com/danielmiessler/SecLists.git
        cd -
    fi
    
    print_success "Additional tools installed"
}

# Make scripts executable
setup_scripts() {
    print_info "Setting up bug bounty scripts..."
    
    # Make all shell scripts executable
    chmod +x *.sh 2>/dev/null || true
    chmod +x *.py 2>/dev/null || true
    
    # Create symlinks in user bin
    mkdir -p $HOME/.local/bin
    
    # Link main automation script
    if [ -f "master_recon_automation.sh" ]; then
        ln -sf "$(pwd)/master_recon_automation.sh" "$HOME/.local/bin/bug-bounty-recon"
        print_success "Created symlink: bug-bounty-recon"
    fi
    
    # Link PDF converter
    if [ -f "convert_to_pdf.py" ]; then
        ln -sf "$(pwd)/convert_to_pdf.py" "$HOME/.local/bin/md2pdf"
        print_success "Created symlink: md2pdf"
    fi
    
    # Add to PATH if not already there
    if ! echo $PATH | grep -q "$HOME/.local/bin"; then
        echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
        export PATH=$PATH:$HOME/.local/bin
    fi
    
    print_success "Scripts setup completed"
}

# Create configuration files
create_configs() {
    print_info "Creating configuration files..."
    
    # Create resolvers file
    cat > $HOME/resolvers.txt << 'EOF'
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
208.67.222.222
208.67.220.220
9.9.9.9
149.112.112.112
64.6.64.6
64.6.65.6
77.88.8.8
77.88.8.1
EOF

    # Create notification config template
    cat > $HOME/.bug_bounty_config << 'EOF'
# Bug Bounty Configuration
# Set your API keys and webhook URLs here

# Telegram Bot Configuration
export TELEGRAM_BOT_TOKEN=""
export TELEGRAM_CHAT_ID=""

# Discord Webhook
export DISCORD_WEBHOOK=""

# API Keys
export SECURITYTRAILS_API=""
export SHODAN_API=""
export VIRUSTOTAL_API=""

# Load this file in your .bashrc:
# source ~/.bug_bounty_config
EOF

    print_success "Configuration files created"
    print_info "Edit ~/.bug_bounty_config to add your API keys"
}

# Create directory structure
create_directories() {
    print_info "Creating directory structure..."
    
    mkdir -p $HOME/{bug-bounty-results,wordlists,tools,scripts}
    mkdir -p $HOME/bug-bounty-results/{targets,reports,automation-logs}
    
    print_success "Directory structure created"
}

# Update nuclei templates
update_nuclei() {
    print_info "Updating Nuclei templates..."
    
    if command -v nuclei &> /dev/null; then
        nuclei -update-templates -silent
        print_success "Nuclei templates updated"
    else
        print_warning "Nuclei not found, skipping template update"
    fi
}

# Generate usage instructions
generate_usage() {
    cat > USAGE.md << 'EOF'
# 🔥 Bug Bounty Toolkit Usage Guide

## 🚀 Quick Start

### 1. Run Complete Automation
```bash
# Full reconnaissance
bug-bounty-recon example.com --full

# Quick scan
bug-bounty-recon example.com --quick

# Passive only
bug-bounty-recon example.com --passive-only
```

### 2. Generate PDF Guide
```bash
# Convert markdown to PDF
md2pdf -i bug_bounty_advanced_guide.md -o guide.pdf

# Enhanced version
md2pdf --enhanced -o enhanced_guide.pdf
```

## 📁 Directory Structure

```
~/
├── bug-bounty-results/     # All scan results
│   ├── targets/           # Per-target directories
│   ├── reports/           # Generated reports
│   └── automation-logs/   # Automation logs
├── wordlists/             # Custom wordlists
│   └── SecLists/         # Downloaded SecLists
├── tools/                 # Additional tools
└── scripts/              # Custom scripts
```

## 🔧 Individual Scripts

### Subdomain Enumeration
```bash
./advanced_subdomain_enum.sh example.com
```

### Passive Reconnaissance
```bash
./passive_recon.sh example.com
```

### HTTP Probing
```bash
./http_probing.sh
```

### Content Discovery
```bash
./content_discovery.sh
```

### Vulnerability Scanning
```bash
./vulnerability_testing.sh example.com
```

## ⚙️ Configuration

### Set API Keys
Edit `~/.bug_bounty_config`:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export SECURITYTRAILS_API="your_api_key"
```

Load configuration:
```bash
source ~/.bug_bounty_config
```

### Notification Setup

#### Telegram
1. Create a bot with @BotFather
2. Get bot token
3. Get your chat ID
4. Add to config file

#### Discord
1. Create webhook in Discord server
2. Add webhook URL to config

## 📊 Reporting

### Manual Report Generation
```bash
./generate_report.sh target.com
```

### Convert to PDF
```bash
python3 convert_to_pdf.py -i report.md -o report.pdf
```

## 🎯 Best Practices

1. **Always check scope** before testing
2. **Use VPN** for anonymity
3. **Rate limit** your requests
4. **Keep logs** of all activities
5. **Verify findings** manually

## 🔍 Troubleshooting

### Tool Not Found
```bash
# Check if in PATH
which subfinder

# Reinstall Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### Permission Denied
```bash
# Make scripts executable
chmod +x *.sh

# Fix ownership
sudo chown -R $USER:$USER $HOME/tools/
```

### DNS Resolution Issues
```bash
# Update resolvers
cat > ~/resolvers.txt << EOF
8.8.8.8
1.1.1.1
EOF
```

## 📚 Learning Resources

- **Documentation**: Check each tool's GitHub page
- **Community**: Join bug bounty Discord/Telegram groups
- **Practice**: Use platforms like HackTheBox, TryHackMe
- **Stay Updated**: Follow security researchers on Twitter

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review tool documentation
3. Search for similar issues online
4. Ask in bug bounty communities

---

*Happy Hunting! 🎯*
EOF

    print_success "Usage guide created: USAGE.md"
}

# Main setup function
main() {
    print_banner
    
    print_info "Starting Bug Bounty Toolkit setup..."
    echo
    
    # Check prerequisites
    check_root
    
    # Installation steps
    install_system_deps
    echo
    
    install_go_tools
    echo
    
    install_python_tools
    echo
    
    install_additional_tools
    echo
    
    # Setup
    setup_scripts
    echo
    
    create_configs
    echo
    
    create_directories
    echo
    
    update_nuclei
    echo
    
    generate_usage
    echo
    
    # Final steps
    print_success "Bug Bounty Toolkit setup completed!"
    echo
    print_info "Next steps:"
    echo -e "  1. ${YELLOW}source ~/.bashrc${NC} (to load new PATH)"
    echo -e "  2. ${YELLOW}source ~/.bug_bounty_config${NC} (after adding API keys)"
    echo -e "  3. ${YELLOW}cat USAGE.md${NC} (for usage instructions)"
    echo
    print_info "Quick test:"
    echo -e "  ${CYAN}bug-bounty-recon --help${NC}"
    echo
    
    # Tool verification
    print_info "Verifying tool installation..."
    TOOLS=("subfinder" "httpx" "nuclei" "ffuf" "dnsx")
    
    for tool in "${TOOLS[@]}"; do
        if command -v "$tool" &> /dev/null; then
            print_success "$tool installed"
        else
            print_warning "$tool not found in PATH"
        fi
    done
    
    echo
    print_success "Setup complete! Happy hunting! 🎯"
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi