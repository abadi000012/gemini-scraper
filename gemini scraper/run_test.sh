#!/bin/bash
# Simple test script for the scraper

cd "/Users/aba/Documents/gemini scraper"

echo "=========================================="
echo "Testing Gemini Scraper"
echo "=========================================="
echo ""

echo "1. Checking Python version..."
python3 --version
echo ""

echo "2. Testing imports..."
python3 -c "
import sys
errors = []

try:
    import playwright
    print('  ✓ playwright')
except ImportError as e:
    print(f'  ✗ playwright: {e}')
    errors.append('playwright')

try:
    from playwright_stealth import stealth_async
    print('  ✓ playwright-stealth')
except ImportError as e:
    print(f'  ✗ playwright-stealth: {e}')
    errors.append('playwright-stealth')

try:
    import pandas
    print('  ✓ pandas')
except ImportError as e:
    print(f'  ✗ pandas: {e}')
    errors.append('pandas')

try:
    import requests
    print('  ✓ requests')
except ImportError as e:
    print(f'  ✗ requests: {e}')
    errors.append('requests')

try:
    from slugify import slugify
    print('  ✓ python-slugify')
except ImportError as e:
    print(f'  ✗ python-slugify: {e}')
    errors.append('python-slugify')

try:
    from pydoll.browser import Chrome
    print('  ✓ pydoll-python')
except ImportError:
    print('  ⚠️  pydoll-python (optional - not installed)')

if errors:
    print(f'\n✗ Missing dependencies: {", ".join(errors)}')
    print('Install with: pip3 install ' + ' '.join(errors))
    sys.exit(1)
else:
    print('\n✓ All required dependencies installed!')
"

echo ""
echo "3. Testing scraper module..."
python3 -c "
from scraper import scrape_with_requests, generate_filename
print('  ✓ Module imports successfully')

# Test generate_filename
filename = generate_filename('https://www.example.com/test')
print(f'  ✓ generate_filename works: {filename}')

# Quick test with requests
print('  Testing requests scraper...')
result = scrape_with_requests('https://www.example.com', timeout=5)
if result['status'] == 'success':
    print(f'  ✓ Requests scraper works! (Status: {result.get(\"status_code\")})')
else:
    print(f'  ✗ Requests scraper failed: {result[\"status\"]}')
"

echo ""
echo "=========================================="
echo "Test completed!"
echo "=========================================="
echo ""
echo "To run the full scraper:"
echo "  python3 scraper.py"
echo ""
echo "To scrape Alibaba products:"
echo "  python3 scrape_alibaba.py"
echo ""

