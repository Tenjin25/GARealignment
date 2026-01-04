#!/usr/bin/env python3
"""
Extract actual election margins for counties from the JSON data
"""
import json

# Load the data
with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Counties we want to analyze
counties = [
    'Henry', 'Newton', 'Cobb', 'Douglas', 'Gwinnett', 'Rockdale',
    'Jackson', 'Forsyth', 'Fayette', 'Hall', 'Columbia', 'Cherokee'
]

# Get presidential election data for 2000 and 2024
results_by_year = data['results_by_year']

def get_margin(year, county):
    """Get the margin for a county in a given year's presidential race"""
    year_data = results_by_year.get(str(year), {})
    
    # Find presidential contest key
    pres_key = None
    for key in year_data.keys():
        if 'president' in key.lower():
            pres_key = key
            break
    
    if not pres_key:
        return None
    
    contest_data = year_data[pres_key].get('results', {})
    county_data = contest_data.get(county)
    
    if not county_data:
        return None
    
    return county_data.get('margin_pct', 'N/A')

print("County Margin Trends (Presidential Elections):\n")
print(f"{'County':<15} {'2000':<15} {'2024':<15}")
print("-" * 45)

for county in counties:
    margin_2000 = get_margin(2000, county)
    margin_2024 = get_margin(2024, county)
    print(f"{county:<15} {str(margin_2000):<15} {str(margin_2024):<15}")

# Also get governor data for comparison
print("\n\nGovernor Race Margins:\n")
print(f"{'County':<15} {'2002':<15} {'2022':<15}")
print("-" * 45)

def get_gov_margin(year, county):
    """Get the margin for a county in a given year's governor race"""
    year_data = results_by_year.get(str(year), {})
    
    # Find governor contest key
    gov_key = None
    for key in year_data.keys():
        if 'governor' in key.lower():
            gov_key = key
            break
    
    if not gov_key:
        return None
    
    contest_data = year_data[gov_key].get('results', {})
    county_data = contest_data.get(county)
    
    if not county_data:
        return None
    
    return county_data.get('margin_pct', 'N/A')

for county in counties:
    margin_2002 = get_gov_margin(2002, county)
    margin_2022 = get_gov_margin(2022, county)
    print(f"{county:<15} {str(margin_2002):<15} {str(margin_2022):<15}")
