import time
import os
import random
import json
import cv2
import numpy as np
import requests

random.seed(0)

IMAGE_WIDTH = 1024
IMAGE_HEIGH = 768


def get_country_by_coordinates(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=" + \
        str(lat)+"&lon="+str(lon)

    res = None
    while res is None or res.status_code != 200:
        try:
            res = requests.get(url, timeout=10)
        except:
            print(url)
            print(res)
            print("No connection, retrying in 1 min")
            time.sleep(60)
    res = res.json()
    if "address" not in res:
        return "unknown", "unknown"
    return res["address"]["country"], res["address"]["country_code"]


def format_image(image_path):
    try:
        img = cv2.imread(image_path)
    except:
        print("No such image: " + image_path)
        return

    if img.shape[1] < IMAGE_WIDTH:
        img = np.append(img, np.zeros(
            (img.shape[0], IMAGE_WIDTH-img.shape[1], 3)), axis=1)
    assert(img.shape[1] == IMAGE_WIDTH)
    img = img[:-IMAGE_WIDTH//16, :]  # crop off watermark

    height = img.shape[0]
    bar_top = (IMAGE_HEIGH-height)//2
    bar_bottom = (IMAGE_HEIGH-height) - bar_top
    if bar_top > 0:
        img = np.append(np.zeros((bar_top, IMAGE_WIDTH, 3)), img, axis=0)
    else:
        img = img[-bar_top:, :]
    if bar_bottom > 0:
        img = np.append(img, np.zeros((bar_bottom, IMAGE_WIDTH, 3)), axis=0)
    else:
        img = img[:bar_bottom, :]

    cv2.imwrite(image_path, img,[int(cv2.IMWRITE_JPEG_QUALITY), 65])


class LocationSaver:
    def __init__(self, save_path):
        self.save_path = save_path
        self.location_index = 0
        while os.path.exists(self.save_path + str(self.location_index) + '.jpg'):
            self.location_index += 1

    def save_new_location(self, lat, lon, direction):
        country, country_code = get_country_by_coordinates(lat, lon)
        json_data = {
            "lat": lat,
            "lon": lon,
            "direction": direction,
            "country": country,
            "country_code": country_code
        }
        with open(self.save_path+str(self.location_index) + '.json', 'w') as f:
            json.dump(json_data, f)

        self.location_index += 1
        return self.save_path + str(self.location_index-1) + '.jpg'


if __name__ == "__main__":
    print(get_country_by_coordinates(59, 18))
