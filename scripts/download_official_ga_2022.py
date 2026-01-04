"""
Scrape official Georgia SOS 2022 results for accurate county-level data
The official results are published at sos.ga.gov
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

def try_download_csv():
    """
    Georgia SOS publishes CSV files for county-level results
    Try to download them directly
    """
    
    # Known CSV URLs from Georgia SOS for 2022 General Election
    # These are typically at https://results.enr.clarityelections.com/GA/115465/
    
    base_urls = [
        # Try direct CSV download links
        "https://results.enr.clarityelections.com/GA/115465/314741/reports/detailxls.zip",
        "https://results.enr.clarityelections.com/GA/115465/314741/reports/detail.zip",
        
        # County detail reports
        "https://sos.ga.gov/sites/default/files/2022-11/2022%20General%20Election%20Results.xlsx",
        "https://sos.ga.gov/elections/2022-general-election-results",
    ]
    
    for url in base_urls:
        print(f"Trying: {url}")
        try:
            response = requests.get(url, timeout=15, allow_redirects=True)
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"  Size: {len(response.content)} bytes")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                
                # Save based on content type
                if 'excel' in content_type or 'spreadsheet' in content_type or url.endswith('.xlsx'):
                    filename = 'ga_2022_official_results.xlsx'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Saved to {filename}")
                    return filename, 'excel'
                
                elif 'zip' in content_type or url.endswith('.zip'):
                    filename = 'ga_2022_official_results.zip'
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Saved to {filename}")
                    return filename, 'zip'
                
                elif 'html' in content_type:
                    # Try to parse HTML for download links
                    soup = BeautifulSoup(response.text, 'html.parser')
                    links = soup.find_all('a', href=True)
                    csv_links = [a['href'] for a in links if '.csv' in a['href'].lower() or 'download' in a['href'].lower()]
                    excel_links = [a['href'] for a in links if '.xlsx' in a['href'].lower() or '.xls' in a['href'].lower()]
                    
                    print(f"  Found {len(csv_links)} CSV links and {len(excel_links)} Excel links")
                    
                    if excel_links:
                        print("  Excel links found:")
                        for link in excel_links[:5]:
                            print(f"    - {link}")
                    
                    if csv_links:
                        print("  CSV links found:")
                        for link in csv_links[:5]:
                            print(f"    - {link}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    return None, None

def search_sos_website():
    """
    Search the GA SOS website for downloadable results
    """
    print("\nSearching GA SOS website...")
    
    urls_to_check = [
        "https://sos.ga.gov/page/2022-general-election-results",
        "https://results.enr.clarityelections.com/GA/115465/web.307039/#/summary",
    ]
    
    for url in urls_to_check:
        print(f"\nChecking: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for download links
                download_links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    text = a.get_text().strip()
                    
                    if any(word in href.lower() for word in ['download', 'excel', 'csv', 'xlsx', 'xls', 'report', 'detail']):
                        download_links.append((text, href))
                
                if download_links:
                    print(f"  Found {len(download_links)} potential download links:")
                    for text, href in download_links[:10]:
                        print(f"    - {text}: {href}")
                else:
                    print("  No download links found")
        
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("Searching for official Georgia 2022 election results")
    print("=" * 70)
    
    filename, file_type = try_download_csv()
    
    if not filename:
        search_sos_website()
        
        print("\n" + "=" * 70)
        print("MANUAL DOWNLOAD INSTRUCTIONS:")
        print("=" * 70)
        print("\n1. Visit: https://sos.ga.gov/page/2022-general-election-results")
        print("2. Look for 'County Results' or 'Detailed Results' download link")
        print("3. Download the Excel/CSV file")
        print("4. Save it as 'ga_2022_official_results.xlsx' in this directory")
        print("\nAlternatively:")
        print("1. Visit: https://results.enr.clarityelections.com/GA/115465/")
        print("2. Click on each Commissioner race")
        print("3. Look for 'Export' or 'Download' button")
        print("4. Download county-level results")
    
    else:
        print(f"\n✓ Downloaded: {filename}")
        print("Next step: Extract and parse the data")
