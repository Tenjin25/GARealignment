"""
Try to access GA 2022 data by downloading the reports directly
"""
from clarify import Jurisdiction, Parser
import requests
import json

print("Attempting to download GA 2022 election reports...\n")

url = 'https://results.enr.clarityelections.com/GA/115465/'

try:
    jurisdiction = Jurisdiction(url=url, level='state')
    print(f"Jurisdiction: {jurisdiction.url}\n")
    
    # Try to construct summary URL manually
    print("Trying different summary URL patterns...")
    
    possible_urls = [
        f"{url}summary.html",
        f"{url}Web01/en/summary.html",
        f"{url}307039/Web01/en/summary.html",
        f"{url}json/en/summary.json",
        f"{url}json/summary.json",
        f"{url}xml/en/summary.xml",
        f"{url}reports/summary.txt",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Referer': url
    }
    
    for test_url in possible_urls:
        print(f"  Trying: {test_url}")
        try:
            r = requests.get(test_url, headers=headers, timeout=10)
            if r.status_code == 200 and len(r.text) > 100:
                print(f"    ✓ SUCCESS! ({len(r.text)} bytes)")
                print(f"    Content type: {r.headers.get('content-type', 'unknown')}")
                
                # Save the content
                filename = f"sos_report_{test_url.split('/')[-1]}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                print(f"    Saved to: {filename}")
                
                # Try to parse it
                if 'json' in test_url:
                    try:
                        data = r.json()
                        print(f"    JSON keys: {list(data.keys())[:10] if isinstance(data, dict) else 'list'}")
                    except:
                        pass
                
                break
            else:
                print(f"    {r.status_code}")
        except Exception as e:
            print(f"    Error: {str(e)[:40]}")
    
    # Try using the parser directly
    print("\n\nTrying Parser class...")
    parser = Parser()
    print(f"Parser created: {type(parser)}")
    
    # Check parser methods
    methods = [m for m in dir(parser) if not m.startswith('_')]
    print(f"Parser methods: {', '.join(methods[:20])}")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
