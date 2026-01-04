import csv
import json

# Load the precinct data
print("Loading 2022 precinct data...")
with open('data/20221108__ga__general__precinct.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print(f"\nColumns: {list(rows[0].keys())}")

# Clean up column names (they have spaces)
for row in rows:
    cleaned = {}
    for k, v in row.items():
        key = k.strip() if k else 'unknown'
        val = v.strip() if (v and isinstance(v, str)) else (v if v else '')
        cleaned[key] = val
    row.clear()
    row.update(cleaned)

# Check unique offices
offices = set(r['office'] for r in rows)
print(f"\nUnique offices ({len(offices)}):")
for office in sorted(offices):
    print(f"  - {office}")

# Check counties for statewide offices
print("\n\nChecking Commissioner of Agriculture:")
agr_rows = [r for r in rows if 'Agriculture' in r.get('office', '')]
print(f"  Total Agriculture rows: {len(agr_rows)}")
counties = set(r['county'] for r in agr_rows)
print(f"  Unique counties: {len(counties)}")
print(f"  Sample counties: {sorted(list(counties))[:10]}")

print("\n\nChecking Commissioner of Insurance:")
ins_rows = [r for r in rows if 'Insurance' in r.get('office', '')]
print(f"  Total Insurance rows: {len(ins_rows)}")
counties = set(r['county'] for r in ins_rows)
print(f"  Unique counties: {len(counties)}")

print("\n\nChecking Commissioner of Labor:")
lab_rows = [r for r in rows if 'Labor' in r.get('office', '')]
print(f"  Total Labor rows: {len(lab_rows)}")
counties = set(r['county'] for r in lab_rows)
print(f"  Unique counties: {len(counties)}")

print("\n\nChecking State School Superintendent:")
sup_rows = [r for r in rows if 'School' in r.get('office', '') or 'Superintendent' in r.get('office', '')]
print(f"  Total Superintendent rows: {len(sup_rows)}")
counties = set(r['county'] for r in sup_rows)
print(f"  Unique counties: {len(counties)}")

# Now check what we have in the current data
print("\n\n=== CURRENT DATA ===")
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    election_data = json.load(f)

year_2022 = election_data.get('results_by_year', {}).get('2022', {})
print(f"2022 contests: {list(year_2022.keys())}")

for contest_key in year_2022:
    results = year_2022[contest_key].get('results', {})
    print(f"\n{contest_key}: {len(results)} counties")
    if len(results) < 159:
        print(f"  Missing {159 - len(results)} counties!")
