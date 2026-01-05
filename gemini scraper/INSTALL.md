# Complete Installation Guide

## Quick Install (All Commands in One)

Run this single command to install everything:

```bash
cd "/Users/aba/Documents/gemini scraper" && \
pip3 install playwright playwright-stealth pandas requests python-slugify --user && \
python3 -m playwright install chromium
```

Or use the installation script:

```bash
cd "/Users/aba/Documents/gemini scraper"
chmod +x install_all.sh
./install_all.sh
```

## Step-by-Step Installation

### 1. Install Python Packages

```bash
pip3 install playwright playwright-stealth pandas requests python-slugify --user
```

**What this installs:**
- `playwright` - Browser automation framework
- `playwright-stealth` - Anti-bot detection evasion
- `pandas` - Data processing and CSV export
- `requests` - HTTP library for downloading images
- `python-slugify` - URL to filename conversion

### 2. Install Playwright Browser

```bash
python3 -m playwright install chromium
```

This downloads the Chromium browser that Playwright uses.

### 3. Verify Installation

```bash
python3 -c "
import playwright
from playwright_stealth import stealth_sync
import pandas
import requests
from slugify import slugify
print('✓ All dependencies installed successfully!')
"
```

## Troubleshooting

### If `pip3` command not found:
- On macOS, use: `python3 -m pip install ...`
- Make sure Python 3 is installed: `python3 --version`

### If `playwright` command not found:
- Use: `python3 -m playwright install chromium`
- This is the correct way to run Playwright commands

### If you get permission errors:
- Add `--user` flag to pip install commands
- This installs packages to your user directory

## After Installation

Run the scraper:

```bash
cd "/Users/aba/Documents/gemini scraper"
python3 alibaba_image_scraper.py
```

