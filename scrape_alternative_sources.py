"""
Try alternative sources that might have collected complete GA 2022 county data
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

sources_to_try = [
    {
        'name': 'New York Times 2022 GA Results',
        'url': 'https://www.nytimes.com/interactive/2022/11/08/us/elections/results-georgia.html',
        'method': 'html'
    },
    {
        'name': 'Politico 2022 GA Results',
        'url': 'https://www.politico.com/2022-election/results/georgia/',
        'method': 'html'
    },
    {
        'name': 'CNN 2022 GA Results',
        'url': 'https://www.cnn.com/election/2022/results/georgia',
        'method': 'html'
    },
    {
        'name': 'Associated Press API',
        'url': 'https://api.ap.org/elections/v2/2022-11-08/GA',
        'method': 'api'
    },
    {
        'name': 'Decision Desk HQ',
        'url': 'https://results.decisiondeskhq.com/2022/General/Georgia',
        'method': 'html'
    }
]

print("Checking alternative data sources for GA 2022 county results...\n")

for source in sources_to_try:
    print(f"Trying: {source['name']}")
    print(f"  URL: {source['url']}")
    
    try:
        r = requests.get(source['url'], headers=headers, timeout=15)
        print(f"  Status: {r.status_code}")
        
        if r.status_code == 200:
            # Check for embedded JSON data
            if 'json' in r.headers.get('content-type', '').lower():
                try:
                    data = r.json()
                    print(f"  ✓ JSON response! Keys: {list(data.keys())[:5]}")
                    filename = f"{source['name'].replace(' ', '_').lower()}.json"
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"  Saved to: {filename}")
                except:
                    pass
            
            # Look for embedded data in script tags
            soup = BeautifulSoup(r.text, 'html.parser')
            scripts = soup.find_all('script', type='application/json')
            
            if scripts:
                print(f"  Found {len(scripts)} JSON script tags")
                for i, script in enumerate(scripts[:3]):
                    try:
                        data = json.loads(script.string)
                        if 'county' in str(data).lower() or 'commissioner' in str(data).lower():
                            print(f"    Script {i} contains relevant data!")
                            filename = f"{source['name'].replace(' ', '_').lower()}_script_{i}.json"
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            print(f"    Saved to: {filename}")
                    except:
                        pass
            
            # Check for data tables
            tables = soup.find_all('table')
            if len(tables) > 0:
                print(f"  Found {len(tables)} tables")
                for i, table in enumerate(tables[:2]):
                    try:
                        df = pd.read_html(str(table))[0]
                        if len(df) > 50:  # Likely county data
                            print(f"    Table {i}: {len(df)} rows - might be county data!")
                            filename = f"{source['name'].replace(' ', '_').lower()}_table_{i}.csv"
                            df.to_csv(filename, index=False)
                            print(f"    Saved to: {filename}")
                    except:
                        pass
            
            print(f"  ✓ Page accessible ({len(r.text):,} bytes)")
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")
    
    print()

print("\n" + "="*60)
print("\nIf no complete data found, the only option is to:")
print("1. Use only the 116 counties we have real data for")
print("2. Or manually enter missing county data from county election websites")
print("3. Or accept estimated data with clear warnings")
