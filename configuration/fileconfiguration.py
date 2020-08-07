from pathlib import Path
base_path = Path().absolute()
raw_glc_file = Path(base_path, 'raw', 'nasa_global_landslide_catalog_point.csv')
short_glc_file = Path(base_path,'raw','short_glc.csv')