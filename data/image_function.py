import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import reshape_as_raster, reshape_as_image
def combineRGBBands(downloaded_paths):
    for download_path in downloaded_paths:
        img1 = cv2.imread(os.path.join(download_path,os.listdir(download_path)[0]),0)
        img2 = cv2.imread(os.path.join(download_path,os.listdir(download_path)[1]),0)
        img3 = cv2.imread(os.path.join(download_path,os.listdir(download_path)[2]),0)
        rgb_img = cv2.merge([img1,img2,img3])
        cv2.imwrite(os.path.join(download_path,'rgb.tif'),rgb_img)
        plt.imshow(rgb_img)
        plt.show()