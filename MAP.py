# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 11:01:35 2018

@author: kar129
"""

import numpy as np
import os
from collections import OrderedDict

main_dir = "D:/Internship/Week 5 - KNN search/2018/NHK/VGG19_4_3/style/l2/Data4/quary_results/" 

sim_loc=np.load(main_dir + "image_loc.npy")

im_dis=np.load(main_dir + "image_dis.npy")

count=0
AP=0

for i in range(806):
    common_im=0
    total_im=0
    precision=0
    PATH_TO_IMAGES = 'D:/Labelled_Final/'+str(i)+'/'
    image_paths = os.listdir(PATH_TO_IMAGES)
    
    for img in range(len(image_paths)):
        if image_paths[img][0:2]=='A_':
            image_paths[img]=image_paths[img][2:]
    

    dir_size=len(image_paths)
    NN=sim_loc[count]
    Dis=im_dis[count]
    dic={}
    for data in range(len(NN)):
        dic[NN[data]]=Dis[data]
    d_sorted = OrderedDict(sorted(dic.items(), key=lambda x: x[1]))
    #print(d_sorted)
    count+=dir_size
    
    for im in d_sorted:
    
        if im in image_paths:
            common_im+=1
            total_im+=1
            precision+=(common_im/total_im)
        else:
            total_im+=1
            

        #print(common_im,total_im)
        #print(precision)
    #print(total_im)
    if common_im!=0:
        AP+=(precision/common_im)
    
MAP=(AP/806)*100
print(MAP)
            
        