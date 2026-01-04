import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Detailed Check: 2000 US Senate & Public Service Commissioner ===\n')

year_2000 = data['results_by_year']['2000']

# Check US Senate
print('=== US SENATE 2000 ===\n')
senate = year_2000['us_senate_2000']['results']

print('Sample counties with detailed data:\n')
samples = ['Appling', 'Banks', 'Cherokee', 'Cobb', 'DeKalb', 'Fulton']

for county in samples:
    if county in senate:
        c = senate[county]
        print(f'{county}:')
        print(f'  Dem: {c["dem_candidate"]} - {c["dem_votes"]:,} votes')
        print(f'  Rep: {c["rep_candidate"]} - {c["rep_votes"]:,} votes')
        print(f'  Other: {c["other_votes"]:,}')
        print(f'  Total: {c["total_votes"]:,}')
        print(f'  Winner: {c["winner_name"]} ({c["margin_pct"]})')
        print(f'  Competitiveness: {c["competitiveness"]["category"]} - {c["competitiveness"]["party"]}')
        print()

# Check Public Service Commissioner
print('\n=== PUBLIC SERVICE COMMISSIONER 2000 ===\n')
psc = year_2000['public_service_commissioner_2000']['results']

print('Sample counties with detailed data:\n')
for county in samples:
    if county in psc:
        c = psc[county]
        print(f'{county}:')
        print(f'  Dem: {c["dem_candidate"]} - {c["dem_votes"]:,} votes')
        print(f'  Rep: {c["rep_candidate"]} - {c["rep_votes"]:,} votes')
        print(f'  Other: {c["other_votes"]:,}')
        print(f'  Total: {c["total_votes"]:,}')
        print(f'  Winner: {c["winner_name"]} ({c["margin_pct"]})')
        print(f'  Competitiveness: {c["competitiveness"]["category"]} - {c["competitiveness"]["party"]}')
        print()

# Show distribution of winners
print('\n=== Winner Distribution ===\n')

print('US Senate 2000:')
senate_winners = {}
for county, cdata in senate.items():
    winner = cdata['winner_name']
    senate_winners[winner] = senate_winners.get(winner, 0) + 1
for winner, count in sorted(senate_winners.items(), key=lambda x: -x[1]):
    print(f'  {winner}: {count} counties')

print('\nPublic Service Commissioner 2000:')
psc_winners = {}
for county, cdata in psc.items():
    winner = cdata['winner_name']
    psc_winners[winner] = psc_winners.get(winner, 0) + 1
for winner, count in sorted(psc_winners.items(), key=lambda x: -x[1]):
    print(f'  {winner}: {count} counties')

# Check if there are any Republican-leaning counties
print('\n=== Republican Counties in These Races ===\n')

print('US Senate - Republican wins:')
rep_senate = [(c, d) for c, d in senate.items() if d['winner'] == 'REPUBLICAN']
print(f'Total: {len(rep_senate)} counties')
for county, cdata in sorted(rep_senate, key=lambda x: -float(x[1]['margin_pct'].replace('R+', '').replace('D+', '')))[:5]:
    print(f'  {county}: {cdata["winner_name"]} {cdata["margin_pct"]} → {cdata["competitiveness"]["category"]}')

print('\nPublic Service Commissioner - Republican wins:')
rep_psc = [(c, d) for c, d in psc.items() if d['winner'] == 'REPUBLICAN']
print(f'Total: {len(rep_psc)} counties')
for county, cdata in sorted(rep_psc, key=lambda x: -float(x[1]['margin_pct'].replace('R+', '').replace('D+', '')))[:5]:
    print(f'  {county}: {cdata["winner_name"]} {cdata["margin_pct"]} → {cdata["competitiveness"]["category"]}')
