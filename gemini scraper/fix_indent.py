#!/usr/bin/env python3
"""Fix indentation in alibaba_image_scraper.py"""

with open('alibaba_image_scraper.py', 'r') as f:
    lines = f.readlines()

# Fix lines 150-151 specifically
for i in range(len(lines)):
    line = lines[i]
    # Replace tabs with spaces
    if '\t' in line:
        lines[i] = line.replace('\t', '    ')

# Write back
with open('alibaba_image_scraper.py', 'w') as f:
    f.writelines(lines)

print("Fixed indentation (replaced tabs with spaces)")

