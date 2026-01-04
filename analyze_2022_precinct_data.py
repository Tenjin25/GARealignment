import pandas as pd
import json

print("Analyzing 2022 precinct data for Commissioner races...\n")

# Load the precinct data with error handling
try:
    df = pd.read_csv('data/20221108__ga__general__precinct.csv', on_bad_lines='skip', low_memory=False)
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit(1)

print(f"Total rows: {len(df):,}")
print(f"Columns: {list(df.columns)}\n")

# Filter for Commissioner races
commissioner_races = df[df['office'].str.contains('Commissioner', case=False, na=False)]
print(f"Commissioner race rows: {len(commissioner_races):,}")

# Check unique offices
print("\nUnique Commissioner offices:")
for office in sorted(commissioner_races['office'].unique()):
    print(f"  - {office}")

# For each commissioner race, count counties
print("\n" + "="*60)
for office in sorted(commissioner_races['office'].unique()):
    office_data = commissioner_races[commissioner_races['office'] == office]
    counties = office_data['county'].unique()
    print(f"\n{office}:")
    print(f"  Counties with data: {len(counties)}")
    print(f"  Total votes: {office_data['votes'].sum():,}")
    
    # List missing counties (GA has 159 total)
    all_counties_df = df[df['office'] == 'U.S. Senate']  # Use Senate as reference
    all_counties = set(all_counties_df['county'].unique())
    missing = sorted(all_counties - set(counties))
    
    if missing:
        print(f"  Missing counties ({len(missing)}): {', '.join(missing[:10])}")
        if len(missing) > 10:
            print(f"    ... and {len(missing) - 10} more")
    
    # Check data quality - any weird values?
    candidates = office_data.groupby('candidate')['votes'].sum().sort_values(ascending=False)
    print(f"  Top candidates:")
    for cand, votes in candidates.head(3).items():
        print(f"    {cand}: {votes:,} votes")

print("\n" + "="*60)
print("\nChecking if we can get missing counties from the data...")

# Maybe the data is there but formatted differently or in different columns
print("\nUnique values in 'office' column (first 30):")
for office in sorted(df['office'].unique())[:30]:
    print(f"  - {office}")
