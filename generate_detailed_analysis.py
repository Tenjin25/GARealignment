#!/usr/bin/env python3
"""
Generate detailed year-by-year analysis for key counties
"""
import json

with open('data/results_by_year_grouped.final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

counties = ['Henry', 'Newton', 'Cobb', 'Douglas', 'Gwinnett', 'Rockdale', 
            'Jackson', 'Forsyth', 'Fayette', 'Hall', 'Columbia', 'Cherokee']

# Presidential years
pres_years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

def get_pres_data(year, county):
    """Get presidential data for a county in a year"""
    year_data = data['results_by_year'].get(str(year), {})
    
    # Find presidential contest
    for key in year_data.keys():
        if 'president' in key.lower():
            results = year_data[key].get('results', {})
            county_data = results.get(county)
            if county_data:
                return {
                    'margin': county_data.get('margin_pct', 'N/A'),
                    'dem_pct': round((county_data.get('dem_votes', 0) / county_data.get('two_party_total', 1)) * 100, 2) if county_data.get('two_party_total', 0) > 0 else 0,
                    'rep_pct': round((county_data.get('rep_votes', 0) / county_data.get('two_party_total', 1)) * 100, 2) if county_data.get('two_party_total', 0) > 0 else 0,
                    'dem_votes': county_data.get('dem_votes', 0),
                    'rep_votes': county_data.get('rep_votes', 0),
                    'total': county_data.get('total_votes', 0),
                    'dem_candidate': county_data.get('dem_candidate', ''),
                    'rep_candidate': county_data.get('rep_candidate', ''),
                    'winner': county_data.get('winner_party', '')
                }
    return None

print("=" * 100)
print("DETAILED COUNTY ANALYSIS - PRESIDENTIAL ELECTIONS 2000-2024")
print("=" * 100)

for county in counties:
    print(f"\n{'='*100}")
    print(f"{county.upper()} COUNTY")
    print(f"{'='*100}")
    
    trend_data = []
    flip_year = None
    last_winner = None
    
    for year in pres_years:
        data_point = get_pres_data(year, county)
        if data_point:
            trend_data.append((year, data_point))
            
            # Detect flip
            if last_winner and last_winner != data_point['winner']:
                flip_year = year
            last_winner = data_point['winner']
    
    # Print year-by-year
    print(f"\n{'Year':<6} {'Margin':<12} {'Dem%':<8} {'Rep%':<8} {'Dem Votes':<12} {'Rep Votes':<12} {'Turnout':<12} {'Winner'}")
    print("-" * 100)
    
    for year, d in trend_data:
        print(f"{year:<6} {str(d['margin']):<12} {d['dem_pct']:<8.2f} {d['rep_pct']:<8.2f} "
              f"{d['dem_votes']:<12,} {d['rep_votes']:<12,} {d['total']:<12,} {d['winner']}")
    
    # Calculate total shift
    if len(trend_data) >= 2:
        first_year, first_data = trend_data[0]
        last_year, last_data = trend_data[-1]
        
        print(f"\n📊 OVERALL TREND ({first_year}-{last_year}):")
        print(f"   Margin Shift: {first_data['margin']} → {last_data['margin']}")
        print(f"   Turnout Change: {first_data['total']:,} → {last_data['total']:,} "
              f"({((last_data['total']/first_data['total'])-1)*100:+.1f}%)")
        
        if flip_year:
            print(f"   🔄 FLIPPED in {flip_year}: {trend_data[pres_years.index(flip_year)-1][1]['winner']} → "
                  f"{trend_data[pres_years.index(flip_year)][1]['winner']}")
        
        # Find tipping point (when margin became competitive)
        for i, (year, d) in enumerate(trend_data):
            margin_val = float(d['margin'].replace('R+', '').replace('D+', ''))
            if i > 0 and margin_val < 10 and float(trend_data[i-1][1]['margin'].replace('R+', '').replace('D+', '')) >= 10:
                print(f"   ⚠️  Became COMPETITIVE in {year} (margin < 10 points)")
                break

print("\n" + "=" * 100)
