import cv2
import time

from pose_engine import PoseEngine
from PIL import Image

def_h = 480
def_w = 640

def detect_pose(engine, img, inp_h, inp_w):
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    #img = cv2.resize(img, (480, 360))

    pil_image = Image.fromarray(img)
    poses, inference_time = engine.DetectPosesInImage(pil_image)
    #print('Inference time: %.f ms' % (inference_time * 1000))

    for pose in poses:
      if pose.score < 0.3: continue
      #print('\nCheckinggggggg')
      for label, keypoint in pose.keypoints.items():
          #print('  %-20s x=%-4d y=%-4d score=%.1f' %
          #      (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
          cv2.circle(img, (int(keypoint.point[0]*(inp_w/def_w)), 
                           int(keypoint.point[1]*(inp_h/def_h))), 5, [0, 224, 255], -1)
    #print(int(1/(inference_time)))
    return img

def detect_status():
    time.sleep(0.05)