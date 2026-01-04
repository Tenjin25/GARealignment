import json

with open('ga_2022_sos_raw2.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('localityElections type:', type(d.get('localityElections')))
locs = d.get('localityElections')
print('Number of localities:', len(locs) if locs else 0)

if locs and len(locs) > 0:
    print('\nFirst locality keys:', list(locs[0].keys()))
    print('\nFirst locality ballotItems count:', len(locs[0].get('ballotItems', [])))
    
    if len(locs[0].get('ballotItems', [])) > 5:
        agr_item = locs[0]['ballotItems'][5]
        print('\nAgriculture Commissioner ballot item:')
        print('  Name:', agr_item.get('name', [{}])[0].get('text', 'N/A'))
        print('  Has summaryResults:', 'summaryResults' in agr_item)
        if 'summaryResults' in agr_item:
            print('  Candidates:', len(agr_item['summaryResults'].get('ballotOptions', [])))
