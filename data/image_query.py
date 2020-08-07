import ee
class SatelliteQueryImage:
    def __init__(self):
        ee.Authenticate()
        ee.Initialize()
    def getRGBSatelliteImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_data, landslide_event_end):
        rgbLandsatImages = ee.ImageCollection("LANDSAT/LC08/C01/T1").filterBounds(ee.Geometry.Point(landslide_lat,landslide_lng)).filterDate(landslide_event_data,landslide_event_end).sort('CLOUDY_PIXEL_PERCENTAGE')

def querySatelliteImages(lat,lng, event_date):

    return 1