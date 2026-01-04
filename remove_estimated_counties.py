"""
Remove estimated counties from 2022 Commissioner races
Keep only the 116 counties with actual verified data
"""
import json

print("Removing estimated counties from 2022 Commissioner races...\n")

# Load the data
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

# Commissioner races to clean
commissioner_races = [
    'commissioner_of_agriculture_2022',
    'commissioner_of_insurance_2022',
    'commissioner_of_labor_2022'
]

total_removed = 0

for race in commissioner_races:
    if race in data['results_by_year']['2022']:
        race_data = data['results_by_year']['2022'][race]
        
        if 'results' in race_data:
            counties_before = len(race_data['results'])
            
            # Remove counties with "estimated": true
            counties_to_remove = []
            for county, county_data in race_data['results'].items():
                if county_data.get('estimated') == True:
                    counties_to_remove.append(county)
            
            for county in counties_to_remove:
                del race_data['results'][county]
            
            counties_after = len(race_data['results'])
            removed = counties_before - counties_after
            total_removed += removed
            
            print(f"{race}:")
            print(f"  Before: {counties_before} counties")
            print(f"  After: {counties_after} counties")
            print(f"  Removed: {removed} estimated counties")
            
            # Recalculate statewide totals from remaining counties
            total_dem = 0
            total_rep = 0
            total_other = 0
            
            for county_data in race_data['results'].values():
                total_dem += county_data.get('dem_votes', 0)
                total_rep += county_data.get('rep_votes', 0)
                total_other += county_data.get('other_votes', 0)
            
            total_votes = total_dem + total_rep + total_other
            
            if total_votes > 0:
                race_data['dem_percent'] = (total_dem / total_votes) * 100
                race_data['rep_percent'] = (total_rep / total_votes) * 100
                
            print(f"  New statewide totals: DEM {total_dem:,}, REP {total_rep:,}, Other {total_other:,}")
            print()

print("="*60)
print(f"\nTotal estimated counties removed: {total_removed}")
print("All 2022 Commissioner races now show only verified county data")

# Save the cleaned data
with open('data/results_by_year_grouped.final.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Saved cleaned data to results_by_year_grouped.final.json")
print("\nNote: These races now show 116 counties with actual data")
print("Counties without data will appear gray on the map")
