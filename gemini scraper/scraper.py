#!/usr/bin/env python3
"""
Web Scraper using Playwright with Stealth Mode, Pydoll, or Requests
Supports scraping with anti-detection features
"""

import asyncio
import pandas as pd
import requests
from slugify import slugify
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# Try to import Pydoll (optional dependency)
try:
    from pydoll.browser import Chrome
    PYDoll_AVAILABLE = True
except ImportError:
    PYDoll_AVAILABLE = False


async def scrape_with_playwright(url: str, wait_time: int = 3000):
    """
    Scrape a webpage using Playwright with stealth mode
    
    Args:
        url: The URL to scrape
        wait_time: Time to wait for page to load (milliseconds)
    
    Returns:
        Dictionary with page content and metadata
    """
    async with async_playwright() as p:
        # Launch browser with stealth mode
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        # Apply stealth techniques
        await stealth_async(page)
        
        try:
            # Navigate to the page
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(wait_time)
            
            # Extract page content
            title = await page.title()
            content = await page.content()
            text_content = await page.inner_text('body')
            
            # Get page metadata
            url_final = page.url
            
            result = {
                'url': url_final,
                'title': title,
                'content': content,
                'text': text_content,
                'status': 'success'
            }
            
        except Exception as e:
            result = {
                'url': url,
                'title': None,
                'content': None,
                'text': None,
                'status': f'error: {str(e)}'
            }
        
        finally:
            await browser.close()
    
    return result


def scrape_with_requests(url: str, timeout: int = 30):
    """
    Scrape a webpage using requests library (simpler, faster)
    
    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with page content and metadata
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        result = {
            'url': url,
            'status_code': response.status_code,
            'content': response.text,
            'headers': dict(response.headers),
            'status': 'success'
        }
        
    except Exception as e:
        result = {
            'url': url,
            'status_code': None,
            'content': None,
            'headers': None,
            'status': f'error: {str(e)}'
        }
    
    return result


async def scrape_with_pydoll(url: str, wait_time: int = 3):
    """
    Scrape a webpage using Pydoll (evasion-first automation framework)
    
    Args:
        url: The URL to scrape
        wait_time: Time to wait for page to load (seconds)
    
    Returns:
        Dictionary with page content and metadata
    """
    if not PYDoll_AVAILABLE:
        return {
            'url': url,
            'title': None,
            'content': None,
            'text': None,
            'status': 'error: Pydoll not installed. Install with: pip3 install pydoll-python'
        }
    
    try:
        async with Chrome() as browser:
            tab = await browser.start()
            
            # Navigate to the page
            await tab.go_to(url)
            await asyncio.sleep(wait_time)
            
            # Extract page content using JavaScript evaluation
            from pydoll.commands import RuntimeCommands
            
            # Get title
            title_response = await tab._execute_command(
                RuntimeCommands.evaluate('document.title')
            )
            title = title_response['result']['result']['value'] if title_response.get('result', {}).get('result', {}).get('value') else ''
            
            # Get page source (HTML)
            content = await tab.page_source
            
            # Get text content from body
            text_response = await tab._execute_command(
                RuntimeCommands.evaluate('document.body.innerText')
            )
            text_content = text_response['result']['result']['value'] if text_response.get('result', {}).get('result', {}).get('value') else ''
            
            # Get current URL
            url_final = await tab.current_url
            
            result = {
                'url': url_final,
                'title': title,
                'content': content,
                'text': text_content,
                'status': 'success'
            }
            
    except Exception as e:
        result = {
            'url': url,
            'title': None,
            'content': None,
            'text': None,
            'status': f'error: {str(e)}'
        }
    
    return result


def save_to_dataframe(results: list):
    """
    Convert scraping results to a pandas DataFrame
    
    Args:
        results: List of result dictionaries
    
    Returns:
        pandas DataFrame
    """
    df = pd.DataFrame(results)
    return df


def generate_filename(url: str, prefix: str = 'scraped', extension: str = 'txt'):
    """
    Generate a safe filename from URL using slugify
    
    Args:
        url: The URL to convert to filename
        prefix: Prefix for the filename
        extension: File extension
    
    Returns:
        Safe filename string
    """
    # Extract domain and path from URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    path = parsed.path.strip('/').replace('/', '_') or 'index'
    domain = parsed.netloc.replace('www.', '')
    
    # Create slug from domain and path
    slug = f"{domain}_{path}"
    slug = slugify(slug, max_length=100)
    
    filename = f"{prefix}_{slug}.{extension}"
    return filename


async def scrape_multiple_urls(urls: list, method: str = 'playwright'):
    """
    Scrape multiple URLs
    
    Args:
        urls: List of URLs to scrape
        method: Scraping method - 'playwright', 'pydoll', or 'requests'
    
    Returns:
        List of result dictionaries
    """
    results = []
    
    if method == 'playwright':
        for url in urls:
            print(f"Scraping {url} with Playwright...")
            result = await scrape_with_playwright(url)
            results.append(result)
    elif method == 'pydoll':
        for url in urls:
            print(f"Scraping {url} with Pydoll...")
            result = await scrape_with_pydoll(url)
            results.append(result)
    else:  # requests
        for url in urls:
            print(f"Scraping {url} with requests...")
            result = scrape_with_requests(url)
            results.append(result)
    
    return results


def main():
    """
    Main function to demonstrate the scraper
    """
    # Example URLs to scrape
    example_urls = [
        'https://www.example.com',
        'https://www.google.com'
    ]
    
    print("Web Scraper Tool")
    print("=" * 50)
    
    # Ask user for URLs
    print("\nEnter URLs to scrape (one per line, empty line to finish):")
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        if url.startswith('http://') or url.startswith('https://'):
            urls.append(url)
        else:
            print(f"Warning: '{url}' doesn't look like a valid URL. Skipping...")
    
    if not urls:
        print("No URLs provided. Using example URLs...")
        urls = example_urls
    
    # Ask user for scraping method
    print("\nChoose scraping method:")
    print("1. Playwright (with stealth mode, handles JavaScript)")
    print("2. Pydoll (evasion-first, best for anti-bot sites)")
    print("3. Requests (faster, simpler, no JavaScript)")
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == '1':
        method = 'playwright'
    elif choice == '2':
        method = 'pydoll'
        if not PYDoll_AVAILABLE:
            print("\n⚠️  Warning: Pydoll is not installed.")
            print("Install it with: pip3 install pydoll-python")
            print("Falling back to Playwright...")
            method = 'playwright'
    else:
        method = 'requests'
    
    # Scrape URLs
    print(f"\nScraping {len(urls)} URL(s) with {method.upper()}...")
    results = asyncio.run(scrape_multiple_urls(urls, method=method))
    
    # Convert to DataFrame
    df = save_to_dataframe(results)
    
    # Display results
    print("\n" + "=" * 50)
    print("Scraping Results:")
    print("=" * 50)
    print(df[['url', 'status']].to_string())
    
    # Save to CSV
    csv_filename = 'scraping_results.csv'
    df.to_csv(csv_filename, index=False)
    print(f"\nResults saved to {csv_filename}")
    
    # Save individual files
    print("\nSaving individual files...")
    for result in results:
        if result.get('status') == 'success':
            if method in ['playwright', 'pydoll'] and result.get('text'):
                content = result['text']
            elif result.get('content'):
                content = result['content']
            else:
                continue
            
            filename = generate_filename(result['url'])
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved: {filename}")
    
    print("\nScraping complete!")


if __name__ == '__main__':
    main()

