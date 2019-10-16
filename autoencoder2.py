# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 15:54:53 2018

@author: kar129
"""
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
import h5py

encoding_dim = 4096
input_dim=256*513

input_img = Input(shape=(input_dim,))
# "encoded" is the encoded representation of the input
encoded = Dense(50000, activation='relu')(input_img)
encoded = Dense(10000, activation='relu')(encoded)
encoded = Dense(encoding_dim, activation='relu')(encoded)

# "decoded" is the lossy reconstruction of the input
decoded = Dense(10000, activation='relu')(encoded)
decoded = Dense(50000, activation='relu')(decoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded)

# this model maps an input to its reconstruction
autoencoder= Model(input_img,decoded)
# this model maps an input to its encoded representation
encoder= Model(input_img,encoded)

# create a placeholder for an encoded (32-dimensional) input
encoded_input = Input(shape=(encoding_dim,))
# retrieve the last layer of the autoencoder model
decoder_layer1 = autoencoder.layers[-3]
decoder_layer2 = autoencoder.layers[-2]
decoder_layer3 = autoencoder.layers[-1]
# create the decoder model
#decoder = Model(encoded_input, decoder_layer3(decoder_layer2(decoder_layer1(encoded_input))))

autoencoder.compile(optimizer='adam', loss='mean_squared_error')

#for ep in range(5):
#    for j in range(1,26):

x_train=np.transpose(np.load("E:/GM/vgg19_gram_matrix1.npy"))
print(x_train.shape)

autoencoder.fit(x_train, x_train,epochs=1,batch_size=10,shuffle=False)
                
#autoencoder.save("Autoencoder_1.h5")    
#encoder.save("Encoder_1.h5")           

