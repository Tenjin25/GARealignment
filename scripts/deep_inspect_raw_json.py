import json

# Check if the raw JSON has county-level detail we missed
with open('ga_2022_sos_raw2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check localityElections structure more carefully
if data.get('localityElections'):
    print("LocalityElections structure exists!")
    print(f"Number of localities: {len(data['localityElections'])}")
    
    # Find a locality with the contests we need
    for loc in data['localityElections'][:5]:
        loc_name = loc.get('name', [{}])[0].get('text', 'Unknown') if loc.get('name') else 'Unknown'
        print(f"\n{loc_name}:")
        print(f"  Keys: {list(loc.keys())[:15]}")
        
        # Check if there's contest data
        if 'publicReportCategories' in loc:
            categories = loc['publicReportCategories']
            print(f"  Public report categories: {len(categories) if categories else 0}")
            
            if categories:
                for cat in categories[:3]:
                    print(f"    Category: {cat.get('name', [{}])[0].get('text', 'N/A') if cat.get('name') else 'N/A'}")
                    if 'contests' in cat:
                        print(f"      Contests: {len(cat.get('contests', []))}")

# Check if contest results are stored elsewhere
print("\n" + "="*70)
print("Checking ballot items for county breakdowns...")
print("="*70)

ballot_items = data.get('ballotItems', [])
# Look at Commissioner of Agriculture (index 5)
if len(ballot_items) > 5:
    agr_item = ballot_items[5]
    print(f"\nContest: {agr_item['name'][0]['text']}")
    print(f"Keys: {list(agr_item.keys())}")
    
    # Check if there's a results breakdown by locality
    if 'localityResults' in agr_item:
        print(f"Has localityResults: {len(agr_item['localityResults'])} localities")
    
    # Check summary results structure
    if 'summaryResults' in agr_item:
        summary = agr_item['summaryResults']
        print(f"Summary results keys: {list(summary.keys())}")
        
        ballot_opts = summary.get('ballotOptions', [])
        if ballot_opts:
            print(f"\nCandidates ({len(ballot_opts)}):")
            for opt in ballot_opts:
                name = opt['name'][0]['text']
                votes = opt.get('voteCount', 0)
                print(f"  {name}: {votes:,} votes")
                
                # Check if there's county breakdown in groupResults
                if 'groupResults' in opt:
                    groups = opt['groupResults']
                    print(f"    Has {len(groups)} vote groups")
