import os.path
from PIL import Image

from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.render import canvas

class OLED:
    def __init__(self):
       self.status = "None"
       # self.stopped is initialized to False 
       self.stopped = True
       # thread instantiation  
       self.t = Thread(target=self.display, args=())
       self.t.daemon = True # daemon threads run in background

    def display(self):
        while True:
            with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((30, 40), "Hello World", fill="white")

    def start(self):
        try:
            serial = i2c(port=1, address=0x3C)
            device = sh1106(serial)
            display()
        except KeyboardInterrupt:
            pass

'''
if __name__ == "__main__":
    start()
'''