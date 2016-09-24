# Loads librarys
import RPi.GPIO as GPIO
import time

global no_signal
global signal

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
    GPIO.output(out_middle, True)
    time.sleep(0.00001)
    GPIO.output(out_middle, False)

    while GPIO.input(in_middle) == 0:
        no_signal = time.time()

    while GPIO.input(in_middle) == 1:
        signal = time.time()

    dif = (signal - no_signal)

    distance = dif / 0.000058
    return distance_mid

def dist_left():
    global distance_left
    GPIO.output(out_left, True)
    time.sleep(0.00001)
    GPIO.output(out_left, False)

    while GPIO.input(in_left) == 0:
        no_signal = time.time()

    while GPIO.input(in_left) == 1:
        signal = time.time()

    dif = (signal - no_signal)

    distance = dif / 0.000058
    return distance_left

def dist_right():
    global distance_right
    GPIO.output(out_right, True)
    time.sleep(0.00001)
    GPIO.output(out_right, False)

    while GPIO.input(in_right) == 0:
        no_signal = time.time()

    while GPIO.input(in_right) == 1:
        signal = time.time()

    dif = (signal - no_signal)

    distance = dif / 0.000058
    return distance_right

while True:
    dist_mid()
    dist_left()
    dist_right()
    print(distance_left , distance_mid, distance_right)
    time.sleep(0.2)
