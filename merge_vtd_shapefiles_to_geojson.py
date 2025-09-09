
import os
import glob
import geopandas as gpd
import pandas as pd

# Directory containing all extracted 2009 VTD shapefiles
VTD_DIR = 'data/2009_vtd'
OUTPUT_GEOJSON = 'data/ga_2009_vtd_merged.geojson'

# Find all shapefiles in the directory (recursively)
shapefiles = glob.glob(os.path.join(VTD_DIR, '**', '*.shp'), recursive=True)

if not shapefiles:
    print(f'No shapefiles found in {VTD_DIR}')
    exit(1)

print(f'Found {len(shapefiles)} shapefiles. Merging...')

gdfs = []
for shp in shapefiles:
    try:
        gdf = gpd.read_file(shp)
        gdf['source_file'] = os.path.basename(shp)  # Optionally track source
        gdfs.append(gdf)
    except Exception as e:
        print(f'Failed to read {shp}: {e}')

if not gdfs:
    print('No valid shapefiles to merge.')
    exit(1)

merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=gdfs[0].crs)

print(f'Writing merged GeoJSON to {OUTPUT_GEOJSON} ...')
merged.to_file(OUTPUT_GEOJSON, driver='GeoJSON')
print('Done!')
