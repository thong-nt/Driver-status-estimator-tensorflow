import threading
import subprocess

from PIL import Image

from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.render import canvas
from threading import Thread

def input_direction(argument):
    switcher = {
            "M": "Moving",               #Move straight ahead
            "Re": "Reversing",                        #Reversing 
            "L": "Turn Left",                         #Turn Left
            "R": "Turn right",                        #Turn right
    }
    return switcher.get(argument, " ")

class OLED:
    def __init__(self):
       self.status = "None"
       self.serial = i2c(port=1, address=0x3C)
       self.device = sh1106(self.serial)
       self.driver = ""
       self.car = ""
       # self.stopped is initialized to False 
       self.stopped = True
       # thread instantiation  
       self.t = Thread(target=self.display, args=())
       self.t.daemon = True # daemon threads run in background

    def update(self,data,driver,car):
        self.status = data
        self.driver = driver
        self.car = car

    def display(self):
        while True:
            if self.stopped is True :
                break

            cmd = "hostname -I"
            IP = (str(subprocess.check_output(cmd, shell = True)).split(' ')[0]).split(r"'")[1]

            with canvas(self.device) as draw:
                #draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((5, 5), f"IP: {IP}", fill="white")
                draw.text((5, 15), f"Direction: {input_direction(self.status)}", fill="white")
                draw.text((5, 25), f"Driver: {self.driver.split('!')[0]}", fill="white")
                draw.text((5, 35), f"Car: {self.car}", fill="white")

    def start(self):
        self.stopped = False
        self.t.start()
    
    def stop(self):
        self.stopped = True
        self.t.join()


'''
if __name__ == "__main__":
    start()
'''

