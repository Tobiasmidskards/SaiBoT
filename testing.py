# Loading library functions
import time 
import pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Sets the GPIO pins to motors
Drive_1 = 7
Drive_2 = 11
Drive_3 = 13
Drive_4 = 15

# Sets the pins as in/out 
GPIO.setup(Drive_1, GPIO.OUT)
GPIO.setup(Drive_2, GPIO.OUT)
GPIO.setup(Drive_3, GPIO.OUT)
GPIO.setup(Drive_4, GPIO.OUT)

# Functions
# Set all as off
def MotorOff():
	GPIO.output(DRIVE_1, GPIO.LOW)
	GPIO.output(DRIVE_2, GPIO.LOW)
	GPIO.output(DRIVE_3, GPIO.LOW)
	GPIO.output(DRIVE_4, GPIO.LOW)

# Settings for joystick  
forward_left = Drive_1
forward_right = Drive_4
backward_left = Drive_2
backward_left = Drive_3

axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False 		# Set this to True if up and down appear to be swapped
axisLeftRight = 0 			# Joystick axis to read for left / right position
axisLeftRightInverted = False 		# Set this to True if left and right appear to be swapped
interval = 0.1 				# Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
global speedCount
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

# Initializing joystick 
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("SaiBot - Press [CTRL + C] to quit")

# function to handle pygame events
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

    # Handles each event individually
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
		if event.key == pygame.K_ESCAPE:
			moveQuit = False
				
		elif event.type == pygame.JOYBUTTONDOWN:
			# a button has been pressed
			hadEvent = True
			if joystick.get_button(0) == True:
				squarePressed = True
			if joystick.get_button(1) == True:
				crossPressed = True
				
		elif event.type == pygame.JOYBUTTONUP:
			# a button has been released
			hadEvent = True
			if joystick.get_button(0) == False:
				squarePressed = False
			if joystick.get_button(1) == False:
				crossPressed = False
			
		elif event.type == pygame.JOYAXISMOTION:
			# A joystick has been moved, read axis positions (-1 to +1)
			hadEvent = True
			upDown = joystick.get_axis(axisUpDown)
			leftRight = joystick.get_axis(2)
			# Invert any axes which are incorrect
			if axisUpDownInverted:
				upDown = -upDown
			if axisLeftRightInverted:
				leftRight = -leftRight

            		print (upDown)
            		print (leftRight)
			''' 
            # only 4 ways output
			# Determine Up / Down values
			if upDown < -0.1:
				moveUp = True
				moveDown = False
			elif upDown > 0.1:
				moveUp = False
				moveDown = True
			else:
				moveUp = False
				moveDown = False
			# Determine Left / Right values
			if leftRight < -0.1:
				moveLeft = True
				moveRight = False
			elif leftRight > 0.1:
				moveLeft = False
				moveRight = True
			else:
				moveLeft = False
				moveRight = False
            '''

# Testing with PWD
try:
	print 'Press [X] to quit'
	counter = 0	
	
	# Loop indefinitely
	while True:
		# Get the currently pressed keys on the keyboard
		PygameHandler(pygame.event.get())
		if hadEvent:
			# Keys have changed, generate the command list based on keys
			hadEvent = False
			counter = (counter + 1)
			
			if moveQuit:
				break
			elif moveLeft:
				leftState = False
				rightState = True
				rightStateCounter = False
				leftStateCounter = True
				print('Left')

			elif moveRight:
				leftState = True
				rightState = False
				rightStateCounter = True
				leftStateCounter = False
				print('Right')
				
			elif moveUp:
				leftState = True
				rightState = True
				leftStateCounter = False
				rightStateCounter = False
				print('Up')
				
			elif moveDown:
				leftStateCounter = True
				rightStateCounter = True
				leftState = False
				rightState = False
				print('Down')
				
				
			else:
				leftState = False
				rightState = False
				leftStateCounter = False
				rightStateCounter = False
				
			GPIO.output(leftDrive, leftState)
			GPIO.output(rightDrive, rightState)
			GPIO.output(leftDriveCounter, leftStateCounter)
			GPIO.output(rightDriveCounter, rightStateCounter)
			
		# Wait for the interval period
			
		time.sleep(interval)
	# Disable all drives
	MotorOff()
except KeyboardInterrupt:
	# CTRL+C exit, disable all drives
	MotorOff()
	GPIO.cleanup()

'''
try:
	print 'Press [X] to quit'
	counter = 0
		
		
	
	# Loop indefinitely
	while True:
		# Get the currently pressed keys on the keyboard
		PygameHandler(pygame.event.get())
		if hadEvent:
			# Keys have changed, generate the command list based on keys
			hadEvent = False
			counter = (counter + 1)
			
			if moveQuit:
				break
			elif moveLeft:
				leftState = False
				rightState = True
				rightStateCounter = False
				leftStateCounter = True
				print('Left')

			elif moveRight:
				leftState = True
				rightState = False
				rightStateCounter = True
				leftStateCounter = False
				print('Right')
				
			elif moveUp:
				leftState = True
				rightState = True
				leftStateCounter = False
				rightStateCounter = False
				print('Up')
				
			elif moveDown:
				leftStateCounter = True
				rightStateCounter = True
				leftState = False
				rightState = False
				print('Down')
				
				
			else:
				leftState = False
				rightState = False
				leftStateCounter = False
				rightStateCounter = False
				
			GPIO.output(leftDrive, leftState)
			GPIO.output(rightDrive, rightState)
			GPIO.output(leftDriveCounter, leftStateCounter)
			GPIO.output(rightDriveCounter, rightStateCounter)
			
		# Wait for the interval period
			
		time.sleep(interval)
	# Disable all drives
	MotorOff()
except KeyboardInterrupt:
	# CTRL+C exit, disable all drives
	MotorOff()
	GPIO.cleanup()
'''
