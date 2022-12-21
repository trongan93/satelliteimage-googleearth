import pandas as pd
from model.portModel import PortRecord, PortStorageImageData
def readRecordData(input_file):
    glc_data = pd.read_csv(input_file)
    # print(glc_data.shape)
    portRecords = []
    for index, recordItem in glc_data.iterrows():
        portRecord = PortRecord(lat=recordItem['latitude'], lng=recordItem['longitude'], name=recordItem['name'], country=recordItem['country'], referenceCode=recordItem['country'])
        # portRecord.printOut()
        portRecords.append(portRecord)
    return portRecords

def getRecordDownloadedPaths(record, storage_paths):
    return PortStorageImageData(lat=record._lat, lng=record._lng, name=record._name, country=record._country, referenceCode=record._referenceCode, storage_paths=storage_paths)

def saveDownloadPaths(records, path):
    records_array = []
    for record in records:
        records_array.append(record.toArray())
    df = pd.DataFrame(records_array, columns=['lat', 'lng', 'name', 'country', 'reference code', 'storage_paths'])
    # print(df)
    df.to_csv(path, index=False, header=True)
    print('done to save a downloaded paths')