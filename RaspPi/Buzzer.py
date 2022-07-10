import threading

from gpiozero import Buzzer
from time import sleep
from threading import Thread # library for multi-threading

buzzer = Buzzer(26)

class Warning:
   def __init__(self):
       self.status = "None"
       self.act_dir= "None"
       self.but_dir= "None"
       self.flag = 0
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

          if self.flag == 0:
             if self.status == "Distracted":
                if self.act_dir != self.but:
                   buzzer.on()
                else:
                   buzzer.off()
             else:
               buzzer.off()
          else: buzzer.off()

   def get_status(self, data, but):
       self.status = data.split('!')[0]
       self.act_dir = data.split('!')[1]
       self.but = but

   def pause(self, flag):
       self.flag = flag

   def stop(self):
        self.stopped = True
        self.t.join()
