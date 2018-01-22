# coding:UTF-8
import cv2, os, argparse, shutil, grovepi, time
from binascii import hexlify
from time import sleep
import sys

from slacker import Slacker
sys.path.insert(1, '/home/pi/nfcpy')
import nfc
import pasori
#import subprocess

FLAGS = None

SAVE_PATH = "./outputs/"

CASCADE = ["default","alt","alt2","tree","profile","nose"]

parser = argparse.ArgumentParser()
    
parser.add_argument(
        "--cascade",
        type=str,
        default="alt",
        choices=CASCADE,
        help="cascade file."
  )
parser.add_argument(
        "--scale",
        type=float,
        default=1.11,
        help="scaleFactor value of detectMultiScale."
  )
parser.add_argument(
        "--neighbors",
        type=int,
        default=2,
        help="minNeighbors value of detectMultiScale."
  )
parser.add_argument(
        "--min",
        type=int,
        default=80,
        help="minSize value of detectMultiScale."
  )
parser.add_argument(
        "--input_dir",
        type=str,
        default="./inputs/",
        help="The path of input directory."
  )
parser.add_argument(
        "--move_dir",
        type=str,
        default="./done/",
        help="The path of moving detected files."
  )

FLAGS, unparsed = parser.parse_known_args() 

if   FLAGS.cascade == CASCADE[0]:#"default":
    cascade_path = "./models/haarcascade_frontalface_default.xml"
    print(CASCADE[0])
elif FLAGS.cascade == CASCADE[1]:#"alt":
    cascade_path = "./models/haarcascade_frontalface_alt.xml"
elif FLAGS.cascade == CASCADE[2]:#"alt2":
    cascade_path = "./models/haarcascade_frontalface_alt2.xml"
elif FLAGS.cascade == CASCADE[3]:#"tree":
    cascade_path = "./models/haarcascade_frontalface_alt_tree.xml"
elif FLAGS.cascade == CASCADE[4]:#"profile":
    cascade_path = "./models/haarcascade_profileface.xml"
elif FLAGS.cascade == CASCADE[5]:#"nose":
    cascade_path = "./models/haarcascade_mcs_nose.xml"

faceCascade = cv2.CascadeClassifier(cascade_path)

files =  os.listdir(FLAGS.input_dir)

if FLAGS.move_dir == "":
    if os.path.exists(SAVE_PATH):
        shutil.rmtree(SAVE_PATH)
    os.mkdir(SAVE_PATH)
    
   
# -------------slacker---------------------   
token = "xoxp-297365796705-297365796865-301035400788-1745f628725456ca54ff66b8b6f9a4fd"
slacker = Slacker(token)
channel_name = "#" + "general"

print(FLAGS)

#顔認証
def cut_image():
    face_detect_count = 0

    face_undetected_count = 0
    for file_name in files:
        try: 
            if os.path.isfile(FLAGS.input_dir + file_name):
        
                img = cv2.imread(FLAGS.input_dir + file_name)
                print("read end")

                if img is None:
                    print(file_name + ':Cannot read image file')
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                face = faceCascade.detectMultiScale(gray, scaleFactor=FLAGS.scale, minNeighbors=FLAGS.neighbors, minSize=(FLAGS.min, FLAGS.min))
                if len(face) > 0:
                    for rect in face:
                        shutil.copy(FLAGS.input_dir + file_name, FLAGS.move_dir)
                        time.sleep(2)
                        print("slack file uprode")
                        print(FLAGS.input_dir + file_name)
                        
                      #  result = slacker.files.upload(FLAGS.input_dir + file_name, channels=['C8RSJLBD2'])
                      #  slacker.pins.add(channel='C8RSJLBD2', file_=result.body['file']['id'])
                else:
                    print(file_name + ':No Face')
                    face_undetected_count = face_undetected_count + 1
                    
        except KeyboardInterrupt:
            print ("Error")
            break;
    print('Undetected Image Files:%d' % face_undetected_count)
    time.sleep(1.5)
    print("------end---------")
    


def taken_photo():
    camera = cv2.VideoCapture(0)
    for i in range(5):
        r, img = camera.read()
        time.sleep(0.5)
        photo = 'image%04d.jpg' % i
        cv2.imwrite(os.path.join(FLAGS.input_dir, photo), img)
                       
        print('taked phote')
        
    camera.release()
    cut_image()
        
def light_sensor():
    light_sensor = 0
    threshold = 1
    grovepi.pinMode(light_sensor, "INPUT")
    #py = subprocess.Popen(['python','pasori.py'])
    while True:
        try:
            sensor_value = grovepi.analogRead(light_sensor)
            resistance = (float)(1023 - sensor_value) * 5 / sensor_value
            time.sleep(.5)
            if resistance < threshold:
                print("sensor_value = %d resistance = %.2f" %(sensor_value, resistance))
                taken_photo() 
        except Exception as e:
            print('%r' % e)
        except KeyboardInterrupt:
            print ("Error")
            break;
        

if __name__ == '__main__':
    light_sensor()