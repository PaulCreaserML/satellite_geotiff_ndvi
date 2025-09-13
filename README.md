# GeoTIFF NDVI Calculator
This repository provides a pair of Python scripts to perform a fundamental remote sensing task: calculating the Normalized Difference Vegetation Index (NDVI) from a multi-band GeoTIFF file.

## Problem Statement
This project directly solves the following common geospatial problem:

"You are given a multi-band GeoTIFF file from an Earth observation satellite. Write a program that reads this file, extracts the Red and Near-Infrared (NIR) bands, and calculates the Normalized Difference Vegetation Index (NDVI) for each pixel. Save the resulting NDVI map as a new single-band GeoTIFF, preserving the original georeferencing information."

This code demonstrates how to read raster data, perform array arithmetic using NumPy, and write a new georeferenced file while maintaining its spatial integrity.

Files Included
create_mock_geotiff.py: A utility script that generates a sample multi-band GeoTIFF file (sample_multiband.tif).

calculate_ndvi.py: The main script that reads a GeoTIFF, calculates the NDVI, and saves the result (ndvi_output.tif).

requirements.txt: A list of the required Python libraries for the project.

## Requirements
Python 3.6+

The Python libraries listed in requirements.txt.

## Installation
It is highly recommended to run this project within a Python virtual environment to manage dependencies.

Clone the Repository

git clone <repository_url>
cd <repository_directory>

Create and Activate a Virtual Environment

On macOS and Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate

After activation, you will see (venv) at the beginning of your command prompt.

Install the Required Libraries
With your virtual environment active, install all dependencies from the requirements.txt file:

pip install -r requirements.txt

Usage Guide
Ensure your virtual environment is active before running the scripts.

Step 1: Generate Mock Data

First, run the data generator script. This will create a file named sample_multiband.tif in the same directory.

python create_mock_geotiff.py

You will see a confirmation message: Successfully created mock GeoTIFF: sample_multiband.tif.

Step 2: Calculate NDVI

Now, run the main NDVI calculation script. It will read sample_multiband.tif, perform the calculation, and create a new file named ndvi_output.tif.

python calculate_ndvi.py

Upon completion, you will see the message: NDVI calculation complete. Output saved to: ndvi_output.tif.

Step 3: View the Result

You can now open ndvi_output.tif in any GIS software (e.g., QGIS, ArcGIS Pro). The resulting image will be a single-band raster where pixel values range from -1 to +1. Higher values (whiter areas) represent healthier vegetation, which you will see in the center of the image as simulated by the mock data generator.

Using Your Own GeoTIFF Data
To analyze your own satellite imagery, modify the if __name__ == '__main__': block at the bottom of calculate_ndvi.py:

Update File Paths: Change input_geotiff to the path of your data file. You can also change output_ndvi_geotiff if you wish.

input_geotiff = 'path/to/your/data.tif'
output_ndvi_geotiff = 'your_ndvi_result.tif'

IMPORTANT: Set Correct Band Numbers
You must update the RED_BAND_NUMBER and NIR_BAND_NUMBER variables to match the band order of your specific satellite data. Band numbers are 1-based.

Here are the correct band numbers for some common satellites:

Landsat 8 / 9: Red = Band 4, NIR = Band 5

Sentinel-2: Red = Band 4, NIR = Band 8

Update the script accordingly:

# Example for Landsat 8
RED_BAND_NUMBER = 4
NIR_BAND_NUMBER = 5

# License
This project is licensed under the MIT License. See the LICENSE file for details.


