import os
import json
import codecs

def reindex_locations(input_folders, output_folder):
    assert(output_folder[-1] == "/")
    location_index = 0
    for input_folder in input_folders:
        assert(input_folder[-1] == "/")
        file_names = os.listdir(input_folder)
        for file_name in file_names:
            if file_name[-5:] == ".json":
                os.rename(input_folder+file_name, output_folder +
                          str(location_index)+".json")
                os.rename(
                    input_folder+file_name[:-5]+".jpg", output_folder+str(location_index)+".jpg")
                location_index += 1


def json_to_csv(folders):
    column_names = ["lat", "lon", "country", "country_code"]
    for folder in folders:
        file_names = os.listdir(folder)
        for j,file_name in enumerate(file_names):
            if file_name[-5:] == ".json":
                csv_string = ""
                with codecs.open(folder+file_name, "r", "utf-8") as f:
                    json_data = json.load(f)
                for i, column_name in enumerate(column_names):
                    if i != 0:
                        csv_string += ","
                    csv_string += str(json_data[column_name])
                csv_string += "\n"
                with codecs.open(folder+file_name[:-5]+".csv", "w", "utf-8") as f:
                    f.write(csv_string)
                if j%100==0:
                    print(j)


json_to_csv(["../../geoguessrBotDatasets/geoguessrWorld/"])
# reindex_locations(["locationsGeoguessr/"],"locationGeoguessrx/")
