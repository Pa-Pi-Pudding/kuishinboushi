import os
import grovepi
import cv2
import time

camera = cv2.VideoCapture(0)
light_sensor = 0

# Turn on LED once sensor exceeds threshold resistance
threshold = 25

grovepi.pinMode(light_sensor, "INPUT")

while True:
    try:
        sensor_value = grovepi.analogRead(light_sensor)

        resistance = (float)(1023 - sensor_value) * 5 / sensor_value
        if resistance < threshold:
            if os.path.isdir("Image")== False:
                    os.path.makedirs("Image")
            for i in range(5):
                r, img = camera.read()
                time.sleep(0.1)
                path = ("Image")
                photo = 'image%04d.jpg' % i
                cv2.imwrite(os.path.join(path, photo), img)
                       
                print('taked phote')
            
        print("sensor_value = %d resistance = %.2f" %(sensor_value, resistance))
        time.sleep(.5)
        
    except Exception as e:
        print('%r' % e)
    except KeyboardInterrupt:
        print ("Error")
        break;
