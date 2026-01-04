import geopandas as gpd

# Input shapefile path (update if needed)
input_shapefile = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\tl_2020_13_county20\tl_2020_13_county20.shp"
# Output GeoJSON path
output_geojson = r"C:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\tl_2020_13_county20.geojson"

gdf = gpd.read_file(input_shapefile)
gdf.to_file(output_geojson, driver="GeoJSON")
print("Conversion complete:", output_geojson)
