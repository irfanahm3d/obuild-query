import pandas as pd
import geopandas as gpd
from shapely.geometry import box


def main():
    # Load the dataset from CSV
    # Replace 'path_to_your_google_open_buildings_dataset.csv' with your dataset path
    buildings = pd.read_csv("path_to_your_google_open_buildings_dataset.csv")

    # Convert to GeoDataFrame and define the geometry column
    gdf = gpd.GeoDataFrame(
        buildings, geometry=gpd.points_from_xy(buildings.longitude, buildings.latitude)
    )

    # Filter buildings by score > 0.75
    filtered_buildings = gdf[gdf["score"] > 0.75]

    # Define the bounding box for Saidpur Village
    # Coordinates: South, West, North, East
    bounding_box = (33.7260, 73.0600, 33.7400, 73.0750)

    # Create a bounding box geometry
    bbox = box(bounding_box[1], bounding_box[0], bounding_box[3], bounding_box[2])

    # Filter buildings within the bounding box
    buildings_in_bbox = filtered_buildings[filtered_buildings.intersects(bbox)]

    # Count the number of buildings
    building_count = len(buildings_in_bbox)

    print(f"Number of buildings in Saidpur Village with score > 0.75: {building_count}")
