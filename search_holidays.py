# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 19:44:54 2018

@author: kar129
"""

# Copyright (c) Jathushan Rajasegaran
# Email - brjathu@gmail.com
# University of Moratuwa
# Department of Electronics and Telecommunication


import os
import numpy as np
import tensorflow as tf
import scipy.io
import scipy.misc
import scipy.spatial.distance
import time
from sklearn.decomposition import PCA
from PIL import Image
import skimage
import skimage.io
import skimage.transform
import sys

# parameters
bool_PCA = True
batch_size_all = 1491
batch_size_quary = 1
best_simalr = 20
#test_case = str(sys.argv[1])
#a = float(sys.argv[2])
#b = float(sys.argv[3])

#LOG_FILE = open('/srv/jathushan/data/logs/log_search_' + test_case  +'.txt', 'a')

############################ UDF #######################


def load_image(path):
    # load image
    # img = skimage.io.imread(path)
    img = np.array(Image.open(path).convert("RGB"))

    img = img / 255.0
    assert (0 <= img).all() and (img <= 1.0).all()
    # print(img.shape)
    # we crop image from center
    # short_edge = min(img.shape[:2])
    # yy = int((img.shape[0] - short_edge) / 2)
    # xx = int((img.shape[1] - short_edge) / 2)
    # crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
    # resize to 224, 224
    resized_img = skimage.transform.resize(img, (224, 224), mode="constant")
    # print(resized_img.shape)
    return resized_img


#def logEntry(TMP_STRING):
#    LOG_FILE.write(str(TMP_STRING))
#    LOG_FILE.write("\n")
#    LOG_FILE.flush()
#    print(str(TMP_STRING))

######################## Pipe line  ####################

top_icon2 = np.load("holidays_labelled_style.npy")
top_icon = np.load("holidays_labelled_style.npy")
quary_size = top_icon.shape[0]    #3909
print(quary_size)
quary_image_loc = top_icon[:, 0]   
quary_content = top_icon[:, 1:]   # 3910 x 4096
quary_style = top_icon2[:, 1:]        # 3910 x 4096

# create tf model
for b in range(1,2):
    with tf.device('/cpu:0'):
        tf_quary_style = tf.placeholder("float", [quary_size, 4096])
        tf_quary_content = tf.placeholder("float", [quary_size, 4096])
    
        tf_style = tf.placeholder("float", [batch_size_all, 4096])
        tf_content = tf.placeholder("float", [batch_size_all, 4096])
    
        # cosine distance
        c_D1 = tf.matmul(tf.square(tf_quary_content), tf.ones_like(tf.transpose(tf_content)))
        c_D2 = tf.matmul(tf.ones_like(tf_quary_content), tf.transpose(tf.square(tf_content)))
        c_DD = tf.matmul(tf_quary_content, tf.transpose(tf_content))
        c_L2 = c_D1 + c_D2 - 2 * c_DD
        c_cosine = 1 - c_DD / (tf.sqrt(c_D1 * c_D2))
    
        s_D1 = tf.matmul(tf.square(tf_quary_style), tf.ones_like(tf.transpose(tf_style)))
        s_D2 = tf.matmul(tf.ones_like(tf_quary_style), tf.transpose(tf.square(tf_style)))
        s_DD = tf.matmul(tf_quary_style, tf.transpose(tf_style))
        s_L2 = s_D1 + s_D2 - 2 * s_DD
        s_cosine = 1 - s_DD / (tf.sqrt(s_D1 * s_D2))
    
        cosine = 0*c_cosine + s_cosine
        L2 =  c_L2
    
     
    with tf.Session() as sess:
        # collect quary data
    
        # get closest pairs in all data
        # simialar_style_images = np.ndarray([quary_size, best_simalr, 224, 224, 3])
        simialar_content_images_distance = np.ones([quary_size, best_simalr]) * 1e10
        simialar_content_images_names = np.ndarray([quary_size, best_simalr], dtype='object')
        simialar_content_apk_names = np.ndarray([quary_size, best_simalr], dtype='object')
    
        for big in [1]:
            Big2 = np.load("holidays_style.npy")
            Big = np.load("holidays_style.npy")
            all_image_loc = Big[:, 0]
            all_image_size = Big.shape[0]
            
            start_time = time.time()
            for batch in range(int(all_image_size / batch_size_all)):
                np_images_loc = all_image_loc[batch * batch_size_all: (batch + 1) * batch_size_all]
                np_c = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 1:]
                np_s = Big2[batch * batch_size_all: (batch + 1) * batch_size_all, 1:]
                #logEntry(batch)
                c, l2 = sess.run([ cosine,L2], feed_dict={tf_content: np_c, tf_quary_content: quary_content,tf_style: np_s, tf_quary_style: quary_style})
                # logEntry(simialar_style_images_distance)
                # logEntry(c)
                # logEntry(all_image_names[batch * batch_size_all: (batch + 1) * batch_size_all])
                for i in range(quary_size):
                    if(best_simalr < c.shape[1]):
                        ind_sort = np.argsort(c[i])[0:best_simalr]
                    else:
                        ind_sort = np.argsort(c[i])
                    sorted_dis = c[i][ind_sort]
    
                    j = 0
                    for d in sorted_dis:
                        ind = np.argmax(simialar_content_images_distance[i])
                        id_x = []
                        for x in simialar_content_images_names[i, :]:
                            if(x is not None):
                                id_x.append(x.split("/")[-1])
                        if(simialar_content_images_distance[i][ind] > d and not(np_images_loc[ind_sort][j].split("/")[-1] in id_x)):
                            # simialar_style_images[i, ind] = np_images[ind_sort][j]
                            simialar_content_images_distance[i, ind] = d
                            simialar_content_images_names[i, ind] = np_images_loc[ind_sort][j]
                        j += 1
    
            
        
        main_dir = "./"
        
        np.save(main_dir + "image_loc"+str(b)+".npy", simialar_content_images_names)
        np.save(main_dir + "apk_loc"+str(b)+".npy", simialar_content_apk_names)
        np.save(main_dir + "image_dis"+str(b)+".npy", simialar_content_images_distance)
        np.save(main_dir + "quary"+str(b)+".npy", np.array(quary_image_loc, dtype="object"))
