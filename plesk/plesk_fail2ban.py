#!/usr/bin/env python3

import json
import subprocess
import sys
import requests
from pathlib import Path

# Configuration
QUIC_CLOUD_IPS_URL = "https://quic.cloud/ips?json"
PLESK_CLI = "/usr/sbin/plesk"

def check_requirements():
    """Check if required tools are installed"""
    required_tools = ['jq', 'curl']
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"Error: {tool} is not installed. Please install it and rerun the script.")
            sys.exit(1)

def check_plesk_cli():
    """Verify if Plesk CLI exists"""
    if not Path(PLESK_CLI).is_file():
        print(f"Error: Plesk CLI not found at {PLESK_CLI}. Please verify the path.")
        sys.exit(1)

def get_quic_cloud_ips():
    """Fetch the QUIC.cloud IP list"""
    try:
        response = requests.get(QUIC_CLOUD_IPS_URL)
        if response.status_code != 200:
            print("Error: Failed to fetch IP list from QUIC.cloud.")
            sys.exit(1)
        
        return response.json()
    except Exception as e:
        print(f"Error: Failed to fetch IP list from QUIC.cloud: {e}")
        sys.exit(1)

def get_trusted_ips():
    """Get the current list of trusted IPs from Plesk"""
    try:
        result = subprocess.run(
            [PLESK_CLI, 'bin', 'ip_ban', '--trusted'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse output and extract IPs
        ips = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                ip = line.split()[0]  # First column is the IP
                ips.append(ip)
        
        return ips
    except subprocess.CalledProcessError as e:
        print(f"Error getting trusted IPs: {e}")
        return []

def add_ips(ips):
    """Add IPs to the trusted list"""
    total = len(ips)
    added = 0
    skipped = 0
    
    print("Fetching current trusted IPs...")
    current_ips = get_trusted_ips()
    print(f"Total IPs to add: {total}")
    
    for i, ip in enumerate(ips, 1):
        print(f"\rProcessing: {i}/{total}", end="", flush=True)
        
        if ip in current_ips:
            skipped += 1
        else:
            try:
                result = subprocess.run(
                    [PLESK_CLI, 'bin', 'ip_ban', '--add-trusted', ip],
                    capture_output=True,
                    check=True
                )
                added += 1
            except subprocess.CalledProcessError:
                pass  # IP addition failed
    
    print(f"\n\nSummary: Added: {added} | Skipped: {skipped}\n")

def remove_ips(ips):
    """Remove IPs from the trusted list"""
    total = len(ips)
    removed = 0
    not_found = 0
    
    print("Fetching current trusted IPs...")
    current_ips = get_trusted_ips()
    print(f"Total IPs to remove: {total}")
    
    for i, ip in enumerate(ips, 1):
        print(f"\rProcessing: {i}/{total}", end="", flush=True)
        
        if ip in current_ips:
            try:
                result = subprocess.run(
                    [PLESK_CLI, 'bin', 'ip_ban', '--remove-trusted', ip],
                    capture_output=True,
                    check=True
                )
                removed += 1
            except subprocess.CalledProcessError:
                pass  # IP removal failed
        else:
            not_found += 1
    
    print(f"\n\nSummary: Removed: {removed} | Not Found: {not_found}\n")

def main():
    # Check requirements
    check_requirements()
    check_plesk_cli()
    
    # Check for script arguments
    if len(sys.argv) != 2:
        print("Usage: python3 plesk_fail2ban.py -add | -delete")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action not in ['-add', '-delete']:
        print("Usage: python3 plesk_fail2ban.py -add | -delete")
        sys.exit(1)
    
    # Get QUIC.cloud IPs
    ips = get_quic_cloud_ips()
    
    if action == '-add':
        add_ips(ips)
    elif action == '-delete':
        remove_ips(ips)

if __name__ == "__main__":
    main() 