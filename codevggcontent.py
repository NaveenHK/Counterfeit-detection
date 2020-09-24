# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 11:03:38 2018

@author: kar129
"""

import os
from vgg19 import VGG19
from keras.preprocessing import image
from imagenet_utils import preprocess_input
from keras.models import Model
import numpy as np
#import pickle 
#import time
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

PATH_TO_IMAGES_MAIN = './Labelled_Final/'
base_model = VGG19(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)

labelled_data=np.empty((3539,4097),dtype=object)

i=0
for upcount in range(806):
    PATH_TO_IMAGES = PATH_TO_IMAGES_MAIN+str(upcount)+'/'
    image_paths = os.listdir(PATH_TO_IMAGES)
    #print(image_paths)
    
    for im in image_paths:
        
        img_path = PATH_TO_IMAGES+im
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        features = model.predict(x)
        labelled_data[i,0]=im
        labelled_data[i,1:]=features# A numpy ndarray of dim (1,4096) is saved to dictionary to each image by its name as key.
        i=i+1
    print(upcount)
np.save('vgg19_labelled_data',labelled_data)
#print(labelled_data)
print(i)