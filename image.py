def getImageFromImageCollection(ee):
    first = ee.ImageCollection("LANDSAT/LC08/C01/T1") \
        .filterBounds(ee.Geometry.Point(-70.48, 43.3631)) \
        .filterDate('2019-01-01', '2019-02-01') \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()
    print("Successful to get an image from collection")
    return first

def getImage(ee, name):
    image = ee.Image(name).select(['B4', 'B3', 'B2'])
    return image