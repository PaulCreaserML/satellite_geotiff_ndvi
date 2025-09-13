import rasterio
import numpy as np
from rasterio.transform import from_origin

def create_mock_geotiff(filepath, bands=5, height=256, width=256):
    """
    Creates a mock multi-band GeoTIFF file for testing purposes.
    This simulates a satellite image with some basic georeferencing.

    Args:
        filepath (str): The path where the GeoTIFF will be saved.
        bands (int): The number of bands in the GeoTIFF.
        height (int): The height of the raster in pixels.
        width (int): The width of the raster in pixels.
    """
    # Define georeferencing information (transform and CRS)
    # This sets the top-left corner coordinates and pixel size.
    transform = from_origin(west=140.0, north=-35.0, xsize=0.01, ysize=0.01)
    crs = 'EPSG:4326' # WGS 84 Coordinate Reference System

    # Create random data for all bands. Satellite data is often uint16.
    mock_data = np.random.randint(100, 4000, size=(bands, height, width), dtype=np.uint16)

    # To make the NDVI calculation meaningful, we'll simulate a vegetated area.
    # We designate Band 1 as Red and Band 2 as NIR.
    # In the center of the image, we will increase NIR and decrease Red values.
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 3
    y, x = np.ogrid[:height, :width]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2

    # In the "vegetated" area (the circle), boost NIR and reduce Red
    # to simulate healthy vegetation's spectral response.
    mock_data[1, mask] = mock_data[1, mask] + 2500  # Boost NIR (band 2)
    mock_data[0, mask] = mock_data[0, mask] // 2    # Reduce Red (band 1)


    # Prepare metadata for the new GeoTIFF file
    meta = {
        'driver': 'GTiff',
        'dtype': 'uint16',
        'nodata': None,
        'width': width,
        'height': height,
        'count': bands,
        'crs': crs,
        'transform': transform,
    }

    # Write the data to a new file
    try:
        with rasterio.open(filepath, 'w', **meta) as dst:
            dst.write(mock_data)
        print(f"Successfully created mock GeoTIFF: {filepath}")
        print(f"This file has {bands} bands. For this specific file, use Red=Band 1 and NIR=Band 2 for your NDVI calculation.")
    except Exception as e:
        print(f"Error creating mock GeoTIFF: {e}")

if __name__ == '__main__':
    # Define the name for our sample input file
    output_filename = 'sample_multiband.tif'
    create_mock_geotiff(output_filename)

