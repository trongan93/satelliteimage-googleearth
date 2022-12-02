import ee
import configuration.satelliteconfiguration as sl_config
import math


class SatelliteQueryImage:
    def __init__(self, authenticate):
        if authenticate == 1:
            ee.Authenticate()
            ee.Initialize()
        else:
            ee.Initialize()

    def defineImageRegion(self, landslide_lng, landslide_lat):
        # print(landslideSize)
        # print(landslide_lng, landslide_lat)
        # lef_lat, lef_lng = self.newPointFromPointByDistance(landslide_lng,landslide_lat,-3.750) # 3750(m) = 125 pixels * 30m/pixel
        # right_lat, right_lng = self.newPointFromPointByDistance(landslide_lng, landslide_lat, 3.750)

        # lef_lat, lef_lng = self.newPointFromPointByDistance(landslide_lng, landslide_lat, -5.304)  # 5304(m) = 176.8 pixels * 30m/pixel
        # right_lat, right_lng = self.newPointFromPointByDistance(landslide_lng, landslide_lat, 5.304)
        # rectangle = ee.Geometry.Rectangle(lef_lng, lef_lat, right_lng, right_lat)

        lef_lat_30_m_pixel, lef_lng_30_m_pixel = self.newPointFromPointByDistance(landslide_lng, landslide_lat, -5.310) #phai tinh theo canh huyen cua goc 90 do
        right_lat_30_m_pixel, right_lng_30_m_pixel = self.newPointFromPointByDistance(landslide_lng, landslide_lat, 5.310)
        rectangle_30m_per_pixel = ee.Geometry.Rectangle(lef_lng_30_m_pixel, lef_lat_30_m_pixel, right_lng_30_m_pixel, right_lat_30_m_pixel)

        lef_lat_10_m_pixel, lef_lng_10_m_pixel = self.newPointFromPointByDistance(landslide_lng, landslide_lat, -1.770)
        right_lat_10_m_pixel, right_lng_10_m_pixel = self.newPointFromPointByDistance(landslide_lng, landslide_lat, 1.770)
        rectangle_10m_per_pixel = ee.Geometry.Rectangle(lef_lng_10_m_pixel, lef_lat_10_m_pixel, right_lng_10_m_pixel, right_lat_10_m_pixel)

        return [rectangle_30m_per_pixel,rectangle_10m_per_pixel]


    def newPointFromPointByDistance(self, lng, lat, distance):
        # Ref: https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
        # Distance in km
        R = 6378.1  # Radius of the Earth
        # brng = 1.57  # Bearing is 90 degrees converted to radians.
        # brng = 4.7123889804 # Bearing is 270 degrees converted to radians.
        brng = 2.3561944902  # Bearing is 135 degrees converted to radians
        # d = 15  # Distance in km
        # lat2  52.20444 - the lat result I'm hoping for
        # lon2  0.36056 - the long result I'm hoping for.

        lat1 = math.radians(lat)  # Current lat point converted to radians
        lon1 = math.radians(lng)  # Current long point converted to radians

        lat2 = math.asin(
            math.sin(lat1) * math.cos(distance / R) + math.cos(lat1) * math.sin(distance / R) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(distance / R) * math.cos(lat1),
                                 math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        # print('current lat and lng: ', lat, lng )
        # print(lat2)
        # print(lon2)
        # print('new lat and lng: ', lat2, lon2)
        return lat2, lon2

    def getLANDSAT8Images(self, lat, lng, start_date, end_date):
        # return ee.ImageCollection(sl_config.LANDSAT_8).filterBounds(
        #     ee.Geometry.Point(lng, lat)).filterDate(start_date, end_date).filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',sl_config.CLOUDY_PERCENTAGE_FILTER)).sort('CLOUDY_PIXEL_PERCENTAGE')

        return ee.ImageCollection(sl_config.LANDSAT_8).filterBounds(
            ee.Geometry.Point(lng, lat)).filterDate(start_date, end_date).filterMetadata('CLOUD_COVER', 'less_than', sl_config.CLOUDY_PERCENTAGE_FILTER).sort('CLOUDY_PIXEL_PERCENTAGE')

    def getLANDSAT7Images(self, lat, lng, start_date,
                          end_date):
        # return ee.ImageCollection(sl_config.LANDSAT_7).filterBounds(ee.Geometry.Point(lng, lat)).filterDate(start_date, end_date).filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',sl_config.CLOUDY_PERCENTAGE_FILTER)).sort('CLOUDY_PIXEL_PERCENTAGE')
        return ee.ImageCollection(sl_config.LANDSAT_7).filterBounds(ee.Geometry.Point(lng, lat)).filterDate(start_date, end_date).filterMetadata('CLOUD_COVER', 'less_than', sl_config.CLOUDY_PERCENTAGE_FILTER).sort('CLOUDY_PIXEL_PERCENTAGE')

    def getSENTINEL2Images(self, lat, lng, start_date, end_date):
        # return ee.ImageCollection(sl_config.SENTINEL_2).filterBounds(ee.Geometry.Point(lng, lat)).filterDate(start_date, end_date).filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',sl_config.CLOUDY_PERCENTAGE_FILTER)).sort('CLOUDY_PIXEL_PERCENTAGE')
        return ee.ImageCollection(sl_config.SENTINEL_2).filterBounds(ee.Geometry.Point(lng, lat)).filterDate(start_date,end_date).filterMetadata('CLOUD_COVERAGE_ASSESSMENT', 'less_than', sl_config.CLOUDY_PERCENTAGE_FILTER).sort('CLOUDY_PIXEL_PERCENTAGE')

    def getALOS2Images(self, lat, lng, start_date, end_date):
        # return ee.ImageCollection(sl_config.ALOS_2).filterBounds(ee.Geometry.Point(lng, lat)).filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',sl_config.CLOUDY_PERCENTAGE_FILTER)).filterDate(start_date,end_date).sort('CLOUDY_PIXEL_PERCENTAGE')
        return ee.ImageCollection(sl_config.ALOS_2).filterBounds(ee.Geometry.Point(lng, lat)).filterDate(start_date,end_date).filterMetadata('CLOUD_COVER', 'less_than', sl_config.CLOUDY_PERCENTAGE_FILTER).sort('CLOUDY_PIXEL_PERCENTAGE')

    def getSatellitesImages(self, lat, lng, start_date, end_date):
        error_landsat_8 = error_landsat_7 = error_sentinel_2 = error_alos_2 = ''
        if sl_config.LANDSAT_8_TIME_RANGE[0] < start_date < sl_config.LANDSAT_8_TIME_RANGE[1]:
            landsat_8_images = self.getLANDSAT8Images(lat, lng, start_date, end_date)
        else:
            landsat_8_images = ''
            error_landsat_8 = 'Landsat 8: landslide event date not in satellite range'
        if sl_config.LANDSAT_7_TIME_RANGE[0] < start_date < sl_config.LANDSAT_7_TIME_RANGE[1]:
            landsat_7_images = self.getLANDSAT7Images(lat, lng, start_date, end_date)
        else:
            landsat_7_images = ''
            error_landsat_7 = 'Landsat 7: landslide event date not in satellite range'
        if sl_config.SENTINEL_2_TIME_RANGE[0] < start_date < sl_config.SENTINEL_2_TIME_RANGE[1]:
            sentinel_2_images = self.getSENTINEL2Images(lat, lng, start_date, end_date)
        else:
            sentinel_2_images = ''
            error_sentinel_2 = 'Sentinel 2: landslide event date not in satellite range'
        if sl_config.ALOS_2_TIME_RANGE[0] < start_date < sl_config.ALOS_2_TIME_RANGE[1]:
            alos_2_images = self.getALOS2Images(lat, lng, start_date, end_date)
        else:
            alos_2_images = ''
            error_alos_2 = 'ALOS 2: landslide event date not in satellite range'
        return {'landsat_8': landsat_8_images, 'landsat_7': landsat_7_images, 'sentinel_2': sentinel_2_images,
                'alos_2': alos_2_images}, {'landsat_8_error': error_landsat_8, 'landsat_7_error': error_landsat_7,
                                           'sentinel_2_error': error_sentinel_2, 'alos_2_error': error_alos_2}

    def getLANDSAT8_RGBImages(self, landsat8_images):
        if landsat8_images != '':
            return landsat8_images.select(['B4', 'B3', 'B2'])  # band 2: blue, band 3: green, band 4: red
        else:
            return ''

    def getLANDSAT7_RGBImages(self, landsat_7_images):
        if landsat_7_images != '':
            return landsat_7_images.select(['B3', 'B2', 'B1'])  # band 1: blue, band 2: green, band 3: red
        else:
            return ''

    def getSENTINEL2_RGBImages(self, sentinel_2_images):
        if sentinel_2_images != '':
            return sentinel_2_images.select(['B4', 'B3', 'B2'])  # band 2: blue, band 3: green, band 4: red
        else:
            return ''

    def getALOS2_RGBImages(self, alos_2_images):
        if alos_2_images != '':
            return alos_2_images.select(['B3', 'B2', 'B1'])  # band 1: blue, band 2: green, band 3: red
        else:
            return ''

    def getSatellitesImageRGB(self, satellitesImagesContainLandslide):
        landsat_8_images = satellitesImagesContainLandslide['landsat_8']
        landsat_8_rgb_images = self.getLANDSAT8_RGBImages(landsat_8_images)
        landsat_7_images = satellitesImagesContainLandslide['landsat_7']
        landsat_7_rgb_images = self.getLANDSAT7_RGBImages(landsat_7_images)
        sentinel_2_images = satellitesImagesContainLandslide['sentinel_2']
        sentinel_2_rgb_images = self.getSENTINEL2_RGBImages(sentinel_2_images)
        alos_2_images = satellitesImagesContainLandslide['alos_2']
        alos_2_rgb_images = self.getALOS2_RGBImages(alos_2_images)
        return {'landsat_8_rgb_images': landsat_8_rgb_images, 'landsat_7_rgb_images': landsat_7_rgb_images,
                'sentinel_2_rgb_images': sentinel_2_rgb_images, 'alos_2_rgb_images': alos_2_rgb_images}

    def getBestSatelliteRGBImage(self, rgbSatelliteImages):
        landsat_8_rgb_images = rgbSatelliteImages['landsat_8_rgb_images']
        if landsat_8_rgb_images != '':
            landsat_8_best_rgb = ee.Image(landsat_8_rgb_images.first())
        else:
            landsat_8_best_rgb = ''

        landsat_7_rgb_images = rgbSatelliteImages['landsat_7_rgb_images']
        if landsat_7_rgb_images != '':
            landsat_7_best_rgb = ee.Image(landsat_7_rgb_images.first())
        else:
            landsat_7_best_rgb = ''

        sentinel_2_rgb_images = rgbSatelliteImages['sentinel_2_rgb_images']
        if sentinel_2_rgb_images != '':
            sentinel_2_best_rgb = ee.Image(sentinel_2_rgb_images.first())
        else:
            sentinel_2_best_rgb = ''

        alos_2_rgb_images = rgbSatelliteImages['alos_2_rgb_images']
        if alos_2_rgb_images != '':
            alos_2_best_rgb = ee.Image(alos_2_rgb_images.first())
        else:
            alos_2_best_rgb = ''

        return {'ee': ee, 'landsat_8_best_rgb': landsat_8_best_rgb, 'landsat_7_best_rgb': landsat_7_best_rgb,
                'sentinel_2_best_rgb': sentinel_2_best_rgb, 'alos_2_best_rgb': alos_2_best_rgb}

class RandomLowLightImage():
    def __init__(self, authenticate):
        if authenticate == 1:
            ee.Authenticate()
            ee.Initialize()
        else:
            ee.Initialize()
    def getLowLightImages_Landsat9(self, cloud_lte = 100):
        cloud_filter = ee.Filter.lte('CLOUD_COVER', cloud_lte)
        images_collection = ee.ImageCollection(sl_config.LANDSAT_9).filter(cloud_filter)
        return  images_collection
    def getBestImage(self, images_collection):
        return ee, ee.Image(images_collection.first())