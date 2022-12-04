# Driver's Distraction Estimation

## Introduction
Distracted driving is dangerous, it killed three thousand four hundred forty-two lives in 2020.
Distracted driving is any activity that diverts attention from driving, such as:
+ Eating while driving
+ Texting or using phone while driving
+ Falling asleep while driving
If you take your eyes off the road for 5 seconds at speed of 55 miles per hour, the accidence would happen.

Therefore, this project will focus on two objects:
+ Create a predictive model that can classify whenever a driver is in safe situation or doing distracted actions.
+ Secondly, this model have to work well in embedded environment. Like, it have to be fast enough to catch up the next action of driver on time and be able to interact with the driver by alert him or her when being distracted.

## Requirements
+ Python: Version 3.8.x
Note: to avoid invalid or incorrect results, sklearn version should be 0.24.2 and python version is 3.6.x or higher.

## Setup
+ Rasperry Pi: Connect Pin IO like below picutre:

![alt text](https://github.com/zek213/Driver-status-estimator-tensorflow/blob/main/test_data/pin%20setup.JPG)

+ Connect Ethernet cable from NVIDIA Jetson board to Rasperry PI, change the IP address as well.

## How to run
#Server - Raspberry Pi 2:
Run Server.py to turn on the server

```bash
python Server.py
```

Comment all lines containts connect_pi object in run_program.py to ignore the server.

#Client - Nvidia Jetson Nano:
Run run_program.py to run the client.

```bash
python run_program.py
```
## Demo
https://youtu.be/QK9FPy-3e_8
