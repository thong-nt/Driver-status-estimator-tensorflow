import threading

from gpiozero import Buzzer
from time import sleep
from threading import Thread # library for multi-threading

buzzer = Buzzer(26)

class Warning:
   def __init__(self):
       self.status = "None"
       # self.stopped is initialized to False 
       self.stopped = True
       # thread instantiation  
       self.t = Thread(target=self.buzzing, args=())
       self.t.daemon = True # daemon threads run in background
 
   def start(self):
        self.stopped = False
        self.t.start()
   
   def buzzing(self):
       while True:
          if self.stopped is True :
             break
          if self.status == "0":
             buzzer.on()
          else:
             buzzer.off()

   def get_status(self, data):
       self.status = data

   def stop(self):
        self.stopped = True
        self.t.join()
        buzzer.off()
