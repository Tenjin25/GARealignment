import json
import sys

# Usage: python trim_json_keys.py input.json output.json
if len(sys.argv) != 3:
    print('Usage: python trim_json_keys.py input.json output.json')
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

def trim_keys(obj):
    if isinstance(obj, dict):
        return {k.strip(): trim_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [trim_keys(i) for i in obj]
    else:
        return obj

with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

trimmed = trim_keys(data)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(trimmed, f, indent=2)

print(f'Whitespace trimmed from all keys. Output written to {output_path}')
