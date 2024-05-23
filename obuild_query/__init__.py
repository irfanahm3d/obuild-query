import pandas as pd
import geopandas as gpd
from shapely.geometry import box
from tqdm import tqdm

import click


@click.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True),
    required=True,
    help="Path to the gzipped CSV file",
)
@click.option(
    "--bbox",
    type=(float, float, float, float),
    required=True,
    help="Bounding box coordinates in the form: south west north east",
)
@click.option(
    "--chunk-size",
    type=int,
    default=100000,
    help="The size to chunk the dataset. Adjust this size based on your memory constraints",
)
def main(file_path, bbox, chunk_size):
    # Unpack the bounding box coordinates
    south, west, north, east = bbox

    # Create a bounding box geometry
    bbox_geometry = box(west, south, east, north)

    # Initialize an empty list to store filtered chunks
    filtered_chunks = []

    # Get the total number of lines in the file for progress percentage calculation
    total_lines = sum(
        1 for _ in pd.read_csv(file_path, compression="gzip", chunksize=chunk_size)
    )

    # Read the CSV file in chunks
    with pd.read_csv(file_path, compression="gzip", chunksize=chunk_size) as reader:
        for chunk in tqdm(
            reader,
            total=total_lines,
            unit="chunk",
            desc="Processing chunks",
            unit_scale=True,
        ):
            # Convert the chunk to a GeoDataFrame and define the geometry column
            gdf_chunk = gpd.GeoDataFrame(
                chunk, geometry=gpd.points_from_xy(chunk.longitude, chunk.latitude)
            )

            # Filter buildings within the bounding box
            buildings_in_bbox = gdf_chunk[gdf_chunk.intersects(bbox_geometry)]

            # Append the filtered chunk to the list
            filtered_chunks.append(buildings_in_bbox)

    # Concatenate all filtered chunks into a single GeoDataFrame
    filtered_buildings = pd.concat(filtered_chunks, ignore_index=True)

    # Count the number of buildings
    building_count = len(filtered_buildings)

    print(f"Number of buildings in bounding box: {building_count}")
