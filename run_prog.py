from pose_engine import PoseEngine
from PIL import Image

import numpy as np
import os
import time
import cv2
import threading, queue

from WebcamStream import WebcamStream
from threadscheduler import ODD, EVEN

inp_h = 360#480
inp_w = 480#640

def run(engine, model):
  # initializing and starting multi-threaded webcam input stream 
  webcam_stream = WebcamStream(0, inp_h, inp_w) # 0 id for main camera
  webcam_stream.start()
    
  start = time.time()
  idx = 0
  queue_to_main, queue_to_worker = queue.Queue(), queue.Queue()
  odd_thread = ODD(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
  even_thread = EVEN(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
  lock = threading.Lock()
  while(True):#time.time()-start < 30):
    print(idx)
    if webcam_stream.stopped is True :
        break
    else :
        if idx == 0:
            frame = webcam_stream.read()
            print("Even: {}".format(even_thread.is_alive()))
            even_thread.start()
            idx += 1
            queue_to_worker.put(frame)
        else:
            if odd_thread.is_alive() == True or even_thread.is_alive() == True:
                i = queue_to_main.get()
            elif i == "":
                if idx%2 == 0: i = "call even"
                elif idx%2 == 0: i = "call even"
            #print(i)
            if i == "call even":
                if even_thread.is_alive() == True:
                    continue
                lock.acquire()
                print("Even: {}".format(even_thread.is_alive()))
                even_thread = EVEN(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
                frame = webcam_stream.read()
                even_thread.start()
                idx += 1
                queue_to_worker.put(frame)
                lock.release()
            elif i == "call odd":
                if odd_thread.is_alive() == True:
                    continue  
                lock.acquire()
                print("Odd: {}".format(odd_thread.is_alive()))
                odd_thread = ODD(inp_h, inp_w, queue_to_main, queue_to_worker, engine, model, idx)
                frame = webcam_stream.read()
                odd_thread.start()
                idx += 1
                queue_to_worker.put(frame)
                lock.release()
            elif i == "odd Done":  
                lock.acquire()
                pic = odd_thread.ret()
                #odd_thread.join()
                cv2.imshow('frame' , pic)
                lock.release()
            elif i == "even Done": 
                lock.acquire() 
                pic = even_thread.ret()
                #even_thread.join()
                cv2.imshow('frame' , pic) 
                lock.release()
            i = ""
            #cv2.imshow("Testing",frame)
            key = cv2.waitKey(1)

            if key == ord('q'):
                webcam_stream.stop() # stop the webcam stream
                break

if __name__ == '__main__':
  engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
  model = 0
  run(engine, model)
  

