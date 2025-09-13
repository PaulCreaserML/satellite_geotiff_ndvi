import rasterio
import numpy as np

def calculate_ndvi(input_path, output_path, red_band_num, nir_band_num):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI) from a
    multi-band GeoTIFF file and saves it as a new single-band GeoTIFF.

    The NDVI formula is: NDVI = (NIR - Red) / (NIR + Red)

    Args:
        input_path (str): Path to the input multi-band GeoTIFF file.
        output_path (str): Path to save the output single-band NDVI GeoTIFF.
        red_band_num (int): The band number for the Red channel (1-based).
        nir_band_num (int): The band number for the Near-Infrared (NIR) channel (1-based).
    """
    try:
        # Open the source dataset using a with statement for automatic cleanup
        with rasterio.open(input_path) as src:
            # --- 1. Read Bands ---
            # Ensure the requested bands exist in the file
            if not (0 < red_band_num <= src.count and 0 < nir_band_num <= src.count):
                raise ValueError(
                    f"Invalid band numbers. File has {src.count} bands, "
                    f"but Red band {red_band_num} and NIR band {nir_band_num} were requested."
                )

            # Read the Red and NIR bands into numpy arrays.
            # Convert to a floating-point type for calculations.
            red = src.read(red_band_num).astype(np.float32)
            nir = src.read(nir_band_num).astype(np.float32)

            # --- 2. Calculate NDVI ---
            # Suppress 'division by zero' warnings that occur where Red and NIR are both 0.
            with np.errstate(divide='ignore', invalid='ignore'):
                ndvi = (nir - red) / (nir + red)

            # Handle the results of division by zero. After the operation, these
            # pixels will be 'nan' (not a number). We'll set them to 0.
            ndvi[np.isnan(ndvi)] = 0
            # Also handle potential 'inf' values if they arise
            ndvi[np.isinf(ndvi)] = 0
            # Clip the NDVI values to the valid range of -1 to 1.
            ndvi = np.clip(ndvi, -1, 1)

            # --- 3. Write Output GeoTIFF ---
            # Copy the metadata from the source file. This preserves the
            # georeferencing, CRS, and other important information.
            out_meta = src.meta.copy()

            # Update the metadata for our output file.
            # We are creating a single-band file with a float data type.
            out_meta.update({
                "driver": "GTiff",
                "count": 1,
                "dtype": 'float32',
                "nodata": -9999  # Define a no-data value
            })

            # Write the NDVI numpy array to a new GeoTIFF file.
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(ndvi, 1) # Write to the first and only band

        print(f"NDVI calculation complete. Output saved to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
        print("Please run 'create_mock_geotiff.py' first to generate the sample file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # --- Configuration ---
    # Define the input and output file paths.
    input_geotiff = 'sample_multiband.tif'
    output_ndvi_geotiff = 'ndvi_output.tif'

    # IMPORTANT: Define the band numbers for your specific data.
    # Band numbers are 1-based (the first band is 1, not 0).
    # These numbers depend on the satellite/sensor. Common examples:
    # - Landsat 8/9: Red = Band 4, NIR = Band 5
    # - Sentinel-2:  Red = Band 4, NIR = Band 8
    # For our mock GeoTIFF created by `create_mock_geotiff.py`, we use:
    RED_BAND_NUMBER = 1
    NIR_BAND_NUMBER = 2

    print("Starting NDVI calculation...")
    calculate_ndvi(input_geotiff, output_ndvi_geotiff, RED_BAND_NUMBER, NIR_BAND_NUMBER)

