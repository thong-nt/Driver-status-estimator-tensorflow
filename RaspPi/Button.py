import signal
import sys
import RPi.GPIO as GPIO

BUTTON_UP = 16
BUTTON_DOWN = 17
BUTTON_LEFT = 22
BUTTON_RIGHT = 27

status = ""

def input_direction(argument):
    switcher = {
        16: "Move straight ahead",
        17: "Reversing",
        22: "Turn left",
        27: "Turn right",
    }
    return switcher.get(argument, "nothing")

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    global status
    status = input_direction(channel)
    print(status)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    bounce = 200
    GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(BUTTON_UP, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_DOWN, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_LEFT, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
    GPIO.add_event_detect(BUTTON_RIGHT, GPIO.FALLING, 
            callback=button_pressed_callback, bouncetime=bounce)
   
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
