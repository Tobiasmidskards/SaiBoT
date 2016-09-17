# Loads librarys
import RPi.GPIO as GPIO
import time
import pygame


GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes.

# Settings for joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False 		# Set this to True if up and down appear to be swapped
axisLeftRight = 0 			# Joystick axis to read for left / right position
axisLeftRightInverted = False 		# Set this to True if left and right appear to be swapped
interval = 0.1 				# Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Define accelerate counter
global acc
acc = 0

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False

def init():
  global leftf
  global leftb
  global rightf
  global rightb

  GPIO.setup(7, GPIO.OUT)# set GPIO 7 as output for LeftFwd
  GPIO.setup(11, GPIO.OUT)# set GPIO 11 as output for LeftBwd
  GPIO.setup(13, GPIO.OUT)# set GPIO 13 as output for RightFwd
  GPIO.setup(15, GPIO.OUT)# set GPIO 15 as output for RightBwd

  leftf = GPIO.PWM(7, 100)   # create object LeftFwd for PWM on port 7 at 100 Hertz
  leftb = GPIO.PWM(11, 100)  # create object LeftBwd for PWM on port 11 at 100 Hertz

  rightf = GPIO.PWM(15, 100) # create object RightFwd for PWM on port 15 at 100 Hertz
  rightb = GPIO.PWM(13, 100) # create object RightBwd for PWM on port 13 at 100 Hertz

  leftf.start(0)             # start white led on 0 percent duty cycle (off)
  leftb.start(0)             # 100 percent = (on)

  rightf.start(0)
  rightb.start(0)

def MotorOff():
    leftf.ChangeDutyCycle(0)
    leftb.ChangeDutyCycle(0)
    rightf.ChangeDutyCycle(0)
    rightb.ChangeDutyCycle(0)
    leftf.stop()
    leftb.stop()
    rightb.stop()
    rightf.stop()

    print ("motor off")

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
         elif event.type == pygame.JOYAXISMOTION:
             # A joystick has been moved, read axis positions (-1 to +1)
             hadEvent = True
             upDown = joystick.get_axis(axisUpDown)
             leftRight = joystick.get_axis(axisLeftRight)

             if upDown < -0.1:
                 moveUp = True
                 moveDown = False
             elif upDown > 0.1:
                 moveUp = False
                 moveDown = True
             else:
                 moveUp = False
                 moveDown = False
             if leftRight < -0.1:
                  moveLeft = True
                  moveRight = False
             elif leftRight > 0.1:
                  moveLeft = False
                  moveRight = True
             else:
                  moveLeft = False
                  moveRight = False


try:
    print 'Press [CTRL + C]'
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

            #elif moveLeft:

            #elif moveRight:

            elif moveUp:
                acc += 5
                if acc < 101:
                    leftf.ChangeDutyCycle(acc)
                    rightf.ChangeDutyCycle(acc)

            #elif moveDown:

            else:
                acc = 0
                MotorOff()

            print (acc)

        time.sleep(0.1)

except KeyboardInterrupt:
    MotorOff()
    GPIO.cleanup()
