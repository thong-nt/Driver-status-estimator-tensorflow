import cv2
import time
import math
import pandas as pd

from pose_engine import PoseEngine
from PIL import Image

def_h = 480
def_w = 640

features = ["nose_x", "nose_y", "neck_x", "neck_y",	"r_sho_x", "r_sho_y", "l_sho_x", "l_sho_y",	"r_eye_x",	"r_eye_y",	"l_eye_x",	"l_eye_y",	"r_ear_x",	"r_ear_y",	"l_ear_x",	"l_ear_y"]
fdist = ['NeNo','NeLs','NeRs','NeLey','NeRey','NeLea','NeRea']
state = ['Safe', 'Distracted']
def Dis(xa,ya,xb,yb):
    if xb == 0 and yb == 0:
        dist = 0
    else:
        dist = math.sqrt( (xb - xa)**2 + (yb - ya)**2 )
    return dist

def get_dist(df,df_dist):
    df_dist.at[0,'NeNo']  = Dis(df['neck_x'][0], df['neck_y'][0], df['nose_x'][0], df['nose_y'][0])
    df_dist.at[0,'NeLs']  = Dis(df['neck_x'][0], df['neck_y'][0], df['l_sho_x'][0], df['l_sho_y'][0])
    df_dist.at[0,'NeRs']  = Dis(df['neck_x'][0], df['neck_y'][0], df['r_sho_x'][0], df['r_sho_y'][0])
    df_dist.at[0,'NeLey'] = Dis(df['neck_x'][0], df['neck_y'][0], df['l_eye_x'][0], df['l_eye_y'][0])
    df_dist.at[0,'NeRey'] = Dis(df['neck_x'][0], df['neck_y'][0], df['r_eye_x'][0], df['r_eye_y'][0])
    df_dist.at[0,'NeLea'] = Dis(df['neck_x'][0], df['neck_y'][0], df['l_ear_x'][0], df['l_ear_y'][0])
    df_dist.at[0,'NeRea'] = Dis(df['neck_x'][0], df['neck_y'][0], df['r_ear_x'][0], df['r_ear_y'][0])

    dex = [df_dist['NeNo'][0],df_dist['NeLs'][0],df_dist['NeRs'][0],df_dist['NeLey'][0],df_dist['NeRey'][0],df_dist['NeLea'][0],df_dist['NeRea'][0]]
    maxV = max(dex)

    df_dist.loc[0] = df_dist.loc[0]/maxV
    return df_dist

def detect_pose(engine, img, inp_h, inp_w):
    img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    #img = cv2.resize(img, (480, 360))

    pil_image = Image.fromarray(img)
    poses, inference_time = engine.DetectPosesInImage(pil_image)
    #print('Inference time: %.f ms' % (inference_time * 1000))
    df = pd.DataFrame(columns=features)
    df_dist = pd.DataFrame(columns=fdist)

    for pose in poses:
      if pose.score < 0.25: continue
      
      for label, keypoint in pose.keypoints.items():
        #print('  %-20s x=%-4d y=%-4d score=%.1f' %
        #        (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
        cv2.circle(img, (int(keypoint.point[0]*(inp_w/def_w)), 
                           int(keypoint.point[1]*(inp_h/def_h))), 3, [0, 224, 255], -1)
        df.at[0,label.name+'_x'] = keypoint.point[0]*(inp_w/def_w)
        df.at[0,label.name+'_y'] = keypoint.point[1]*(inp_h/def_h)
    #print(int(1/(inference_time)))
    #print(df)
    if df.size > 0:
        get_dist(df,df_dist)
    #print(df_dist)
    return img, df_dist

def detect_status(model, poses, img):
    if poses.size == 0:
        cv2.putText(img, "Distracted", (0,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
    else:
        y_pred = model.predict(poses)
        cv2.putText(img, state[y_pred[0]], (0,40), cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255), 3) 
    #time.sleep(0.05)
    return img