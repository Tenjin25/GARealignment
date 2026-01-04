import json

# Check what contests are in the raw2 file
with open('ga_2022_sos_raw2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

contests = data.get('ballotItems', [])
print(f'Total ballot items: {len(contests)}')
print('\nAll statewide contests:')

for i, c in enumerate(contests[:30]):
    name_obj = c.get('name', [{}])
    if isinstance(name_obj, list) and len(name_obj) > 0:
        name = name_obj[0].get('text', 'N/A')
    else:
        name = 'N/A'
    print(f'  {i+1}. {name}')
