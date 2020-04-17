import os
from tensorflow.keras import datasets, layers, models
import tensorflow as tf
import faulthandler
faulthandler.enable()
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

@tf.function
def tensor_gps_distance(origin, destination):
    lat1 = origin[0]
    lon1 = origin[1]
    lat2 = destination[0]
    lon2 = destination[1]
    lat1 *= math.pi/2 
    lat2 *= math.pi/2
    lon1 *= math.pi 
    lon2 *= math.pi 
    radius = 6371 
    dlat = (lat2 - lat1)
    dlon = (lon2 - lon1)
    a = (tf.math.sin(dlat / 2) * tf.math.sin(dlat / 2) +
         tf.math.cos((lat1)) * tf.math.cos((lat2)) *
         tf.math.sin(dlon / 2) * tf.math.sin(dlon / 2))
    c = 2 * tf.math.atan2(tf.math.sqrt(a), tf.math.sqrt(1 - a))
    d = radius * c

    return d

@tf.function
def geoguessr_loss(y_actual,y_pred):
    return tf.math.sqrt((y_actual[0]-y_pred[0])*(y_actual[0]-y_pred[0])+(y_actual[1]-y_pred[1])*(y_actual[1]-y_pred[1]))#1-tf.math.exp(-tensor_gps_distance(y_actual,y_pred)/2000)

class CNNModel:
    def __init__(self):
        self.setup_model()

    def setup_model(self):
        self.model = models.Sequential()
        self.model.add(layers.Conv2D(
            32, (3, 3), activation='relu', input_shape=(48, 64, 3)))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(16, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(16, (3, 3), activation='relu'))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(16, activation='relu'))
        self.model.add(layers.Dense(2))
        print(self.model.summary())

        self.model.compile(optimizer="adam",#tf.keras.optimizers.Adam(learning_rate=0.001),
                           #loss=geoguessr_loss)
                           loss=tf.keras.losses.MeanSquaredLogarithmicError())

    def train(self, train_dataset, val_dataset,epochs):
        history = self.model.fit(train_dataset, epochs=epochs,
                                      validation_data=val_dataset)
        self.validation_loss_history = history.history["val_loss"]
        self.training_loss_history = history.history["loss"]

    def predict(self, inputs):
        return self.model.predict(inputs)
    