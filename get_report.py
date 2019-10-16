from __future__ import print_function
import json
import hashlib
from virus_total_apis import PrivateApi as VirusTotalPrivateApi
import numpy as np
import os
import pickle
import sys


def sha256sum(filename):
    """
    Efficient sha256 checksum realization

    Take in 8192 bytes each time
    The block size of sha256 is 512 bytes
    """
    with open(filename, 'rb') as f:
        m = hashlib.sha256()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
    
API_KEY = '0d8a7ee919ee20042cc31d7565986da4b995703d4089f2cee967ae10a5462b91'

file = "/srv/jathushan/data/apk/top1000/upload_manual/za.co.vodacom.android.app.apk"
EICAR_MD5 = "671793b66a4d6130e22c9fd101b122ea2b55ecb423bf061ddc91e65be51ffc0d"

vt = VirusTotalPrivateApi(API_KEY)

response = vt.get_file_report(EICAR_MD5)
# print(json.dumps(response, sort_keys=False, indent=4))



s = int(sys.argv[1])
# aa = np.load("/home/jathushan/2018/app_analysis/data/uploaded.npy")
# c = 0


aa = os.listdir("/srv/jathushan/data/apk/top1000/main/top1000/") 
c = 0 

if ((s+1)*100>950):
    aa = aa[s*100:-1]
else:
    aa = aa[s*100:(s+1)*100]
    
    
for i in aa:
    j = "/srv/jathushan/data/apk/top1000/main/top1000/"+i
    file = i.split("/")[-1][0:-4]+".pickle"
    if(file not in os.listdir("report2_main/")):
        sha = sha256sum(j)
        response = vt.get_file_report(sha)
        if(response["response_code"]==200):
            if(response["results"]["response_code"]==1):
                res = json.dumps(response, sort_keys=False, indent=4)
                with open("report2_main/" + file, 'wb') as f:
                    pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)
                print("dumped",c)
            else:
                print("waiting in queue",i)
        else:
            print(response["response_code"],i)
    c +=1
    
    
    
    
    
    
    