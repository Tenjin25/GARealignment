"""
Remove all 2022 Commissioner races from the data
"""
import json

print("Removing 2022 Commissioner races completely...\n")

# Load the data
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

# Commissioner races to remove
commissioner_races = [
    'commissioner_of_agriculture_2022',
    'commissioner_of_insurance_2022',
    'commissioner_of_labor_2022'
]

removed_count = 0

for race in commissioner_races:
    if race in data['results_by_year']['2022']:
        del data['results_by_year']['2022'][race]
        print(f"✓ Removed: {race}")
        removed_count += 1
    else:
        print(f"  Not found: {race}")

print(f"\n{'='*60}")
print(f"Total races removed: {removed_count}")
print("\n2022 elections now include only:")
for race_key in sorted(data['results_by_year']['2022'].keys()):
    print(f"  - {race_key}")

# Save the cleaned data
with open('data/results_by_year_grouped.final.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Saved to results_by_year_grouped.final.json")
print("\nCommissioner races removed from map completely.")
