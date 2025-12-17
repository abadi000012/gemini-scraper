import os
import time
import random
import re
import requests
import pandas as pd
from slugify import slugify
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
# Your Mac Firefox Profile Path
# NOTE: You MUST Close Firefox completely before running this script.
FIREFOX_PROFILE_PATH = "/Users/aba/Library/Application Support/Firefox/Profiles/b5kr8f0f.default-release"

URLS = [
    "https://www.alibaba.com/product-detail/Chancee-K80-Factory-Price-Concrete-Double_1600874046823.html",
    "https://www.alibaba.com/product-detail/Compact-Large-Ride-On-Street-Vacuum_1601427314632.html",
    "https://www.alibaba.com/product-detail/48V-Electric-Double-Brush-Ride-On_1601445626156.html"
]

# Output paths - where scraped data will be saved
SCRAPER_BASE_PATH = "/Users/aba/Documents/git hub copilot version scraper"
OUTPUT_CSV = os.path.join(SCRAPER_BASE_PATH, "alibaba_products.csv")
IMAGE_DIR_ROOT = os.path.join(SCRAPER_BASE_PATH, "scraped_images")

# --- HELPER FUNCTIONS ---

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_alibaba_image_url(url):
    if not url: return None
    url = url.split('?')[0]
    # Remove size suffixes like .jpg_350x350.jpg
    clean_url = re.sub(r'(_\d+x\d+.*$|\.jpg_.*$|\.png_.*$)', '', url)
    if clean_url.startswith("//"): clean_url = "https:" + clean_url
    return clean_url

def download_image_authenticated(url, folder_path, image_name, cookies, user_agent):
    """Downloads using the browser's cookies to avoid 403 Forbidden errors."""
    headers = {'User-Agent': user_agent, 'Referer': 'https://www.alibaba.com/'}
    session_cookies = {c['name']: c['value'] for c in cookies}
    
    try:
        response = requests.get(url, headers=headers, cookies=session_cookies, stream=True, timeout=15)
        if response.status_code == 200:
            # Determine extension
            ext = "jpg"
            if "png" in url: ext = "png"
            elif "webp" in url: ext = "webp"
            
            filename = f"{image_name}.{ext}"
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return file_path
    except Exception as e:
        print(f"   ❌ Image download failed: {e}")
    return None

# --- MAIN LOGIC ---

def run_scraper():
    print(f"\n{'='*70}")
    print(f"Alibaba Scraper: Personal Firefox Profile")
    print(f"{'='*70}")
    
    # Ensure base directory and image directory exist
    create_directory(SCRAPER_BASE_PATH)
    create_directory(IMAGE_DIR_ROOT)
    scraped_data = []

    with sync_playwright() as p:
        try:
            print(f"1. Launching Firefox from: {FIREFOX_PROFILE_PATH}")
            # Launch Persistent Context (Uses your Real Firefox)
            browser_context = p.firefox.launch_persistent_context(
                user_data_dir=FIREFOX_PROFILE_PATH,
                headless=False,
                viewport={'width': 1440, 'height': 900},
                # Determine executable path automatically or fallback to system default
            )
        except Exception as e:
            print("\n❌ CRITICAL ERROR: Could not open Firefox.")
            print(f"Error details: {e}")
            print("\n⚠️  SOLUTION: Please make sure Firefox is CLOSED completely (Cmd+Q) before running this.")
            return

        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()

        for index, url in enumerate(URLS):
            print(f"\n[{index+1}/{len(URLS)}] Navigating...")
            
            # Navigation Loop (Manual Captcha Handling)
            while True:
                try:
                    page.goto(url, timeout=60000)
                    page.wait_for_timeout(2000)

                    # Check for "Punish" (Captcha) or Login block
                    if "punish" in page.url or "captcha" in page.url or page.locator(".nc_wrapper").is_visible():
                        print("\n🛑 BLOCKED! The script is paused.")
                        print("👉 Please solve the Captcha/Slider in the Chrome window now.")
                        input(">>> PRESS ENTER HERE WHEN THE PRODUCT PAGE IS VISIBLE <<<")
                        continue
                    
                    # Check for Title
                    page.wait_for_selector("h1", timeout=5000)
                    break # Loop success
                except:
                    print("   ⚠️ Page load issue (or captcha). Retrying...")
                    time.sleep(2)

            # --- DATA EXTRACTION ---
            title = page.locator('h1').first.inner_text().strip()
            print(f"✅ Product: {title[:40]}...")
            
            product_slug = slugify(title, max_length=50)
            product_path = os.path.join(IMAGE_DIR_ROOT, product_slug)
            create_directory(product_path)

            # Price
            price = "N/A"
            for sel in ['.price', '.product-price', '.ma-price-wrap', '.main-price', '.promotion-price']:
                if page.locator(sel).count() > 0:
                    price = page.locator(sel).first.inner_text().strip()
                    break

            # MOQ
            moq = "N/A"
            try:
                moq_loc = page.get_by_text(re.compile(r"Min.*Order", re.IGNORECASE))
                if moq_loc.count() > 0:
                    moq = moq_loc.first.inner_text().strip()
            except: pass

            # --- IMAGES ---
            print("📸 extracting images...")
            image_urls = set()
            
            # 1. Get Main Image immediately
            main_img_sel = '.main-image img, .detail-main-image img, .image-viewer-img'
            if page.locator(main_img_sel).count() > 0:
                src = page.locator(main_img_sel).first.get_attribute('src')
                clean = clean_alibaba_image_url(src)
                if clean: image_urls.add(clean)

            # 2. Click Thumbnails
            thumbs = page.locator('.main-image-thumb-ul li, .image-list li, .detail-next-slick-slide').all()
            if thumbs:
                # Limit to first 6 to be fast
                for thumb in thumbs[:6]:
                    try:
                        thumb.hover()
                        thumb.click(force=True)
                        page.wait_for_timeout(600) # Small wait for load
                        
                        src = page.locator(main_img_sel).first.get_attribute('src')
                        clean = clean_alibaba_image_url(src)
                        if clean: image_urls.add(clean)
                    except: pass
            
            print(f"   Found {len(image_urls)} unique images.")

            # --- DOWNLOAD ---
            cookies = browser_context.cookies()
            ua = page.evaluate("navigator.userAgent")
            downloaded_paths = []

            for i, img_url in enumerate(image_urls):
                local_path = download_image_authenticated(img_url, product_path, f"img_{i}", cookies, ua)
                if local_path: downloaded_paths.append(local_path)

            scraped_data.append({
                "Title": title,
                "Price": price,
                "MOQ": moq,
                "URL": url,
                "Images": " | ".join(downloaded_paths)
            })

            # Random Human Sleep
            sleep_time = random.uniform(5, 9)
            print(f"   Sleeping {sleep_time:.1f}s...")
            time.sleep(sleep_time)

        browser_context.close()

    if scraped_data:
        df = pd.DataFrame(scraped_data)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n✅ SUCCESS! Data saved to {OUTPUT_CSV}")
    else:
        print("\n❌ No data extracted.")

if __name__ == "__main__":
    run_scraper()
