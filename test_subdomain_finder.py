#!/usr/bin/env python3
"""
Test script for Advanced Subdomain Discovery Tool
এই script টি tool এর বিভিন্ন functionality test করে
"""

import sys
import os
import time
import traceback
from pathlib import Path

# Add the main script to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the main classes
try:
    from advanced_subdomain_finder import AdvancedSubdomainFinder, Colors, logger
    from config import get_comprehensive_wordlist, create_default_config
    print(f"{Colors.GREEN}[✓] Successfully imported all modules{Colors.END}")
except ImportError as e:
    print(f"{Colors.RED}[✗] Import error: {e}{Colors.END}")
    traceback.print_exc()
    sys.exit(1)

def test_config_loading():
    """Configuration loading test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing configuration loading...{Colors.END}")
    
    try:
        # Test config creation
        config = create_default_config()
        print(f"{Colors.GREEN}[✓] Default config creation successful{Colors.END}")
        
        # Test wordlist generation
        wordlist = get_comprehensive_wordlist()
        print(f"{Colors.GREEN}[✓] Wordlist generation successful ({len(wordlist)} words){Colors.END}")
        
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Config test failed: {e}{Colors.END}")
        return False

def test_class_initialization():
    """Class initialization test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing class initialization...{Colors.END}")
    
    try:
        # Test with valid domain
        finder = AdvancedSubdomainFinder("example.com", threads=10, timeout=5)
        print(f"{Colors.GREEN}[✓] Class initialization successful{Colors.END}")
        print(f"    - Domain: {finder.domain}")
        print(f"    - Threads: {finder.threads}")
        print(f"    - Timeout: {finder.timeout}")
        print(f"    - Resolvers: {len(finder.resolvers)}")
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Class initialization failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_dns_functionality():
    """DNS functionality test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing DNS functionality...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("google.com", threads=5, timeout=5)
        
        # Test wildcard detection
        print("  - Testing wildcard detection...")
        finder.check_wildcard()
        print(f"{Colors.GREEN}[✓] Wildcard detection completed{Colors.END}")
        
        # Test single DNS lookup
        print("  - Testing DNS lookup...")
        result = finder.dns_bruteforce("www")
        if result:
            print(f"{Colors.GREEN}[✓] DNS lookup successful (found www.google.com){Colors.END}")
        else:
            print(f"{Colors.YELLOW}[!] DNS lookup completed (no new findings){Colors.END}")
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] DNS functionality test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_wordlist_loading():
    """Wordlist loading test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing wordlist loading...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("example.com", threads=5, timeout=5)
        
        # Test default wordlist
        wordlist = finder.load_wordlist()
        print(f"{Colors.GREEN}[✓] Default wordlist loaded ({len(wordlist)} words){Colors.END}")
        
        # Test with custom wordlist
        test_wordlist_file = Path("test_wordlist.txt")
        with open(test_wordlist_file, 'w') as f:
            f.write("www\napi\nmail\ntest\n")
        
        custom_wordlist = finder.load_wordlist(str(test_wordlist_file))
        print(f"{Colors.GREEN}[✓] Custom wordlist loaded ({len(custom_wordlist)} words){Colors.END}")
        
        # Cleanup
        test_wordlist_file.unlink()
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Wordlist loading test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_ai_functionality():
    """AI functionality test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing AI functionality...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("example.com", threads=5, timeout=5)
        
        # Test AI prediction
        predictions = finder.ai_predictor.predict("example.com", num_predictions=10)
        print(f"{Colors.GREEN}[✓] AI prediction successful ({len(predictions)} predictions){Colors.END}")
        
        # Show some predictions
        if predictions:
            print(f"    - Sample predictions: {predictions[:3]}")
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] AI functionality test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_output_functionality():
    """Output functionality test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing output functionality...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("example.com", threads=5, timeout=5)
        
        # Add some test data
        finder.found_subdomains.add("www.example.com")
        finder.found_subdomains.add("api.example.com")
        finder.live_subdomains.add("www.example.com")
        
        # Test saving results
        finder.save_results("test_results")
        
        # Check if files were created
        txt_file = finder.output_dir / "test_results.txt"
        csv_file = finder.output_dir / "test_results.csv"
        json_file = finder.output_dir / "test_results.json"
        
        if txt_file.exists() and csv_file.exists() and json_file.exists():
            print(f"{Colors.GREEN}[✓] Output files created successfully{Colors.END}")
            print(f"    - TXT: {txt_file}")
            print(f"    - CSV: {csv_file}")
            print(f"    - JSON: {json_file}")
            
            # Cleanup test files
            txt_file.unlink()
            csv_file.unlink()
            json_file.unlink()
        else:
            print(f"{Colors.RED}[✗] Some output files missing{Colors.END}")
            return False
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Output functionality test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_certificate_transparency():
    """Certificate Transparency functionality test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing Certificate Transparency...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("google.com", threads=5, timeout=5)
        
        # Test CT search (limited to avoid rate limiting)
        initial_count = len(finder.found_subdomains)
        finder.certificate_transparency()
        final_count = len(finder.found_subdomains)
        
        print(f"{Colors.GREEN}[✓] Certificate Transparency search completed{Colors.END}")
        print(f"    - Found {final_count - initial_count} new subdomains from CT logs")
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Certificate Transparency test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def test_rate_limiting():
    """Rate limiting functionality test করে"""
    print(f"\n{Colors.YELLOW}[*] Testing rate limiting...{Colors.END}")
    
    try:
        finder = AdvancedSubdomainFinder("example.com", threads=5, timeout=5)
        
        # Test DNS rate limiting
        start_time = time.time()
        for i in range(3):
            finder.rate_limit_dns()
        dns_time = time.time() - start_time
        
        # Test HTTP rate limiting  
        start_time = time.time()
        for i in range(3):
            finder.rate_limit_http()
        http_time = time.time() - start_time
        
        print(f"{Colors.GREEN}[✓] Rate limiting functional{Colors.END}")
        print(f"    - DNS rate limiting time: {dns_time:.2f}s")
        print(f"    - HTTP rate limiting time: {http_time:.2f}s")
        
        # Cleanup
        finder.cleanup()
        return True
    except Exception as e:
        print(f"{Colors.RED}[✗] Rate limiting test failed: {e}{Colors.END}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║              ADVANCED SUBDOMAIN FINDER - TEST SUITE           ║")
    print("║                    Functionality Testing                      ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    # Run all tests
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Class Initialization", test_class_initialization),
        ("Wordlist Loading", test_wordlist_loading),
        ("AI Functionality", test_ai_functionality),
        ("Output Functionality", test_output_functionality),
        ("DNS Functionality", test_dns_functionality),
        ("Certificate Transparency", test_certificate_transparency),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}Running Test: {test_name}{Colors.END}")
        print(f"{Colors.BLUE}{'='*60}{Colors.END}")
        
        try:
            if test_func():
                passed += 1
                print(f"{Colors.GREEN}[✓] {test_name} PASSED{Colors.END}")
            else:
                failed += 1
                print(f"{Colors.RED}[✗] {test_name} FAILED{Colors.END}")
        except Exception as e:
            failed += 1
            print(f"{Colors.RED}[✗] {test_name} FAILED with exception: {e}{Colors.END}")
    
    # Final summary
    print(f"\n{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                        TEST SUMMARY                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    total_tests = passed + failed
    print(f"{Colors.YELLOW}Total Tests: {total_tests}{Colors.END}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {failed}{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! Tool is ready to use.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed. Please check the errors above.{Colors.END}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Test interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error during testing: {e}{Colors.END}")
        traceback.print_exc()
        sys.exit(1)