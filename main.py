#主程序 ver1 3/8 14:05
import scanner as scan
import RecogniseBarcode as reco
import cv2
import numpy as np
import zlib
import time
import win32com.client
import os
import OCR
import os
import json
import shutil

def copy_file(source, destination):
    try:
        shutil.copy(source, destination)
        print("文件复制成功！")
    except FileNotFoundError:
        print("文件不存在！")
jsonstr = ""
with open("lang/English.lang") as file:
    jsonstr = file.read()
lang = json.loads(jsonstr)
while True:
    print(lang["Welcome"])
    aa = input('>')
    if aa == 'q':
        os._exit(0)
    if aa == '1':
        TID = OCR.scanOcr()
        copy_file("scanned.jpg","D:\WINHWFile\{}.jpg".format(TID))
        print("SCAN OK.TID:{}".format(TID))
        time.sleep(2)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

