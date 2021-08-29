# -*- coding: utf-8 -*-
"""Copy of car brand classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sPjwRJO57Py1-zYL-PfXdysWUezjSR_i
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir("/content/gdrive/My Drive")
!ls

train_path="/content/gdrive/My Drive/Datasets/Train"
test_path="/content/gdrive/My Drive/Datasets/Test"
class_names=os.listdir(train_path)
class_names_test=os.listdir(test_path)

class_names

class_names_test

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import ResNet50
#from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

IMAGE_SIZE = [224, 224]

resnet =  ResNet50(input_shape = IMAGE_SIZE + [3], weights='imagenet', include_top= False)

for layer in resnet.layers:
  layer.trainable = False

folders = glob('/content/gdrive/My Drive/Datasets/Train/*')

x = Flatten()(resnet.output)

prediction = Dense(len(folders), activation='softmax')(x)

model = Model(inputs= resnet.input, outputs=prediction)

model.summary()

model.compile(
    loss = 'categorical_crossentropy',
    optimizer='adam',
    metrics = ['accuracy']
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale= 1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip= True)
test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/gdrive/My Drive/Datasets/Train',
                                                 target_size= (224,224),
                                                 batch_size= 32,
                                                 class_mode = 'categorical')

len(training_set)

len(test_set)

test_set = test_datagen.flow_from_directory('/content/gdrive/My Drive/Datasets/Test',
                                                 target_size= (224,224),
                                                 batch_size= 32,
                                                 class_mode = 'categorical')

r = model.fit_generator(
    training_set,
    validation_data= test_set, epochs=50,
    steps_per_epoch = 2,
    validation_steps=2
)

r.history

# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

from tensorflow.keras.models import load_model
model.save('model_resnet50.h5')

y_pred = model.predict(test_set)

y_pred

import numpy as np
y_pred = np.argmax(y_pred, axis=1)

y_pred

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model('model_resnet50.h5')

img = image.load_img('/content/gdrive/My Drive/Datasets/Test/lamborghini//11.jpg', target_size= (224,224))

x = image.img_to_array(img)
x

x.shape

x= x/255

x = np.expand_dims(x, axis=0)
img_data = preprocess_input(x)
img_data.shape

model.predict(img_data)

a= np.argmax(model.predict(img_data), axis=1)

a==1

