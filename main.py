from pathlib import Path
from configuration import fileconfiguration as fconfig
from data import landslide_record as record
from data import image_query as img_query
def main(execute_option, sync_glc):
    if sync_glc == 1:
        print("Sync data file from GLC to landslide short file")
        landslideRecords = record.readRecordData(fconfig.raw_glc_file)
        record.save_short_landslide_record(landslideRecords, fconfig.short_glc_file)
        print("Successful to change from GLC raw file to short datafile at: ", fconfig.short_glc_file)
    if execute_option == 1:
        print("Executed selection 1; Query satellite from glc short file")
        landslideRecords = record.read_short_landslide_record(fconfig.short_glc_file)
        for landslideRecord in landslideRecords:
            landslideimages = img_query.querySatelliteImages(landslideRecord.lat, landslideRecord.lng, landslideRecord.event_date)
            break #tmp - remove after test on 1 image



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--sync', required=False, help='sync data from GLC file',type=int, default=0)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. to query satellite images contain landslide', type=int)
    args = parser.parse_args()
    main(execute_option=args.execute, sync_glc=args.sync)
