import json
import pandas as pd

# Load the existing JSON
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

# Load the 2000 CSV to get correct Mack Mattingly votes
df = pd.read_csv('data/20001107__ga__general.csv')
df.columns = df.columns.str.strip()

# Filter for US Senate
senate_2000 = df[df['office'].str.strip() == 'U.S. Senate']

# Get vote totals by county and party
print("Recalculating 2000 US Senate results with only Mack Mattingly votes...")

# Process each county
for county_name in senate_2000['county'].unique():
    county_data = senate_2000[senate_2000['county'] == county_name]
    
    # Get Democrat votes (Zell Miller)
    dem_votes = county_data[county_data['party'].str.strip() == 'Democrat']['votes'].sum()
    
    # Get ONLY Mack Mattingly's Republican votes
    mattingly_votes = county_data[
        (county_data['party'].str.strip() == 'Republican') & 
        (county_data['candidate'].str.contains('Mack Mattingly', na=False))
    ]['votes'].sum()
    
    # Get other votes
    other_votes = county_data[~county_data['party'].str.strip().isin(['Democrat', 'Republican'])]['votes'].sum()
    
    total_votes = dem_votes + mattingly_votes + other_votes
    two_party_total = dem_votes + mattingly_votes
    
    # Calculate margin and winner
    if mattingly_votes > dem_votes:
        winner = 'REPUBLICAN'
        margin = mattingly_votes - dem_votes
        margin_pct = f"R+{round((margin / two_party_total * 100), 2)}"
    else:
        winner = 'DEMOCRAT'
        margin = dem_votes - mattingly_votes
        margin_pct = f"D+{round((margin / two_party_total * 100), 2)}"
    
    margin_pct_val = abs(margin / two_party_total * 100) if two_party_total > 0 else 0
    
    # Determine competitiveness category
    if margin_pct_val >= 40:
        category = 'Annihilation'
    elif margin_pct_val >= 30:
        category = 'Dominant'
    elif margin_pct_val >= 20:
        category = 'Stronghold'
    elif margin_pct_val >= 10:
        category = 'Safe'
    elif margin_pct_val >= 5.5:
        category = 'Likely'
    elif margin_pct_val >= 1:
        category = 'Lean'
    elif margin_pct_val >= 0.5:
        category = 'Tilt'
    else:
        category = 'Tossup'
    
    party_label = 'REPUBLICAN' if winner == 'REPUBLICAN' else 'DEMOCRAT'
    
    # Update the JSON
    county_key = county_name.strip().title()
    if county_key in data['results_by_year']['2000']['us_senate_2000']['results']:
        county_entry = data['results_by_year']['2000']['us_senate_2000']['results'][county_key]
        
        # Update vote totals
        county_entry['dem_votes'] = int(dem_votes)
        county_entry['rep_votes'] = int(mattingly_votes)
        county_entry['other_votes'] = int(other_votes)
        county_entry['total_votes'] = int(total_votes)
        county_entry['two_party_total'] = int(two_party_total)
        county_entry['margin'] = int(margin)
        county_entry['margin_pct'] = margin_pct
        county_entry['winner'] = winner
        county_entry['winner_party'] = winner
        county_entry['winner_name'] = 'Mack Mattingly' if winner == 'REPUBLICAN' else 'Zell Miller'
        county_entry['winner_votes'] = int(mattingly_votes) if winner == 'REPUBLICAN' else int(dem_votes)
        
        # Update competitiveness
        county_entry['competitiveness'] = {
            'category': category,
            'party': party_label,
            'code': f"{party_label}_{category.upper()}",
            'color': '#cb181d' if winner == 'REPUBLICAN' else '#3182bd'  # Example colors
        }
        
        print(f"  Updated {county_key}: {margin_pct} ({category} {party_label})")

print("\nRemoving Public Service Commission races from all years...")

# Remove all public_service_commissioner contests
years_to_check = list(data['results_by_year'].keys())
removed_count = 0

for year in years_to_check:
    contests_to_remove = [key for key in data['results_by_year'][year].keys() 
                          if 'public_service' in key.lower() or 'commissioner' in key.lower() and 
                          not any(x in key.lower() for x in ['agriculture', 'insurance', 'labor'])]
    
    for contest_key in contests_to_remove:
        del data['results_by_year'][year][contest_key]
        removed_count += 1
        print(f"  Removed {year}: {contest_key}")

print(f"\nTotal PSC contests removed: {removed_count}")

# Save the updated JSON
with open('data/results_by_year_grouped.final.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nDone! Updated data/results_by_year_grouped.final.json")
