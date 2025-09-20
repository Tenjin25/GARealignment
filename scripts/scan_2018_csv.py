import csv

CSV_PATH = "data/merged_precincts_2018.csv"

# List all columns in the CSV and sample a few rows for inspection
def main():
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("Columns:", reader.fieldnames)
        print("\nSample rows:")
        for i, row in enumerate(reader):
            print(row)
            if i >= 4:
                break

if __name__ == "__main__":
    main()
