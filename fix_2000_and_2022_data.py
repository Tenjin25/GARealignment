import json
import os

def calculate_competitiveness(margin_pct, winner_party):
    """Calculate competitiveness rating based on margin and winner."""
    margin = abs(margin_pct)
    
    if margin >= 40:
        category = "Annihilation"
        party = winner_party
    elif margin >= 30:
        category = "Dominant"
        party = winner_party
    elif margin >= 20:
        category = "Stronghold"
        party = winner_party
    elif margin >= 10:
        category = "Safe"
        party = winner_party
    elif margin >= 5.5:
        category = "Likely"
        party = winner_party
    elif margin >= 1:
        category = "Lean"
        party = winner_party
    elif margin >= 0.5:
        category = "Tilt"
        party = winner_party
    else:
        category = "Tossup"
        party = "TOSSUP"
    
    # Generate code and color
    if party == "TOSSUP":
        code = "TOSSUP"
        color = "#f7f7f7"
    else:
        code = f"{party}_{category.upper()}"
        if party == "REPUBLICAN":
            if margin >= 40: color = "#67000d"
            elif margin >= 30: color = "#a50f15"
            elif margin >= 20: color = "#cb181d"
            elif margin >= 10: color = "#ef3b2c"
            elif margin >= 5.5: color = "#fb6a4a"
            elif margin >= 1: color = "#fcae91"
            else: color = "#fee8c8"
        else:  # DEMOCRAT
            if margin >= 40: color = "#08306b"
            elif margin >= 30: color = "#08519c"
            elif margin >= 20: color = "#3182bd"
            elif margin >= 10: color = "#6baed6"
            elif margin >= 5.5: color = "#9ecae1"
            elif margin >= 1: color = "#c6dbef"
            else: color = "#e1f5fe"
    
    return {
        "category": category,
        "party": party,
        "code": code,
        "color": color
    }

def parse_margin_pct(margin_str):
    """Parse margin percentage from string like 'R+30.29' or 'D+10.42'."""
    if isinstance(margin_str, (int, float)):
        return float(margin_str)
    if isinstance(margin_str, str) and (margin_str.startswith('R+') or margin_str.startswith('D+')):
        return float(margin_str[2:])
    return 0.0

def fix_2000_ratings(data):
    """Fix competitiveness ratings for 2000 contests."""
    year_2000 = data['results_by_year'].get('2000', {})
    fixed_count = 0
    
    for contest_name, contest_data in year_2000.items():
        if 'results' not in contest_data:
            continue
            
        for county_name, county_data in contest_data['results'].items():
            margin_str = county_data.get('margin_pct', '')
            winner_party = county_data.get('winner_party', '').upper()
            
            if not margin_str or not winner_party:
                continue
            
            margin_pct = parse_margin_pct(margin_str)
            correct_comp = calculate_competitiveness(margin_pct, winner_party)
            
            current_comp = county_data.get('competitiveness', {})
            if (current_comp.get('category') != correct_comp['category'] or
                current_comp.get('party') != correct_comp['party'] or
                current_comp.get('code') != correct_comp['code'] or
                current_comp.get('color') != correct_comp['color']):
                
                county_data['competitiveness'] = correct_comp
                fixed_count += 1
                print(f"Fixed {county_name} in {contest_name}: {margin_str} -> {correct_comp['category']} {correct_comp['party']}")
    
    return fixed_count

def check_missing_2022_counties(data):
    """Check which counties are missing from 2022 contests."""
    year_2022 = data['results_by_year'].get('2022', {})
    
    print("\n2022 Contest County Counts:")
    for contest_name, contest_data in year_2022.items():
        if 'results' in contest_data:
            county_count = len(contest_data['results'])
            print(f"  {contest_name}: {county_count} counties")
            
            if county_count < 159:
                print(f"    Missing {159 - county_count} counties!")
    
    # Get list of all counties from governor (should be complete)
    governor_counties = set(year_2022.get('governor_2022', {}).get('results', {}).keys())
    print(f"\nGovernor contest has {len(governor_counties)} counties")
    
    # Check other contests
    for contest_name in ['lieutenant_governor_2022', 'secretary_of_state_2022', 'attorney_general_2022']:
        if contest_name in year_2022:
            contest_counties = set(year_2022[contest_name].get('results', {}).keys())
            missing = governor_counties - contest_counties
            if missing:
                print(f"\n{contest_name} is missing {len(missing)} counties:")
                print(f"  {', '.join(sorted(list(missing)[:10]))}" + (" ..." if len(missing) > 10 else ""))

def main():
    json_path = 'data/results_by_year_grouped.final.json'
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return
    
    print("Loading data...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    print("\n=== Fixing 2000 Contest Ratings ===")
    fixed_2000 = fix_2000_ratings(data)
    print(f"\nFixed {fixed_2000} county ratings in 2000")
    
    print("\n=== Checking 2022 Missing Counties ===")
    check_missing_2022_counties(data)
    
    # Save the fixed data
    output_path = 'data/results_by_year_grouped.final.json'
    print(f"\nSaving to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Done!")

if __name__ == '__main__':
    main()
