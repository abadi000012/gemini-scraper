#!/usr/bin/env python3
"""Test Playwright browser installation"""

from playwright.sync_api import sync_playwright
import sys

print("Testing Playwright browser installation...")
print("=" * 50)

try:
    with sync_playwright() as p:
        print("1. Playwright instance created ✓")
        
        # Check if chromium is installed
        try:
            browser_type = p.chromium
            print("2. Chromium browser type available ✓")
        except Exception as e:
            print(f"2. Chromium not available: {e}")
            sys.exit(1)
        
        # Try to launch browser
        print("3. Attempting to launch browser...")
        try:
            browser = p.chromium.launch(headless=False)
            print("   ✓ Browser launched successfully")
            
            # Wait a moment
            import time
            time.sleep(2)
            
            # Try to create context
            print("4. Attempting to create context...")
            try:
                context = browser.new_context()
                print("   ✓ Context created successfully")
                
                # Try to create page
                print("5. Attempting to create page...")
                try:
                    page = context.new_page()
                    print("   ✓ Page created successfully")
                    
                    # Try to navigate
                    print("6. Attempting to navigate to test page...")
                    page.goto('https://www.example.com', timeout=10000)
                    print("   ✓ Navigation successful")
                    
                    title = page.title()
                    print(f"   Page title: {title}")
                    
                    # Clean up
                    page.close()
                    context.close()
                    browser.close()
                    
                    print("\n" + "=" * 50)
                    print("✓ All tests passed! Browser is working correctly.")
                    print("=" * 50)
                    
                except Exception as e:
                    print(f"   ✗ Page creation failed: {e}")
                    browser.close()
                    sys.exit(1)
                    
            except Exception as e:
                print(f"   ✗ Context creation failed: {e}")
                print("   This is the error you're experiencing.")
                browser.close()
                sys.exit(1)
                
        except Exception as e:
            print(f"   ✗ Browser launch failed: {e}")
            print("\nTroubleshooting:")
            print("1. Try: python3 -m playwright install --force chromium")
            print("2. Check if Chrome/Chromium is installed on your system")
            print("3. Try running with headless=True to see if it's a display issue")
            sys.exit(1)
            
except Exception as e:
    print(f"✗ Playwright error: {e}")
    sys.exit(1)

