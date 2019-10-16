# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 20:15:50 2018

@author: kar129
"""


import numpy as np
import os
from collections import OrderedDict
main_dir = "./"   #Top 5
#main_dir2 = "D:/Internship/Week 5/2018/NHK/Data3/quary_results/"    #Top10
#main_dir3 = "D:/Internship/Week 5/2018/NHK/Data1/quary_results/"      #Top 100
topk=[5,10,15,20]
for b in range(1,2):
    for top in topk:
        sim_loc=np.load(main_dir + "image_loc"+str(b)+".npy")
        #print(sim_loc)
        #sim_loc=np.load(main_dir + "image_loc.npy")
        #app_nam=np.load(main_dir + "apk_loc.npy")
        im_dis=np.load(main_dir + "image_dis"+str(b)+".npy")
        #quary_loc=np.load(main_dir + "quary.npy")
        ##im_dis2=np.load(main_dir2 + "image_dis.npy")
        ##im_dis3=np.load(main_dir3 + "image_dis.npy")
        count=0
        total=0
        #number=0
        for i in range(500):
            #PATH_TO_IMAGES = 'D:/Labelled_Final/'+str(i)+'/'
            #image_paths = os.listdir(PATH_TO_IMAGES)
            
        #    for img in range(len(image_paths)):
        #        if image_paths[img][0:2]=='A_':
        #            image_paths[img]=image_paths[img][2:]
            #print(image_paths)
            
            #dir_size=len(image_paths)
            NN=sim_loc[i]
            dis=im_dis[i]
            dic={}
            for data in range(len(NN)):
                dic[NN[data]]=dis[data]
            d_sorted = OrderedDict(sorted(dic.items(), key=lambda x: x[1]))
            
            if i<10:
                num='00'+str(i)
            elif 10<=i<100:
                num='0'+str(i)
            else:
                num=str(i)
            #count+=dir_size
            #base_image=image_paths[0]
            #print(image_paths)
            n=0
            for im in d_sorted:
                if n<top:
                    if '1'+num in im :
                        total+=1
                    n+=1
        #    for j in range(len(image_paths)):
        #        results=sim_loc[count]
        #        for item in results:
        #            if item in image_paths:
        #                total+=1
                
                #count+=1
            #print(image_paths)
        #print(number)
        #print (total)
        #print(sim_loc.shape[0])
        #print(total_retrieved)
        print ('top-',top,'style- ',str(b), (total/(1491))*100)
            
                
                
        
        
        
        
        
        #quary_size1 = sim_loc[12]
        #if image_paths[0][2:]==quary_size1[3]:
        #    print('YES')
        #quary_size2= np.sort(im_dis2[0])
        #quary_size3= (np.sort(im_dis3[0]))[0:10]
        
        #print(quary_size1)
        #print(quary_size2)
        #print(quary_size3)
        #quary_image_loc = top_icon[:, 0]
        #quary_content = top_icon[:, 2:4098]
        #quary_style = top_icon[:, 4098:]