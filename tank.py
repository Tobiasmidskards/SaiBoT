# Loads librarys
import RPi.GPIO as GPIO
import time
import pygame

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes.
GPIO.setwarnings(False)

# Settings for joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False 		# Set this to True if up and down appear to be swapped
axisLeftRight = 3 			# Joystick axis to read for left / right position
axisLeftRightInverted = False 		# Set this to True if left and right appear to be swapped
interval = 0.1 				# Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Define accelerate counter
global acc
global accside
acc = 0
accside = 0

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
global squarePressed
global CrossPressed
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
squarePressed = False
crossPressed = False

def init():
  global leftf
  global leftb
  global rightf
  global rightb
  global noSignal
  noSignal = 0

  GPIO.setup(7, GPIO.OUT)# set GPIO 7 as output for LeftFwd
  GPIO.setup(11, GPIO.OUT)# set GPIO 11 as output for LeftBwd
  GPIO.setup(13, GPIO.OUT)# set GPIO 13 as output for RightFwd
  GPIO.setup(15, GPIO.OUT)# set GPIO 15 as output for RightBwd

  # GPIO pins for distance
  trigger = 12
  echo = 16

  GPIO.setup(trigger, GPIO.OUT)
  GPIO.setup(echo, GPIO.IN)

  leftf = GPIO.PWM(7, 100)   # create object LeftFwd for PWM on port 7 at 100 Hertz
  leftb = GPIO.PWM(11, 100)  # create object LeftBwd for PWM on port 11 at 100 Hertz

  rightf = GPIO.PWM(15, 100) # create object RightFwd for PWM on port 15 at 100 Hertz
  rightb = GPIO.PWM(13, 100) # create object RightBwd for PWM on port 13 at 100 Hertz

  leftf.start(0)             # start white led on 0 percent duty cycle (off)
  leftb.start(0)             # 100 percent = (on)

  rightf.start(0)
  rightb.start(0)

def dist():
    global distance
    global noSignal
    global Signal
    GPIO.output(12, True)
    time.sleep(0.00001)
    GPIO.output(12, False)

    while GPIO.input(16) == 0:
        noSignal = time.time()

    while GPIO.input(16) == 1:
        Signal = time.time()

    difference = (Signal - noSignal)

    distance = difference / 0.000058
    return distance

def MotorOff():
    leftf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)

# Initializing joysticks
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("SaiBot - Press [ESC] to quit")

# Function to handle joystick
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global squarePressed
    global crossPressed

    # Handles each events individually
    for event in events:
         if event.type == pygame.QUIT:
             # User exit
             hadEvent = True
             moveQuit = True
         elif event.type == pygame.KEYDOWN:
             # A key has been pressed, see if it is one we want
             hadEvent = True
             if event.key == pygame.K_ESCAPE:
                 moveQuit = True
         elif event.type == pygame.KEYUP:
             # A key has been released, see if it is one we want
             hadEvent = True
             if event.type == pygae.K_ESCAPE:
                 moveQuit = False

         elif event.type == pygame.JOYBUTTONDOWN:
            # a button has been pressed
            hadEvent = True
            if joystick.get_button(0) == True:
                squarePressed = True
            if joystick.get_button(1) == True:
                crossPressed = True

         elif event.type == pygame.JOYBUTTONUP:
            hadEvent = True
            if joystick.get_button(0) == False:
                squarePressed = False
            if joystick.get_button(1) == False:
                crossPressed = False

###############################################################################
         elif event.type == pygame.JOYAXISMOTION:
             # A joystick has been moved, read axis positions (-1 to +1)
             hadEvent = True
             global left
             global right
             up = 0
             upr = 0
             down = 0
             downr = 0

             left = joystick.get_axis(1)
             right = joystick.get_axis(5)

             if left < 0:
                 up = left * (-1) * (100)
             elif left > 0:
                 down = left * 100

             else:
                 print left

             if right < 0:
                 upr = right * (-1) * (100)

             elif right > 0:
                 downr = right * 100
             else:
                 print right

             print "left:", int(up) , int(down)
             print "right:", int(upr) , int(downr)

###############################################################################

# to autonomos mode
def forw(mode):

    leftf.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)

def backw(mode):

    leftf.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)

def right(mode):

    leftf.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)

def left(mode):

    leftf.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)


try:
    print ("Press [CTRL + C]")
    init()
    check = 1
    # Main Loop
    while True:
        # Get the currently activated inputs
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False

            if moveQuit:
                break

            # elif :

            else:
                acc = 35
                accside = 35
                MotorOff()


        time.sleep(0.1)
        print (acc , "acc")
        print (accside , "accside")
        check += 1
        if check > 15:
            check = 0
            print ("\nI'm a happy robot!\n")
            #print "The distance is:", distance


except KeyboardInterrupt:
    MotorOff()
    leftf.stop()
    leftb.stop()
    rightb.stop()
    rightf.stop()
    GPIO.cleanup()
