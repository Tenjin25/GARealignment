"""
This script uses Selenium to access the GA SOS results portal and extract data.
Install: pip install selenium
Also needs: Chrome browser installed
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

print("Setting up Chrome WebDriver...")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in background
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

try:
    driver = webdriver.Chrome(options=chrome_options)
    
    print("Loading GA SOS results page...")
    url = 'https://results.sos.ga.gov/results/public/Georgia/elections/2022NovGen'
    driver.get(url)
    
    # Wait for page to load
    time.sleep(5)
    
    print("Page loaded. Looking for data...")
    
    # Try to find contest/county data in the page
    # Look for JSON in script tags
    scripts = driver.find_elements(By.TAG_NAME, 'script')
    print(f"Found {len(scripts)} scripts")
    
    for i, script in enumerate(scripts):
        content = script.get_attribute('innerHTML') or ''
        if 'commissioner' in content.lower() or 'county' in content.lower():
            print(f"\nScript {i} contains relevant data ({len(content)} chars)")
            # Try to extract JSON
            if '{' in content and '}' in content:
                print("  Contains JSON-like data")
    
    # Check for download links
    links = driver.find_elements(By.TAG_NAME, 'a')
    download_links = []
    for link in links:
        href = link.get_attribute('href') or ''
        text = link.text or ''
        if 'download' in text.lower() or 'csv' in href.lower() or 'excel' in href.lower():
            download_links.append({'text': text, 'href': href})
    
    if download_links:
        print(f"\n✓ Found {len(download_links)} download links:")
        for link in download_links[:10]:
            print(f"  {link['text']}: {link['href']}")
    else:
        print("\n✗ No download links found")
    
    # Take a screenshot for debugging
    driver.save_screenshot('sos_page_screenshot.png')
    print("\nSaved screenshot to sos_page_screenshot.png")
    
    # Save page source
    with open('sos_page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Saved page source to sos_page_source.html")
    
    driver.quit()
    print("\nDone!")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nNote: Make sure Chrome browser and chromedriver are installed")
    print("Install selenium: pip install selenium")
