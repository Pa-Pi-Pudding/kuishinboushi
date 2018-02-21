import grovepi_light_sensor_facedetect
import pasori
import time


ls_class = grovepi_light_sensor_facedetect.LightSensor()
pasori_class = pasori.Felica_reader()
while True:
    ls_class.light_sensor()
    t = pasori_class.reader()
    print(t)
    if t == True:
        time.sleep(6.5)
