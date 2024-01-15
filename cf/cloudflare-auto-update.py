#!/usr/bin/env python3

import json
import base64
import os
import sys
import requests
import time
from pathlib import Path
from datetime import datetime

# Configuration
CONFIG_FILE = "config.json"
CONFIG_DIR = os.path.expanduser("~/.cloudflare-auto-update")
CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

def print_box(message):
    """Print message in a box format"""
    lines = message.split('\n')
    max_length = max(len(line) for line in lines) if lines else 0
    
    print(f"\n+{'-' * (max_length + 2)}+")
    for line in lines:
        print(f"| {line:<{max_length}} |")
    print(f"+{'-' * (max_length + 2)}+")

def show_progress(current, total, operation="Processing"):
    """Show progress bar"""
    if total == 0:
        return
    
    progress_percent = int((current * 100) / total)
    bar_length = 50
    filled_bar = int((current * bar_length) / total)
    empty_bar = bar_length - filled_bar
    
    bar = "#" * filled_bar + " " * empty_bar
    print(f"\r{operation}: [{bar}] {progress_percent}% ({current}/{total})", end="", flush=True)

def configure_credentials():
    """Prompt for credentials and save them"""
    print("\nPlease enter your Cloudflare credentials:")
    
    cf_email = input("Cloudflare Email: ").strip()
    cf_api_key = input("Cloudflare API Key: ").strip()
    cf_zone_id = input("Cloudflare Zone ID: ").strip()
    
    if not cf_email or not cf_api_key or not cf_zone_id:
        print("\nAuthentication error: One or more credential inputs are empty.\n")
        return False
    
    # Validate credentials
    if not validate_credentials(cf_email, cf_api_key, cf_zone_id):
        print("Credential validation failed. Configuration not saved.")
        return False
    
    # Encode credentials
    encoded_email = base64.b64encode(cf_email.encode()).decode()
    encoded_api_key = base64.b64encode(cf_api_key.encode()).decode()
    encoded_zone_id = base64.b64encode(cf_zone_id.encode()).decode()
    
    # Save config
    config = {
        "email": encoded_email,
        "api_key": encoded_api_key,
        "zone_id": encoded_zone_id
    }
    
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\nConfig saved to {CONFIG_PATH}\n")
        return True
    except Exception as e:
        print(f"Error: Failed to save config to {CONFIG_PATH}: {e}")
        return False

def load_credentials():
    """Load credentials from config file"""
    if not os.path.exists(CONFIG_PATH):
        print(f"Config file not found at {CONFIG_PATH}. Please configure credentials.")
        configure_credentials()
        return None, None, None
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        
        cf_email = base64.b64decode(config['email']).decode()
        cf_api_key = base64.b64decode(config['api_key']).decode()
        cf_zone_id = base64.b64decode(config['zone_id']).decode()
        
        return cf_email, cf_api_key, cf_zone_id
    except Exception as e:
        print(f"Error loading config: {e}")
        return None, None, None

def validate_credentials(email, api_key, zone_id):
    """Validate Cloudflare credentials"""
    if not email or not api_key or not zone_id:
        print("\nAuthentication error: One or more credential inputs are empty.\n")
        return False
    
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"\nAuthentication error: HTTP {response.status_code}\n")
            return False
        
        data = response.json()
        if not data.get('success'):
            print("\nAuthentication error: Invalid Cloudflare credentials.\n")
            return False
        
        return True
    except Exception as e:
        print(f"\nAuthentication error: {e}\n")
        return False

def get_quic_cloud_ips():
    """Fetch QUIC.cloud IPs"""
    url = "https://quic.cloud/ips?json"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Unable to access QUIC.cloud IPs (HTTP status: {response.status_code}).")
            return None
        
        return response.json()
    except Exception as e:
        print(f"Error fetching QUIC.cloud IPs: {e}")
        return None

def get_script_managed_rules(email, api_key, zone_id):
    """Get all allowlisted rules added by this script"""
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    ids = []
    page = 1
    
    while True:
        try:
            response = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules",
                headers=headers,
                params={"page": page, "per_page": 50}
            )
            
            if response.status_code != 200:
                break
            
            data = response.json()
            
            for rule in data.get('result', []):
                notes = rule.get('notes', '')
                if 'QUIC.cloud IP, IP allowed on ' in notes:
                    ids.append(rule['id'])
            
            total_pages = data.get('result_info', {}).get('total_pages', 0)
            if page >= total_pages:
                break
            
            page += 1
        except Exception as e:
            print(f"Error fetching rules: {e}")
            break
    
    return ids

def get_script_managed_ips(email, api_key, zone_id):
    """Get rule IPs added by this script"""
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    ips = []
    page = 1
    
    while True:
        try:
            response = requests.get(
                f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules",
                headers=headers,
                params={"page": page, "per_page": 50}
            )
            
            if response.status_code != 200:
                break
            
            data = response.json()
            
            for rule in data.get('result', []):
                notes = rule.get('notes', '')
                if 'QUIC.cloud IP, IP allowed on ' in notes:
                    ips.append(rule['configuration']['value'])
            
            total_pages = data.get('result_info', {}).get('total_pages', 0)
            if page >= total_pages:
                break
            
            page += 1
        except Exception as e:
            print(f"Error fetching rules: {e}")
            break
    
    return ips

def delete_rule(email, api_key, zone_id, rule_id):
    """Delete a firewall rule"""
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules/{rule_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('success', False)
        return False
    except Exception:
        return False

def add_rule(email, api_key, zone_id, ip, notes):
    """Add a new firewall rule"""
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "mode": "whitelist",
        "configuration": {
            "target": "ip",
            "value": ip
        },
        "notes": notes
    }
    
    try:
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('success', False)
        return False
    except Exception:
        return False

def main():
    # Check for --configure flag
    if len(sys.argv) > 1 and sys.argv[1] == "--configure":
        configure_credentials()
        return
    
    # Check for delete mode
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        print("Deleting all QUIC.cloud IPs added by this script...")
        
        # Load credentials
        cf_email, cf_api_key, cf_zone_id = load_credentials()
        if not cf_email:
            return
        
        # Get script managed rules
        script_managed_rule_ids = get_script_managed_rules(cf_email, cf_api_key, cf_zone_id)
        total_ips = len(script_managed_rule_ids)
        
        if total_ips == 0:
            print("No QUIC.cloud IPs found to delete.")
            return
        
        total_deleted = 0
        for i, rule_id in enumerate(script_managed_rule_ids):
            if delete_rule(cf_email, cf_api_key, cf_zone_id, rule_id):
                total_deleted += 1
            
            show_progress(i + 1, total_ips, "Deleting")
        
        print()  # New line after progress bar
        print_box(f"Successfully deleted {total_deleted} QUIC.cloud IPs from the CF WAF.")
        return
    
    # Load credentials
    cf_email, cf_api_key, cf_zone_id = load_credentials()
    if not cf_email:
        return
    
    # Get QUIC.cloud IPs
    quic_cloud_ips = get_quic_cloud_ips()
    if not quic_cloud_ips:
        return
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Remove outdated IPs
    print("Removing outdated IPs...")
    current_managed_ips = get_script_managed_ips(cf_email, cf_api_key, cf_zone_id)
    ips_to_remove = []
    
    for ip in current_managed_ips:
        if ip not in quic_cloud_ips:
            # Find rule ID for this IP
            headers = {
                "X-Auth-Email": cf_email,
                "X-Auth-Key": cf_api_key,
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(
                    f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/firewall/access_rules/rules",
                    headers=headers,
                    params={"configuration.value": ip}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('result'):
                        rule_id = data['result'][0]['id']
                        ips_to_remove.append(rule_id)
            except Exception:
                continue
    
    # Remove outdated IPs
    progress = 0
    total_ips = len(ips_to_remove)
    removed = 0
    
    if total_ips == 0:
        print("No outdated IPs to remove.")
    else:
        for rule_id in ips_to_remove:
            if delete_rule(cf_email, cf_api_key, cf_zone_id, rule_id):
                removed += 1
            
            progress += 1
            show_progress(progress, total_ips, "Removing")
        
        print()  # New line after progress bar
    
    # Add new IPs
    print("\nAdding new IPs...")
    ips_to_add = [ip for ip in quic_cloud_ips if ip not in current_managed_ips]
    
    progress = 0
    total_ips = len(ips_to_add)
    added = 0
    
    if total_ips == 0:
        print("No new IPs to add.")
    else:
        for ip in ips_to_add:
            notes = f"QUIC.cloud IP, IP allowed on {current_date}"
            if add_rule(cf_email, cf_api_key, cf_zone_id, ip, notes):
                added += 1
            
            progress += 1
            show_progress(progress, total_ips, "Adding")
        
        print()  # New line after progress bar
    
    # Summary output
    print_box(f"Successfully added {added} IPs and removed {removed} outdated IPs from CF WAF.")

if __name__ == "__main__":
    main() 