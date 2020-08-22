import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import reshape_as_raster, reshape_as_image
# filepath = '/mnt/d/ProjectData/GoogleEarthEnginee/test_export_landsat_3_bands.tif'
filepath = '/home/trongan93/Downloads/landslideImg.tif'

# Ref: https://rasterio.readthedocs.io/en/latest/topics/image_processing.html#imageorder
src = rasterio.open(filepath)
array = src.read()
print(array.shape)
image = reshape_as_image(array)
plt.imshow(image)
plt.show()