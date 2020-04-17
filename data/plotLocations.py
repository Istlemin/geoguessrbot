import matplotlib.pyplot as plt
import mplleaflet
import os
import json

PATH = "locationsGeoguessr/"

def main():
    lat = []
    lon = []

    location_index = 0
    while os.path.exists(PATH + str(location_index) + '.json'):
        with open(PATH + str(location_index) + '.json',"r") as f:
            data = json.loads(f.read())
            lat.append(data["lat"])
            lon.append(data["lon"])
        location_index += 1

    plt.plot(lon, lat, 'rs')
    mplleaflet.show()

main()
