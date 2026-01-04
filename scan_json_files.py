import json
import os

def scan_json_file(filepath):
    print(f"\nScanning: {filepath}")
    if not os.path.exists(filepath):
        print("File not found.")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        print("Top-level keys:", list(data.keys()))
        for key in data:
            value = data[key]
            if isinstance(value, dict):
                print(f"  Key '{key}' contains {len(value)} sub-keys.")
            elif isinstance(value, list):
                print(f"  Key '{key}' contains a list of length {len(value)}.")
            else:
                print(f"  Key '{key}' contains a value of type {type(value).__name__}.")
    elif isinstance(data, list):
        print(f"Top-level is a list of length {len(data)}.")
    else:
        print(f"Top-level is of type {type(data).__name__}.")

if __name__ == "__main__":
    files = [
        r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\ga_county_results_trimmed.updated.json",
        r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data_files\results_by_year_grouped.json"
    ]
    for file in files:
        scan_json_file(file)
