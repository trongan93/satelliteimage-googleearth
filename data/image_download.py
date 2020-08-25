import requests
import os
import errno
import zipfile
import configuration.fileconfiguration as fileconfig
def get_url(name, image, scale, region):
    try:
        path = image.getDownloadURL({
            'name': (name),
            'scale': scale,
            'region': (region)
        })
        return path
    except:
        return ''

def getURLImage(ee, image, lat, lng, img_region, object_id, img_name):
    img_name = "{}_{}_{}_{}".format(object_id,lng, lat, img_name)
    url = get_url(name=img_name, image=image, scale=30, region=img_region)
    return url

def downloadBestRGBImages(satelliteImages, lat, lng, img_region, object_id, error_query):
    urlLinks_obj = []
    errors_data = []
    ee = satelliteImages['ee']
    landsat_8_best_rgb = satelliteImages['landsat_8_best_rgb']
    landsat_7_best_rgb = satelliteImages['landsat_7_best_rgb']
    sentinel_2_best_rgb = satelliteImages['sentinel_2_best_rgb']
    alos_2_best_rgb = satelliteImages['alos_2_best_rgb']

    landsat_8_error = error_query['landsat_8_error']
    landsat_7_error = error_query['landsat_7_error']
    sentinel_2_error = error_query['sentinel_2_error']
    alos_2_error = error_query['alos_2_error']

    if landsat_8_error == '':
        landsat_8_best_rgb_link = getURLImage(ee,landsat_8_best_rgb, lat, lng, img_region, object_id, 'landsat_8_best_rgb')
        if landsat_8_best_rgb_link != '':
            urlLinks_obj.append('landsat_8')
            urlLinks_obj.append(landsat_8_best_rgb_link)
        else:
            errors_data.append('landsat_8')
            errors_data.append('NO DATA')
        # # Test
        # from demo import exportImage as ex_img
        # ex_img.exportToDrive(ee,landsat_8_best_rgb,'{}_landsat_8_best_rgb'.format(object_id), img_region)
        # # End Test - remove when testing finish
    else:
        errors_data.append('landsat_8')
        errors_data.append(landsat_8_error)

    if landsat_7_error == '':
        landsat_7_best_rgb_link = getURLImage(ee,landsat_7_best_rgb, lat, lng, img_region, object_id, 'landsat_7_best_rgb')
        if landsat_7_best_rgb_link != '':
            urlLinks_obj.append('landsat_7')
            urlLinks_obj.append(landsat_7_best_rgb_link)
        else:
            errors_data.append('landsat_7')
            errors_data.append('NO DATA')
    else:
        errors_data.append('landsat_7')
        errors_data.append(landsat_7_error)

    if sentinel_2_error == '':
        sentinel_2_best_rgb_link = getURLImage(ee,sentinel_2_best_rgb, lat, lng, img_region, object_id, 'sentinel_2_best_rgb')
        if sentinel_2_best_rgb_link != '':
            urlLinks_obj.append('sentinel_2')
            urlLinks_obj.append(sentinel_2_best_rgb_link)
        else:
            errors_data.append('sentinel_2')
            errors_data.append('NO DATA')
    else:
        errors_data.append('sentinel_2')
        errors_data.append(sentinel_2_error)

    if alos_2_error == '':
        alos_2_best_rgb_link = getURLImage(ee,alos_2_best_rgb, lat, lng, img_region, object_id, 'alos_2_best_rgb')
        if alos_2_best_rgb_link != '':
            urlLinks_obj.append('alos_2')
            urlLinks_obj.append(alos_2_best_rgb_link)
        else:
            errors_data.append('alos_2')
            errors_data.append('NO DATA')
    else:
        errors_data.append('alos_2')
        errors_data.append(alos_2_error)
    return urlLinks_obj, errors_data

def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
        fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def downloadLandslideFilesToLocal(objectid, urls_obj):
    # print(objectid)
    # print(urls_obj)
    saved_paths = []
    for i in range(0, len(urls_obj), 2):
        satellite = urls_obj[i]
        url = urls_obj[i+1]
        if url != '':
            r = requests.get(url, allow_redirects = True)
            # filename = getFilename_fromCd(r.headers.get('content-disposition'))
            saved_path = "{}/{}/{}/Positive".format(fileconfig.base_saved_data_path, objectid, satellite)
            if not os.path.exists(saved_path):
                os.makedirs(saved_path)
            saved_path_file = "{}/downloaded.zip".format(saved_path)
            open(saved_path_file,'wb').write(r.content)
            with zipfile.ZipFile(saved_path_file, 'r') as zip_ref:
                zip_ref.extractall(saved_path)
            os.remove(saved_path_file)
            saved_paths.append(saved_path)
    return saved_paths
