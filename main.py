import ee
ee.Initialize()
print(ee.Image('USGS/SRTMGL1_003').getInfo()) #test
# import datetime
# ee_date = ee.Date('2020-01-01') #time in utc
# # py_date = datetime.datetime.utcfromtimestamp(ee_date.getInfo()['value']/1000.0)
#
# # Load a landsat image and select three bands.
# landsat = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_123032_20140515').select(['B4', 'B3', 'B2']);
#
# # Create a geometry representing an export region.
# geometry = ee.Geometry.Rectangle([116.2621, 39.8412, 116.4849, 40.01236]);
#
# # Export the image, specifying scale and region.
# task = ee.batch.Export.image.toDrive(image = landsat, description = 'imageToDriveExample', scale = 30, region = geometry);
# task.start()