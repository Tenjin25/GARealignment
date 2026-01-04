"""
Fetch GA 2022 election data using the Clarify library
"""
from clarify import Jurisdiction
import json
import time

print("Fetching Georgia 2022 General Election data...\n")

# GA 2022 General Election URL
url = 'https://results.enr.clarityelections.com/GA/115465/'

try:
    print(f"Creating jurisdiction for: {url}")
    jurisdiction = Jurisdiction(url=url, level='state')
    
    print(f"✓ Jurisdiction created: {jurisdiction.name if hasattr(jurisdiction, 'name') else 'Georgia'}\n")
    
    # Get summary results
    print("Fetching summary results...")
    summary_url = jurisdiction.report_url('summary')
    print(f"Summary URL: {summary_url}\n")
    
    # Parse summary data
    print("Parsing summary data...")
    summary = jurisdiction.get_subjurisdictions()
    
    print(f"Found {len(summary)} sub-jurisdictions (counties)")
    
    # Get detailed results for each county
    print("\nFetching detailed county results...")
    all_results = {}
    
    for i, county in enumerate(summary[:5]):  # Test with first 5 counties
        print(f"  {i+1}. {county.name}")
        try:
            # Get results for this county
            county_results = county.get_subjurisdictions()
            all_results[county.name] = {
                'name': county.name,
                'results_count': len(county_results) if county_results else 0
            }
        except Exception as e:
            print(f"     Error: {e}")
        time.sleep(0.5)  # Be nice to the server
    
    # Save the data
    with open('clarify_ga_2022_test.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✓ Saved test data to clarify_ga_2022_test.json")
    
    # Now try to get statewide contest data
    print("\nFetching contest data...")
    try:
        # Check what methods are available
        methods = [m for m in dir(jurisdiction) if not m.startswith('_')]
        print(f"Available methods: {', '.join(methods[:15])}")
        
        # Try to get detailed results
        if hasattr(jurisdiction, 'get_detailed_results'):
            detailed = jurisdiction.get_detailed_results()
            print(f"Detailed results type: {type(detailed)}")
            
    except Exception as e:
        print(f"Error getting contests: {e}")
    
    print("\n✓ SUCCESS! Clarify library is working.")
    print("\nNext step: Extract all 159 counties and Commissioner race data")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
