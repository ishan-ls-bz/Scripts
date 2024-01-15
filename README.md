# QUIC.cloud Server Management Scripts

This repository contains Python scripts for automating server management tasks related to QUIC.cloud services. These scripts help maintain firewall rules, IP allowlists, and server configurations automatically.

## Overview

These scripts are designed to work with popular server management platforms and cloud services to ensure QUIC.cloud IP addresses are properly configured and maintained. They can be run manually or automated via cron jobs for continuous operation.

## Available Scripts

### 1. [Cloudflare Auto Update Script](cf/README.md)
**Location**: `cf/cloudflare-auto-update.py`

Automatically manages Cloudflare firewall rules for QUIC.cloud IP addresses:
- Fetches latest QUIC.cloud IP addresses
- Adds new IPs to Cloudflare allowlist
- Removes outdated IPs from firewall rules
- Progress tracking and detailed logging
- Secure credential management

**Use Case**: Cloudflare users who need to maintain up-to-date firewall rules for QUIC.cloud services.

### 2. [Plesk Fail2Ban Manager](plesk/README.md)
**Location**: `plesk/plesk_fail2ban.py`

Manages QUIC.cloud IP addresses in Plesk Fail2Ban trusted lists:
- Adds QUIC.cloud IPs to Plesk trusted IP list
- Removes IPs when needed
- Prevents Fail2Ban from blocking QUIC.cloud services
- Duplicate entry prevention

**Use Case**: Plesk server administrators using Fail2Ban who need to ensure QUIC.cloud services remain accessible.

## Requirements

- **Python 3.6 or higher**
- **Required packages**: `requests` (install via `pip install requests`)
- **Platform**: Linux, macOS, Windows (cross-platform compatible)

## Quick Start

1. **Clone or download** this repository
2. **Navigate** to the specific script directory
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Follow** the individual script README for setup and usage

## Installation

Each script has its own installation instructions and requirements. Please refer to the individual README files:

- [Cloudflare Script Setup](cf/README.md#installation)
- [Plesk Script Setup](plesk/README.md#installation)

## Usage

Scripts can be run manually or automated via cron jobs. See individual README files for specific usage examples:

- [Cloudflare Usage](cf/README.md#usage)
- [Plesk Usage](plesk/README.md#usage)

## Features

- **Automated IP Management**: Fetches and updates IP addresses automatically
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Error Handling**: Robust error handling and user feedback
- **Cron Integration**: Easy to set up as automated tasks
- **Secure**: Encrypted credential storage and validation
- **Progress Tracking**: Visual progress indicators for long operations

## Contributing

These scripts are designed to be maintainable and extensible. Feel free to:
- Report issues or bugs
- Suggest improvements
- Submit pull requests
- Adapt for other platforms

## License

This project is open source and available under the same license as the original QUIC.cloud scripts.

## Support

For issues related to:
- **Script functionality**: Check the individual script README files
- **QUIC.cloud services**: Contact QUIC.cloud support
- **Platform-specific issues**: Refer to platform documentation

---

**Note**: These are Python conversions of the original bash scripts, offering improved cross-platform compatibility and maintainability while preserving all original functionality. 