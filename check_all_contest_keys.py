import json

with open('data/results_by_year_grouped.final.json') as f:
    data = json.load(f)

for year in sorted(data['results_by_year'].keys()):
    print(f'\n{year}:')
    for key in data['results_by_year'][year].keys():
        print(f'  - {key}')
