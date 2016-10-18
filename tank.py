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


# Setup pygame and key states
global hadEvent
global moveQuit
hadEvent = True
moveQuit = False

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
    global moveQuit

    # Handles each events individually
    for event in events:
         if event.type == pygame.QUIT:
             # User exit
             hadEvent = True
             moveQuit = True

###############################################################################
         elif event.type == pygame.JOYAXISMOTION:
             # A joystick has been moved, read axis positions (-1 to +1)
             hadEvent = True
             global left
             global right
             global up
             global down
             global upr
             global downr
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
                 up = 0
                 down = 0

             if right < 0:
                 upr = right * (-1) * (100)

             elif right > 0:
                 downr = right * 100
             else:
                 upr = 0
                 downr = 0

###############################################################################


try:
    print ("Press [CTRL + C]")
    init()
    # Main Loop
    while True:
        # Get the currently activated inputs
        PygameHandler(pygame.event.get())
        if hadEvent:
            # Keys have changed, generate the command list based on keys
            hadEvent = False

            if moveQuit:
                break

            leftf.ChangeDutyCycle(up)
            rightf.ChangeDutyCycle(upr)
            leftb.ChangeDutyCycle(down)
            rightb.ChangeDutyCycle(downr)


        print "L:", int(up) , int(down) , "R:", int(upr) , int(downr)
        time.sleep(0.1)

except KeyboardInterrupt:
    leftf.stop()
    leftb.stop()
    rightb.stop()
    rightf.stop()
    GPIO.cleanup()
