import sys
import os
from configuration import fileconfiguration as fconfig, landslideconfiguration as ls_config
log = open(os.path.join(fconfig.base_saved_data_path,"main-executing.log"), "a")
sys.stdout = log

from data import landslide_record as record
from data import image_query as img_query, image_download as img_download, image_function as img_function
import datetime
def main(execute_option, gg_authenticate, sync_glc):
    if sync_glc == 1:
        print("Sync data file from GLC to landslide short file")
        landslideRecords = record.readRecordData(fconfig.raw_glc_file)
        record.save_short_landslide_record(landslideRecords, fconfig.short_glc_file)
        print("Successful to change from GLC raw file to short datafile at: ", fconfig.short_glc_file)

    if execute_option == 1:
        print("Executed selection 1; query satellite images contain landslide from glc short file")
        imageQueries = img_query.SatelliteQueryImage(authenticate=gg_authenticate)
        landslideRecords = record.read_short_landslide_record(fconfig.short_glc_file)
        landslide_storage_records = []
        for landslideRecord in landslideRecords:
            if landslideRecord.size == 'large' or landslideRecord.size == 'very_large' or landslideRecord.size == 'catastrophic':
                print("Landslide region: IN PROCESSING ON object ",landslideRecord.object_id, " at ", landslideRecord.event_date, " ; landslide size is ", landslideRecord.size)
                event_date = datetime.datetime.strptime(landslideRecord.event_date,'%Y-%m-%d %H:%M:%S')
                landslide_image_region = imageQueries.defineImageRegion(landslideRecord.lng, landslideRecord.lat)
                landslide_satellites_images, error_query = imageQueries.getSatellitesImages(landslideRecord.lat, landslideRecord.lng, event_date, event_date + datetime.timedelta(days=ls_config.LANDSLIDE_EVEN_COLLTECTION_TIME))
                landslide_rgb_satellites_images = imageQueries.getSatellitesImageRGB(landslide_satellites_images)
                landslide_best_rgb_satellites_image = imageQueries.getBestSatelliteRGBImage(landslide_rgb_satellites_images)
                url_links_obj, errors_data = img_download.downloadBestRGBImages(landslide_best_rgb_satellites_image, landslideRecord.lat, landslideRecord.lng, landslide_image_region, landslideRecord.object_id, error_query)
                downloaded_paths = img_download.downloadLandslideImageFilesToLocal(landslideRecord.object_id, url_links_obj)
                rgb_paths = img_function.combineRGBBands(downloaded_paths)
                landslide_storage_records.append(record.getRecordDownloadedPaths(landslideRecord, rgb_paths))
                if errors_data != []:
                    print('object {} gets errors'.format(landslideRecord.object_id))
                    print(errors_data)
                # break # tmp - remove after test on 1 image
        record.saveDownloadPaths(landslide_storage_records, fconfig.landslide_storage_saved_paths)
    elif execute_option == 2:
        print("Executed selection 2; query satellite images with non-landslide from glc short file")
        imageQueries = img_query.SatelliteQueryImage(authenticate=gg_authenticate)
        landslideRecords = record.read_short_landslide_record(fconfig.short_glc_file)
        non_landslide_storage_records = []
        for landslideRecord in landslideRecords:
            if landslideRecord.size == 'large' or landslideRecord.size == 'very_large' or landslideRecord.size == 'catastrophic':
                print("Non-landslide region: IN PROCESSING ON object ",landslideRecord.object_id, " at ", landslideRecord.event_date, " ; landslide size is ", landslideRecord.size)
                event_date = datetime.datetime.strptime(landslideRecord.event_date, '%Y-%m-%d %H:%M:%S')
                non_landslide_point_lat, non_landslide_point_lng = imageQueries.newPointFromPointByDistance(landslideRecord.lng, landslideRecord.lat, 20) #20 km to right-left with angle 45 degree from landslide point
                non_landslide_image_region = imageQueries.defineImageRegion(non_landslide_point_lng, non_landslide_point_lat)
                non_landslide_satellite_images, error_query = imageQueries.getSatellitesImages(non_landslide_point_lat, non_landslide_point_lng, event_date, event_date + datetime.timedelta(days=ls_config.LANDSLIDE_EVEN_COLLTECTION_TIME))
                non_landslide_rgb_satellites_images = imageQueries.getSatellitesImageRGB(non_landslide_satellite_images)
                non_landslide_best_rgb_satellites_image = imageQueries.getBestSatelliteRGBImage(non_landslide_rgb_satellites_images)
                url_links_obj, errors_data = img_download.downloadBestRGBImages(non_landslide_best_rgb_satellites_image, non_landslide_point_lat, non_landslide_point_lng, non_landslide_image_region, landslideRecord.object_id, error_query)
                downloaded_paths = img_download.downloadNonLandslideImageFilesToLocal(landslideRecord.object_id, url_links_obj)
                rgb_paths = img_function.combineRGBBands(downloaded_paths)
                non_landslide_storage_records.append(record.getRecordDownloadedPaths(landslideRecord, rgb_paths))
                if errors_data != []:
                    print('object {} gets errors'.format(landslideRecord.object_id))
                    print(errors_data)
                # break  # tmp - remove after test on 1 image
        record.saveDownloadPaths(non_landslide_storage_records, fconfig.non_landslide_storage_saved_paths)
    elif execute_option == 3:
        print("Executed selection 3; build dataset folder")
        landslideDownloadedRecords = record.readDownloadedPaths(fconfig.landslide_storage_saved_paths)
        for landslideDownloaded in landslideDownloadedRecords:
            print('move positive data at ', landslideDownloaded.object_id)
            downloaded_paths_string = landslideDownloaded.storage_paths
            if type(downloaded_paths_string) != str:
                continue
            downloaded_paths = downloaded_paths_string.split(',')
            for downloaded_path in downloaded_paths:
                if downloaded_path != '' and downloaded_path != ' ':
                    downloaded_path = downloaded_path.strip()
                    download_path_values = downloaded_path.split('/')
                    new_file_name = "{}_{}_{}".format(download_path_values[5].strip(), download_path_values[6].strip(), download_path_values[8].strip())
                    new_file_path = os.path.join(fconfig.dataset_path,"Positive",new_file_name)
                    img_download.copy_image_to_dataset(downloaded_path,new_file_path)
            # break # tmp - remove after test on 1 image

        nonLandslideDownloadedRecords = record.readDownloadedPaths(fconfig.non_landslide_storage_saved_paths)
        for nonLandslideDownloaded in nonLandslideDownloadedRecords:
            print('move negative data at ', nonLandslideDownloaded.object_id)
            downloaded_paths_string = nonLandslideDownloaded.storage_paths
            if type(downloaded_paths_string) != str:
                continue
            downloaded_paths = downloaded_paths_string.split(',')
            for downloaded_path in downloaded_paths:
                if downloaded_path != '' and downloaded_path != ' ':
                    downloaded_path = downloaded_path.strip()
                    download_path_values = downloaded_path.split('/')
                    new_file_name = "{}_{}_{}".format(download_path_values[5].strip(), download_path_values[6].strip(),
                                                      download_path_values[8].strip())
                    new_file_path = os.path.join(fconfig.dataset_path, "Negative", new_file_name)
                    img_download.copy_image_to_dataset(downloaded_path, new_file_path)
            # break  # tmp - remove after test on 1 image


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--sync', required=False, help='sync data from GLC file',type=int, default=0)
    parser.add_argument('--authenticate', required=False, help='Authenticate to Google Earth Engine API', type=int, default=1)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. to query satellite images contain landslide', type=int)
    args = parser.parse_args()
    main(execute_option=args.execute, gg_authenticate=args.authenticate , sync_glc=args.sync)
