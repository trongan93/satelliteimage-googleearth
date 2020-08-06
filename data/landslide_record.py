from model.landslideModel import LandslideRecord, LandslideDownloadImageData

import pandas as pd
import os
from pathlib import Path

def countByLandslideSize(landslideRecords):
    print('Total landslide record: ', len(landslideRecords))
    countLarge = countMedium = countVeryLarge = countSmall = countExtraLarge = countOther = countCatastrophic=0
    for record in landslideRecords:
        if record.size == "medium":
            countMedium += 1
        elif record.size == "large":
            countLarge += 1
        elif record.size == "very_large":
            countVeryLarge += 1
        elif record.size == "small":
            countExtraLarge += 1
        elif record.size == 'catastrophic':
            countCatastrophic += 1
        else:
            countOther +=1

    print("Landslide number of Small size: ", countSmall)
    print("Landslide number of Medium size: ", countMedium)
    print("Landslide number of Large size: ", countLarge)
    print("Landslide number of Very large size: ", countVeryLarge)
    print("Landslide number of Catastrophic size: ", countCatastrophic)
    print("Landslide number of Another size: ", countOther)

def replace_landslide_size(record):
    if record.size == "Medium" or record.size == "medium":
        record.size = 'medium'
    elif record.size == "Large" or record.size == "large":
        record.size = 'large'
    elif record.size == "Very_large" or record.size == "very_large":
        record.size = 'very_large'
    elif record.size == "Small" or record.size == "small":
        record.size = 'small'
    elif record.size == "catastrophic":
        record.size = 'catastrophic'
    else:
        print(record.size)
        record.size = 'unknown'
    return record

def readRecordData(input_file):
    glc_data = pd.read_csv(input_file)
    # print(glc_data.shape)
    landslides = []
    for index, recordItem in glc_data.iterrows():
        landslideRecord = LandslideRecord(object_id=recordItem['OBJECTID'], event_id=recordItem['event_id'], landslide_category=recordItem['landslide_category'],
                                          lat=recordItem['latitude'], lng=recordItem['longitude'],
                                          event_date=recordItem['event_date'], size=recordItem['landslide_size'],
                                          country=recordItem['country_name'])
        if landslideRecord.landslide_category == 'landslide':
            landslideRecord = replace_landslide_size(landslideRecord)
            landslides.append(landslideRecord)
    return landslides

def save_short_landslide_record(landslideRecords,path):
    landslideRecords_Array = []
    for landslideRecord in landslideRecords:
        landslideRecords_Array.append(landslideRecord.toArray())
    # print(landslideRecords_Array[0])
    df = pd.DataFrame(landslideRecords_Array, columns=['object_id','event_id','lat','lng','event_date','size','country','landslide_category'])
    print(df)
    df.to_csv(path, index=False, header=True)
    print('done to save a short glc file')

if __name__ == "__main__":
    base_path = Path().absolute().parent
    input_path_from_glcdata = Path(base_path,'raw','nasa_global_landslide_catalog_point.csv')
    short_glc_data = Path(base_path,'raw','short_glc.csv')
    landslideRecords = readRecordData(input_path_from_glcdata)
    save_short_landslide_record(landslideRecords,short_glc_data)