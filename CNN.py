import faulthandler
faulthandler.enable()

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

from utils import DatasetLoader


print("Initiating dataset loader")
dataset_loader = DatasetLoader("data/locationsGeoguessr/",(48,64),"coordinates")

print("Loading train dataset")
train_images, train_labels = dataset_loader.load_dataset(0,9000)
print("Loading test dataset")
test_images, test_labels = dataset_loader.load_dataset(9000,10000)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 64, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(16, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(16, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(2))

print(model.summary())

model.compile(optimizer='adam',
              loss=tf.keras.losses.MeanSquaredError())

print(train_images.shape)
print(train_labels.shape)
print(test_images.shape)
print(test_labels.shape)

history = model.fit(train_images, train_labels, epochs=100, 
                    validation_data=(test_images, test_labels))


plt.figure(figsize=(10,10))
plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label = 'Validation loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='lower right')
plt.show()



train_predictions = model.predict(train_images)

plt.figure(figsize=(10,10))
print("yes")
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    print(train_images[i].shape)
    plt.imshow(train_images[i])
    plt.xlabel(str(list(train_labels[i].numpy()))+"\n"+str(list(train_predictions[i])))

plt.show()