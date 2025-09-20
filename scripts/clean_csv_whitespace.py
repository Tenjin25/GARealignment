import csv

INPUT_CSV = "data/2018/merged_precincts_2018.csv"
OUTPUT_CSV = "data/2018/merged_precincts_2018.cleaned.csv"

def clean_csv_whitespace(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = [fn.strip() for fn in reader.fieldnames]
        rows = []
        for row in reader:
            clean_row = {fn.strip(): (v.strip() if isinstance(v, str) else v) for fn, v in row.items()}
            rows.append(clean_row)
    with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Cleaned CSV written to {output_path}")

if __name__ == "__main__":
    clean_csv_whitespace(INPUT_CSV, OUTPUT_CSV)
