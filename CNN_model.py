import os
from tensorflow.keras import datasets, layers, models
import tensorflow as tf
import faulthandler
faulthandler.enable()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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

        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.MeanSquaredError())

    def train(self, train_dataset, val_dataset,epochs):
        history = self.model.fit(train_dataset, epochs=epochs,
                                      validation_data=val_dataset)
        self.loss_history = history.history["val_loss"]

    def predict(self, inputs):
        return self.model.predict(inputs)
    