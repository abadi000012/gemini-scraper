# Advanced CAPTCHA Bypass Guide

## Current Features

The scraper now includes:

1. **Improved CAPTCHA Detection** - Automatically detects CAPTCHA pages
2. **Manual Solving** - Waits up to 120 seconds for you to solve CAPTCHAs
3. **Human-like Behavior** - Random mouse movements, realistic scrolling, delays
4. **Longer Delays** - 10-20 seconds between products to reduce triggers
5. **Optional 2captcha Integration** - Automatic CAPTCHA solving (paid service)

## Manual CAPTCHA Solving (Current Method)

When a CAPTCHA is detected:
1. The script will pause and wait up to 120 seconds
2. Solve the CAPTCHA in the browser window
3. The script will automatically detect when it's solved and continue

## Automatic CAPTCHA Solving (Optional)

### Option 1: 2captcha Service (Paid)

1. **Sign up** at https://2captcha.com
2. **Get your API key** from the dashboard
3. **Install the library:**
   ```bash
   pip3 install 2captcha-python
   ```
4. **Set your API key:**
   ```bash
   export TWOCAPTCHA_API_KEY='your_api_key_here'
   ```
5. **Run the scraper** - it will automatically use 2captcha when CAPTCHAs appear

**Note:** 2captcha costs ~$2.99 per 1000 CAPTCHAs. For Alibaba, you might need it if you're scraping many products.

### Option 2: Anti-Captcha Service

Similar to 2captcha:
```bash
pip3 install anticaptchaofficial
export ANTICAPTCHA_API_KEY='your_key'
```

## Reducing CAPTCHA Triggers

The scraper now includes:

1. **Human-like delays** - Random 1-3 second delays before navigation
2. **Realistic scrolling** - Variable scroll amounts with reading pauses
3. **Mouse movements** - Random mouse movements to simulate human behavior
4. **Longer product delays** - 10-20 seconds between products
5. **Realistic browser fingerprint** - Uses Safari on macOS settings

## Additional Tips

1. **Use Proxies** - Rotating IPs can help avoid rate limits
2. **Limit Scraping Speed** - Don't scrape too many products too quickly
3. **Use Residential IPs** - Datacenter IPs trigger more CAPTCHAs
4. **Respect robots.txt** - Some sites have scraping policies

## Troubleshooting

### CAPTCHA keeps appearing:
- Increase delays between products (edit the delay range in code)
- Use a VPN/proxy to change your IP
- Consider using 2captcha for automatic solving

### Manual solving not working:
- Make sure you solve the CAPTCHA completely
- Wait for the page to fully reload after solving
- The script will detect when the CAPTCHA page is gone

### Still getting blocked:
- Alibaba has very aggressive bot detection
- Consider scraping during off-peak hours
- Use residential proxies
- Limit to fewer products per session

