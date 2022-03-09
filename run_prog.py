from pose_engine import PoseEngine
from PIL import Image

import numpy as np
import os
import time
import cv2

def run(vid,engine):
  start = time.time()
  count = 0
  while(time.time()-start < 30):
    ret, img = vid.read()
  
    # You may need to convert the color.
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
          cv2.circle(img, (int(keypoint.point[0]), int(keypoint.point[1])), 5, [0, 224, 255], -1)
    #print(int(1/(inference_time)))
    count += 1
    cv2.imshow("Check",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break

  print(count/(time.time()-start))

if __name__ == '__main__':
 
  vid = cv2.VideoCapture(0)
  engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
  
  run(vid,engine)
  

