import os
import random
from pymapillary import Mapillary
from pymapillary.utils import *
from downloaderUtils import LocationSaver, format_image

IMAGE_WIDTH = 1024
IMAGE_HEIGH = 768
SAVE_PATH = "locationsMapillary/"
MAX_PER_REQUEST = 1000


class MapillaryLocationDownloader:
    def __init__(self):
        self.location_saver = LocationSaver(SAVE_PATH)
        self.map_api = Mapillary(
            "dThHWFVHb0dNdnIyb0xDbm11NHVadzo1MjgxMWMyZDNjOTM0YjAy")

    def download_location(self, location_data):
        image_key = location_data["properties"]["key"]
        lon, lat = location_data["geometry"]["coordinates"]
        direction = location_data["properties"]["ca"]

        image_file_path = self.location_saver.save_new_location(
            lat, lon, direction)
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
        download_image_by_key(image_key, IMAGE_WIDTH, image_file_path)
        format_image(image_file_path)

    def download_randomly_in_bounding_box(self, boundingbox, num):
        if num == 0:
            return 0

        lat1, lon1, lat2, lon2 = boundingbox

        bbox = ",".join(map(lambda x: "%.6f" % x, [lon1, lat1, lon2, lat2]))

        try:
            res = self.map_api.search_images(
                bbox=bbox, per_page=MAX_PER_REQUEST)
        except:
            print(bbox)
            raise "Error while searching images in Mapillary"
        if "features" not in res:
            print(res)
        res_locations = res["features"]

        if len(res_locations) == MAX_PER_REQUEST and num > 1:
            # Too many locations, splitting up query to spread out images
            mid_lat = (lat1+lat2)/2
            mid_lon = (lon1+lon2)/2

            new_bounding_boxes = []
            new_bounding_boxes.append([lat1, lon1, mid_lat, mid_lon])
            new_bounding_boxes.append([mid_lat, lon1, lat2, mid_lon])
            new_bounding_boxes.append([lat1, mid_lon, mid_lat, lon2])
            new_bounding_boxes.append([mid_lat, mid_lon, lat2, lon2])
            random.shuffle(new_bounding_boxes)

            has_downloaded = 0
            for i in range(4):
                has_downloaded += self.download_randomly_in_bounding_box(
                    new_bounding_boxes[i], (num-has_downloaded)//(4-i))
            return has_downloaded

        num = min(len(res_locations), num)

        for location_data in random.choices(res_locations, k=num):
            self.download_location(location_data)

        return num
