import time
import webbrowser


def exportToDrive(ee, image, img_desciption, region):
    print("Exporting image to Drive")
    # Export the image, specifying scale and region.
    task1 = ee.batch.Export.image.toDrive(image=image, description=img_desciption, scale=10, region=region);
    task1.start()

    while True:
        status = task1.status()
        print(status)
        time.sleep(1)
        if status['state'] == 'COMPLETED':
            print("Completed task", )
            # task1.stop()
            break
def get_url(name, image, scale, region):
    """It will open and download automatically a zip folder containing Geotiff data of 'image'.
    If additional parameters are needed, see also:
    https://github.com/google/earthengine-api/blob/master/python/ee/image.py

    Parameters:
        name (str): name of the created folder
        image (ee.image.Image): image to export
        scale (int): resolution of export in meters (e.g: 30 for Landsat)
        region (list): region of interest

    Returns:
        path (str)
     """
    path = image.getDownloadURL({
        'name':(name),
        'scale': scale,
        'region':(region)
        })

    # webbrowser.open_new_tab(path)
    return path

# def exportImages(ee, images):
#     ee.batch.Download
#     print(count)