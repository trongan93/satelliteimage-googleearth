import argparse
from configuration import fileconfiguration as fconfig
from data import image_query as img_query, image_download as img_download, image_function as img_function
from data import port_record
import datetime
def main(execute_option, gg_authenticate):
    if execute_option == 1:
        print("Executing option 1: ")
        imageQueries = img_query.RandomLowLightImage(gg_authenticate)
        print(imageQueries)
        lowlight_Landsat9_images = imageQueries.getLowLightImages_Landsat9(cloud_lte=10)
        current_ee, lowlight_Landsat9_image = imageQueries.getBestImage(lowlight_Landsat9_images)
        # print(lowlight_Landsat9_image)
        image = img_download.downloadBestRGBImages(current_ee, lowlight_Landsat9_image)

    if execute_option == 10:
#     Test get URL
        import ee
        ee.Initialize()
        # A Sentinel-2 surface reflectance image.
        img = ee.Image('COPERNICUS/S2_SR/20210109T185751_20210109T185931_T10SEG')
        # A small region within the image.
        region = ee.Geometry.BBox(-122.0859, 37.0436, -122.0626, 37.0586)
        # Single-band GeoTIFF files wrapped in a zip file.
        url1 = img.getDownloadUrl({
            'name': 'single_band',
            'bands': [
                {'id': 'B3', 'crs': 'EPSG: 4326', },
                {'id': 'B8', 'crs': 'EPSG: 4326'},
                {'id': 'B11', 'crs': 'EPSG: 4326'}
            ]
        })
        print('url 1: ', url1)

        url2 = img.getDownloadUrl({
            'name': 'single_band',
            'bands': ['B3', 'B8', 'B11'],
            'region': region
        })
        print('url 2: ', url2)

    if execute_option == 20:
        print("Evaluation downloaded image file in GEOTIFF")
        import rasterio
        from rasterio.plot import show as tiff_show
        fp = r'/home/trongan93/Downloads/single_band3/single_band.B3.tif'
        img = rasterio.open(fp)
        tiff_show(img)

    if execute_option == 30:
        print("Download the sea port satellite images")
        imageQueries = img_query.SatelliteQueryImage(authenticate=gg_authenticate)
        portRecords = port_record.readRecordData(fconfig.seaport_file)
        storage_records = []
        for portRecord in portRecords:
        #     query the low-light image of the seaport
            portRecord.printOut()
            port_image_region = imageQueries.defineImageRegion(portRecord._lng, portRecord._lat)
            port_satellites_images, error_query = imageQueries.getSatellitesImages(lat = portRecord._lat, lng = portRecord._lng, start_date=datetime.datetime.now() - datetime.timedelta(days=365), end_date=datetime.datetime.now())
            port_rgb_satellites_images = imageQueries.getSatellitesImageRGB(port_satellites_images)
            port_best_rgb_satellite_image = imageQueries.getBestSatelliteRGBImage(port_rgb_satellites_images)
            url_links_obj, errors_data = img_download.downloadBestRGBImages(port_best_rgb_satellite_image, portRecord._lat, portRecord._lng, port_image_region, str("lng_%f_lat_%f" % (portRecord._lng,portRecord._lat)),error_query)
            downloaded_paths = img_download.downloadLandslideImageFilesToLocal(str("lng_%f_lat_%f" % (portRecord._lng,portRecord._lat)), url_links_obj)
            print(downloaded_paths)
            rgb_paths = img_function.combineRGBBandsNonNormolize(downloaded_paths)
            storage_records.append(port_record.getRecordDownloadedPaths(portRecord, rgb_paths))
            if errors_data != []:
                print('object ', str("lng_%f_lat_%f" % (portRecord._lng,portRecord._lat)), ' gets errors')
                print(errors_data)
            break



        #     if landslideRecord.size == 'large' or landslideRecord.size == 'very_large' or landslideRecord.size == 'catastrophic':
        #         print("Landslide region: IN PROCESSING ON object ", landslideRecord.object_id, " at ",
        #               landslideRecord.event_date, " ; landslide size is ", landslideRecord.size)
        #         event_date = datetime.datetime.strptime(landslideRecord.event_date, '%Y-%m-%d %H:%M:%S')
        #         landslide_image_region = imageQueries.defineImageRegion(landslideRecord.lng, landslideRecord.lat)
        #         landslide_satellites_images, error_query = imageQueries.getSatellitesImages(landslideRecord.lat,
        #                                                                                     landslideRecord.lng,
        #                                                                                     event_date,
        #                                                                                     event_date + datetime.timedelta(
        #                                                                                         days=ls_config.LANDSLIDE_EVEN_COLLTECTION_TIME))
        #         landslide_rgb_satellites_images = imageQueries.getSatellitesImageRGB(landslide_satellites_images)
        #         landslide_best_rgb_satellites_image = imageQueries.getBestSatelliteRGBImage(
        #             landslide_rgb_satellites_images)
        #         url_links_obj, errors_data = img_download.downloadBestRGBImages(landslide_best_rgb_satellites_image,
        #                                                                         landslideRecord.lat,
        #                                                                         landslideRecord.lng,
        #                                                                         landslide_image_region,
        #                                                                         landslideRecord.object_id,
        #                                                                         error_query)
        #         downloaded_paths = img_download.downloadLandslideImageFilesToLocal(landslideRecord.object_id,
        #                                                                            url_links_obj)
        #         rgb_paths = img_function.combineRGBBands(downloaded_paths)
        #         storage_records.append(record.getRecordDownloadedPaths(landslideRecord, rgb_paths))
        #         if errors_data != []:
        #             print('object {} gets errors'.format(landslideRecord.object_id))
        #             print(errors_data)
        #         # break # tmp - remove after test on 1 image
        # port_record.saveDownloadPaths(storage_records, fconfig.seaport_dataset_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--authenticate', required=False, help='Authenticate to Google Earth Engine API', type=int, default=1)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. test 1 low-light image', type=int)
    args = parser.parse_args()
    print(args.execute)
    main(execute_option=args.execute, gg_authenticate=args.authenticate)