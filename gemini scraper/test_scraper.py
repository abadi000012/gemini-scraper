#!/usr/bin/env python3
"""
Quick test script to verify the scraper is working
"""

import asyncio
import sys

# Test imports
print("Testing imports...")
try:
    import playwright
    print("✓ playwright")
except ImportError as e:
    print(f"✗ playwright: {e}")
    sys.exit(1)

try:
    from playwright_stealth import stealth_async
    print("✓ playwright-stealth")
except ImportError as e:
    print(f"✗ playwright-stealth: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("✓ pandas")
except ImportError as e:
    print(f"✗ pandas: {e}")
    sys.exit(1)

try:
    import requests
    print("✓ requests")
except ImportError as e:
    print(f"✗ requests: {e}")
    sys.exit(1)

try:
    from slugify import slugify
    print("✓ python-slugify")
except ImportError as e:
    print(f"✗ python-slugify: {e}")
    sys.exit(1)

try:
    from pydoll.browser import Chrome
    print("✓ pydoll-python")
    PYDoll_AVAILABLE = True
except ImportError:
    print("⚠️  pydoll-python (optional - not installed)")
    PYDoll_AVAILABLE = False

print("\n" + "="*50)
print("Testing scraper functions...")
print("="*50)

# Test the scraper module
try:
    from scraper import (
        scrape_with_playwright,
        scrape_with_requests,
        scrape_with_pydoll,
        generate_filename,
        save_to_dataframe
    )
    print("✓ All scraper functions imported successfully")
except ImportError as e:
    print(f"✗ Error importing scraper functions: {e}")
    sys.exit(1)

# Test generate_filename
test_url = "https://www.example.com/test-page"
filename = generate_filename(test_url)
print(f"✓ generate_filename works: {filename}")

# Test with a simple URL using requests (fastest)
print("\nTesting requests scraper with example.com...")
try:
    result = scrape_with_requests("https://www.example.com", timeout=10)
    if result['status'] == 'success':
        print(f"✓ Requests scraper works!")
        print(f"  Status code: {result.get('status_code')}")
        print(f"  Content length: {len(result.get('content', ''))} chars")
    else:
        print(f"✗ Requests scraper failed: {result['status']}")
except Exception as e:
    print(f"✗ Error testing requests scraper: {e}")

# Test Playwright scraper
print("\nTesting Playwright scraper with example.com...")
print("(This may take a few seconds...)")
try:
    result = asyncio.run(scrape_with_playwright("https://www.example.com", wait_time=2000))
    if result['status'] == 'success':
        print(f"✓ Playwright scraper works!")
        print(f"  Title: {result.get('title', 'N/A')[:50]}")
        print(f"  Content length: {len(result.get('content', ''))} chars")
        print(f"  Text length: {len(result.get('text', ''))} chars")
    else:
        print(f"✗ Playwright scraper failed: {result['status']}")
except Exception as e:
    print(f"✗ Error testing Playwright scraper: {e}")

# Test Pydoll scraper if available
if PYDoll_AVAILABLE:
    print("\nTesting Pydoll scraper with example.com...")
    print("(This may take a few seconds...)")
    try:
        result = asyncio.run(scrape_with_pydoll("https://www.example.com", wait_time=2))
        if result['status'] == 'success':
            print(f"✓ Pydoll scraper works!")
            print(f"  Title: {result.get('title', 'N/A')[:50]}")
            print(f"  Content length: {len(result.get('content', ''))} chars")
            print(f"  Text length: {len(result.get('text', ''))} chars")
        else:
            print(f"✗ Pydoll scraper failed: {result['status']}")
    except Exception as e:
        print(f"✗ Error testing Pydoll scraper: {e}")
else:
    print("\n⚠️  Skipping Pydoll test (not installed)")

print("\n" + "="*50)
print("✓ All tests completed!")
print("="*50)

