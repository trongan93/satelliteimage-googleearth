from pathlib import Path
from configuration import fileconfiguration as fconfig, landslideconfiguration as ls_config
from data import landslide_record as record
from data import image_query as img_query, image_download as img_download
import datetime
def main(execute_option, gg_authenticate, sync_glc):
    if sync_glc == 1:
        print("Sync data file from GLC to landslide short file")
        landslideRecords = record.readRecordData(fconfig.raw_glc_file)
        record.save_short_landslide_record(landslideRecords, fconfig.short_glc_file)
        print("Successful to change from GLC raw file to short datafile at: ", fconfig.short_glc_file)

    if execute_option == 1:
        print("Executed selection 1; Query satellite from glc short file")
        imageQueries = img_query.SatelliteQueryImage(authenticate=gg_authenticate)
        landslideRecords = record.read_short_landslide_record(fconfig.short_glc_file)
        for landslideRecord in landslideRecords:
            # print(landslideRecord.event_date)
            event_date = datetime.datetime.strptime(landslideRecord.event_date,'%Y-%m-%d %H:%M:%S.%f')
            landslideImageRegion = imageQueries.defineImageRegion(landslideRecord.size, landslideRecord.lng, landslideRecord.lat)
            landslideSatellitesImages, error_query = imageQueries.getSatellitesImagesContainLandslide(landslideRecord.lat,landslideRecord.lng,event_date, event_date + datetime.timedelta(days=ls_config.LANDSLIDE_EVEN_COLLTECTION_TIME))
            landslideRGBSatellitesImages = imageQueries.getSatellitesImageRGB(landslideSatellitesImages)
            landslideBestRGBSatellitesImage = imageQueries.getBestSatelliteRGBImage(landslideRGBSatellitesImages)
            urlLinks = img_download.downloadBestRGBImages(landslideBestRGBSatellitesImage, landslideRecord.lat, landslideRecord.lng, landslideImageRegion, landslideRecord.object_id, error_query)
            print(urlLinks)
            break #tmp - remove after test on 1 image



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--sync', required=False, help='sync data from GLC file',type=int, default=0)
    parser.add_argument('--authenticate', required=False, help='Authenticate to Google Earth Engine API', type=int, default=1)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. to query satellite images contain landslide', type=int)
    args = parser.parse_args()
    main(execute_option=args.execute, gg_authenticate=args.authenticate , sync_glc=args.sync)
