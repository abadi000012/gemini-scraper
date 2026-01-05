#!/usr/bin/env python3
"""Quick test - writes results to file for verification"""

import sys
import asyncio
from datetime import datetime

def log(message):
    """Log to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}\n"
    print(msg, end='')
    with open('test_results.txt', 'a') as f:
        f.write(msg)

log("="*60)
log("Starting Scraper Test")
log("="*60)

# Test 1: Imports
log("\n1. Testing imports...")
try:
    import playwright
    log("   ✓ playwright")
except ImportError as e:
    log(f"   ✗ playwright: {e}")
    sys.exit(1)

try:
    from playwright_stealth import stealth_async
    log("   ✓ playwright-stealth")
except ImportError as e:
    log(f"   ✗ playwright-stealth: {e}")
    sys.exit(1)

try:
    import pandas as pd
    log("   ✓ pandas")
except ImportError as e:
    log(f"   ✗ pandas: {e}")
    sys.exit(1)

try:
    import requests
    log("   ✓ requests")
except ImportError as e:
    log(f"   ✗ requests: {e}")
    sys.exit(1)

try:
    from slugify import slugify
    log("   ✓ python-slugify")
except ImportError as e:
    log(f"   ✗ python-slugify: {e}")
    sys.exit(1)

try:
    from pydoll.browser import Chrome
    log("   ✓ pydoll-python")
    PYDoll_AVAILABLE = True
except ImportError:
    log("   ⚠️  pydoll-python (optional - not installed)")
    PYDoll_AVAILABLE = False

# Test 2: Import scraper functions
log("\n2. Testing scraper module imports...")
try:
    from scraper import (
        scrape_with_playwright,
        scrape_with_requests,
        scrape_with_pydoll,
        generate_filename,
        save_to_dataframe
    )
    log("   ✓ All scraper functions imported")
except ImportError as e:
    log(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 3: Test generate_filename
log("\n3. Testing utility functions...")
test_url = "https://www.example.com/test-page"
filename = generate_filename(test_url)
log(f"   ✓ generate_filename: {filename}")

# Test 4: Test requests scraper (fastest)
log("\n4. Testing requests scraper...")
try:
    result = scrape_with_requests("https://www.example.com", timeout=10)
    if result['status'] == 'success':
        log(f"   ✓ Requests scraper: SUCCESS")
        log(f"     Status code: {result.get('status_code')}")
        log(f"     Content length: {len(result.get('content', ''))} chars")
    else:
        log(f"   ✗ Requests scraper: {result['status']}")
except Exception as e:
    log(f"   ✗ Error: {e}")

# Test 5: Test Playwright scraper
log("\n5. Testing Playwright scraper (this may take 10-15 seconds)...")
try:
    result = asyncio.run(scrape_with_playwright("https://www.example.com", wait_time=2000))
    if result['status'] == 'success':
        log(f"   ✓ Playwright scraper: SUCCESS")
        log(f"     Title: {result.get('title', 'N/A')[:60]}")
        log(f"     Content length: {len(result.get('content', ''))} chars")
        log(f"     Text length: {len(result.get('text', ''))} chars")
    else:
        log(f"   ✗ Playwright scraper: {result['status']}")
except Exception as e:
    log(f"   ✗ Error: {e}")

# Test 6: Test Pydoll if available
if PYDoll_AVAILABLE:
    log("\n6. Testing Pydoll scraper (this may take 10-15 seconds)...")
    try:
        result = asyncio.run(scrape_with_pydoll("https://www.example.com", wait_time=2))
        if result['status'] == 'success':
            log(f"   ✓ Pydoll scraper: SUCCESS")
            log(f"     Title: {result.get('title', 'N/A')[:60]}")
            log(f"     Content length: {len(result.get('content', ''))} chars")
            log(f"     Text length: {len(result.get('text', ''))} chars")
        else:
            log(f"   ✗ Pydoll scraper: {result['status']}")
    except Exception as e:
        log(f"   ✗ Error: {e}")
else:
    log("\n6. Skipping Pydoll test (not installed)")

log("\n" + "="*60)
log("Test completed! Check test_results.txt for full log.")
log("="*60)

