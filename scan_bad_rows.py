import csv
import os

def scan_for_bad_rows(data_dir='data/cleaned'):
    for fname in os.listdir(data_dir):
        if not fname.endswith('.csv'):
            continue
        fpath = os.path.join(data_dir, fname)
        with open(fpath, 'r', encoding='utf-8-sig', newline='') as infile:
            reader = csv.reader(infile)
            rows = list(reader)
            if not rows:
                continue
            header = rows[0]
            ncols = len(header)
            for i, row in enumerate(rows[1:], 2):
                if len(row) != ncols:
                    print(f"{fname} line {i}: Wrong number of columns ({len(row)} vs {ncols})")
                for j, val in enumerate(row):
                    # Check for non-numeric in vote columns (simple heuristic: column name contains 'vote')
                    if 'vote' in header[j].lower():
                        try:
                            float(val)
                        except ValueError:
                            if val.strip() != '' and not val.strip().isalpha():
                                print(f"{fname} line {i}: Non-numeric in vote column '{header[j]}': '{val}'")

if __name__ == '__main__':
    scan_for_bad_rows()
