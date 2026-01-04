"""
Rename the standardized 2022 file to match the naming convention.
"""

import os
import shutil

old_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\2022_ga_general_precinct-level.csv"
new_file = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\20221108__ga__general__precinct-total.csv"

if os.path.exists(old_file):
    shutil.copy(old_file, new_file)
    print(f"File copied to: {new_file}")
    print(f"Original file kept at: {old_file}")
else:
    print(f"Source file not found: {old_file}")
