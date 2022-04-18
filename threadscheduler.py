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
        self.chek = None

    def run(self):
        img1 = self.queue_worker.get()
        self.chek = detect_pose(self.tpu, img1, self.w, self.h)
        self.queue_main.put('call even')
        detect_status()
        #if len(current_poses) > 0:
        #    self.threadlock.acquire()
        #    img1 = get_res(df, df_dist, self.idx, current_poses, self.model, img1)
        #    self.threadlock.release()
        self.queue_main.put('odd Done')
    
    def ret(self):
        threading.Thread.join(self)
        return self.chek

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
        self.chek = None

    def run(self):
        img2 = self.queue_worker.get()
        self.chek = detect_pose(self.tpu, img2, self.w, self.h)
        self.queue_main.put('call odd')
        detect_status()
        #if len(current_poses) > 0:
        #    self.threadlock.acquire()
        #    img1 = get_res(df, df_dist, self.idx, current_poses, self.model, img2)
        #    self.threadlock.release()
        self.queue_main.put('even Done')

    def ret(self):
        threading.Thread.join(self)
        return self.chek
