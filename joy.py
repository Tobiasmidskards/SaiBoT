#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import pygame
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 7
DRIVE_2 = 11
DRIVE_3 = 15
DRIVE_4 = 13

# GPIO pins for distance
trigger = 12
echo = 16


# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

# Setup for distance sensor
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# Function to set all drives off
def MotorOff():
	GPIO.output(DRIVE_1, GPIO.LOW)
	GPIO.output(DRIVE_2, GPIO.LOW)
	GPIO.output(DRIVE_3, GPIO.LOW)
	GPIO.output(DRIVE_4, GPIO.LOW)
	

# Settings for JoyBorg
leftDrive = DRIVE_1                     # Drive number for left motor
rightDrive = DRIVE_4                    # Drive number for right motor
leftDriveCounter = DRIVE_2
rightDriveCounter = DRIVE_3
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False 		# Set this to True if up and down appear to be swapped
axisLeftRight = 0 			# Joystick axis to read for left / right position
axisLeftRightInverted = False 		# Set this to True if left and right appear to be swapped
interval = 0.1 				# Time between keyboard updates in seconds, smaller responds faster but uses more processor time

# speedcontroller testing

#global level
#global current
#global speedTick
#level = 0
#current = 33
#speedTick = 0

#def Tick():
#	global speedTick
#	speedTick = (speedTick + 1)
#	if speedTick == 3:
#		speedTick = 0
#	speed(speedTick)

#def speed(level):
#	global current
#
#	first = GPIO.PWM(7, 100)
#	second = GPIO.PWM(11, 100)
#	third = GPIO.PWM(13, 100)
#	fourth = GPIO.PWM(15, 100)
#	first.start(33)
#	second.start(33)
#	third.start(33)
#	fourth.start(33)
#
#	if level == 0:
#		current = 33
#	elif level == 1:
#		current = 66
#	elif level == 2:
#		current = 100
#	else:
#		print('doesnt work')
#
#	first.ChangeDutyCycle(current)
#	second.ChangeDutyCycle(current)
#	third.ChangeDutyCycle(current)
#	fourth.ChangeDutyCycle(current)

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
global distance

hadEvent = True
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
squarePressed = False
crossPressed = False

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("JoyBorg - Press [ESC] to quit")

def dist():
	global distance
	#GPIO.output(12, True)
	#time.sleep(0.00001)
	#GPIO.output(12, False)

	#while GPIO.input(echo) == 0:
	#	noSignal = time.time()

	#while GPIO.input(echo) == 1:
	#	Signal = time.time()

	#difference = (Signal - noSignal)

	#distance = difference / 0.000058
	distance = 16
	return distance


# Function to handle pygame events
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
	# Handle each event individually
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
			hadEvent = True
			if joystick.get_button(0) == False:
				squarePressed = False
			if joystick.get_button(1) == False:
				crossPressed = False
			
		elif event.type == pygame.JOYAXISMOTION:
			# A joystick has been moved, read axis positions (-1 to +1)
			hadEvent = True
			upDown = joystick.get_axis(axisUpDown)
			leftRight = joystick.get_axis(axisLeftRight)
			# Invert any axes which are incorrect
			if axisUpDownInverted:
				upDown = -upDown
			if axisLeftRightInverted:
				leftRight = -leftRight
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
		
				
				

try:
	print 'Press [ESC] to quit'
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
				rightStateCounter = True
				print('Left')

			elif moveRight:
				leftState = True
				rightState = False
				leftStateCounter = True
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
				
			elif squarePressed:
				print('Square has been pressed')
				
			elif crossPressed:
				print('Cross has been pressed')
				moveQuit = True
				
			elif dist() < 15:
				MotorOff()
				print('For your safety - Motors has been disabled')
				
			else:
				leftState = False
				rightState = False
				leftStateCounter = False
				rightStateCounter = False
				if counter > 40:
					print('There is connection - Dont worry')
					counter = 0
				
			GPIO.output(leftDrive, leftState)
			GPIO.output(rightDrive, rightState)
			GPIO.output(leftDriveCounter, rightStateCounter)
			GPIO.output(rightDriveCounter, rightStateCounter)
			
		# Wait for the interval period
		dist()
		if counter == 10 and 20:
			print "The distance is:" (distance)
			
		time.sleep(interval)
	# Disable all drives
	MotorOff()
except KeyboardInterrupt:
	# CTRL+C exit, disable all drives
	MotorOff()
	GPIO.cleanup()
