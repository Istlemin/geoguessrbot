import tensorflow as tf
import numpy as np
import json



class DatasetLoader():
    def __init__(self, folder_path,  input_img_size, output_type):
        self.output_type = output_type
        self.folder_path = folder_path
        self.input_img_size = input_img_size

    def get_coordinates(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
            lat = data["lat"]
            lon = data["lon"]
        return tf.constant([lat,lon],dtype=tf.float32)

    def decode_img(self, img):
        # convert the compressed string to a 3D uint8 tensor
        img = tf.image.decode_jpeg(img, channels=3)
        # Use `convert_image_dtype` to convert to floats in the [0,1] range.
        img = tf.image.convert_image_dtype(img, tf.float32)
        # resize the image to the desired size.
        return tf.image.resize(img, self.input_img_size)

    def read_from_index(self, file_index):
        label = self.get_coordinates(self.folder_path + str(file_index) + ".json")
        img = tf.io.read_file(self.folder_path + str(file_index) + ".jpg")
        img = self.decode_img(img)
        #print(list(img))
        return img, label

    def load_dataset(self,start_index, end_index):
        imgs = []
        labels = []
        for i in range(start_index,end_index):
            img,label = self.read_from_index(i)
            imgs.append(img)
            labels.append(label)
            if i%100==0:
                print(i)
        print("Done loading")
        #imgs = np.array(imgs)
        #print("Converted imgs to np")
        #labels = np.array(labels)
        #print("Converted labels to np")
        return tf.stack(imgs),tf.stack(labels)
    
