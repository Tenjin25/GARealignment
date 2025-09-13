import json
import sys

def trim_keys_and_strings(obj):
    if isinstance(obj, dict):
        return {k.strip(): trim_keys_and_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [trim_keys_and_strings(i) for i in obj]
    elif isinstance(obj, str):
        return obj.strip()
    else:
        return obj

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python trim_json_keys_and_strings.py input.json output.json')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    trimmed = trim_keys_and_strings(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(trimmed, f, indent=2)

    print(f'Whitespace trimmed from all keys and string values. Output written to {output_path}')
