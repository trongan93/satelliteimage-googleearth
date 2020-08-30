from pathlib import Path
base_path = Path().absolute()
raw_glc_file = Path(base_path, 'raw', 'nasa_global_landslide_catalog_point.csv')
short_glc_file = Path(base_path,'raw','short_glc.csv')
# short_glc_file = Path(base_path,'raw','test_glc.csv')
base_saved_data_path = "/mnt/d/ProjectData/Landslide_Google_Earth_Engine"
landslide_storage_saved_paths = Path(base_saved_data_path,'landslide_downloaded_paths.csv')
non_landslide_storage_saved_paths = Path(base_saved_data_path,'non_landslide_downloaded_paths.csv')