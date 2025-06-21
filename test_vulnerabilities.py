#!/usr/bin/env python3
"""
Vulnerability Test Script
Tests that the vulnerability patterns in this repository can be detected.
"""

import os
import re
import json
import csv
from pathlib import Path

class VulnerabilityTester:
    def __init__(self):
        self.results = {
            'secrets_found': 0,
            'pii_patterns': 0,
            'config_issues': 0,
            'log_violations': 0,
            'total_files_scanned': 0
        }
        
    def scan_for_secrets(self, content, filename):
        """Scan for hardcoded secrets and API keys"""
        secret_patterns = [
            r'sk_live_[a-zA-Z0-9]+',  # Stripe keys
            r'AKIA[0-9A-Z]{16}',      # AWS Access Keys
            r'AIza[0-9A-Za-z\\-_]{35}', # Google API Keys
            r'ghp_[0-9a-zA-Z]{36}',   # GitHub tokens
            r'TWL[a-f0-9]{32}',       # Twilio SIDs
            r'password.*[:=]\s*["\']?[^"\'\s]+',  # Passwords
            r'secret.*[:=]\s*["\']?[^"\'\s]+',    # Secrets
        ]
        
        for pattern in secret_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.results['secrets_found'] += len(matches)
                print(f"  [SECRETS] Found {len(matches)} secrets in {filename}")
                
    def scan_for_pii(self, content, filename):
        """Scan for PII patterns"""
        pii_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',     # SSN
            r'\b4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit cards
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
            r'\b\d{3}-\d{3}-\d{4}\b',     # Phone numbers
            r'\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b',  # Addresses
        ]
        
        for pattern in pii_patterns:
            matches = re.findall(pattern, content)
            if matches:
                self.results['pii_patterns'] += len(matches)
                print(f"  [PII] Found {len(matches)} PII patterns in {filename}")
                
    def scan_file(self, filepath):
        """Scan individual file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                filename = os.path.basename(filepath)
                
                self.scan_for_secrets(content, filename)
                self.scan_for_pii(content, filename)
                
                # Check for specific vulnerability patterns
                if 'password' in content.lower() and 'admin123' in content:
                    self.results['config_issues'] += 1
                    print(f"  [CONFIG] Found weak admin password in {filename}")
                    
                if filename.endswith('.log') and any(word in content.lower() for word in ['ssn', 'credit', 'password']):
                    self.results['log_violations'] += 1
                    print(f"  [LOGS] Found PII in log file {filename}")
                    
                self.results['total_files_scanned'] += 1
                
        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
            
    def run_tests(self):
        """Run vulnerability detection tests"""
        print("🔍 Running Vulnerability Detection Tests")
        print("=" * 50)
        
        # Scan all files in repository
        repo_root = Path('.')
        target_files = [
            '*.py', '*.js', '*.json', '*.env', '*.log', '*.txt', 
            '*.csv', '*.sql', '*.yml', '*.yaml', '*.md'
        ]
        
        for pattern in target_files:
            for filepath in repo_root.glob(pattern):
                if filepath.name not in ['.git', '__pycache__', 'node_modules']:
                    print(f"\nScanning: {filepath}")
                    self.scan_file(filepath)
                    
        # Print results
        print("\n" + "=" * 50)
        print("📊 VULNERABILITY DETECTION RESULTS")
        print("=" * 50)
        print(f"Total files scanned: {self.results['total_files_scanned']}")
        print(f"Secrets/API keys found: {self.results['secrets_found']}")
        print(f"PII patterns detected: {self.results['pii_patterns']}")
        print(f"Configuration issues: {self.results['config_issues']}")
        print(f"Log file violations: {self.results['log_violations']}")
        
        total_issues = (self.results['secrets_found'] + 
                       self.results['pii_patterns'] + 
                       self.results['config_issues'] + 
                       self.results['log_violations'])
        
        print(f"\nTotal vulnerability patterns detected: {total_issues}")
        
        if total_issues >= 100:
            print("✅ PASS: Repository contains sufficient vulnerability patterns for testing")
        else:
            print("⚠️  WARNING: Low vulnerability count detected")
            
        return self.results

def main():
    """Main function"""
    print("Privacy Test Repository - Vulnerability Detection Test")
    print("This script validates that vulnerability patterns can be detected by scanning tools.\n")
    
    tester = VulnerabilityTester()
    results = tester.run_tests()
    
    # Save results to JSON
    with open('vulnerability_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: vulnerability_test_results.json")

if __name__ == "__main__":
    main()