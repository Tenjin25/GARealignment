"""
Check what counties are in the 2022 data
"""
import json

# Load the results
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Get counties from 2022 data
if '2022' in results['results_by_year']:
    contests = results['results_by_year']['2022']
    
    # Get governor counties (has 162)
    if 'governor_2022' in contests:
        counties = sorted(contests['governor_2022']['results'].keys())
        print(f"Governor 2022 has {len(counties)} counties:\n")
        
        # Check for suspicious counties
        suspicious = []
        for county in counties:
            # Check for non-standard county names
            if county.lower() in ['state floating', 'absentee', 'provisional', 'total', 'statewide']:
                suspicious.append(county)
            elif len(county) < 3:
                suspicious.append(county)
        
        if suspicious:
            print(f"Suspicious entries ({len(suspicious)}):")
            for s in suspicious:
                print(f"  - {s}")
        
        # Show all counties
        print(f"\nAll counties:")
        for i, county in enumerate(counties, 1):
            print(f"{i:3d}. {county}")
