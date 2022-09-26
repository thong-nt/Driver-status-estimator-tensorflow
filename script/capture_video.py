import numpy as np
import cv2
import time

# This will return video from the first webcam on your computer.
cap = cv2.VideoCapture(0)  
  
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
start = time.time()
previouse_frame = start
# loop runs if capturing has been initialized. 
while(previouse_frame-start<90):
    # reads frames from a camera 
    # ret checks return at each frame
    ret, frame = cap.read()
    out.write(frame) 
    cv2.imshow('Original', frame)
  
    previouse_frame = time.time()
    # Wait for 'a' key to stop the program 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# Close the window / Release webcam
cap.release()
  
# After we release our webcam, we also release the output
out.release() 
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()