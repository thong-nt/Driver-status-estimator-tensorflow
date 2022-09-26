import cv2

from PIL import Image
from cv2 import imread
from cv2 import imshow
from pose_engine import PoseEngine

import os
import pandas as pd
import math 

def_h = 480
def_w = 640
inp_h = 360#480
inp_w = 480#640

features = ["neck_x", "neck_y", "nose_x", "nose_y",  "l_sho_x", "l_sho_y", "r_sho_x", "r_sho_y", "l_eye_x",	"l_eye_y", "r_eye_x", "r_eye_y",
    	"l_ear_x",	"l_ear_y", "r_ear_x",	"r_ear_y"]
fdist = ['NeNo','NeLs','NeRs','NeLey','NeRey','NeLea','NeRea']

def Dis(xa,ya,xb,yb):
    if xb == 0 and yb == 0:
        dist = 0
    else:
        dist = math.sqrt( (xb - xa)**2 + (yb - ya)**2 )
    return dist

def get_dist(df,df_dist,idx):
    comp_ = 2
    dex = []
    for fea_ in fdist:
        df_dist.at[idx,fea_]  = Dis(df['neck_x'][idx], df['neck_y'][idx], df[features[comp_]][idx], df[features[comp_+1]][idx])
        dex.append(df_dist.at[idx,fea_])
        comp_ += 2

    maxV = max(dex)
    df_dist.loc[idx] = df_dist.loc[idx]/maxV
    return df_dist

if __name__ == '__main__':
    engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
    d = "/media/zek/My Passport/Finland/backup/Newdataset/check/left"
    df = pd.DataFrame(columns=features)
    df_dist = pd.DataFrame(columns=fdist)

    idx = 0
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            print(full_path)
            img = cv2.imread(full_path)
            img = cv2.resize(img, (inp_w,inp_h))
            img = cv2.cvtColor(img, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (480, 360))

            pil_image = Image.fromarray(img)
            poses, inference_time = engine.DetectPosesInImage(pil_image)
            #print('Inference time: %.f ms' % (inference_time * 1000))

            for pose in poses:
                if pose.score < 0.25: continue
                
                for label, keypoint in pose.keypoints.items():
                #print('  %-20s x=%-4d y=%-4d score=%.1f' %
                #        (label.name, keypoint.point[0], keypoint.point[1], keypoint.score))
                    cv2.circle(img, (int(keypoint.point[0]*(inp_w/def_w)), 
                                        int(keypoint.point[1]*(inp_h/def_h))), 3, [0, 224, 255], -1)
                    df.at[idx,label.name+'_x'] = keypoint.point[0]*(inp_w/def_w)
                    df.at[idx,label.name+'_y'] = keypoint.point[1]*(inp_h/def_h)
            if df.size > 0:
                get_dist(df,df_dist,idx)

            idx += 1            
            cv2.imshow('Test',img)
            key = cv2.waitKey(0)
            if key == ord('n'):
                print(df_dist)
                continue
        
    print(df_dist)
    file = '/media/zek/My Passport/Finland/backup/Newdataset/files/left_false_23rd_Aug.csv'
    df_dist.to_csv(file, index=False)
