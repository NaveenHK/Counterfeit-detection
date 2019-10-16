# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:36:34 2018

@author: kar129
"""




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

def top_k(loc,b,z,topk):
    sim_loc=np.load(loc)
    count=0
    total=0
    #number=0
    for i in range(806):
        PATH_TO_IMAGES = 'D:/Labelled_Final/'+str(i)+'/'
        image_paths = os.listdir(PATH_TO_IMAGES)
        
        for img in range(len(image_paths)):
            if image_paths[img][0:2]=='A_':
                image_paths[img]=image_paths[img][2:]
        #print(image_paths)
        
        dir_size=len(image_paths)
        NN=sim_loc[count]
        
        count+=dir_size
        #base_image=image_paths[0]
        #print(image_paths)
        for im in NN:
            if im in image_paths:
                total+=1
    #    for j in range(len(image_paths)):
    #        results=sim_loc[count]
    #        for item in results:
    #            if item in image_paths:
    #                total+=1
            
            #count+=1
        #print(image_paths)
    RR=(total/(sim_loc.shape[0]))*100
    #print(number)
    #print (total)
    #print(total_retrieved)
    print ("top-",topk,"style-", b,"text-", z,"Retieval Rate-", RR)
    return None

# parameters
bool_PCA = True
batch_size_all = 20000
batch_size_quary = 1
best_simalr_list = [50]
#test_case = str(sys.argv[1])
main_dir = "D:/Results/data/cosine/"

top_icon = np.load("D:/Combined/combined_labelled.npy")
quary_size = top_icon.shape[0]
print(quary_size)
quary_image_loc = top_icon[:, 0]
quary_content = top_icon[:, 1:4097]
quary_style = top_icon[:, 4097:8193]
quary_text =  top_icon[:, 8193:]

for z in range(0,11):
    for b in range(1,11):
        for best_simalr in best_simalr_list:
            # create tf model
            with tf.device('/gpu'):
                tf_quary_style = tf.placeholder("float", [quary_size, 4096])
                tf_quary_content = tf.placeholder("float", [quary_size, 4096])
                tf_quary_text = tf.placeholder("float", [quary_size, 100])
            
                tf_style = tf.placeholder("float", [batch_size_all, 4096])
                tf_content = tf.placeholder("float", [batch_size_all, 4096])
                tf_text = tf.placeholder("float", [batch_size_all, 100])
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
                
                t_D1 = tf.matmul(tf.square(tf_quary_text), tf.ones_like(tf.transpose(tf_text)))
                t_D2 = tf.matmul(tf.ones_like(tf_quary_text), tf.transpose(tf.square(tf_text)))
                t_DD = tf.matmul(tf_quary_text, tf.transpose(tf_text))
                t_L2 = t_D1 + t_D2 - 2 * t_DD
                t_cosine = 1 - t_DD / (tf.sqrt(t_D1 * t_D2))
            
                cosine = c_cosine  + b*s_cosine + z*t_cosine
                L2 = s_L2 *b+ c_L2  + z*t_L2
                
            
             
            with tf.Session() as sess:
                # collect quary data
            
                # get closest pairs in all data
                # simialar_style_images = np.ndarray([quary_size, best_simalr, 224, 224, 3])
                simialar_style_images_distance = np.ones([quary_size, best_simalr]) * 1e10
                simialar_style_images_names = np.ndarray([quary_size, best_simalr], dtype='object')
                simialar_style_apk_names = np.ndarray([quary_size, best_simalr], dtype='object')
            
                for big in range(1,23):
                    Big = np.load("D:/Combined/embeddings_" + str(big) + ".npy")
                    
                    all_image_loc = Big[:, 0]
                    all_image_size = Big.shape[0]
                    start_time = time.time()
                    for batch in range(int(all_image_size / batch_size_all)):
                        np_images_loc = all_image_loc[batch * batch_size_all: (batch + 1) * batch_size_all]
                        np_c = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 1:4097]
                        np_s = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 4097:8193]
                        np_t = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 8193:]
                        
                        #logEntry(batch)
                        c,l2 = sess.run([ cosine,L2], feed_dict={tf_style: np_s, tf_content: np_c, tf_text: np_t, tf_quary_content: quary_content, tf_quary_style: quary_style, tf_quary_text:quary_text})
                        
                        for i in range(quary_size):
                            if(best_simalr < c.shape[1]):
                                ind_sort = np.argsort(c[i])[0:best_simalr]
                            else:
                                ind_sort = np.argsort(c[i])
                            sorted_dis = c[i][ind_sort]
            
                            j = 0
                            for d in sorted_dis:
                                ind = np.argmax(simialar_style_images_distance[i])
                                id_x = []
                                for x in simialar_style_images_names[i, :]:
                                    if(x is not None):
                                        id_x.append(x.split("/")[-1])
                                if(simialar_style_images_distance[i][ind] > d and not(np_images_loc[ind_sort][j].split("/")[-1] in id_x)):
                                    # simialar_style_images[i, ind] = np_images[ind_sort][j]
                                    simialar_style_images_distance[i, ind] = d
                                    simialar_style_images_names[i, ind] = np_images_loc[ind_sort][j]
                                j += 1
            
                        
                
                
               
                np.save(main_dir + "image_loc_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy", simialar_style_images_names)
                #np.save(main_dir + "apk_loc.npy", simialar_style_apk_names)
                np.save(main_dir + "image_dis_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy", simialar_style_images_distance)
                np.save(main_dir + "quary_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy", np.array(quary_image_loc, dtype="object"))
                loc=main_dir + "image_loc_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy"
                top_k(loc,b,z,best_simalr)
                
