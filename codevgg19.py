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
transformer = pickle.load(open("transformer.pickle", "rb"))
base_model = VGG19(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('block5_conv1').output)

img_path = 'E:/all/'
labelled_data=np.empty((408,4097),dtype=object)
for i in range(1,409):
    name=str(i)+".jpg"
    img = image.load_img(img_path+name, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    features = model.predict(x)
    height=features.shape[1]
    width=features.shape[2]
    filters=features.shape[3]
    G= np.zeros((filters,filters))
    style= np.transpose(np.reshape(features,(height*width,filters)))
    G= np.dot(style,np.transpose(style))
    mat=np.transpose(G[np.triu_indices(512)])
    GM=np.reshape(mat,(1,256*513))
    G2= transformer.transform(GM)
    labelled_data[i-1,0]=name
    labelled_data[i-1,1:]=G2
np.save('products_style',labelled_data)
    #print(features)