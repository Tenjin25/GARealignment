"""
Script to fetch 2022 Georgia election results from official sources
for the missing counties in Commissioner races
"""

import requests
import json
import time

# Georgia SOS Results API endpoint (2022 General Election)
# Based on the structure we saw in ga_2022_sos_raw2.json

def fetch_ga_sos_results():
    """
    The Georgia SOS uses a web interface at:
    https://results.enr.clarityelections.com/GA/
    
    For 2022 general election, the data is likely at:
    https://results.enr.clarityelections.com/GA/115465/web.307039/
    
    Let's try to fetch the summary JSON that contains all results
    """
    
    # Try the API endpoint pattern
    base_url = "https://results.enr.clarityelections.com/GA/115465"
    
    # Common endpoints to try
    endpoints = [
        f"{base_url}/json/en/summary.json",
        f"{base_url}/json/summary.json",
        f"{base_url}/summary.json",
    ]
    
    for endpoint in endpoints:
        print(f"Trying: {endpoint}")
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                print(f"  ✓ Success!")
                data = response.json()
                print(f"  Keys: {list(data.keys())[:10]}")
                return data
            else:
                print(f"  ✗ Status: {response.status_code}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return None

if __name__ == "__main__":
    print("Fetching Georgia SOS 2022 election results...")
    print("=" * 60)
    
    data = fetch_ga_sos_results()
    
    if data:
        # Save to file
        with open('ga_2022_sos_complete.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Data saved to ga_2022_sos_complete.json")
    else:
        print("\n✗ Could not fetch data from GA SOS API")
        print("\nAlternative: Visit https://results.enr.clarityelections.com/GA/115465/")
        print("and look for JSON data endpoints in the browser's Network tab")
