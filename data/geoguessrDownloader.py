from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import base64
import requests
import json
import signal
import sys

from downloaderUtils import LocationSaver
from downloaderUtils import format_image
from privateData import GEOGUESSR_SESSISON_ID



SAVE_PATH = "locationsGeoguessrUrbanWorld/"
URBAN_WORLD_URL = "https://www.geoguessr.com/maps/5b3d510b7a2b425ef47b54fd/play"
WORLD_URL = "https://www.geoguessr.com/maps/world/play"
ACTIVE_MAP = URBAN_WORLD_URL

class GeoguessrDownloader:
    def __init__(self):
        self.location_saver = LocationSaver(SAVE_PATH)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1024x816")

        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
        chrome_driver = os.getenv(
            "HOME")+"/applications/chromedriver/chromedriver"
        self.driver = webdriver.Chrome(
            options=chrome_options, executable_path=chrome_driver)
        self.driver.get(ACTIVE_MAP)
        self.driver.add_cookie(
            {"domain": "geoguessr.com", "name": "_ncfa", "value": GEOGUESSR_SESSISON_ID})

    def getCoordinates(self, token):
        #print("Token:",token)
        res = requests.post("https://www.geoguessr.com/api/v3/games/"+token, headers={
            "cookie": "_ncfa="+GEOGUESSR_SESSISON_ID
        }, data={"token": token, "lat": 0, "lng": 0, "timedOut": "false"})
        
        jsonRes = json.loads(res.text)
        return jsonRes["rounds"][0]["lat"],jsonRes["rounds"][0]["lng"]

    def get_random_location(self):
        self.driver.get(ACTIVE_MAP)
        play_button = self.driver.find_elements_by_css_selector(
            '.game-settings__section .button')[0]
        play_button.click()

        time.sleep(10)

        canvas = self.driver.find_element_by_css_selector(
            ".widget-scene-canvas")
        canvas_base64 = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);", canvas)

        lat, lon = self.getCoordinates(self.driver.current_url.split("/")[-1])

        image_path = self.location_saver.save_new_location(lat,lon,0)

        canvas_png = base64.b64decode(canvas_base64)
        with open(image_path, 'wb') as f:
            f.write(canvas_png)
        format_image(image_path)

        print("Success!")

    def exit(self):
        self.driver.quit()
        print("Driver killed, exiting...")
        sys.exit(0)
        
def main():


    geooguessr_downloader = GeoguessrDownloader()

    try:
        for i in range(1000):
            print("Locations downloaded: ", i)
            geooguessr_downloader.get_random_location()
    except:
        geooguessr_downloader.exit()
    signal.signal(signal.SIGINT, exit)

    geooguessr_downloader.exit()
if __name__ == "__main__":
    main()
