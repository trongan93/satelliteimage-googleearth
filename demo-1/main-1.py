import time
import ee
import image

import exportImage
import cv2

# ee.Authenticate()
ee.Initialize()


# print(ee.Image('USGS/SRTMGL1_003').getInfo()) #test
# # import datetime
# # ee_date = ee.Date('2020-01-01') #time in utc
# # # py_date = datetime.datetime.utcfromtimestamp(ee_date.getInfo()['value']/1000.0)
# #
# # Load a landsat image and select three bands.
# landsat = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515').select(['B4', 'B3', 'B2']);
#
# # Create a geometry representing an export region.
# geometry = ee.Geometry.Rectangle([116.2621, 39.8412, 116.4849, 40.01236]);

# get image by name
img = image.getImage(ee,'LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515')
exportImage.exportToDrive(ee,img,'test_export_landsat_3_bands')

# # get first image from image collection
# fistImage = image.getImageFromImageCollection(ee)
# exportImage.exportToDrive(ee,fistImage,'first_image_from_collection')



# # Export the image, specifying scale and region.
# task1 = ee.batch.Export.image.toDrive(image = landsat, description = 'imagetest2', scale = 30, region = geometry);
# task1.start()
#
# while True:
#     status = task1.status()
#     time.sleep(1)
#     if(status['state']=='COMPLETED'):
#         print("Completed task")
#         task1.stop()
#         break


#Export image to Asset
# task2 = ee.batch.Export.image.toAsset(image = landsat, description = 'imageToDriveExample', scale = 30, region = geometry);
# task2.start()
