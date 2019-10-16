# #!/usr/bin/env python3

# """ VirusTotal File Scan

#     Required libraries:
#         - requests (can be installed manually or through pip)
# """

# __author__ = "Xiaokui Shu"
# __copyright__ = "Copyright 2013, Xiaokui Shu"
# __license__ = "Apache"
# __version__ = "1.0.0"
# __maintainer__ = "Xiaokui Shu"
# __email__ = "subx@vt.edu"
# __status__ = "Prototype"

# import sys
# import os
# import hashlib
# import argparse
# import logging
# import requests
# import json
# import time
# import numpy as np
# import pickle


# def list_all_files(path):
#     """
#     List all file paths

#     @param path: if it is a path, just return, if dir, return paths of files in it

#     Subdirectories not listed
#     No recursive search
#     """
#     assert os.path.isfile(path) or os.path.isdir(path)

#     if os.path.isfile(path):
#         return [path]
#     else:
#         return filter(os.path.isfile, map(lambda x: '/'.join([os.path.abspath(path), x]), os.listdir(path)))


# def sha256sum(filename):
#     """
#     Efficient sha256 checksum realization

#     Take in 8192 bytes each time
#     The block size of sha256 is 512 bytes
#     """
#     with open(filename, 'rb') as f:
#         m = hashlib.sha256()
#         while True:
#             data = f.read(8192)
#             if not data:
#                 break
#             m.update(data)
#         return m.hexdigest()


# class VirusTotal(object):

#     def __init__(self):
#         self.apikey = ""
#         self.URL_BASE = "https://www.virustotal.com/vtapi/v2/"
#         self.HTTP_OK = 200

#         # whether the API_KEY is a public API. limited to 4 per min if so.
#         self.is_public_api = True
#         # whether a retrieval request is sent recently
#         self.has_sent_retrieve_req = False
#         # if needed (public API), sleep this amount of time between requests
#         self.PUBLIC_API_SLEEP_TIME = 20

#         self.logger = logging.getLogger("virt-log")
#         self.logger.setLevel(logging.INFO)
#         self.scrlog = logging.StreamHandler()
#         self.scrlog.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
#         self.logger.addHandler(self.scrlog)
#         self.is_verboselog = True

#     def send_files(self, filenames):
#         """
#         Send files to scan

#         @param filenames: list of target files
#         """
#         url = self.URL_BASE + "file/scan"
#         attr = {"apikey": self.apikey}

#         for filename in filenames:
#             files = {"file": open(filename, 'rb')}
            
            
#             file_size=os.path.getsize(filename)/1024/1024
#             if(file_size>32):
#                 response = requests.get('https://www.virustotal.com/vtapi/v2/file/scan/upload_url', params=attr)
#                 json_response = response.json()
#                 upload_url = json_response['upload_url']
#                 # files_big = {'file': (filename.decode('utf-8'), open(filename, 'rb'))}
#                 res = requests.post(upload_url,  data=attr,files=files)
#             else:
#                 res = requests.post(url, data=attr, files=files)

#             # if res.status_code == self.HTTP_OK:
#             #     resmap = json.loads(res.text)
#             #     if not self.is_verboselog:
#             #         self.logger.info("sent: %s, HTTP: %d, response_code: %d, scan_id: %s",
#             #                          os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_id"])
#             #     else:
#             #         self.logger.info("sent: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
#             # else:
#             #     self.logger.warning("sent: %s, HTTP: %d", os.path.basename(filename), res.status_code)

#         return res.status_code

#     def retrieve_files_reports(self, filenames):
#         """
#         Retrieve Report for file

#         @param filename: target file
#         """
#         for filename in filenames:
#             res = self.retrieve_report(sha256sum(filename))

#             if res.status_code == self.HTTP_OK:
#                 resmap = json.loads(res.text)
#             #     try:
#             #         print(resmap["positives"], resmap["total"])
#             #     except:
#             #         print("not a report")
#             #     # if not self.is_verboselog:
#             #     #     self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
#             #     #                      os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
#             #     # else:
#             #     #     self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
#             # else:
#             #     self.logger.warning("retrieve report: %s, HTTP: %d", os.path.basename(filename), res.status_code)

#         return(res.status_code, resmap)

#     def retrieve_from_meta(self, filename):
#         """
#         Retrieve Report for checksums in the metafile

#         @param filename: metafile, each line is a checksum, best use sha256
#         """
#         with open(filename) as f:
#             for line in f:
#                 checksum = line.strip()
#                 res = self.retrieve_report(checksum)

#                 if res.status_code == self.HTTP_OK:
#                     resmap = json.loads(res.text)
#                     if not self.is_verboselog:
#                         self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
#                                          checksum, res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
#                     else:
#                         self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
#                 else:
#                     self.logger.warning("retrieve report: %s, HTTP: %d", checksum, res.status_code)

#     def retrieve_report(self, chksum):
#         """
#         Retrieve Report for the file checksum

#         4 retrieval per min if only public API used

#         @param chksum: sha256sum of the target file
#         """
#         if self.has_sent_retrieve_req and self.is_public_api:
#             time.sleep(self.PUBLIC_API_SLEEP_TIME)

#         url = self.URL_BASE + "file/report"
#         params = {"apikey": self.apikey, "resource": chksum}
#         res = requests.post(url, data=params)
#         self.has_sent_retrieve_req = True
#         return res


# if __name__ == "__main__":
#     vt = VirusTotal()
#     # try:
#     #     with open(os.getenv("HOME") + '/.virustotal.api') as keyfile:
#     #         vt.apikey = keyfile.read().strip()
#     # except:
#     #     print('[Error] Please put your VirusTotal API Key in file "$HOME/.virustotal.api"')
#     #     sys.exit()
#     # vt.apikey = "9aa6fd296ab4dec1ded7bf2f64a74b5a9a1e4befe58efb759bb4c8d1334e4d78"
#     vt.apikey = "0d8a7ee919ee20042cc31d7565986da4b995703d4089f2cee967ae10a5462b91"

#     parser = argparse.ArgumentParser(description='Virustotal File Scan')
#     parser.add_argument("-p", "--private", help="the API key belongs to a private API service", action="store_true")
#     parser.add_argument("-v", "--verbose", help="print verbose log (everything in response)", action="store_true")
#     parser.add_argument("-s", "--send", help="send a file or a directory of files to scan", metavar="PATH")
#     parser.add_argument("-r", "--retrieve", help="retrieve reports on a file or a directory of files", metavar="PATH")
#     parser.add_argument("-m", "--retrievefrommeta", help="retrieve reports based on checksums in a metafile (one sha256 checksum for each line)", metavar="METAFILE")
#     parser.add_argument("-l", "--log", help="log actions and responses in file", metavar="LOGFILE")
#     parser.add_argument("-th", "--throshold", help="log actions and responses in file", metavar="LOGFILE")
#     parser.add_argument("-b", "--batch", help="k th batch")
#     args = parser.parse_args()

#     # th = int(args.throshold)
#     if args.log:
#         filelog = logging.FileHandler(args.log)
#         filelog.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S"))
#         vt.logger.addHandler(filelog)

#     if args.private:
#         vt.is_public_api = False

#     if args.verbose:
#         vt.is_verboselog = True

#     # system init end, start to perform operations
#     api_comments = {True: 'Public', False: 'Private'}
#     vt.logger.info("API KEY loaded. %s API used.", api_comments[vt.is_public_api])

#     apk_loc = np.load("data/apk_2.npy")
#     uploaded_loc = np.load("data/uploaded.npy")
    
    
#     # query_loc = np.load("quary.npy")
    
#     # sent_413 = list(np.load("sent_413.npy"))
#     # recived = list(np.load("recived.npy"))
#     malware = 0
    
#     s = int(args.batch)
#     if((s+1)*100>=6290):
#         apk_loc = apk_loc[s*100:]
#     else:
#         apk_loc = apk_loc[s*100:(s+1)*100]
        
#     try:
#         sent = list(np.load("data/sent_"+str(s)+".npy"))
#     except:
#         sent = []
        
#     if args.send:
#         # vt.send_files(list_all_files(args.send))
#         c = 0
#         for q in apk_loc:
#             apk = q
#             if(not(apk in sent) ):
#                 try:
#                     code = vt.send_files([apk])
#                     print(str(s)+"\t"+str(code) + "\t" + str(c))
#                     if(code == 200):
#                         sent.append(apk)
#                         np.save("data/sent_"+str(s)+".npy", np.array(sent))
#                     if(code == 413):
#                         print(str(c)+"\t"+apk)
                        
#                         # sent_413.append(apk)
#                         # os.system("cp " + apk + " to_send/" + apk.split("/")[-1])
                    
#                     # np.save("sent_413.npy", np.array(sent_413))
#                 except Exception as e:
#                     # os.system("cp " + apk + " to_send/" + apk.split("/")[-1])

#                     print(str(s)+"\t"+"error occured")
#                     print(e)
            
#             else:
#                 # print(str(s)+"\t"+"already sent   =>" + apk)
#                 pass
#             c += 1

#     if args.retrieve:
#         x = 0
#         q_count = 0
#         for q in uploaded_loc:
#             # quary = query_loc[q_count]

#             apk =q

#             aa = apk.split("/")[-1][:-4] + ".pickle"
#             try:

#                 if(not(aa in os.listdir("reports/"))):
#                     print(apk)
#                     code, resmap = vt.retrieve_files_reports([apk])
#                     print(code)
#                     if(code == 200):
#                         print(resmap)
#                         print(resmap["positives"], resmap["total"])
#                         # recived.append(apk)

#                         if(resmap["positives"] >= 3):
#                             malware += 1
#                         with open("reports/" + aa, 'wb') as f:
#                             pickle.dump(resmap, f, protocol=pickle.HIGHEST_PROTOCOL)
#                             print("DUMPED" + "     " + "reports/" + aa)
#                         # np.save("recived.npy", np.array(recived, dtype="object"))
#                 else:
#                     with open("reports/" + aa, 'rb') as f:
#                         resmap = pickle.load(f)
#                     x += 1
#                     if(resmap["positives"] >= 3):
#                         malware += 1
#             except:
#                 print("pass")
#                 # os.system("cp " + apk + " to_recive/" + apk.split("/")[-1])
#         # print("total malware = ", str(malware))
#         q_count += 1
#         # vt.retrieve_files_reports(apk_loc)
#         # vt.retrieve_files_reports(list_all_files(args.retrieve))
#         print(malware)
#         print(x)
#     if args.retrievefrommeta:
#         vt.retrieve_from_meta(args.retrievefrommeta)
































#!/usr/bin/env python3

""" VirusTotal File Scan

    Required libraries:
        - requests (can be installed manually or through pip)
"""

__author__ = "Xiaokui Shu"
__copyright__ = "Copyright 2013, Xiaokui Shu"
__license__ = "Apache"
__version__ = "1.0.0"
__maintainer__ = "Xiaokui Shu"
__email__ = "subx@vt.edu"
__status__ = "Prototype"

import sys
import os
import hashlib
import argparse
import logging
import requests
import json
import time
import numpy as np
import pickle


def list_all_files(path):
    """
    List all file paths

    @param path: if it is a path, just return, if dir, return paths of files in it

    Subdirectories not listed
    No recursive search
    """
    assert os.path.isfile(path) or os.path.isdir(path)

    if os.path.isfile(path):
        return [path]
    else:
        return filter(os.path.isfile, map(lambda x: '/'.join([os.path.abspath(path), x]), os.listdir(path)))


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


class VirusTotal(object):

    def __init__(self):
        self.apikey = ""
        self.URL_BASE = "https://www.virustotal.com/vtapi/v2/"
        self.HTTP_OK = 200

        # whether the API_KEY is a public API. limited to 4 per min if so.
        self.is_public_api = True
        # whether a retrieval request is sent recently
        self.has_sent_retrieve_req = False
        # if needed (public API), sleep this amount of time between requests
        self.PUBLIC_API_SLEEP_TIME = 20

        self.logger = logging.getLogger("virt-log")
        self.logger.setLevel(logging.INFO)
        self.scrlog = logging.StreamHandler()
        self.scrlog.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(self.scrlog)
        self.is_verboselog = True

    def send_files(self, filenames):
        """
        Send files to scan

        @param filenames: list of target files
        """
        url = self.URL_BASE + "file/scan"
        attr = {"apikey": self.apikey}

        for filename in filenames:
            files = {"file": open(filename, 'rb')}
            
            
            file_size=os.path.getsize(filename)/1024/1024
            if(file_size>32):
                response = requests.get('https://www.virustotal.com/vtapi/v2/file/scan/upload_url', params=attr)
                json_response = response.json()
                upload_url = json_response['upload_url']
                # files_big = {'file': (filename.decode('utf-8'), open(filename, 'rb'))}
                res = requests.post(upload_url,  data=attr,files=files)
            else:
                res = requests.post(url, data=attr, files=files)

            # if res.status_code == self.HTTP_OK:
            #     resmap = json.loads(res.text)
            #     if not self.is_verboselog:
            #         self.logger.info("sent: %s, HTTP: %d, response_code: %d, scan_id: %s",
            #                          os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_id"])
            #     else:
            #         self.logger.info("sent: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
            # else:
            #     self.logger.warning("sent: %s, HTTP: %d", os.path.basename(filename), res.status_code)

        return res.status_code

    def retrieve_files_reports(self, filenames):
        """
        Retrieve Report for file

        @param filename: target file
        """
        for filename in filenames:
            res = self.retrieve_report(sha256sum(filename))

            if res.status_code == self.HTTP_OK:
                resmap = json.loads(res.text)
            #     try:
            #         print(resmap["positives"], resmap["total"])
            #     except:
            #         print("not a report")
            #     # if not self.is_verboselog:
            #     #     self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
            #     #                      os.path.basename(filename), res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
            #     # else:
            #     #     self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
            # else:
            #     self.logger.warning("retrieve report: %s, HTTP: %d", os.path.basename(filename), res.status_code)

        return(res.status_code, resmap)

    def retrieve_from_meta(self, filename):
        """
        Retrieve Report for checksums in the metafile

        @param filename: metafile, each line is a checksum, best use sha256
        """
        with open(filename) as f:
            for line in f:
                checksum = line.strip()
                res = self.retrieve_report(checksum)

                if res.status_code == self.HTTP_OK:
                    resmap = json.loads(res.text)
                    if not self.is_verboselog:
                        self.logger.info("retrieve report: %s, HTTP: %d, response_code: %d, scan_date: %s, positives/total: %d/%d",
                                         checksum, res.status_code, resmap["response_code"], resmap["scan_date"], resmap["positives"], resmap["total"])
                    else:
                        self.logger.info("retrieve report: %s, HTTP: %d, content: %s", os.path.basename(filename), res.status_code, res.text)
                else:
                    self.logger.warning("retrieve report: %s, HTTP: %d", checksum, res.status_code)

    def retrieve_report(self, chksum):
        """
        Retrieve Report for the file checksum

        4 retrieval per min if only public API used

        @param chksum: sha256sum of the target file
        """
        if self.has_sent_retrieve_req and self.is_public_api:
            time.sleep(self.PUBLIC_API_SLEEP_TIME)

        url = self.URL_BASE + "file/report"
        params = {"apikey": self.apikey, "resource": chksum}
        res = requests.post(url, data=params)
        self.has_sent_retrieve_req = True
        return res


if __name__ == "__main__":
    vt = VirusTotal()
    # try:
    #     with open(os.getenv("HOME") + '/.virustotal.api') as keyfile:
    #         vt.apikey = keyfile.read().strip()
    # except:
    #     print('[Error] Please put your VirusTotal API Key in file "$HOME/.virustotal.api"')
    #     sys.exit()
    # vt.apikey = "9aa6fd296ab4dec1ded7bf2f64a74b5a9a1e4befe58efb759bb4c8d1334e4d78"
    vt.apikey = "0d8a7ee919ee20042cc31d7565986da4b995703d4089f2cee967ae10a5462b91"

    parser = argparse.ArgumentParser(description='Virustotal File Scan')
    parser.add_argument("-p", "--private", help="the API key belongs to a private API service", action="store_true")
    parser.add_argument("-v", "--verbose", help="print verbose log (everything in response)", action="store_true")
    parser.add_argument("-s", "--send", help="send a file or a directory of files to scan", metavar="PATH")
    parser.add_argument("-r", "--retrieve", help="retrieve reports on a file or a directory of files", metavar="PATH")
    parser.add_argument("-m", "--retrievefrommeta", help="retrieve reports based on checksums in a metafile (one sha256 checksum for each line)", metavar="METAFILE")
    parser.add_argument("-l", "--log", help="log actions and responses in file", metavar="LOGFILE")
    parser.add_argument("-th", "--throshold", help="log actions and responses in file", metavar="LOGFILE")
    parser.add_argument("-b", "--batch", help="k th batch")
    args = parser.parse_args()

    # th = int(args.throshold)
    if args.log:
        filelog = logging.FileHandler(args.log)
        filelog.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s] %(message)s", datefmt="%m/%d/%Y %I:%M:%S"))
        vt.logger.addHandler(filelog)

    if args.private:
        vt.is_public_api = False

    if args.verbose:
        vt.is_verboselog = True

    # system init end, start to perform operations
    api_comments = {True: 'Public', False: 'Private'}
    vt.logger.info("API KEY loaded. %s API used.", api_comments[vt.is_public_api])


    
    # query_loc = np.load("quary.npy")
    
    # sent_413 = list(np.load("sent_413.npy"))
    # recived = list(np.load("recived.npy"))
    malware = 0
    
    apk_loc = os.listdir("./apks/missing/")
    s = int(args.batch)
    if((s+1)*4>=38):
        apk_loc = apk_loc[s*4:]
    else:
        apk_loc = apk_loc[s*4:(s+1)*4]  
    try:
        sent = list(np.load("data/sss_"+str(s)+".npy"))
    except:
        sent = []
      
    if args.send:
        # vt.send_files(list_all_files(args.send))
        c = 0
        for q in apk_loc:
            apk = "./apks/missing/" + q
            if(not(apk in sent) ):
                try:
                    code = vt.send_files([apk])
                    print(str(code) + "\t" + str(c))
                    if(code == 200):
                        sent.append(apk)
                        np.save("data/sss_"+str(s)+".npy", np.array(sent))
                    if(code == 413):
                        print(str(c)+"\t"+apk)
                        
                        # sent_413.append(apk)
                        # os.system("cp " + apk + " to_send/" + apk.split("/")[-1])
                    
                    # np.save("sent_413.npy", np.array(sent_413))
                except Exception as e:
                    # os.system("cp " + apk + " to_send/" + apk.split("/")[-1])

                    print(str(s)+"\t"+"error occured")
                    print(e)
            
            else:
                # print(str(s)+"\t"+"already sent   =>" + apk)
                pass
            c += 1
    
    if args.retrieve:
        x = 0
        q_count = 0
        for q in apk_loc:
            # quary = query_loc[q_count]

            apk = "./apks/missing/" + q

            aa = apk.split("/")[-1][:-4] + ".pickle"
            try:

                if(not(aa in os.listdir("missing/"))):
                    print(apk)
                    code, resmap = vt.retrieve_files_reports([apk])
                    print(code)
                    if(code == 200):
                        #print(resmap)
                        #print(resmap["positives"], resmap["total"])
                        # recived.append(apk)

                        if(resmap["positives"] >= 3):
                            malware += 1
                        with open("missing/" + aa, 'wb') as f:
                            pickle.dump(resmap, f, protocol=pickle.HIGHEST_PROTOCOL)
                            print("DUMPED" + "     " + "reports/" + aa)
                        # np.save("recived.npy", np.array(recived, dtype="object"))
                else:
                    with open("missing/" + aa, 'rb') as f:
                        resmap = pickle.load(f)
                    x += 1
                    if(resmap["positives"] >= 3):
                        malware += 1
            except:
                print("pass")
                # os.system("cp " + apk + " to_recive/" + apk.split("/")[-1])
        # print("total malware = ", str(malware))
        q_count += 1
        # vt.retrieve_files_reports(apk_loc)
        # vt.retrieve_files_reports(list_all_files(args.retrieve))
        print(malware)
        print(x)
    if args.retrievefrommeta:
        vt.retrieve_from_meta(args.retrievefrommeta)
