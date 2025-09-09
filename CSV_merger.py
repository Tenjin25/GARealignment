import pandas as pd
import glob
import os

# Path to your data folder (adjust as needed)
data_folder = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2014"

# Find all CSV files in the folder
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

# Read and concatenate all CSVs
df_list = [pd.read_csv(f) for f in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save to a new CSV
merged_df.to_csv(os.path.join(data_folder, "merged_precincts_2014.csv"), index=False)