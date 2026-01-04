import requests
import json
import re
from bs4 import BeautifulSoup

# First, get the main page to find the actual API structure
print("Step 1: Fetching main results page to discover API endpoints...\n")

main_url = 'https://results.sos.ga.gov/results/public/Georgia/elections/2022NovGen'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

try:
    r = requests.get(main_url, headers=headers, timeout=15)
    print(f"Main page status: {r.status_code}")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for embedded JSON data in script tags
        scripts = soup.find_all('script')
        print(f"\nFound {len(scripts)} script tags")
        
        for i, script in enumerate(scripts):
            content = script.string or ''
            
            # Look for API URLs
            api_urls = re.findall(r'["\']([^"\']*(?:api|data|json)[^"\']*?\.json)["\']', content)
            if api_urls:
                print(f"\nScript {i} contains API URLs:")
                for url in set(api_urls):
                    print(f"  {url}")
            
            # Look for embedded data objects
            if 'contests' in content.lower() or 'results' in content.lower():
                # Try to find JSON data assignments
                json_matches = re.findall(r'(?:var|const|let)\s+\w+\s*=\s*(\{[\s\S]{100,}?\});', content)
                if json_matches:
                    print(f"\nScript {i} contains embedded data")
                    try:
                        data = json.loads(json_matches[0])
                        print(f"  Successfully parsed JSON with keys: {list(data.keys())}")
                        with open('sos_2022_embedded.json', 'w') as f:
                            json.dump(data, f, indent=2)
                        print("  Saved to sos_2022_embedded.json")
                    except:
                        pass
        
        # Look for data attributes in HTML elements
        data_attrs = soup.find_all(attrs={'data-contests': True})
        data_attrs += soup.find_all(attrs={'data-results': True})
        data_attrs += soup.find_all(attrs={'data-api': True})
        
        if data_attrs:
            print(f"\n\nFound {len(data_attrs)} elements with data attributes")
            for elem in data_attrs[:3]:
                print(f"  {elem.name}: {list(elem.attrs.keys())}")
        
        # Try common SPA patterns
        print("\n\nStep 2: Trying common single-page app API patterns...")
        
        base_patterns = [
            'https://results.sos.ga.gov/results/data/Georgia/elections/2022NovGen',
            'https://results.sos.ga.gov/results/public/Georgia/elections/2022NovGen/data',
            'https://results.sos.ga.gov/data/Georgia/2022NovGen',
        ]
        
        endpoints = ['/contests.json', '/summary.json', '/counties.json', '/results.json']
        
        for base in base_patterns:
            for endpoint in endpoints:
                url = base + endpoint
                try:
                    r2 = requests.get(url, headers={'User-Agent': headers['User-Agent'], 'Accept': 'application/json'}, timeout=5)
                    if r2.status_code == 200:
                        try:
                            data = r2.json()
                            print(f"\n✓ SUCCESS: {url}")
                            print(f"  Type: {type(data)}")
                            if isinstance(data, dict):
                                print(f"  Keys: {list(data.keys())[:10]}")
                            elif isinstance(data, list):
                                print(f"  Length: {len(data)}")
                            
                            with open('sos_2022_found.json', 'w') as f:
                                json.dump(data, f, indent=2)
                            print("  Saved to sos_2022_found.json")
                            exit(0)
                        except:
                            pass
                except:
                    pass
        
        print("\n\nNo direct API access found. The site likely uses server-side rendering or requires session cookies.")
        
except Exception as e:
    print(f"Error: {e}")

print("\nDone!")
