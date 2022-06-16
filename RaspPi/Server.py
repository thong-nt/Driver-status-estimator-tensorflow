import socket 
import threading
import signal
import sys
import RPi.GPIO as GPIO

from Buzzer import Warning
from Oled import OLED

HEADER = 64
PORT = 5050
SERVER = "10.42.0.21"  #socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

BUTTON_UP = 18
BUTTON_DOWN = 17
BUTTON_LEFT = 22
BUTTON_RIGHT = 27

BUTTON_RUN = 6
BUTTON_STOP = 5

status = "M"
check_ = "init"
car = "Run"

def handle_client(conn, addr, buzz, disp):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    settup_IO()
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if car == "Stop": buzz.pause(1)
            else: buzz.pause(0)
            buzz.get_status(msg,status)
            disp.update(status,msg,car)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg} - Direction: {status} - Car: {car}")
    return False



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    #Initialize Buzzer task
    buzz = Warning()
    buzz.start()
    #Initialize OLED interface
    disp = OLED()
    disp.start()
    while True:
        conn, addr = server.accept()
        if (handle_client(conn, addr, buzz, disp)) == False:
            print(f"[{addr}]  Server closed!")
            conn.send("Server closed!".encode(FORMAT))
            conn.close()
            buzz.stop()
            disp.stop()
            break

def input_direction(argument):
    switcher = {
        18: "R",                         #Turn right
        17: "M",                         #Move straight ahead 
        22: "Re",                        #Reversing
        27: "L",                         #Turn left
        6: "Run",
        5: "Stop",
    }
    return switcher.get(argument, "nothing")


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    global status, check_, car
    if channel == 5 or channel == 6:
       print("yes")
       car = input_direction(channel)
    else: 
       status = input_direction(channel)
       if status != check_:
          print(status)
          check_ = status

def settup_IO():
    GPIO.setmode(GPIO.BCM)
    bounce = 100
    GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RUN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_UP, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_DOWN, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_LEFT, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_RIGHT, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_RUN, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_STOP, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)

if __name__ == '__main__':
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(ADDR)
   print("[STARTING] server is starting...")
   start()




