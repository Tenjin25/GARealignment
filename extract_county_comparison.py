import json

# Load the data
with open('data/results_by_year_grouped.final.json', 'r') as f:
    data = json.load(f)

# Target counties
target_counties = [
    'Henry', 'Newton', 'Cobb', 'Douglas', 'Gwinnett', 'Rockdale',
    'Jackson', 'Forsyth', 'Fayette', 'Hall', 'Columbia', 'Cherokee'
]

# Extract 2000 and 2024 data
counties_2000 = data['results_by_year']['2000']['president_2000']['results']
counties_2024 = data['results_by_year']['2024']['president_2024']['results']

print("=" * 80)
print("GEORGIA PRESIDENTIAL ELECTION DATA: 2000 vs 2024 COMPARISON")
print("=" * 80)
print()

for county in target_counties:
    if county in counties_2000 and county in counties_2024:
        data_2000 = counties_2000[county]
        data_2024 = counties_2024[county]
        
        print(f"\n{'=' * 80}")
        print(f"{county.upper()} COUNTY")
        print(f"{'=' * 80}")
        
        print(f"\n2000 Presidential Election:")
        print(f"  Candidates: {data_2000['dem_candidate']} (D) vs {data_2000['rep_candidate']} (R)")
        print(f"  Democratic Votes: {data_2000['dem_votes']:,}")
        print(f"  Republican Votes: {data_2000['rep_votes']:,}")
        print(f"  Total Votes: {data_2000['total_votes']:,}")
        print(f"  Margin: {data_2000['margin_pct']}")
        
        print(f"\n2024 Presidential Election:")
        print(f"  Candidates: {data_2024['dem_candidate']} (D) vs {data_2024['rep_candidate']} (R)")
        print(f"  Democratic Votes: {data_2024['dem_votes']:,}")
        print(f"  Republican Votes: {data_2024['rep_votes']:,}")
        print(f"  Total Votes: {data_2024['total_votes']:,}")
        print(f"  Margin: {data_2024['margin_pct']}")
        
        # Calculate change
        vote_growth = data_2024['total_votes'] - data_2000['total_votes']
        vote_growth_pct = (vote_growth / data_2000['total_votes']) * 100
        
        # Parse margins for comparison
        margin_2000_val = float(data_2000['margin_pct'].replace('R+', '').replace('D+', ''))
        margin_2024_val = float(data_2024['margin_pct'].replace('R+', '').replace('D+', ''))
        
        # Determine shift direction
        if 'R+' in data_2000['margin_pct'] and 'D+' in data_2024['margin_pct']:
            shift = f"FLIPPED from R+{margin_2000_val} to D+{margin_2024_val} (Democratic gain of {margin_2000_val + margin_2024_val:.2f} points)"
        elif 'D+' in data_2000['margin_pct'] and 'R+' in data_2024['margin_pct']:
            shift = f"FLIPPED from D+{margin_2000_val} to R+{margin_2024_val} (Republican gain of {margin_2000_val + margin_2024_val:.2f} points)"
        elif 'R+' in data_2000['margin_pct'] and 'R+' in data_2024['margin_pct']:
            change = margin_2024_val - margin_2000_val
            if change > 0:
                shift = f"Shifted MORE Republican (increased by {change:.2f} points)"
            else:
                shift = f"Shifted LESS Republican (decreased by {abs(change):.2f} points)"
        else:  # Both D+
            change = margin_2024_val - margin_2000_val
            if change > 0:
                shift = f"Shifted MORE Democratic (increased by {change:.2f} points)"
            else:
                shift = f"Shifted LESS Democratic (decreased by {abs(change):.2f} points)"
        
        print(f"\nChange from 2000 to 2024:")
        print(f"  Vote Growth: {vote_growth:,} ({vote_growth_pct:+.1f}%)")
        print(f"  Political Shift: {shift}")

print("\n" + "=" * 80)
