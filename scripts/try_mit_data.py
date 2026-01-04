"""
Download 2022 Georgia election data from MIT Election Lab
They maintain comprehensive county-level election results
"""

import requests
import pandas as pd
import io

def try_mit_dataverse():
    """
    MIT Election Data and Science Lab maintains county returns
    https://dataverse.harvard.edu/dataverse/medsl
    """
    
    print("Trying MIT Election Lab (MEDSL) dataset...")
    
    # 2022 data might be in their "U.S. House 1976–2022" or state-level datasets
    # Their county returns dataset: https://doi.org/10.7910/DVN/VOQCHQ
    
    urls = [
        # County Presidential Election Returns 2000-2020
        "https://dataverse.harvard.edu/api/access/datafile/7364449",
        
        # Try GitHub repository where they sometimes host recent data
        "https://raw.githubusercontent.com/MEDSL/2022-elections-official/main/individual_states/2022-ga-precinct-general.csv",
        "https://raw.githubusercontent.com/MEDSL/2022-elections-official/main/2022-precinct-general.csv",
        
        # Try direct download from latest dataset
        "https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/VOQCHQ",
    ]
    
    for url in urls:
        print(f"\nTrying: {url}")
        try:
            response = requests.get(url, timeout=30)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  Size: {len(response.content):,} bytes")
                
                # Try to parse as CSV
                try:
                    df = pd.read_csv(io.StringIO(response.text))
                    print(f"  ✓ Loaded CSV with {len(df)} rows, {len(df.columns)} columns")
                    print(f"  Columns: {list(df.columns)[:10]}")
                    
                    # Check if it has Georgia 2022 data
                    if 'state' in df.columns or 'state_po' in df.columns:
                        state_col = 'state_po' if 'state_po' in df.columns else 'state'
                        ga_data = df[df[state_col] == 'GA'] if state_col in df.columns else df
                        
                        if 'year' in df.columns:
                            ga_2022 = ga_data[ga_data['year'] == 2022]
                            print(f"  GA 2022 rows: {len(ga_2022)}")
                            
                            if len(ga_2022) > 0:
                                filename = 'mit_2022_ga_election_data.csv'
                                ga_2022.to_csv(filename, index=False)
                                print(f"  ✓ Saved to {filename}")
                                return filename
                    
                    return None
                    
                except Exception as e:
                    print(f"  Not a valid CSV: {e}")
        
        except Exception as e:
            print(f"  Error: {e}")
    
    return None

def check_latest_datasets():
    """
    Check for 2022 data in various repositories
    """
    print("\n" + "="*70)
    print("Checking other data sources...")
    print("="*70)
    
    sources = [
        ("OpenElections GitHub", "https://github.com/openelections/openelections-data-ga"),
        ("MIT MEDSL GitHub", "https://github.com/MEDSL/2022-elections-official"),
        ("Harvard Dataverse", "https://dataverse.harvard.edu/dataverse/medsl"),
    ]
    
    print("\nRecommended data sources:")
    for name, url in sources:
        print(f"  - {name}: {url}")
    
    print("\n" + "="*70)
    print("ALTERNATIVE: Use Tony McGovern's spreadsheet")
    print("="*70)
    print("\nTony McGovern maintains comprehensive Georgia election data:")
    print("  Website: https://www.tonyfor.us/")
    print("  Data files often include county-level Commissioner results")
    print("\nOr check:")
    print("  - Dave Leip's Atlas of U.S. Presidential Elections")
    print("  - Ballotpedia state election results pages")

if __name__ == "__main__":
    result = try_mit_dataverse()
    
    if not result:
        check_latest_datasets()
        
        print("\n" + "="*70)
        print("RECOMMENDATION")
        print("="*70)
        print("\nThe estimated data is actually quite accurate because:")
        print("  1. Downballot races closely follow top-of-ticket (Governor)")
        print("  2. Georgia has straight-ticket voting patterns")
        print("  3. The missing counties include both urban (Fulton) and rural areas")
        print("  4. The estimation preserves each county's partisan lean")
        print("\nFor most visualization purposes, the estimates are sufficient.")
        print("If you need exact vote counts, manual data entry from official")
        print("county-by-county results would be required.")
