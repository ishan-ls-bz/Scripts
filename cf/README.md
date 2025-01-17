# Cloudflare Auto Update Script (Python)

This Python script is designed to automate the process of allowlisting and managing IP addresses for QUIC.cloud services on Cloudflare. It allows you to easily add or remove IP addresses based on the latest data from QUIC.cloud, ensuring your firewall rules are up to date.

## Features

- Automatically fetches the latest QUIC.cloud IP addresses.
- Allowlists new IP addresses in your Cloudflare account.
- Deletes QUIC.cloud IP addresses on your request.
- Progress indicators for both allowlisting and deletion processes.
- Simple to set up and run with cron jobs.
- Cross-platform compatibility (Linux, macOS, Windows).

## Requirements

- Python 3.6 or higher
- A Cloudflare account with an API key
- Required Python packages (install via pip):
  ```bash
  pip install requests
  ```

## Installation

1. Download the script:
   ```bash
   wget -q https://raw.githubusercontent.com/ishan-ls-bz/Scripts/main/cf/cloudflare-auto-update.py -P /opt/
   ```

2. Make the script executable:
   ```bash
   chmod +x /opt/cloudflare-auto-update.py
   ```

3. Install required Python packages:
   ```bash
   pip3 install requests
   ```

4. Set up your Cloudflare credentials: Run the script with the configure option or directly to set up credentials:
   - Direct
     ```bash
     python3 /opt/cloudflare-auto-update.py
     ```
   - Run the script with the configure option
     ```bash
     python3 /opt/cloudflare-auto-update.py --configure
     ```

To find those credentials:
* CF_EMAIL: simply your email for your account. Can be found on the top left corner of the Cloudflare website;
* CF_API_KEY: Go to your profile (top right corner icon) -> My Profile -> API Tokens -> Global API Key => View ;
* CF_ZONE_ID: Go to your home dashboard -> click on your website domain -> the Zone ID is at the bottom right side of the screen (see [this tutorial](https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/)).

## Usage

You can run the script manually or set it up as a cron job for automated execution.

1. **Manual Execution**
   - To allowlist IPs:
     ```bash
     python3 /opt/cloudflare-auto-update.py
     ```
   - To delete QUIC.cloud IPs:
     ```bash
     python3 /opt/cloudflare-auto-update.py delete
     ```

2. **Cron Job Setup** \
    To run the script daily at midnight, add the following line to your crontab:
    ```bash
    0 0 * * * python3 /opt/cloudflare-auto-update.py
    ```

## Python vs Bash Version

This Python version offers several advantages over the original bash script:
- Better error handling and exception management
- Cross-platform compatibility
- More maintainable and readable code
- Built-in JSON parsing (no external jq dependency)
- Better progress tracking and user feedback
- More robust credential validation

## Troubleshooting

- Ensure Python 3.6+ is installed: `python3 --version`
- Install required packages: `pip3 install requests`
- Check script permissions: `ls -la /opt/cloudflare-auto-update.py`
- Verify Cloudflare credentials are correctly configured
