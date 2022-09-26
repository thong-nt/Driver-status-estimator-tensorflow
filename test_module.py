import numpy as np
import os
import time
import cv2
import threading, queue
import pickle
import pandas as pd
import matplotlib.pyplot as plt

from pose_engine import PoseEngine
from pose_modules import *
from Client import *

w = 480
h = 360



time_check = ['Pose','Status','Warning','Time per frame']
res = ['Real']
def running_test(engine,model):

    cap = cv2.VideoCapture(0)#'output.avi')
    #connect_pi = Client(HEADER = 64, PORT = 5050, SERVER = "10.42.0.21")
    #connect_pi.start()
    
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    df_timing = pd.DataFrame(columns=time_check)
    df_res = pd.DataFrame(columns=res)

    # Read until video is completed
    count = 0
    acc = 0
    time_list = []
    fps_list = []
    start = time.perf_counter()
    while(time.perf_counter()-start <= 60):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == True:
            frame = cv2.resize(frame,(w,h))
            frame = cv2.flip(frame,1)
            #start = time.perf_counter()
            proc_img, df, dir = detect_pose(engine, frame, h, w)
            #stage_a = time.perf_counter() 
            proc_img, status = detect_status(model,df,proc_img)
            #stage_b = time.perf_counter()
            #connect_pi.get_message(status+"!"+dir)
            #stage_c = time.perf_counter()
            #df_res.at[count,'Predict'] = status

            #if dir == status:
            #    acc+=1

            #if dir == "Safe": dir = 0
            #else: dir = 1
            #df_res.at[count,'Real'] = dir

            #df_timing.at[count,'Pose'] = round(stage_a - start,4)* 1000
            #df_timing.at[count,'Status'] = round(stage_b - stage_a,4)* 1000
            #df_timing.at[count,'Warning'] = (stage_c - stage_b)* 1000
            #df_timing.at[count,'Time per frame'] = round(stage_c - stage_a,4)*1000
            # Display the resulting frame
            cv2.imshow('Frame',proc_img)
            #df_pose = df
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
               break 
            count=count+1

            end = time.perf_counter()
            time_list.append((end - start))
            fps_list.append(int(count / (end - start)))

        # Break the loop
        else: 
            break

    #y_test = df.iloc[:,1:].values.reshape(-1,1).to_numpy()
    #y_pred = df.iloc[:,0].values.reshape(-1,1).to_numpy()
    



    # When everything done, release the video capture object
    cap.release()
    print(f"Accuaracy: {acc/count*100}")

    #connect_pi.stop()
    #connect_pi.client.shutdown(socket.SHUT_WR)

    # Closes all the frames
    cv2.destroyAllWindows()
    #file = '/home/zek/Thesis/new_test_set.csv'
    #df_res.to_csv(file, index=False)

    plt.figure()
    plt.plot(time_list, fps_list)
    plt.xlabel('Time (s)')
    plt.ylabel('FPS')
    plt.show()

if __name__ == '__main__':
  engine = PoseEngine('models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite')
  model = pickle.load(open("models/finalized_model.sav", 'rb'))
  running_test(engine, model)