# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:42:30 2018

@author: kar129
"""

import pickle
import pandas as pd
import numpy as np
lines = [line.rstrip('\n\t') for line in open('top10100.txt')]
ads=pickle.load(open('ad_vectors.p', "rb" ))
avail=pickle.load(open('availability2.p', "rb" ))
#print(avail)
ads2=pickle.load(open('no_ads.p', "rb" ))
top=pickle.load(open('top10000_threshold_2.92.p', "rb" ))
data= np.empty((20000,11),dtype=object)
#print(ads['com.smartsoftwareltd.templetheftrun'])
#lA={}
#data3=np.empty((13997,3),dtype=object)
def calc(query,ret):
    #print(query[6],ret[9])
    val1=0
    val2=0
    for i in range(124):
        if query[i]==0 and ret[i]==1:
            #print('YES')
            val1+=1
        elif query[i]==1 and ret[i]==0:
            #print('NO')
            val2+=1
    #print(val1,val2)
    return val1-val2
l=[]
dat=np.empty((905,3),dtype=object)
up=0
count2=0
zzz=0
ad_diff=[]
Y=[]
N=[]
T=[]
ll=[]
for i in range(1,16):
    ad_diff.append(i)
for adf in [1]:
    count=0
    yes=[]
    no=[]
    for i in range(10002):
        q=lines[i]
        if q in top:
            data[count,0]=q
            for j in range(len(top[q])):
                data[count,j+1]=top[q][j][:-4]
                
            count+=1
            if q in ads:
                pivot=ads[q]
                data[count,0]=ads2[q]
                for k in range(len(top[q])):
                    aaa=top[q][k][:-4]
                    if aaa in ads:
                        diff=calc(pivot,ads[aaa])
                        if diff>=5:
                            
                            if aaa not in ll:
                                if avail[aaa]=='YES':
                                    dat[up,0]=q
                                    dat[up,1]=aaa
                                    dat[up,2]=diff
                                    up+=1
                                    ll.append(aaa)
                            if avail[aaa]=='YES':
                                if aaa not in yes:
                                    yes.append(aaa)
                            elif avail[aaa]=='NO':
                                if aaa not in no:
                                    no.append(aaa)
                                
                            
                        
                        #data[count,k+1]=diff
#                        if str(diff) not in lA:
#                            lA[str(diff)]=1
#                        else:
#                            lA[str(diff)]+=1
                    else:
                        data[count,k+1]='N/A'
            else:
                pivot=0
                data[count,0]='N/A'
                for k in range(len(top[q])):
                    aaa=top[q][k][:-4]
                    if aaa in ads:
                        data[count,k+1]='N/A'
                    else:
                        data[count,k+1]='N/A'
            count+=1
    Y.append(len(yes))
    N.append(len(no))
    T.append(len(yes)+len(no))
        #print(count)
#print(zzz)
#df=pd.DataFrame(data)
#df.to_csv('ad_details.csv')    
#print(lA)
#def value(lA,k):
#    val=0
#    for i in range(-124,k+1,1):
#        if str(i) not in lA:
#            continue
#        else:
#            val+=lA[str(i)]
#    return val
#        
data2=np.empty((15,4),dtype=object)
data2[:,0]=np.transpose(np.asarray(ad_diff))
data2[:,1]=np.transpose(np.asarray(Y))
data2[:,2]=np.transpose(np.asarray(N))
data2[:,3]=np.transpose(np.asarray(T))
#for i in range(-21,17,1):
#    data2[i+21,0]='<='+str(i)
#    data2[i+21,1]=value(lA,i)
#    
print(len(ll))
#print(tot)
        #print(count)
#print(len(lA))     

df=pd.DataFrame(dat)
df.to_csv('ad_final_list.csv',index=False)
