from abc import ABC


class LandslideData(ABC):
    def __init__(self, lat, lng, event_date, size):
        self.lat = lat
        self.lng = lng
        self.event_date = event_date
        self.size = size


class LandslideRecord(LandslideData):
    def __init__(self, object_id, event_id, lat, lng, event_date, size, country, landslide_category):
        self.object_id = object_id
        self.event_id = event_id
        self.lat = lat
        self.lng = lng
        self.event_date = event_date
        self.size = size
        self.country = country
        self.landslide_category = landslide_category

    def printOut(self):
        print("Landslide Object id ", self.object_id)

    def toArray(self):
        return [self.object_id, self.event_id, self.lat, self.lng, self.event_date, self.size, self.country,
                self.landslide_category]


class LandslideStorageImageData(LandslideRecord):
    def __init__(self, object_id, event_id, lat, lng, event_date, size, country, landslide_category, storage_paths):
        self.object_id = object_id
        self.event_id = event_id
        self.lat = lat
        self.lng = lng
        self.event_date = event_date
        self.size = size
        self.country = country
        self.landslide_category = landslide_category
        self.storage_paths = storage_paths
    def toArray(self):
        return [self.object_id, self.event_id, self.lat, self.lng, self.event_date, self.size, self.country,
                self.landslide_category, self.storage_paths]