# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 11:47:08 2018

@author: NaveenHK
"""

from vgg19 import VGG19
from keras.preprocessing import image
from imagenet_utils import preprocess_input
from keras.models import Model
import numpy as np
import pickle
import os
transformer = pickle.load(open("transformer.pickle", "rb"))
base_model = VGG19(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('block5_conv4').output)

PATH_TO_IMAGES_MAIN = './Labelled_Final/'
i=0
labelled_data=np.empty((3539,4097),dtype=object)

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

        features = model.predict(x)/196/512
        height=features.shape[1]
        width=features.shape[2]
        filters=features.shape[3]
        G= np.zeros((filters,filters))
        style= np.transpose(np.reshape(features,(height*width,filters)))
        G= np.dot(style,np.transpose(style))
        mat=np.transpose(G[np.triu_indices(512)])
        GM=np.reshape(mat,(1,256*513))
        G2= transformer.transform(GM)
        labelled_data[i,0]=im
        labelled_data[i,1:]=G2
        i=i+1
    print(upcount)
np.save('vgg19_style_54_labelled_data',labelled_data)
#print(labelled_data)
print(i)
    
