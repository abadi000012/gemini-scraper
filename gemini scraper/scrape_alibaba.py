#!/usr/bin/env python3
"""
Script to scrape Alibaba product pages
"""

import asyncio
from scraper import scrape_multiple_urls, save_to_dataframe, generate_filename

# Alibaba product URLs to scrape
ALIBABA_URLS = [
    'https://www.alibaba.com/product-detail/Block-Making-Machine-Production-Line_1601589661125.html',
    'https://www.alibaba.com/product-detail/Automatic-Block-Making-Machine-Egg-Laying_1601175010766.html',
    'https://www.alibaba.com/product-detail/QT4-15-Automatic-Block-Construction-Manufacturing_1600559220411.html',
    'https://www.alibaba.com/product-detail/Block-Machine-Making-Automatic-Cement-Production_1601252481200.html',
    'https://www.alibaba.com/product-detail/QT5-15-Block-Making-Machine-with_1601453310582.html'
]

# Product descriptions for reference
PRODUCT_INFO = {
    'https://www.alibaba.com/product-detail/Block-Making-Machine-Production-Line_1601589661125.html': 'Entry-Level / Small Workshop – Manual / Low-Budget Machine',
    'https://www.alibaba.com/product-detail/Automatic-Block-Making-Machine-Egg-Laying_1601175010766.html': 'Mid-Range – Semi-Automatic Block & Brick Maker',
    'https://www.alibaba.com/product-detail/QT4-15-Automatic-Block-Construction-Manufacturing_1600559220411.html': 'Professional Automatic Block Machine',
    'https://www.alibaba.com/product-detail/Block-Machine-Making-Automatic-Cement-Production_1601252481200.html': 'Industrial / High-Capacity Production Line',
    'https://www.alibaba.com/product-detail/QT5-15-Block-Making-Machine-with_1601453310582.html': 'Full Automatic with Mixer – Heavy Use & Versatility'
}


async def main():
    print("=" * 70)
    print("Alibaba Product Scraper")
    print("=" * 70)
    print(f"\nScraping {len(ALIBABA_URLS)} Alibaba product pages...")
    print("Using Pydoll (evasion-first, best for anti-bot sites like Alibaba)\n")
    
    # Scrape all URLs with Pydoll (best for anti-bot evasion on sites like Alibaba)
    # Falls back to Playwright if Pydoll is not available
    try:
        from scraper import PYDoll_AVAILABLE
        if PYDoll_AVAILABLE:
            method = 'pydoll'
            print("✓ Pydoll detected - using evasion-first automation")
        else:
            method = 'playwright'
            print("⚠️  Pydoll not available - using Playwright with stealth mode")
    except:
        method = 'playwright'
        print("⚠️  Using Playwright with stealth mode")
    
    results = await scrape_multiple_urls(ALIBABA_URLS, method=method)
    
    # Add product info to results
    for result in results:
        url = result.get('url', '')
        # Match by URL (handle redirects)
        for original_url, description in PRODUCT_INFO.items():
            if original_url in url or url in original_url:
                result['product_description'] = description
                break
        else:
            result['product_description'] = 'Unknown'
    
    # Convert to DataFrame
    df = save_to_dataframe(results)
    
    # Display summary
    print("\n" + "=" * 70)
    print("Scraping Results Summary:")
    print("=" * 70)
    
    # Show results with product descriptions
    for idx, result in enumerate(results, 1):
        status_icon = "✓" if result.get('status') == 'success' else "✗"
        print(f"\n{idx}. {status_icon} {result.get('product_description', 'Unknown')}")
        print(f"   URL: {result.get('url', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        if result.get('title'):
            print(f"   Title: {result.get('title', 'N/A')[:80]}...")
    
    # Save to CSV
    csv_filename = 'alibaba_scraping_results.csv'
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"\n✓ Results saved to {csv_filename}")
    
    # Save individual HTML files
    print("\nSaving individual HTML files...")
    saved_count = 0
    for result in results:
        if result.get('status') == 'success' and result.get('content'):
            filename = generate_filename(result['url'], prefix='alibaba', extension='html')
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['content'])
                print(f"  ✓ Saved: {filename}")
                saved_count += 1
            except Exception as e:
                print(f"  ✗ Error saving {filename}: {e}")
    
    # Save individual text files
    print("\nSaving individual text files...")
    for result in results:
        if result.get('status') == 'success' and result.get('text'):
            filename = generate_filename(result['url'], prefix='alibaba', extension='txt')
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
                print(f"  ✓ Saved: {filename}")
            except Exception as e:
                print(f"  ✗ Error saving {filename}: {e}")
    
    print("\n" + "=" * 70)
    print(f"Scraping complete! {saved_count}/{len(ALIBABA_URLS)} pages saved successfully.")
    print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())

