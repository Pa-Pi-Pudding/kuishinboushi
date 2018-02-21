# coding:UTF-8
import sys
import cv2, os, argparse, shutil, grovepi,time
from binascii import hexlify
from slacker import Slacker

class LightSensor(object):

    FLAGS = None
    
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
                "--outputs_dir",
                type=str,
                default="./outputs/",
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
    
    
    if FLAGS.input_dir == "":
        if os.path.exists(FLAGS.input_dir):
            shutil.rmtree(FlAGS.input_dir)
        os.mkdir(FLAGS.input_dir)
    
    if FLAGS.outputs_dir == "":
        if os.path.exists(FLAGS.outputs_dir):
            shutil.rmtree(FlAGS_outputs_dir)
        os.mkdir(FLAGS.outputs_dir)

    files =  os.listdir(FLAGS.input_dir)
    # -------------slacker---------------------   
    token = "####-#############-#####################-#########################"
    slacker = Slacker(token)
    channel_name = "#" + "general"
    
    print(FLAGS)
    
    
    def cut_image(self):
        face_detect_count = 0
    
        face_undetected_count = 0
        for file_name in ls_class.files:
            try: 
                if os.path.isfile(ls_class.FLAGS.input_dir + file_name):
            
                    img = cv2.imread(ls_class.FLAGS.input_dir + file_name)
                    print("read end")
    
                    if img is None:
                        print(file_name + ':Cannot read image file')
                        continue
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
                    face = ls_class.faceCascade.detectMultiScale(gray, scaleFactor=ls_class.FLAGS.scale, minNeighbors=ls_class.FLAGS.neighbors, minSize=(ls_class.FLAGS.min, ls_class.FLAGS.min))
                    if len(face) > 0:
                        for rect in face:
                            shutil.copy(ls_class.FLAGS.input_dir + file_name, ls_class.FLAGS.outputs_dir)
                            time.sleep(2)
                            print("slack file uplode")
                            print(ls_class.FLAGS.input_dir + file_name)
                            
                            result = slacker.files.upload(ls_class.FLAGS.outputs_dir + file_name, channels=['C8RSJLBD2'])
                            slacker.pins.add(channel='C8RSJLBD2', file_=result.body['file']['id'])
                    else:
                        print(file_name + ':No Face')
                        face_undetected_count = face_undetected_count + 1
                        
            except KeyboardInterrupt:
                print ("Error")
             #   break;
        print('Undetected Image Files:%d' % face_undetected_count)
        time.sleep(1.5)
        print("------end---------")
        
    
    def taken_photo(self):
        camera = cv2.VideoCapture(0)
        for i in range(5):
            r, img = camera.read()
            time.sleep(0.5)
            photo = 'image%04d.jpg' % i
            cv2.imwrite(os.path.join(ls_class.FLAGS.input_dir, photo), img)
                           
            print('taked phote')
            
        camera.release()
        ls_class.cut_image()
    def light_sensor(self):
        light_sensor = 0
        
        threshold = 10
        grovepi.pinMode(light_sensor,"INPUT")
        for i in range(5):
            try:
           # Get sensor value
               sensor_value = grovepi.analogRead(light_sensor)
               resistance = (float)(1023 - sensor_value) * 10 / sensor_value
               if resistance < threshold:
                   print("light on")
                   ls_class.taken_photo()
               else:
                   print("light off")
                   print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
                   time.sleep(.2)
            except IOError:
                print ("Error")
            except Exception as e:
                print('%r' % e)
            except KeyboardInterrupt:
                print ("Error")
                break;
ls_class = LightSensor()
