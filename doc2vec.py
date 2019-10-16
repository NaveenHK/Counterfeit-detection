# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:37:32 2018

@author: kar129
"""

from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile

import time
import pickle
tagged_data = pickle.load( open( "./words_tagged_final.txt", "rb" ))
print('start')





max_epochs = 1
vec_size = 2048
alpha = 0.025

model = Doc2Vec(size=vec_size,alpha=alpha,min_alpha=alpha,min_count=1,dm =1)   #uses fixed lr
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,total_examples=model.corpus_count,epochs=model.iter) #iter=5
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v2.model")
print("Model Saved")