# coding:UTF-8
from binascii import hexlify
import sys

sys.path.insert(1, '/home/pi/nfcpy')
import nfc
import cv2, os, argparse, shutil, grovepi,time
import grovepi_light_sensor_facedetect
from timeout_decorator import timeout, TimeoutError

class Felica_reader(object):

    TDU = ["NE", "NC", "NM", "EJ", "EK", "EH", "ES", "EF", "EC", "FI""FA", "FR", "AJ", "AD", "JK", "JKM", "RMU", "RMD","RMB", "RMT", "RMG", "RU", "RD", "RB", "RT", "RG",]
    system_code = 0xFE00
    TIMEOUT_SEC = 5 
    mlist = ["15NC010", "aaaaaaaa"]
    
    def on_connect(self,tag):
        print '\n'.join(tag.dump())
        idm, pmm = tag.polling(pasori_class.system_code)
        tag.idm, tag.pmm, tag.sys = idm, pmm, pasori_class.system_code
        
        sc = nfc.tag.tt3.ServiceCode(106, 0x0b)

      
        student_number_bc = nfc.tag.tt3.BlockCode(0, service=0)
        student_name_bc = nfc.tag.tt3.BlockCode(1, service=0)
    
        data1 = tag.read_without_encryption([sc], [student_number_bc])
        data2 = tag.read_without_encryption([sc], [student_name_bc])
        for i in pasori_class.TDU:
            if (i in data1):
                num_locate = data1.decode('UTF-8').find('00', 9)
                name_locate = (hexlify(data2).find('00', 0)) / 2
            
                num= data1.decode('UTF-8')[2:num_locate]
                name = data2.decode('UTF-8')[0:name_locate]
                print name
                print num    
                if pasori_class.mlist.count(num) <= 1:
                    print("the would!")
                    return 1
                    break;

    @timeout(TIMEOUT_SEC)
    def reader(self):
        try:
            clf =  nfc.ContactlessFrontend('usb')
            result = clf.connect(rdwr={'on-connect': pasori_class.on_connect})
            return result
        except TimeoutError:
            print "timeout-now"
pasori_class = Felica_reader()
