import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import rasterio

# Function to normalize the grid values
# https://automating-gis-processes.github.io/CSC/notebooks/L5/plotting-raster.html
def normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    array_min, array_max = array.min(), array.max()
    return ((array - array_min) / (array_max - array_min))

def combineRGBBands(downloaded_paths):
    rgb_paths = ''
    for download_path in downloaded_paths:
        # https://automating-gis-processes.github.io/CSC/notebooks/L5/plotting-raster.html
        path0 = os.path.join(download_path, os.listdir(download_path)[0])
        path1 = os.path.join(download_path, os.listdir(download_path)[1])
        path2 = os.path.join(download_path, os.listdir(download_path)[2])
        dataset0 = rasterio.open(path0)
        dataset1 = rasterio.open(path1)
        dataset2 = rasterio.open(path2)

        red = dataset0.read(1)
        green = dataset1.read(1)
        blue = dataset2.read(1)


        # Normalize the bands
        redn = normalize(red)
        greenn = normalize(green)
        bluen = normalize(blue)

        # Create RGB natural color composite
        rgb = np.dstack((redn, greenn, bluen))

        max_val = np.max(rgb)
        # print(max_val)
        rgb = rgb.astype(np.float64) / max_val # normalize the data to 0 - 1
        rgb = 255 * rgb  # Now scale by 255
        img = rgb.astype(np.uint8)
        rgb_path = os.path.join(download_path,'rgb.tif')
        isWritten = cv2.imwrite(rgb_path,img)
        if isWritten:
            # print(str(rgb_path))
            # rgb_paths.join(str(rgb_path))
            rgb_paths += str(rgb_path)
            rgb_paths += ' , '
            print(rgb_paths)
    return rgb_paths