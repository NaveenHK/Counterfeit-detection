# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 13:37:00 2018

@author: NaveenHK
"""

from vgg16 import VGG16
from keras.preprocessing import image
from imagenet_utils import preprocess_input
from keras.models import Model
import numpy as np

base_model = VGG16(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)

img_path = 'D:/Internship/Internship/data/fish.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

features = model.predict(x)
print(features.shape)
print(features.tolist())