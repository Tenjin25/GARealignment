import json

with open('data/results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('2000 contests:', list(data['results_by_year']['2000'].keys()))
print()

# Check competitiveness format for one county
us_senate = data['results_by_year']['2000']['us_senate_2000']
first_county = list(us_senate.keys())[0]
print(f'First county: {first_county}')
print(f'Competitiveness: {us_senate[first_county]["competitiveness"]}')
