import cv2
import time
import math
import pandas as pd

from pose_engine import PoseEngine
from PIL import Image

#default frame size of the model
def_h = 480
def_w = 640

features = ["neck_x", "neck_y", "nose_x", "nose_y",  "l_sho_x", "l_sho_y", "r_sho_x", "r_sho_y", "l_eye_x",	"l_eye_y", "r_eye_x", "r_eye_y",
    	"l_ear_x",	"l_ear_y", "r_ear_x",	"r_ear_y"]
fdist = ['NeNo','NeLs','NeRs','NeLey','NeRey','NeLea','NeRea']
state = ['Safe', 'Distracted']
def Dis(xa,ya,xb,yb):
    if xb == 0 and yb == 0:
        dist = 0
    else:
        dist = math.sqrt( (xb - xa)**2 + (yb - ya)**2 )
    return dist

def get_dist(df,df_dist):
    comp_ = 2
    dex = []
    for fea_ in fdist:
        df_dist.at[0,fea_]  = Dis(df['neck_x'][0], df['neck_y'][0], df[features[comp_]][0], df[features[comp_+1]][0])
        dex.append(df_dist.at[0,fea_])
        comp_ += 2

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
    dir = "?"
    for pose in poses:
      if pose.score < 0.25: continue
      
      for label, keypoint in pose.keypoints.items():
        #print('  %-20s x=%-4d y=%-4d score=%.1f' %
        #        (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
        if label.name == "nose":
            if keypoint.point[0]*(inp_w/def_w) < inp_w/2-20: dir = "L"
            elif keypoint.point[0]*(inp_w/def_w) > inp_w/2+20: dir = "R"
            else: dir = "?"

        cv2.circle(img, (int(keypoint.point[0]*(inp_w/def_w)), 
                           int(keypoint.point[1]*(inp_h/def_h))), 3, [0, 224, 255], -1)
        df.at[0,label.name+'_x'] = keypoint.point[0]*(inp_w/def_w)
        df.at[0,label.name+'_y'] = keypoint.point[1]*(inp_h/def_h)
    #print(int(1/(inference_time)))
    #print(df)
    if df.size > 0:
        get_dist(df,df_dist)
    #print(df_dist)
    df_dist = df_dist.drop(['NeLs', 'NeRs', 'NeLea', 'NeRea'], axis=1)
    return img, df_dist, dir

def detect_status(model, poses, img):
    status = None
    if poses.size == 0:
        cv2.putText(img, state[1], (0,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
        status = state[1]
    else:
        y_pred = model.predict(poses)
        cv2.putText(img, state[y_pred[0]], (0,40), cv2.FONT_HERSHEY_SIMPLEX,1,(209, 80, 0, 255), 3) 
        status = state[y_pred[0]]
    #time.sleep(0.05)
    return img, status