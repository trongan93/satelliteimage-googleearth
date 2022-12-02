import sys
import os
import argparse
from data import image_query as img_query, image_download as img_download
from data import port_record
def main(execute_option, gg_authenticate):
    if execute_option == 1:
        print("Executing option 1: ")
        imageQueries = img_query.RandomLowLightImage(gg_authenticate)
        print(imageQueries)
        lowlight_Landsat9_images = imageQueries.getLowLightImages_Landsat9(cloud_lte=10)
        current_ee, lowlight_Landsat9_image = imageQueries.getBestImage(lowlight_Landsat9_images)
        # print(lowlight_Landsat9_image)
        image = img_download.downloadBestRGBImages(current_ee, lowlight_Landsat9_image)

    if execute_option == 10:
#     Test get URL
        import ee
        ee.Initialize()
        # A Sentinel-2 surface reflectance image.
        img = ee.Image('COPERNICUS/S2_SR/20210109T185751_20210109T185931_T10SEG')
        # A small region within the image.
        region = ee.Geometry.BBox(-122.0859, 37.0436, -122.0626, 37.0586)
        # Single-band GeoTIFF files wrapped in a zip file.
        url1 = img.getDownloadUrl({
            'name': 'single_band',
            'bands': [
                {'id': 'B3', 'crs': 'EPSG: 4326', },
                {'id': 'B8', 'crs': 'EPSG: 4326'},
                {'id': 'B11', 'crs': 'EPSG: 4326'}
            ]
        })
        print('url 1: ', url1)

        url2 = img.getDownloadUrl({
            'name': 'single_band',
            'bands': ['B3', 'B8', 'B11'],
            'region': region
        })
        print('url 2: ', url2)

    if execute_option == 20:
        print("Evaluation downloaded image file in GEOTIFF")
        import rasterio
        from rasterio.plot import show as tiff_show
        fp = r'/home/trongan93/Downloads/single_band3/single_band.B3.tif'
        img = rasterio.open(fp)
        tiff_show(img)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--authenticate', required=False, help='Authenticate to Google Earth Engine API', type=int, default=1)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. test 1 low-light image', type=int)
    args = parser.parse_args()
    print(args.execute)
    main(execute_option=args.execute, gg_authenticate=args.authenticate)