import time 
import threading, queue
from typing_extensions import Self
import cv2

from pose_modules import *

#features = ["nose_x", "nose_y", "neck_x", "neck_y",	"r_sho_x", "r_sho_y", "l_sho_x", "l_sho_y",	"r_eye_x",	"r_eye_y",	"l_eye_x",	"l_eye_y",	"r_ear_x",	"r_ear_y",	"l_ear_x",	"l_ear_y"]
#fdist = ['NeNo','NeLs','NeRs','NeLey','NeRey','NeLea','NeRea']
#df = pd.DataFrame(columns=features)
#df_dist = pd.DataFrame(columns=fdist)


class ODD(threading.Thread):

    def __init__(self, in_w, in_h, q_main, q_worker, tpu, model, idx):
        self.queue_main = q_main
        self.queue_worker = q_worker
        threading.Thread.__init__(self)
        self.model = model
        self.tpu = tpu
        self.idx = idx
        self.w = in_w
        self.h = in_h
        self.threadlock = threading.Lock()
        self.proc_img = None
        self.status = None
        self.dir = None

    def run(self):
        img1 = self.queue_worker.get()
        self.proc_img, df, self.dir = detect_pose(self.tpu, img1, self.w, self.h)
        self.queue_main.put('call even')
        self.proc_img, self.status = detect_status(self.model,df,self.proc_img)
        self.queue_main.put('odd Done')
    
    def ret(self):
        threading.Thread.join(self)
        self.status = self.status+"!"+self.dir
        return self.proc_img, self.status

class EVEN(threading.Thread):

    def __init__(self, in_w, in_h, q_main, q_worker, tpu, model, idx):
        self.queue_main = q_main
        self.queue_worker = q_worker
        threading.Thread.__init__(self)
        self.model = model
        self.tpu = tpu
        self.idx = idx
        self.w = in_w
        self.h = in_h
        self.threadlock = threading.Lock()
        self.proc_img = None
        self.status = None
        self.dir = None

    def run(self):
        img2 = self.queue_worker.get()
        self.proc_img, df, self.dir = detect_pose(self.tpu, img2, self.w, self.h)
        self.queue_main.put('call odd')
        self.proc_img, self.status = detect_status(self.model,df,self.proc_img)
        self.queue_main.put('even Done')
        
    def ret(self):
        threading.Thread.join(self)
        self.status = self.status+"!"+self.dir
        return self.proc_img, self.status
