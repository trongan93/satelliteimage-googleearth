from abc import ABC
class SeaPortRecord(ABC):
    def __init__(self, lat, lng, name, country, referenceCode):
        self._lat = lat
        self._lng = lng
        self._name = name
        self._country = country
        self._referenceCode = referenceCode

    def printOut(self):
        print("Seaport infor:: lat: %f, lng: %f, name: %s, country: %s, ref_code: %s" % (self._lat, self._lng, self._name, self._country, self._referenceCode))



