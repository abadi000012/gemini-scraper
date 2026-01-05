# Gemini Scraper

A powerful web scraping tool with multiple automation options: **Pydoll** (evasion-first), **Playwright with stealth mode**, and **Requests**. Includes pandas integration and python-slugify for file management.

## Installation

1. Install Python libraries:
```bash
pip3 install playwright playwright-stealth pandas requests python-slugify pydoll-python
```

2. Install the Chromium browser for Playwright:
```bash
python3 -m playwright install chromium
```

**Note:** Pydoll uses your system's Chrome/Chromium browser. Make sure Chrome is installed on your system.

## Usage

Run the scraper:
```bash
python3 scraper.py
```

The script will:
1. Prompt you to enter URLs to scrape
2. Ask you to choose between:
   - **Pydoll** (evasion-first, best for anti-bot sites)
   - **Playwright** (with stealth mode, handles JavaScript)
   - **Requests** (faster, simpler, no JavaScript)
3. Scrape the URLs
4. Save results to `scraping_results.csv`
5. Save individual page contents to files with slugified filenames

## Features

- **Pydoll (Evasion-First)**: Best for bypassing anti-bot systems, human-like interactions, built-in fingerprint evasion
- **Playwright with Stealth Mode**: Bypass bot detection, handle JavaScript-rendered content
- **Requests**: Fast, simple scraping for static content
- **Pandas Integration**: Export results to CSV
- **Slugify**: Generate safe filenames from URLs
- **Error Handling**: Graceful error handling for failed requests

## Scraping Alibaba Products

For scraping Alibaba product pages (which have strong anti-bot protection), use:
```bash
python3 scrape_alibaba.py
```

This script automatically uses Pydoll if available (best for anti-bot evasion), or falls back to Playwright with stealth mode.

## Requirements

- Python 3.7+
- See `requirements.txt` for package versions

