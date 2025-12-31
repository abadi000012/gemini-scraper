#!/bin/bash
# Complete Installation Script for Alibaba Image Scraper
# This script installs all required dependencies

echo "=========================================="
echo "Alibaba Image Scraper - Installation"
echo "=========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install Python packages
echo "Installing Python packages..."
echo "----------------------------------------"
pip3 install playwright playwright-stealth pandas requests python-slugify --user

if [ $? -eq 0 ]; then
    echo "✓ Python packages installed successfully"
else
    echo "❌ Failed to install Python packages"
    exit 1
fi

echo ""

# Install Playwright browser
echo "Installing Playwright Chromium browser..."
echo "----------------------------------------"
python3 -m playwright install chromium

if [ $? -eq 0 ]; then
    echo "✓ Playwright browser installed successfully"
else
    echo "❌ Failed to install Playwright browser"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "To run the scraper:"
echo "  cd '/Users/aba/Documents/gemini scraper'"
echo "  python3 alibaba_image_scraper.py"
echo ""

