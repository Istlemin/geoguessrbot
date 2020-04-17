from tensorflow.keras.losses import MSE
from tensorflow.keras import datasets, layers, models
import tensorflow as tf
import numpy as np


class NoInputModel:
    def __init__(self):
        self.setup_model()

    def setup_model(self):
        self.model = models.Sequential()
        self.model.add(layers.Dense(2, input_shape=(1,)))
        print(self.model.summary())

        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.2),
                           loss=tf.keras.losses.MeanSquaredLogarithmicError())

    def nullify_input(self, img,label):
        return [0], label

    def train(self, train_dataset, validation_dataset, epochs):
        history = self.model.fit(train_dataset.map(self.nullify_input), epochs=epochs,
                                 validation_data=validation_dataset.map(self.nullify_input))
        self.validation_loss_history = history.history["val_loss"]
        self.training_loss_history = history.history["loss"]

    def predict(self, inputs):
        return self.model.predict(np.zeros((inputs.shape[0], 1)))
