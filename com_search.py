# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:21:13 2018

@author: kar129
"""




import pickle
import os
import numpy as np
import tensorflow as tf
import time

from collections import OrderedDict
developer=pickle.load(open('developers.p',"rb"))

def topk(loc,dis,quary,b,z):
    sim_loc=np.load(loc)
    im_dis=np.load(dis)
    quary_loc=np.load(quary)
    top_k=[5,10,15,20]
    
    
    for top in top_k:
        count=0
        total=0
        
        for i in range(806):
            PATH_TO_IMAGES = './Labelled_Final/'+str(i)+'/'
            image_paths = os.listdir(PATH_TO_IMAGES)
            
            for img in range(len(image_paths)):
                if image_paths[img][0:2]=='A_':
                    image_paths[img]=image_paths[img][2:]
            #print(image_paths)
            
            dir_size=len(image_paths)
            NN=sim_loc[count]
            dis=im_dis[count]
            quary=quary_loc[count]
            if quary[0:2]=='A_':
                quary=quary[2:]
            dic={}
            for data in range(len(NN)):
                dic[NN[data]]=dis[data]
            d_sorted = OrderedDict(sorted(dic.items(), key=lambda x: x[1]))
            #print(d_sorted)
            
            num=0
            for im in d_sorted:
                if im[0:2]=='A_':
                    im=im[2:]
                if num<top:
                    if im in image_paths:
                        total+=1
                        num+=1                    
                        continue
                    if im[:-4] in developer:                    
                        if developer[quary[:-4]]==developer[im[:-4]]:                        
                            continue
                        else:
                            num+=1
                else:
                    if num!=top:
                        print('error')
                    break
                
                    
                
                
                
               
            count+=dir_size
        #    for j in range(len(image_paths)):
        #        results=sim_loc[count]
        #        for item in results:
        #            if item in image_paths:
        #                total+=1
                
                #count+=1
            #print(image_paths)
        #print(number)
        
        #print (total)
        #print(total_retrieved)
        RR=(total/(sim_loc.shape[0]))*100
        print ("top_",str(top),"style-", b,"text-", z,"Retieval Rate-", RR)

    
    return None

# parameters
bool_PCA = True
batch_size_all = 3539
batch_size_quary = 1
best_simalr_list = [50]
#test_case = str(sys.argv[1])
main_dir = "./results/"

top_icon = np.load("resnet_style_5c_labelled_data.npy")
quary_size = top_icon.shape[0]
print(quary_size)
quary_image_loc = top_icon[:, 0]
quary_content = top_icon[:, 1:4097]
#quary_style = top_icon[:, 4097:8193]
#quary_text =  top_icon[:, 8193:]

for z in range(0,1):
    for b in range(1,2):
        for best_simalr in best_simalr_list:
            # create tf model
            with tf.device('/cpu:0'):
                #tf_quary_style = tf.placeholder("float", [quary_size, 4096])
                tf_quary_content = tf.placeholder("float", [quary_size, 4096])
                #tf_quary_text = tf.placeholder("float", [quary_size, 100])
            
                #tf_style = tf.placeholder("float", [batch_size_all, 4096])
                tf_content = tf.placeholder("float", [batch_size_all, 4096])
                #tf_text = tf.placeholder("float", [batch_size_all, 100])
                # cosine distance
                c_D1 = tf.matmul(tf.square(tf_quary_content), tf.ones_like(tf.transpose(tf_content)))
                c_D2 = tf.matmul(tf.ones_like(tf_quary_content), tf.transpose(tf.square(tf_content)))
                c_DD = tf.matmul(tf_quary_content, tf.transpose(tf_content))
                c_L2 = c_D1 + c_D2 - 2 * c_DD
                c_cosine = 1 - c_DD / (tf.sqrt(c_D1 * c_D2))
            
#                s_D1 = tf.matmul(tf.square(tf_quary_style), tf.ones_like(tf.transpose(tf_style)))
#                s_D2 = tf.matmul(tf.ones_like(tf_quary_style), tf.transpose(tf.square(tf_style)))
#                s_DD = tf.matmul(tf_quary_style, tf.transpose(tf_style))
#                s_L2 = s_D1 + s_D2 - 2 * s_DD
#                s_cosine = 1 - s_DD / (tf.sqrt(s_D1 * s_D2))
#                
#                t_D1 = tf.matmul(tf.square(tf_quary_text), tf.ones_like(tf.transpose(tf_text)))
#                t_D2 = tf.matmul(tf.ones_like(tf_quary_text), tf.transpose(tf.square(tf_text)))
#                t_DD = tf.matmul(tf_quary_text, tf.transpose(tf_text))
#                t_L2 = t_D1 + t_D2 - 2 * t_DD
#                t_cosine = 1 - t_DD / (tf.sqrt(t_D1 * t_D2))
#            
                cosine = c_cosine  #+ b*s_cosine + z*t_cosine
                L2 = c_L2
                
            
             
            with tf.Session() as sess:
                # collect quary data
            
                # get closest pairs in all data
                # simialar_style_images = np.ndarray([quary_size, best_simalr, 224, 224, 3])
                simialar_style_images_distance = np.ones([quary_size, best_simalr]) * 1e10
                simialar_style_images_names = np.ndarray([quary_size, best_simalr], dtype='object')
                simialar_style_apk_names = np.ndarray([quary_size, best_simalr], dtype='object')
            
                for big in range(1,2):
                    Big = np.load("resnet_style_5c_labelled_data.npy")
                    
                    all_image_loc = Big[:, 0]
                    all_image_size = Big.shape[0]
                    start_time = time.time()
                    for batch in range(int(all_image_size / batch_size_all)):
                        np_images_loc = all_image_loc[batch * batch_size_all: (batch + 1) * batch_size_all]
                        np_c = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 1:4097]
                        #np_s = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 4097:8193]
                        #np_t = Big[batch * batch_size_all: (batch + 1) * batch_size_all, 8193:]
                        
                        #logEntry(batch)
                        c,l2 = sess.run([ cosine,L2], feed_dict={ tf_content: np_c, tf_quary_content: quary_content})
                        
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
                dis=main_dir + "image_dis_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy"
                quary=main_dir + "quary_"+str(best_simalr)+'_'+str(b)+'_'+str(z)+".npy"
                topk(loc,dis,quary,b,z)
                


