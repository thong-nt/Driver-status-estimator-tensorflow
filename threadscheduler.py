import threading

from pose_modules import *

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
