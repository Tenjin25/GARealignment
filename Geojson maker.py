import geopandas as gpd

# Replace with your actual shapefile path (no extension needed)
shapefile_path = "tl_2012_13_vtd10"
gdf = gpd.read_file(shapefile_path)
gdf.to_file("tl_2012_13_vtd10.geojson", driver="GeoJSON")