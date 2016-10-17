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

# GPIOPINS for motors
GPIO.setup(7, GPIO.OUT)# set GPIO 7 as output for LeftFwd
GPIO.setup(11, GPIO.OUT)# set GPIO 11 as output for LeftBwd

GPIO.setup(13, GPIO.OUT)# set GPIO 13 as output for RightFwd
GPIO.setup(15, GPIO.OUT)# set GPIO 15 as output for RightBwd


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

def forward():
    GPIO.output(7, True)
    GPIO.output(15, True)
    GPIO.output(11, False)
    GPIO.output(13, False)

def backward():
    GPIO.output(7, False) # for left
    GPIO.output(15, False) # for right
    GPIO.output(11, True) # back left
    GPIO.output(13, True) # back right

def left():
    GPIO.output(7, False) # for left
    GPIO.output(15, True) # for right
    GPIO.output(11, True) # back left
    GPIO.output(13, False) # back right

def right():
    GPIO.output(7, True) # for left
    GPIO.output(15, False) # for right
    GPIO.output(11, False) # back left
    GPIO.output(13, True) # back right

def stop():
    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(15, False)

def obstacle():
    print ("an obstacle has been detected!")
    stop()
    if distance_left > distance_mid or distance_left > distance_right:
        #stop()
        left()
        print ("Turning LEFT")
        time.sleep(0.02)
    elif distance_right > distance_mid or distance_right > distance_left:
        #stop()
        right()
        time.sleep(0.02)
        print ("Turning RIGHT")
    return 0


def dance():
    stop()
    print ("Time to dance!")
    time.sleep(2)
    for i in range (0,3):
        left()
        time.sleep(0.3)
        forward()
        time.sleep(0.3)
        backward()
        time.sleep(0.3)
        right()
        time.sleep(0.3)
        left()
        time.sleep(0.3)
        backward()
        time.sleep(0.3)
        forward()
        time.sleep(0.3)


try:
    counter = 0
    while True:
        dist_left()
        dist_mid()
        dist_right()
        #stop()
        forward()
        print ("Going forward")
        if distance_mid < 35 or distance_left < 35 or distance_right < 35:
            obstacle()
        print(int(distance_left), int(distance_mid), int(distance_right), "counter: ",counter)
        time.sleep(0.3)
        if counter == 75:
            dance()
            counter = 0
        counter = counter + 1

except KeyboardInterrupt:
    stop()
    GPIO.cleanup()
