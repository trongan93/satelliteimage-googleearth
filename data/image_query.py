import ee
import configuration.satelliteconfiguration as sl_config
class SatelliteQueryImage:
    def __init__(self,authenticate):
        if authenticate == 1:
            ee.Authenticate()
            ee.Initialize()
        else:
            ee.Initialize()

    def getLANDSAT8ImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_date, landslide_event_collection):
        return ee.ImageCollection(sl_config.LANDSAT_8).filterBounds(ee.Geometry.Point(landslide_lat,landslide_lng)).filterDate(landslide_event_date,landslide_event_collection).sort('CLOUDY_PIXEL_PERCENTAGE')
    def getLANDSAT7ImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_date, landslide_event_collection):
        return ee.ImageCollection(sl_config.LANDSAT_7).filterBounds(ee.Geometry.Point(landslide_lat,landslide_lng)).filterDate(landslide_event_date,landslide_event_collection).sort('CLOUDY_PIXEL_PERCENTAGE')
    def getSENTINEL2ImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_date, landslide_event_collection):
        return ee.ImageCollection(sl_config.SENTINEL_2).filterBounds(ee.Geometry.Point(landslide_lat,landslide_lng)).filterDate(landslide_event_date,landslide_event_collection).sort('CLOUDY_PIXEL_PERCENTAGE')
    def getALOS2ImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_date, landslide_event_collection):
        return ee.ImageCollection(sl_config.ALOS_2).filterBounds(ee.Geometry.Point(landslide_lat,landslide_lng)).filterDate(landslide_event_date,landslide_event_collection).sort('CLOUDY_PIXEL_PERCENTAGE')

    def getSatellitesImagesContainLandslide(self, landslide_lat, landslide_lng, landslide_event_date, landslide_event_collection):
        landsat_8_images = self.getLANDSAT8ImagesContainLandslide(landslide_lat,landslide_lng,landslide_event_date,landslide_event_collection)
        landsat_7_images = self.getLANDSAT7ImagesContainLandslide(landslide_lat,landslide_lng,landslide_event_date,landslide_event_collection)
        sentinel_2_images = self.getSENTINEL2ImagesContainLandslide(landslide_lat,landslide_lng,landslide_event_date,landslide_event_collection)
        alos_2_images = self.getALOS2ImagesContainLandslide(landslide_lat,landslide_lng,landslide_event_date,landslide_event_collection)
        return {'landsat_8':landsat_8_images, 'landsat_7':landsat_7_images, 'sentinel_2':sentinel_2_images, 'alos_2':alos_2_images}


    def getLANDSAT8_RGBImages(self,landsat8_images):
        return landsat8_images.select(['B4','B3','B2']) # band 2: blue, band 3: green, band 4: red
    def getLANDSAT7_RGBImages(self,landsat_7_images):
        return landsat_7_images.select(['B3','B2','B1']) # band 1: blue, band 2: green, band 3: red
    def getSENTINEL2_RGBImages(self,sentinel_2_images):
        return sentinel_2_images.select(['B4','B3','B2']) #band 2: blue, band 3: green, band 4: red
    def getALOS2_RGBImages(self,alos_2_images):
        return alos_2_images.select(['B3','B2','B1']) # band 1: blue, band 2: green, band 3: red
    def getSatellitesImageRGB(self, satellitesImagesContainLandslide):
        landsat_8_images = satellitesImagesContainLandslide['landsat_8']
        landsat_8_rgb_images = self.getLANDSAT8_RGBImages(landsat_8_images)
        landsat_7_images = satellitesImagesContainLandslide['landsat_7']
        landsat_7_rgb_images = self.getLANDSAT7_RGBImages(landsat_7_images)
        sentinel_2_images = satellitesImagesContainLandslide['sentinel_2']
        sentinel_2_rgb_images = self.getSENTINEL2_RGBImages(sentinel_2_images)
        alos_2_images = satellitesImagesContainLandslide['alos_2']
        alos_2_rgb_images = self.getALOS2_RGBImages(alos_2_images)
        return {'landsat_8_rgb_images':landsat_8_rgb_images, 'landsat_7_rgb_images':landsat_7_rgb_images, 'sentinel_2_rgb_images':sentinel_2_rgb_images, 'alos_2_rgb_images':alos_2_rgb_images}


    def getBestSatelliteRGBImage(self, rgbSatelliteImages):
        landsat_8_rgb_images = rgbSatelliteImages['landsat_8_rgb_images']
        landsat_8_best_rgb = landsat_8_rgb_images.first()
        landsat_7_rgb_images = rgbSatelliteImages['landsat_7_rgb_images']
        landsat_7_best_rgb = landsat_7_rgb_images.first()
        sentinel_2_rgb_images = rgbSatelliteImages['sentinel_2_rgb_images']
        sentinel_2_best_rgb = sentinel_2_rgb_images.first()
        alos_2_rgb_images = rgbSatelliteImages['alos_2_rgb_images']
        alos_2_best_rgb = alos_2_rgb_images.first()
        return {'landsat_8_best_rgb':landsat_8_best_rgb, 'landsat_7_best_rgb':landsat_7_best_rgb, 'sentinel_2_best_rgb':sentinel_2_best_rgb, 'alos_2_best_rgb':alos_2_best_rgb}
