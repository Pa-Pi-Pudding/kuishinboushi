# coding:UTF-8
from binascii import hexlify
from time import sleep
import sys


sys.path.insert(1, '/home/pi/nfcpy')
import nfc
import cv2, os, argparse, shutil, grovepi
#import grovepi_light_sensor_facedetect

TDU = ["NE", "NC", "NM", "EJ", "EK", "EH", "ES", "EF", "EC", "FI""FA", "FR", "AJ", "AD", "JK", "JKM", "RMU", "RMD",
       "RMB", "RMT", "RMG", "RU", "RD", "RB", "RT", "RG"]
system_code = 0xFE00

#データベースなどを使う予定    
list ={
    "mogemoge":"hoge hoge",
    "mogemoge":"aaaaaa",
    }
mlist = ["15NC010", "15NC012"]

def on_connect(tag):
    
    print '\n'.join(tag.dump())

    idm, pmm = tag.polling(system_code)
    tag.idm, tag.pmm, tag.sys = idm, pmm, system_code
    
    
    sc = nfc.tag.tt3.ServiceCode(106, 0x0b)
  
    student_number_bc = nfc.tag.tt3.BlockCode(0, service=0)
    student_name_bc = nfc.tag.tt3.BlockCode(1, service=0)

    data1 = tag.read_without_encryption([sc], [student_number_bc])
    data2 = tag.read_without_encryption([sc], [student_name_bc])
    
    comparison(data1, data2)

    
def comparison(data1, data2):
    for i in TDU:
        if (i in data1):
            num_locate = data1.decode('UTF-8').find('00', 9)
            name_locate = (hexlify(data2).find('00', 0)) / 2
        
            num= data1.decode('UTF-8')[2:num_locate]
            name = data2.decode('UTF-8')[0:name_locate]
            
            if mlist.count(num) <= 1:
                print("学生です")
      #      print name
        #    print num    thread_1 = threading.Thread(target = main)
            
def main():
        try:
            with nfc.ContactlessFrontend('usb') as clf:
                clf.connect(rdwr={'on-connect': on_connect})
        except:
            print "end"
            sleep(1.5)

               
if __name__ == '__main__':
    main()
   
    
