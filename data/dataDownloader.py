import random
from mapillaryDownloader import MapillaryLocationDownloader

random.seed(0)

def main():
    mapillary_downloader = MapillaryLocationDownloader()
    left_to_download = 10000
    while left_to_download > 0:
        print("Left to download:", left_to_download)
        random_lat = random.randint(-90, 90)
        random_lon = random.randint(-180, 180)
        left_to_download -= mapillary_downloader.download_randomly_in_bounding_box(
            [random_lat, random_lon, random_lat+4, random_lon+4], 10)


if __name__ == "__main__":
    main()
