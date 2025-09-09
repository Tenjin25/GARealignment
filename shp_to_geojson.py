import geopandas as gpd
import os

def shp_to_geojson(shp_path, out_path=None):
    if out_path is None:
        out_path = os.path.splitext(shp_path)[0] + '.geojson'
    gdf = gpd.read_file(shp_path)
    gdf.to_file(out_path, driver='GeoJSON')
    print(f'Converted {shp_path} to {out_path}')

if __name__ == '__main__':
    # Example: convert 2000 GA county shapefile to GeoJSON
    shp_path = 'data/tl_2000_13_county.shp'
    shp_to_geojson(shp_path)
