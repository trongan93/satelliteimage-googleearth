from pathlib import Path
base_path = Path().absolute()
raw_glc_file = Path(base_path, 'raw', 'nasa_global_landslide_catalog_point.csv')
short_glc_file = Path(base_path,'raw','short_glc.csv')
# short_glc_file = Path(base_path,'raw','test_glc.csv')
base_saved_data_path = "/mnt/d/ProjectData/Landslide_Google_Earth_Engine"
landslide_storage_saved_paths = Path(base_saved_data_path,'landslide_downloaded_paths.csv')
non_landslide_storage_saved_paths = Path(base_saved_data_path,'non_landslide_downloaded_paths.csv')
dataset_path = "/mnt/d/ProjectData/LandslideDataset"

seaport_file = Path(base_path, 'raw', 'seaport-locations.csv') # https://www.kaggle.com/code/therohk/world-seaport-airport-dataset-and-codes/data?select=seaport-locations.csv
seaport_dataset_path = Path('/mnt/d/Seaport_satellite_images')
seaport_storage_saved_paths = Path(seaport_dataset_path,'seaport_downloaded_paths.csv')