import tensorflow as tf
import numpy as np
import json
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class DatasetLoader():
    def __init__(self, folder_path,  input_img_size, output_type):
        self.output_type = output_type
        self.folder_path = folder_path
        self.input_img_size = input_img_size

    def get_coordinates(self, file_path):
        label_data = tf.strings.split(tf.io.read_file(file_path),sep=",")
        return tf.stack([tf.strings.to_number(label_data[0])/90,tf.strings.to_number(label_data[1])/180])
        return tf.stack([0,0])

    def decode_img(self, img):
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        return tf.image.resize(img, self.input_img_size)
        #return tf.constant(np.zeros((48,64,3)))

    def read_from_index(self, file_index):
        file_index_str = tf.strings.as_string(file_index)
        label = self.get_coordinates(self.folder_path + file_index_str + ".csv")
        img = tf.io.read_file(self.folder_path + file_index_str + ".jpg")
        img = self.decode_img(img)
        return img, label

    def load_dataset(self,start_index, end_index, cache_file, batch_size=1000):
        indices = np.arange(start_index,end_index)
        ds_indices = tf.data.Dataset.from_tensor_slices(indices)
        datset = ds_indices.map(self.read_from_index, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        return datset.cache(cache_file + ".cache").shuffle(batch_size).batch(batch_size)

