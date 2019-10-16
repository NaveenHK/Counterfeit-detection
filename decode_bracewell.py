



import numpy as np
import os
import sys
import subprocess
import shutil
import pickle
import csv
def get_adds(i):
    with open('./ad_lib.csv', 'r') as f:
        reader = csv.reader(f)
        a = list(reader)
    
    ad_lib = np.array(a)
    ad_lib_dir = ad_lib[1:][:, 1]
    try:
        app_ad = '/flush2/kar129/apks/'+i +'/smali/'
        #print(i,os.listdir(app_ad))
        ads = os.walk(app_ad)
        
        
        aaa = ["/".join(a.split("/")[5:])  for a,b,c in ads]
        #print(aaa)
        p= (set(aaa)&set(ad_lib_dir))
        return p
    except Exception as e:
        return "-"
s  =  int(sys.argv[1])

# if((s+1)*100>=6290):
#     apps = np.load("/home/jathushan/2018/app_analysis/data/apk_2.npy")[s*100:]    
# else:
#     apps = np.load("/home/jathushan/2018/app_analysis/data/apk_2.npy")[s*100:(s+1)*100]

# print(apps.shape)
# for a in apps:
#     subprocess.call(["java","-jar","apktool_2.3.2.jar","d", a,"-o" , "/srv/jathushan/data/decode/top1000/"+a.split("/")[-1][0:-4]])

a = os.listdir("/pc/")
if((s+1)*5000>=47000):
    apps = a[s*5000:]    
else:
    apps = a[s*5000:(s+1)*5000]
#lis=os.listdir('/flush2/kar129/apks/')
apps = ["/flush2/kar129/pc/"+x for x in apps]
print(apps)
d={}
for a in apps:
    subprocess.call(["java","-jar","apktool_2.3.2.jar","d", a,"-o" , "/flush2/kar129/apks/"+a.split("/")[-1][0:-4]])
    addd=get_adds(a)
    d[a]=addd
    ad_file=open('/flush2/kar129/ads/'+a+'.txt','w')
    ad_file.write(str(addd))
    ad_file.close()
    shutil.rmtree('/flush2/kar129/apks/'+a)
pickle.dump( d, open( "ad_details"+str(s)+".p", "wb" ) )   

        
