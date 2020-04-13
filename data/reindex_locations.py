import os

def reindex_locations(input_folders,output_folder):
    assert(output_folder[-1]=="/")
    location_index = 0
    for input_folder in input_folders:
        assert(input_folder[-1]=="/")
        file_names = os.listdir(input_folder)
        for file_name in file_names:
            if file_name[-5:]==".json":
                os.rename(input_folder+file_name,output_folder+str(location_index)+".json")
                os.rename(input_folder+file_name[:-5]+".jpg",output_folder+str(location_index)+".jpg")
                location_index += 1
reindex_locations(["locationsGeoguessr/"],"locationGeoguessrx/")