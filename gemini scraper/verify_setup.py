#!/usr/bin/env python3
"""Verify all dependencies are installed for alibaba_image_scraper.py"""

import sys

print("="*60)
print("Verifying Dependencies for Alibaba Image Scraper")
print("="*60)
print()

missing = []
errors = []

# Check playwright
try:
    from playwright.sync_api import sync_playwright
    print("✓ playwright")
except ImportError as e:
    print(f"✗ playwright - {e}")
    missing.append("playwright")
    errors.append("playwright")

# Check playwright-stealth
try:
    from playwright_stealth import stealth_sync
    print("✓ playwright-stealth")
except ImportError as e:
    print(f"✗ playwright-stealth - {e}")
    missing.append("playwright-stealth")
    errors.append("playwright-stealth")

# Check pandas
try:
    import pandas as pd
    print("✓ pandas")
except ImportError as e:
    print(f"✗ pandas - {e}")
    missing.append("pandas")
    errors.append("pandas")

# Check requests
try:
    import requests
    print("✓ requests")
except ImportError as e:
    print(f"✗ requests - {e}")
    missing.append("requests")
    errors.append("requests")

# Check python-slugify
try:
    from slugify import slugify
    print("✓ python-slugify")
except ImportError as e:
    print(f"✗ python-slugify - {e}")
    missing.append("python-slugify")
    errors.append("python-slugify")

print()
print("="*60)

if missing:
    print("❌ MISSING DEPENDENCIES:")
    print(f"   Run: pip3 install {' '.join(missing)}")
    print()
    print("Then install Playwright browser:")
    print("   playwright install chromium")
    sys.exit(1)
else:
    print("✅ All dependencies installed!")
    print()
    print("To start the scraper:")
    print("   python3 alibaba_image_scraper.py")
    sys.exit(0)

