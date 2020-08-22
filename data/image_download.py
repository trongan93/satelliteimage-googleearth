def get_url(name, image, scale, region):
    path = image.getDownloadURL({
        'name': (name),
        'scale': scale,
        'region': (region)
    })
    return path

def getURLImage(ee, image, lat, lng, img_region, object_id, img_name):
    img_name = "{}_{}_{}_{}".format(object_id,lng, lat, img_name)
    url = get_url(name=img_name, image=image, scale=30, region=img_region)
    return url

def downloadBestRGBImages(satelliteImages, lat, lng, img_region, object_id, error_query):
    urlLinks = []
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
        urlLinks.append(landsat_8_best_rgb_link)
        # # Test
        # from demo import exportImage as ex_img
        # ex_img.exportToDrive(ee,landsat_8_best_rgb,'landsat_8_best_rgb', img_region)
        # # End Test - remove when testing finish
    else:
        errors_data.append(landsat_8_error)

    if landsat_7_error == '':
        landsat_7_best_rgb_link = getURLImage(ee,landsat_7_best_rgb, lat, lng, img_region, object_id, 'landsat_7_best_rgb')
        urlLinks.append(landsat_7_best_rgb_link)
    else:
        errors_data.append(landsat_7_error)

    if sentinel_2_error == '':
        sentinel_2_best_rgb_link = getURLImage(ee,sentinel_2_best_rgb, lat, lng, img_region, object_id, 'sentinel_2_best_rgb')
        urlLinks.append(sentinel_2_best_rgb_link)
    else:
        errors_data.append(sentinel_2_error)

    if alos_2_error == '':
        alos_2_best_rgb_link = getURLImage(ee,alos_2_best_rgb, lat, lng, img_region, object_id, 'alos_2_best_rgb')
        urlLinks.append(alos_2_best_rgb_link)
    else:
        errors_data.append(alos_2_error)

    return urlLinks, errors_data