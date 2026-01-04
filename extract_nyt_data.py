"""
Extract county-level data from NY Times 2022 Georgia results page
"""
import requests
from bs4 import BeautifulSoup
import json
import re

print("Fetching NY Times Georgia 2022 election data...\n")

url = 'https://www.nytimes.com/interactive/2022/11/08/us/elections/results-georgia.html'
headers = {'User-Agent': 'Mozilla/5.0'}

r = requests.get(url, headers=headers, timeout=20)
print(f"Status: {r.status_code}")
print(f"Page size: {len(r.text):,} bytes\n")

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Look for all script tags with JSON data
    scripts = soup.find_all('script')
    print(f"Found {len(scripts)} script tags total\n")
    
    election_data_found = []
    
    for i, script in enumerate(scripts):
        content = script.string or ''
        
        # Look for election data patterns
        if any(keyword in content.lower() for keyword in ['commissioner', 'county', 'georgia', 'precinct']):
            # Try to find JSON objects
            json_patterns = [
                r'window\.__PRELOADED_STATE__\s*=\s*(\{.+?\});',
                r'window\.__INITIAL_STATE__\s*=\s*(\{.+?\});',
                r'var\s+data\s*=\s*(\{.+?\});',
                r'const\s+data\s*=\s*(\{.+?\});',
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    print(f"Script {i}: Found potential data with pattern '{pattern[:30]}...'")
                    try:
                        data = json.loads(matches[0])
                        print(f"  ✓ Parsed JSON successfully!")
                        print(f"  Top-level keys: {list(data.keys())[:10]}")
                        
                        # Save this data
                        filename = f'nyt_data_script_{i}.json'
                        with open(filename, 'w') as f:
                            json.dump(data, f, indent=2)
                        print(f"  Saved to: {filename}\n")
                        
                        election_data_found.append({
                            'script_index': i,
                            'filename': filename,
                            'keys': list(data.keys())
                        })
                        
                    except json.JSONDecodeError as e:
                        print(f"  ✗ JSON parse error: {str(e)[:50]}\n")
    
    # Also save the full HTML for manual inspection
    with open('nyt_full_page.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print("Saved full page to: nyt_full_page.html")
    
    if election_data_found:
        print(f"\n✓ SUCCESS! Found {len(election_data_found)} data sources")
        print("\nData files created:")
        for item in election_data_found:
            print(f"  - {item['filename']} (keys: {', '.join(item['keys'][:5])})")
    else:
        print("\n✗ No embedded JSON data found")
        print("The page may load data dynamically via AJAX")
        print("Check nyt_full_page.html manually for data patterns")

else:
    print(f"✗ Failed to fetch page: {r.status_code}")

print("\nDone!")
