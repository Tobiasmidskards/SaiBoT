# Loads librarys
import RPi.GPIO as GPIO
import time

global nosignal_mid
global signal_mid
global nosignal_left
global signal_left
global nosignal_right
global signal_right
nosignal_mid = 0
signal_mid = 0
nosignal_left = 0
signal_left = 0
nosignal_right = 0
signal_right = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# GPIOPINS for Sonic Sensor System
# middle
out_middle = 12
in_middle = 16
GPIO.setup(out_middle, GPIO.OUT)
GPIO.setup(in_middle, GPIO.IN)

# left
out_left = 29
in_left = 31
GPIO.setup(out_left, GPIO.OUT)
GPIO.setup(in_left, GPIO.IN)

# right
out_right = 33
in_right = 35
GPIO.setup(out_right, GPIO.OUT)
GPIO.setup(in_right, GPIO.IN)

def dist_mid():
    global distance_mid
    global signal_mid
    global nosignal_mid
    GPIO.output(out_middle, True)
    time.sleep(0.00001)
    GPIO.output(out_middle, False)

    while GPIO.input(in_middle) == 0:
        nosignal_mid = time.time()

    while GPIO.input(in_middle) == 1:
        signal_mid = time.time()

    dif = (signal_mid - nosignal_mid)

    distance_mid = dif / 0.000058
    return distance_mid

def dist_left():
    global signal_left
    global nosignal_left
    global distance_left
    GPIO.output(out_left, True)
    time.sleep(0.00001)
    GPIO.output(out_left, False)

    while GPIO.input(in_left) == 0:
        nosignal_left = time.time()

    while GPIO.input(in_left) == 1:
        signal_left = time.time()

    dif = (signal_left - nosignal_left)

    distance_left = dif / 0.000058
    return distance_left

def dist_right():
    global signal_right
    global nosignal_right
    global distance_right
    GPIO.output(out_right, True)
    time.sleep(0.00001)
    GPIO.output(out_right, False)

    while GPIO.input(in_right) == 0:
        nosignal_right = time.time()

    while GPIO.input(in_right) == 1:
        signal_right = time.time()

    dif = (signal_right - nosignal_right)

    distance_right = dif / 0.000058
    return distance_right

''' while True:
    dist_left()
    dist_mid()
    dist_right()
    print(int(distance_left), int(distance_mid), int(distance_right))
    time.sleep(0.5)
    '''
