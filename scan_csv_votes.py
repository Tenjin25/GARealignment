import os
import pandas as pd

def scan_csvs_for_votes_column(data_folder):
    print("Scanning CSV files in:", data_folder)
    for fname in os.listdir(data_folder):
        if not fname.endswith('.csv'):
            continue
        fpath = os.path.join(data_folder, fname)
        try:
            df = pd.read_csv(fpath, nrows=1)
            columns = [c.lower() for c in df.columns]
            if 'votes' in columns:
                print(f"[OK] {fname} contains a 'votes' column.")
            else:
                print(f"[WARN] {fname} does NOT contain a 'votes' column. Columns: {df.columns.tolist()}")
        except Exception as e:
            print(f"[ERROR] Could not read {fname}: {e}")

def print_all_csv_headers(data_folder):
    print("\n--- CSV Headers in data folder ---")
    for fname in os.listdir(data_folder):
        if not fname.endswith('.csv'):
            continue
        fpath = os.path.join(data_folder, fname)
        try:
            df = pd.read_csv(fpath, nrows=1)
            print(f"{fname}: {list(df.columns)}")
        except Exception as e:
            print(f"[ERROR] Could not read {fname}: {e}")

if __name__ == '__main__':
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    scan_csvs_for_votes_column(data_folder)
    print_all_csv_headers(data_folder)
