import datetime
LANDSAT_8 = "LANDSAT/LC08/C01/T1_RT"
LANDSAT_7 = "LANDSAT/LE07/C01/T1_RT"
SENTINEL_2 = "COPERNICUS/S2" #COPERNICUS/S2_SR
ALOS_2 = "JAXA/ALOS/AVNIR-2/ORI"

LANDSAT_8_TIME_RANGE = [datetime.datetime.strptime('2013-04-01','%Y-%m-%d'), datetime.datetime.now()]
LANDSAT_7_TIME_RANGE = [datetime.datetime.strptime('1999-01-01','%Y-%m-%d'), datetime.datetime.now()]
SENTINEL_2_TIME_RANGE = [datetime.datetime.strptime('2015-06-23','%Y-%m-%d'), datetime.datetime.now()]
ALOS_2_TIME_RANGE = [datetime.datetime.strptime('2006-04-26','%Y-%m-%d'), datetime.datetime.strptime('2011-04-18','%Y-%m-%d')]

CLOUDY_PERCENTAGE_FILTER = 20

ALL_SATELLITE = []
ALL_SATELLITE.append([LANDSAT_8,LANDSAT_7,SENTINEL_2,ALOS_2])