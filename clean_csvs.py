import csv
import os

# This script will clean all CSVs in the 'data' folder by removing extra columns beyond the header.
# It will write cleaned files to a 'data/cleaned' subfolder with the same filenames.

def clean_csvs(data_dir='data', out_dir='data/cleaned'):
    os.makedirs(out_dir, exist_ok=True)
    for fname in os.listdir(data_dir):
        if not fname.endswith('.csv'):
            continue
        in_path = os.path.join(data_dir, fname)
        out_path = os.path.join(out_dir, fname)
        with open(in_path, 'r', encoding='utf-8-sig', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)
            if not rows:
                continue
            header = rows[0]
            cleaned_rows = [header]
            for row in rows[1:]:
                cleaned_rows.append(row[:len(header)])
        with open(out_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_rows)
        print(f"Cleaned: {fname} -> {out_path}")

if __name__ == '__main__':
    clean_csvs()
