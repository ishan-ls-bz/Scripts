# QUIC.cloud IPs Fail2Ban Trusted List Manager (Python)

This Python script automates the process of adding and removing QUIC.cloud IPs to/from the Plesk Fail2Ban Trusted (Allow) List. By doing so, it ensures that QUIC.cloud IPs are never blocked by Fail2Ban, improving reliability for LiteSpeed services.

## Features

- Fetches the latest QUIC.cloud IPs automatically
- Adds IPs to the Fail2Ban Trusted List in Plesk
- Removes IPs from the Trusted List if needed
- Prevents duplicate entries
- Logs added and removed IPs for tracking
- Cross-platform compatibility (Linux, macOS, Windows)

## Requirements

- Python 3.6 or higher
- Plesk server with Fail2Ban enabled
- Required Python packages (install via pip):
  ```bash
  pip install requests
  ```
- System tools: `jq` and `curl` (for compatibility checks)

## Installation

1. Download the script using the following command:
   ```bash
   wget https://raw.githubusercontent.com/ishan-ls-bz/Scripts/main/plesk/plesk_fail2ban.py
   ```

2. Make the script executable:
   ```bash
   chmod +x plesk_fail2ban.py
   ```

3. Install required Python packages:
   ```bash
   pip3 install requests
   ```

## Usage

You can run the script manually or set it up as a cron job for automated execution.

1. **Manual Execution**
   - Add QUIC.cloud IPs to Trusted List:
     ```bash
     python3 plesk_fail2ban.py -add
     ```
   - Remove QUIC.cloud IPs from Trusted List:
     ```bash
     python3 plesk_fail2ban.py -delete
     ```

2. **Cron Job Setup** \
    To run the script daily at midnight, add the following line to your crontab:
    ```bash
    0 0 * * * python3 /path/to/plesk_fail2ban.py -add
    ```

## Python vs Bash Version

This Python version offers several advantages over the original bash script:
- Better error handling and exception management
- Cross-platform compatibility
- More maintainable and readable code
- Built-in JSON parsing (no external jq dependency)
- Better progress tracking and user feedback
- More robust subprocess management

## Troubleshooting

- Ensure Python 3.6+ is installed: `python3 --version`
- Install required packages: `pip3 install requests`
- Check script permissions: `ls -la plesk_fail2ban.py`
- Verify Plesk CLI path: `/usr/sbin/plesk`
- Ensure system tools are available: `jq --version` and `curl --version`
