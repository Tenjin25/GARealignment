import json

d = json.load(open('data/results_by_year_grouped.final.json'))
print('2022 contests:')
for k in sorted(d['results_by_year']['2022'].keys()):
    count = len(d['results_by_year']['2022'][k]['results'])
    print(f'  {k}: {count} counties')

print('\nSample estimated counties:')
for county in ['Fulton', 'Gwinnett', 'Cherokee']:
    result = d['results_by_year']['2022']['commissioner_of_agriculture_2022']['results'][county]
    print(f'\n{county} (Agriculture):')
    print(f'  Winner: {result["winner_name"]} ({result["winner_party"]})')
    print(f'  Margin: {result["margin_pct"]}%')
    print(f'  Votes: {result["rep_votes"]:,} R / {result["dem_votes"]:,} D')
    print(f'  Estimated: {result.get("estimated", False)}')
