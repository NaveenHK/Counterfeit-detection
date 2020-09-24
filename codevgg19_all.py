# -*- coding: utf-8 -*-
"""
Created on Sun Apr 5 14:00:56 2020

@author: NaveenHK
"""
import os
from vgg19 import VGG19
from keras.preprocessing import image
from imagenet_utils import preprocess_input
from keras.models import Model
import numpy as np
import pickle
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

PATH_TO_IMAGES_MAIN = '/srv/naveen/images/'
base_model = VGG19(weights='imagenet')
model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)
#transformer = pickle.load(open("transformer.pickle", "rb"))

for upcount in range(1,1003):
    dictionary={}
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
        
#        height=features.shape[1]
#        width=features.shape[2]
#        filters=features.shape[3]
#        G= np.zeros((filters,filters))
#        
#        style= np.transpose(np.reshape(features,(height*width,filters)))
#        G= np.dot(style,np.transpose(style))
#        mat=np.transpose(G[np.triu_indices(512)])
#        GM=np.reshape(mat,(1,256*513))
#        G2= transformer.transform(GM)
        
        dictionary[im]=np.transpose(features)   # A numpy ndarray of dim (4096,1) is saved to dictionary to each image by its name as key.
        
        #print(features.shape)
        #print(features.tolist())
    pickle.dump(dictionary, open( "/srv/naveen/embeddings/vgg19/vgg19_content_embedding"+str(upcount)+".p", "wb" ) )

    



