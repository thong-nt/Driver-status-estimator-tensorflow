from asyncio import events
from pose_engine import PoseEngine
from PIL import Image

import numpy as np
import os
import time
import cv2
import threading, queue
import pickle

from WebcamStream import WebcamStream
from threadscheduler import ODD, EVEN
from Client import *

resolution = [[360, 480], [480, 640], [720, 1280]]
# Initialize the size of input frames.
#inp_h = 720#360#480
#inp_w = 1280#480#640
inp_h, inp_w = resolution[0]

def run(engine, model):
  # initializing and starting multi-threaded webcam input stream 
  webcam_stream = WebcamStream(0, inp_h, inp_w) # 0 id for main camera
  webcam_stream.start()

  connect_pi = Client(HEADER = 64, PORT = 5050, SERVER = "10.42.0.21")
  connect_pi.start()

  idx = 0
  previouse_frame = 0
  queue_to_main, queue_to_worker = queue.Queue(), queue.Queue()
  odd_thread = ODD(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
  even_thread = EVEN(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
  lock = threading.Lock()

  while(True):#time.time()-start < 30):
    if webcam_stream.stopped is True :
        break
    else :
        if idx == 0:
            frame = cv2.flip(webcam_stream.read(),1)
            #frame = cv2.flip(webcam_stream.read()[100:300,120:400] , 1)
            even_thread.start()
            idx += 1
            queue_to_worker.put(frame)
        else:
            if odd_thread.is_alive() == True or even_thread.is_alive() == True:
                i = queue_to_main.get()
            else:
                if idx%2 == 0: i = "call even"
                elif idx%2 == 0: i = "call even"
            if i == "call even":
                if even_thread.is_alive() == True:
                    continue
                lock.acquire()
                even_thread = EVEN(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
                frame = cv2.flip(webcam_stream.read(),1)
                #even_thread = EVEN(250, 280, queue_to_main, queue_to_worker, engine, model, idx)
                #frame = cv2.flip(webcam_stream.read()[100:350,120:400] , 1)
                even_thread.start()
                idx += 1
                queue_to_worker.put(frame)
                lock.release()
            elif i == "call odd":
                if odd_thread.is_alive() == True:
                    continue  
                lock.acquire()
                odd_thread = ODD(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
                frame = cv2.flip(webcam_stream.read(),1)
                #odd_thread = ODD(250, 280, queue_to_main, queue_to_worker, engine, model, idx)
                #frame = cv2.flip(webcam_stream.read()[100:350,120:400] , 1)
                odd_thread.start()
                idx += 1
                queue_to_worker.put(frame)
                lock.release()
            elif i == "odd Done":  
                lock.acquire()
                pic, status = odd_thread.ret()
                odd_thread.join()
                connect_pi.get_message(status)
                cv2.imshow('frame' , pic)
                lock.release()
                print("fps:", int(1 / (time.perf_counter() - previouse_frame)))
            elif i == "even Done": 
                lock.acquire() 
                pic, status = even_thread.ret()
                even_thread.join()
                connect_pi.get_message(status)
                cv2.imshow('frame' , pic) 
                lock.release()
                previouse_frame = time.perf_counter()

            key = cv2.waitKey(1)

            if key == ord('q'):
                connect_pi.stop()
                connect_pi.client.shutdown(socket.SHUT_WR)
                webcam_stream.stop() # stop the webcam stream
                del connect_pi, webcam_stream, odd_thread, even_thread
                break
  
if __name__ == '__main__':
  engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
  model = pickle.load(open("models/finalized_model_0.24.2.sav", 'rb'))
  run(engine, model)
  

