import re
import json

with open('nyt_full_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Look for embedded data patterns
patterns = [
    (r'window\.__PRELOADED_STATE__', 'PRELOADED_STATE'),
    (r'window\.__INITIAL_STATE__', 'INITIAL_STATE'),
    (r'"commissioner', 'commissioner keyword'),
    (r'"agriculture', 'agriculture keyword'),
    (r'"insurance', 'insurance keyword'),
    (r'"labor', 'labor keyword'),
]

print('Searching for data patterns in NY Times page:\n')
for pattern, name in patterns:
    matches = re.findall(pattern, content, re.IGNORECASE)
    if matches:
        print(f'  Found {len(matches)} matches for: {name}')

# Check if there's any JSON-LD structured data
json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
if json_ld:
    print(f'\nFound {len(json_ld)} JSON-LD scripts')

# Look for large JSON objects
large_json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
potential_json = re.findall(large_json_pattern, content)
json_objects = [j for j in potential_json if len(j) > 1000 and ('county' in j.lower() or 'race' in j.lower())]

if json_objects:
    print(f'\nFound {len(json_objects)} large JSON-like objects with election keywords')
    print(f'Sizes: {[len(j) for j in json_objects[:5]]} bytes')

print('\nDone checking HTML file')
