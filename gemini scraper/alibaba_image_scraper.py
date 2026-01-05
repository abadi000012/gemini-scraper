#!/usr/bin/env python3
"""
Alibaba Product Image Scraper (Anti-Detection Mode)
Advanced version with navigator.webdriver hiding and infinite pause on blocks
"""

import os
import time
import random
import re
import requests
import pandas as pd
from slugify import slugify
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
URLS = [
    "https://www.alibaba.com/product-detail/Chancee-K80-Factory-Price-Concrete-Double_1600874046823.html",
    "https://www.alibaba.com/product-detail/Compact-Large-Ride-On-Street-Vacuum_1601427314632.html",
    "https://www.alibaba.com/product-detail/48V-Electric-Double-Brush-Ride-On_1601445626156.html"
]

OUTPUT_CSV = "alibaba_products.csv"
IMAGE_DIR_ROOT = "scraped_images"

# --- HELPER FUNCTIONS ---

def create_directory(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def clean_alibaba_image_url(url):
    """Clean Alibaba image URLs to get high-res version."""
    if not url:
        return None
    url = url.split('?')[0]
    clean_url = re.sub(r'(_\d+x\d+.*$|\.jpg_.*$|\.png_.*$)', '', url)
    if clean_url.startswith("//"):
        clean_url = "https:" + clean_url
    return clean_url

def download_image_authenticated(url, folder_path, image_name, cookies, user_agent):
    """Download image with browser cookies and user agent for authentication."""
    headers = {
        'User-Agent': user_agent,
        'Referer': 'https://www.alibaba.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    session_cookies = {c['name']: c['value'] for c in cookies}
    
    try:
        response = requests.get(url, headers=headers, cookies=session_cookies, stream=True, timeout=20)
        if response.status_code == 200:
            file_extension = "jpg"
            if "." in url:
                candidate = url.split('.')[-1].split('?')[0].split('_')[0]
                if len(candidate) in [3, 4] and candidate.lower() in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                    file_extension = candidate.lower()
            
            filename = f"{image_name}.{file_extension}"
            file_path = os.path.join(folder_path, filename)
            
            total_size = 0
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
            
            # Verify file was downloaded
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                file_size_kb = total_size / 1024
                print(f"    ✓ Downloaded: {filename} ({file_size_kb:.1f} KB)")
                return file_path
            else:
                print(f"    ✗ File is empty: {filename}")
                if os.path.exists(file_path):
                    os.remove(file_path)
                return None
        else:
            print(f"    ✗ HTTP {response.status_code} for image")
            return None
    except Exception as e:
        print(f"    ❌ Download error: {e}")
    return None

def human_scroll(page):
    """Scrolls with random pauses to look human."""
    print("  Scrolling (human-like)...")
    for _ in range(random.randint(3, 5)):
        scroll_amount = random.randint(300, 700)
        page.mouse.wheel(0, scroll_amount)
        page.wait_for_timeout(random.randint(500, 1500))
    # Scroll back up a bit
    page.mouse.wheel(0, -1000)
    page.wait_for_timeout(1000)
    print("  ✓ Scrolling completed")

# --- MAIN LOGIC ---

def run_scraper():
    """Main scraper function with anti-detection features."""
    print(f"\n{'='*70}")
    print("Alibaba Scraper (Anti-Detection Mode)")
    print(f"{'='*70}")
    
    create_directory(IMAGE_DIR_ROOT)
    scraped_data = []

    with sync_playwright() as p:
        print("\n1. Launching Safari (WebKit)...")
        browser = p.webkit.launch(headless=False)
        print("   ✓ Browser launched")
        
        # High-res viewport and specific locale
        print("2. Creating browser context...")
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15',
            locale='en-US',
            timezone_id='Asia/Riyadh'  # Matches your region to look consistent
        )
        print("   ✓ Context created")

        # *** CRITICAL: REMOVE AUTOMATION FLAGS ***
        # This script runs on every page load to hide "navigator.webdriver"
        print("3. Injecting anti-detection scripts...")
        context.add_init_script("""
            // Hide webdriver flag
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Chrome runtime (for compatibility)
            window.chrome = {
                runtime: {}
            };
            
            // Remove automation indicators
            delete navigator.__proto__.webdriver;
        """)
        print("   ✓ Anti-detection scripts injected")
        
        page = context.new_page()
        print("   ✓ Page created")

        # 1. Warm up on Homepage
        print("\n4. Warming up on Homepage...")
        try:
            page.goto("https://www.alibaba.com", timeout=60000)
            page.wait_for_timeout(3000)
            print("   ✓ Homepage loaded")
        except Exception as e:
            print(f"   ⚠️  Homepage warm-up failed: {e}")

        print("\n" + "="*70)
        print("Starting product scraping...")
        print("="*70)

        for index, url in enumerate(URLS):
            print(f"\n[{index+1}/{len(URLS)}] Processing: {url[:60]}...")
            print("-" * 70)
            
            # --- NAVIGATION & BLOCK CHECK LOOP ---
            while True:
                try:
                    print("  Navigating to page...")
                    page.goto(url, timeout=60000, wait_until='domcontentloaded')
                    page.wait_for_timeout(2000)

                    # Check for Block/Login indicators
                    is_blocked = False
                    current_url = page.url.lower()
                    
                    if "login" in current_url or "punish" in current_url or "security" in current_url:
                        is_blocked = True
                    
                    # Also check page title
                    try:
                        title_text = page.title().lower()
                        if "security" in title_text or "robot" in title_text or "verify" in title_text or "captcha" in title_text:
                            is_blocked = True
                    except:
                        pass

                    if is_blocked:
                        print("\n" + "🛑" * 35)
                        print("🛑 BLOCKED! 🛑")
                        print("🛑" * 35)
                        print("\nThe script is PAUSED.")
                        print("1. Go to the browser window.")
                        print("2. Slide the slider / Solve the captcha.")
                        print("3. Wait for the product page to fully load.")
                        print("4. Make sure you can see the product title and images.")
                        print("\n" + "-" * 70)
                        input(">>> PRESS ENTER HERE ONCE THE PAGE IS NORMAL <<<")
                        print("-" * 70)
                        continue  # Retry the loop
                    
                    # If we are here, we are not blocked. Wait for H1.
                    try:
                        page.wait_for_selector('h1', timeout=10000)
                        print("  ✓ Page loaded successfully")
                        break  # Success! Break the retry loop
                    except:
                        print("  ⚠️  Page loaded but no Title found. Assuming block/glitch.")
                        input(">>> PLEASE FIX PAGE MANUALLY & PRESS ENTER <<<")
                        continue

                except Exception as e:
                    print(f"  ⚠️  Navigation error: {e}")
                    input(">>> CHECK BROWSER & PRESS ENTER TO RETRY <<<")

            # --- SCRAPING START ---
            print("  ✅ Page loaded. Starting data extraction...")
            human_scroll(page)

            # Extract Title
            try:
                title = page.locator('h1').first.inner_text().strip()
                print(f"  ✓ Product: {title[:50]}...")
            except Exception as e:
                print(f"  ✗ Could not extract title: {e}")
                title = "N/A"
            
            product_slug = slugify(title, max_length=50)
            product_path = os.path.join(IMAGE_DIR_ROOT, product_slug)
            create_directory(product_path)

            # Extract Price
            price = "N/A"
            price_selectors = ['.price', '.product-price', '.ma-price-wrap', '.main-price', '.promotion-price', '[class*="price"]']
            for sel in price_selectors:
                try:
                    if page.locator(sel).count() > 0:
                        price = page.locator(sel).first.inner_text().strip()
                        print(f"  ✓ Price: {price[:50]}")
                        break
                except:
                    continue
            if price == "N/A":
                print("  ⚠️  Price not found")

            # Extract MOQ
            moq = "N/A"
            try:
                moq_loc = page.get_by_text(re.compile(r"Min.*Order", re.IGNORECASE))
                if moq_loc.count() > 0:
                    moq = moq_loc.first.inner_text().strip()
                    print(f"  ✓ MOQ: {moq[:50]}")
            except:
                print("  ⚠️  MOQ not found")

            # Extract Images
            print("  Grabbing images...")
            image_urls = set()
            downloaded_paths = []

            # 2024 Selectors
            thumb_selectors = [
                '.main-image-thumb-ul li',
                '.image-list li',
                '.detail-next-slick-slide',
                '.main-image-thumb-item',
                '[class*="thumb"] li',
                '[class*="thumbnail"] li'
            ]
            
            thumbs = []
            for ts in thumb_selectors:
                try:
                    if page.locator(ts).count() > 0:
                        thumbs = page.locator(ts).all()
                        print(f"  ✓ Found {len(thumbs)} thumbnails")
                        break
                except:
                    continue
            
            main_img_sel = '.main-image img, .detail-main-image img, .image-viewer-img, .image-view img, [class*="main-image"] img'

            # Get Main Image First (Always exists)
            try:
                if page.locator(main_img_sel).count() > 0:
                    src = page.locator(main_img_sel).first.get_attribute('src')
                    if src:
                        clean = clean_alibaba_image_url(src)
                        if clean:
                            image_urls.add(clean)
                            print("  ✓ Found main image")
            except Exception as e:
                print(f"  ⚠️  Could not get main image: {e}")

            # Click Thumbs to get more images
            if len(thumbs) > 0:
                print(f"  Processing {min(len(thumbs), 6)} thumbnails...")
                for i, thumb in enumerate(thumbs[:6]):  # Limit to 6 images
                    try:
                        thumb.scroll_into_view_if_needed()
                        thumb.hover()
                        page.wait_for_timeout(random.randint(200, 400))
                        thumb.click(force=True)
                        page.wait_for_timeout(random.randint(600, 1000))
                        
                        if page.locator(main_img_sel).count() > 0:
                            src = page.locator(main_img_sel).first.get_attribute('src')
                            if src:
                                clean = clean_alibaba_image_url(src)
                                if clean:
                                    image_urls.add(clean)
                                    print(f"    ✓ Image {i+1}: Found")
                    except Exception as e:
                        print(f"    ⚠️  Thumbnail {i+1} error: {e}")
                        continue

            print(f"  ✓ Found {len(image_urls)} unique images")
            
            # Download images with authentication
            if image_urls:
                print("  Downloading images...")
                current_cookies = context.cookies()
                user_agent = page.evaluate("navigator.userAgent")
                
                for i, img_url in enumerate(image_urls):
                    local = download_image_authenticated(
                        img_url,
                        product_path,
                        f"img_{i+1:02d}",
                        current_cookies,
                        user_agent
                    )
                    if local:
                        downloaded_paths.append(local)
            else:
                print("  ⚠️  No images found to download")

            # Save data
            scraped_data.append({
                "Product Title": title,
                "Price": price,
                "Min Order Quantity": moq,
                "Source URL": url,
                "Images Count": len(downloaded_paths),
                "Local Images": " | ".join(downloaded_paths) if downloaded_paths else "None"
            })
            print(f"  ✓ Product data saved: {title[:40]}...")

            # Random sleep between products (except last one)
            if index < len(URLS) - 1:
                delay = random.uniform(8, 15)
                print(f"\n  ⏳ Sleeping {delay:.1f}s before next product...")
                time.sleep(delay)

        print("\n" + "="*70)
        print("Closing browser...")
        browser.close()
        print("✓ Browser closed")

    # Write CSV
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print(f"\n{'='*70}")
        print(f"✅ Done! CSV saved to {OUTPUT_CSV}")
        print(f"✅ Total products scraped: {len(scraped_data)}")
        print(f"✅ Images saved to: {IMAGE_DIR_ROOT}/")
        print("="*70)
    else:
        print("\n❌ No data extracted.")

if __name__ == "__main__":
    print("="*70)
    print("Alibaba Product Image Scraper")
    print("Anti-Detection Mode (Advanced)")
    print("="*70)
    print(f"Products to scrape: {len(URLS)}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Images directory: {IMAGE_DIR_ROOT}/")
    print("="*70)
    print("\n⚠️  IMPORTANT:")
    print("   - A browser window will open")
    print("   - If you see a CAPTCHA/block, solve it in the browser")
    print("   - The script will pause and wait for you to press Enter")
    print("   - This version has advanced anti-detection features")
    print("")
    
    input("Press Enter to start scraping...")
    run_scraper()
