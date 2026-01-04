#!/usr/bin/env python3
"""
Correct competitiveness ratings across all years to match the 7-tier system.
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JSON_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.json')
OUT_PATH = os.path.join(ROOT, 'data', 'results_by_year_grouped.corrected.json')

def calculate_competitiveness(margin_pct, winner_party):
    """Calculate competitiveness category based on margin using 7-tier system"""
    margin = abs(margin_pct)
    
    if margin >= 40:
        category = "Annihilation"
        code = f"{winner_party}_ANNIHILATION"
        color = "#67000d" if winner_party == "REPUBLICAN" else "#08306b"
        party = winner_party
    elif margin >= 30:
        category = "Dominant"
        code = f"{winner_party}_DOMINANT"
        color = "#a50f15" if winner_party == "REPUBLICAN" else "#08519c"
        party = winner_party
    elif margin >= 20:
        category = "Stronghold"
        code = f"{winner_party}_STRONGHOLD"
        color = "#cb181d" if winner_party == "REPUBLICAN" else "#3182bd"
        party = winner_party
    elif margin >= 10:
        category = "Safe"
        code = f"{winner_party}_SAFE"
        color = "#ef3b2c" if winner_party == "REPUBLICAN" else "#6baed6"
        party = winner_party
    elif margin >= 5.5:
        category = "Likely"
        code = f"{winner_party}_LIKELY"
        color = "#fb6a4a" if winner_party == "REPUBLICAN" else "#9ecae1"
        party = winner_party
    elif margin >= 1:
        category = "Lean"
        code = f"{winner_party}_LEAN"
        color = "#fcae91" if winner_party == "REPUBLICAN" else "#c6dbef"
        party = winner_party
    elif margin >= 0.5:
        category = "Tilt"
        code = f"{winner_party}_TILT"
        color = "#fee8c8" if winner_party == "REPUBLICAN" else "#e1f5fe"
        party = winner_party
    else:
        category = "Tossup"
        code = "TOSSUP"
        color = "#f7f7f7"
        party = "TOSSUP"  # Neutral for true tossups
    
    return {
        "category": category,
        "party": party,
        "code": code,
        "color": color
    }

def parse_margin_pct(margin_str):
    """Parse margin_pct string like 'R+30.29' or 'D+10.42' to get numeric value and party"""
    if not margin_str or not isinstance(margin_str, str):
        return 0, "REPUBLICAN"
    
    margin_str = margin_str.strip()
    party = "REPUBLICAN" if margin_str.startswith('R') else "DEMOCRAT"
    
    # Extract numeric value
    try:
        value = float(margin_str.replace('R+', '').replace('D+', '').replace('%', ''))
        return value, party
    except:
        return 0, party

print('Loading results JSON...')
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

total_updated = 0
total_checked = 0
updates_by_year = {}

print('Processing all years and contests...\n')

for year, year_data in data['results_by_year'].items():
    year_updates = 0
    
    for contest_name, contest_data in year_data.items():
        results = contest_data.get('results', {})
        
        for county_name, county_data in results.items():
            total_checked += 1
            
            # Get margin info
            margin_pct_str = county_data.get('margin_pct', '')
            margin_value, winner_party = parse_margin_pct(margin_pct_str)
            
            # If no margin_pct but we have winner and votes, calculate it
            if not margin_pct_str and 'winner' in county_data:
                winner_party = county_data['winner']
                dem_votes = county_data.get('dem_votes', 0)
                rep_votes = county_data.get('rep_votes', 0)
                two_party_total = county_data.get('two_party_total', dem_votes + rep_votes)
                
                if two_party_total > 0:
                    margin = abs(rep_votes - dem_votes)
                    margin_value = (margin / two_party_total * 100)
            
            # Calculate correct competitiveness
            correct_comp = calculate_competitiveness(margin_value, winner_party)
            
            # Check if current competitiveness matches
            current_comp = county_data.get('competitiveness', {})
            
            needs_update = False
            if not current_comp:
                needs_update = True
            elif (current_comp.get('category') != correct_comp['category'] or
                  current_comp.get('code') != correct_comp['code'] or
                  current_comp.get('color') != correct_comp['color']):
                needs_update = True
            
            if needs_update:
                county_data['competitiveness'] = correct_comp
                total_updated += 1
                year_updates += 1
    
    if year_updates > 0:
        updates_by_year[year] = year_updates
        print(f'Year {year}: Updated {year_updates} counties')

print(f'\n=== Summary ===')
print(f'Total counties checked: {total_checked:,}')
print(f'Total counties updated: {total_updated:,}')
print(f'Years affected: {len(updates_by_year)}')

if total_updated > 0:
    print(f'\nWriting corrected data to {OUT_PATH}...')
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print('Done!')
else:
    print('\nNo updates needed - all competitiveness ratings are correct!')
