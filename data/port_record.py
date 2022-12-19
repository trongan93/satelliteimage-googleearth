import pandas as pd
from model.portModel import SeaPortRecord
def readRecordData(input_file):
    glc_data = pd.read_csv(input_file)
    # print(glc_data.shape)
    portRecords = []
    for index, recordItem in glc_data.iterrows():
        portRecord = SeaPortRecord(lat=recordItem['latitude'], lng=recordItem['longitude'], name=recordItem['name'], country=recordItem['country'], referenceCode=recordItem['country'])
        # portRecord.printOut()
        portRecords.append(portRecord)
    return portRecords


def saveDownloadPaths(storage_records, seaport_dataset_path):
    return None