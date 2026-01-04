#!/usr/bin/env python3
"""
Fill missing 2022 county info from the aligned CSV.
Writes: data_files/Election_Data_GA.v04/filled_missing_2022.json
Also prints a short summary.
"""
import csv
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'election_data_GA.v04-aligned.csv')
MISSING_PATH = os.path.join(ROOT, 'missing_dict.json')
OUT_PATH = os.path.join(ROOT, 'data_files', 'Election_Data_GA.v04', 'filled_missing_2022.json')

def normalize(s):
    if s is None:
        return ''
    s = s.strip().lower()
    # remove non-alphanumeric
    s = re.sub(r"[^a-z0-9]", '', s)
    return s

if not os.path.exists(CSV_PATH):
    print('CSV not found at', CSV_PATH)
    raise SystemExit(1)

with open(CSV_PATH, newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh, skipinitialspace=True)
    rows = list(reader)

# build name map
name_map = {}
for r in rows:
    name = r.get('Name') or r.get(' Name') or r.get('Name ')
    if not name:
        # try first non-empty field after GEOID
        for k in r:
            if k.lower().startswith('geoid'):
                continue
            if r[k].strip():
                name = r[k]
                break
    key = normalize(name)
    if key in name_map:
        # keep first occurrence but store list
        if isinstance(name_map[key], list):
            name_map[key].append(r)
        else:
            name_map[key] = [name_map[key], r]
    else:
        name_map[key] = r

# load missing
with open(MISSING_PATH, encoding='utf-8') as fh:
    missing = json.load(fh)

if '2022' not in missing:
    print('No 2022 section in missing_dict.json')
    raise SystemExit(1)

missing_2022 = missing['2022']
output = {}
not_found = []
found_count = 0

# columns to extract: any column name containing '22' (case-insensitive)
csv_columns = rows[0].keys() if rows else []
columns_22 = [c for c in csv_columns if '22' in c]
# fallback: if none, include all
if not columns_22:
    columns_22 = list(csv_columns)

for contest, counties in missing_2022.items():
    output[contest] = {}
    for county in counties:
        n = normalize(county)
        candidate = None
        # direct match
        if n in name_map:
            candidate = name_map[n]
        else:
            # try partial match: any name_map key containing n or vice-versa
            for k in name_map:
                if n and (n in k or k in n):
                    candidate = name_map[k]
                    break
        if not candidate:
            # try matching by first word
            for k in name_map:
                if k.split()[0] == n.split()[0]:
                    candidate = name_map[k]
                    break
        if not candidate:
            not_found.append(county)
            continue
        # if multiple rows, pick first
        if isinstance(candidate, list):
            candidate = candidate[0]
        entry = {
            'GEOID20': candidate.get('GEOID20') or candidate.get(' GEOID20') or candidate.get('GEOID20 '),
            'Name': candidate.get('Name'),
            'data': {k: candidate.get(k) for k in columns_22}
        }
        output[contest][county] = entry
        found_count += 1

# write output
with open(OUT_PATH, 'w', encoding='utf-8') as fh:
    json.dump(output, fh, indent=2)

print(f'Wrote {OUT_PATH}')
print(f'Found entries: {found_count}')
if not_found:
    print('Counties not found (left unchanged):', len(not_found))
    for c in not_found:
        print(' -', c)
else:
    print('All missing counties located and written.')

```