"""
Use the Clarify library to fetch GA 2022 election data from the official SOS site
"""

from clarify import Jurisdiction
import json

print("Using Clarify library to fetch GA 2022 election data...\n")

# GA uses Clarity Elections system
# The jurisdiction code for Georgia 2022 General is typically the state abbreviation
try:
    # Try to create a jurisdiction for Georgia
    print("Step 1: Creating jurisdiction for Georgia...")
    
    # Common GA SOS Clarity URLs
    urls_to_try = [
        'https://results.enr.clarityelections.com/GA/115465/',  # 2022 General
        'https://results.enr.clarityelections.com/GA/115465/web.307039',
    ]
    
    for url in urls_to_try:
        print(f"\nTrying: {url}")
        try:
            jurisdiction = Jurisdiction(url=url, level='state')
            print(f"✓ Jurisdiction created successfully!")
            
            # Get election info
            print(f"\nElection: {jurisdiction.name if hasattr(jurisdiction, 'name') else 'Georgia 2022'}")
            
            # Get available reports/contests
            print("\nFetching contests...")
            
            # Try to get summary data
            if hasattr(jurisdiction, 'get_summary'):
                summary = jurisdiction.get_summary()
                print(f"Summary data: {type(summary)}")
                
                # Save summary
                with open('clarify_summary_2022.json', 'w') as f:
                    json.dump(summary, f, indent=2, default=str)
                print("Saved summary to clarify_summary_2022.json")
            
            # Try to get detailed results
            if hasattr(jurisdiction, 'report_url'):
                print(f"\nReport URL: {jurisdiction.report_url}")
            
            # Get county-level data
            if hasattr(jurisdiction, 'get_subjurisdictions'):
                print("\nFetching county data...")
                counties = jurisdiction.get_subjurisdictions()
                print(f"Found {len(counties)} counties")
                
                # Save county list
                with open('clarify_counties_2022.json', 'w') as f:
                    json.dump([str(c) for c in counties], f, indent=2)
                print("Saved counties to clarify_counties_2022.json")
            
            # Try to get results by contest
            if hasattr(jurisdiction, 'get_results'):
                print("\nFetching detailed results...")
                results = jurisdiction.get_results()
                print(f"Results type: {type(results)}")
                
                # Save results
                with open('clarify_results_2022.json', 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print("Saved results to clarify_results_2022.json")
            
            print(f"\n✓ SUCCESS! Data retrieved from {url}")
            break
            
        except Exception as e:
            print(f"✗ Error with {url}: {e}")
            continue
    
    print("\n" + "="*60)
    print("\nExploring jurisdiction object attributes:")
    if 'jurisdiction' in locals():
        attrs = [attr for attr in dir(jurisdiction) if not attr.startswith('_')]
        print(f"Available methods/attributes: {', '.join(attrs[:20])}")
        
        # Try calling some common methods
        for method in ['report_url', 'name', 'level']:
            if hasattr(jurisdiction, method):
                try:
                    value = getattr(jurisdiction, method)
                    print(f"  {method}: {value if not callable(value) else value()}")
                except:
                    pass

except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTrying alternative approach...")
    
    # Try using clarify.Parser directly
    try:
        from clarify import Parser
        
        print("\nUsing Parser class...")
        parser = Parser()
        # This might need specific parameters
        print("Parser created. Check clarify documentation for usage.")
        
    except Exception as e2:
        print(f"Parser error: {e2}")

print("\nDone!")
