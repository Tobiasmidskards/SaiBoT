import pygame
import RPi.GPIO as GPIO
import time
import webiopi

webiopi.setDebug()
GPIO = webiopi.GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

motorRightPin = 7
motorLeftPin = 11
GPIO.setFunction(motorRightPin, GPIO.OUT)
GPIO.setFunction(motorLeftPin, GPIO.OUT)

motorFdPin = 13
motorRdPin = 15
GPIO.setFunction(motorFdPin, GPIO.OUT)
GPIO.setFunction(motorRdPin, GPIO.OUT)
GPIO.setFunction(motorFdPin, GPIO.PWM)
GPIO.setFunction(motorRdPin, GPIO.PWM)


def initiate():
	global acceleration
	global motorFspeed
	global motorRspeed
	global speedstep
	global maxspeed
	global minspeed

	acceleration = 0
	motorFspeed = 0
	motorRspeed = 0
	speedstep = 10
	maxspeed = 90
	minspeed = 0

def reverse():
    GPIO.output(motorRdPin, GPIO.PWM)
    GPIO.output(motorFdPin, GPIO.PWM)


def forward():
    GPIO.output(motorRdPin, GPIO.PWM)
    GPIO.output(motorFdPin, GPIO.PWM)

def stop():
	GPIO.digitalWrite(motorRdPin, GPIO.PWM)
	GPIO.digitalWrite(motorFdPin, GPIO.PWM)

	# motorFspeed, motorRspeed, acceleration
	initiate()
	return 0, 0, 0

def stear_left():
    GPIO.output(motorRightPin, GPIO.LOW)
    GPIO.output(motorLeftPin, GPIO.HIGH)

def stear_right():
    GPIO.output(motorRightPin, GPIO.HIGH)
    GPIO.output(motorLeftPin, GPIO.LOW)

def center():
	GPIO.digitalWrite(motorRightPin, GPIO.LOW)
	GPIO.digitalWrite(motorLeftPin, GPIO.LOW)

# This functions sets the motor speed.
def setacceleration(value):

	global motorFspeed
	global motorRspeed
	global acceleration
	global minspeed
	global maxspeed

	acceleration = acceleration + value

	minspeed, maxspeed = getMinMaxSpeed()

	#Set Min and Max values for acceleration
	if(acceleration < -90):
		acceleration = -90

	if(acceleration > 90):
		acceleration = 90

	if(acceleration > 0):
		# drive forward
		forward()
		motorFspeed = acceleration
		motorRspeed = acceleration
		print("forward: ", motorFspeed, motorRspeed)
	elif(acceleration == 0):
		# stopp motors
		motorFspeed = acceleration
		motorRspeed = acceleration
		motorFspeed, motorRspeed, acceleration = stop()
		print("stop: ", motorFspeed, motorRspeed)
	else:
		# drive backward
		reverse()
		motorFspeed = (acceleration * -1)
		motorRspeed = (acceleration * -1)
		#print("backward: ", motorFspeed, motorRspeed)

	motorFspeed, motorRspeed = check_motorpseed(motorFspeed, motorRspeed)
	print("check: ", motorFspeed, motorRspeed)

def check_motorpseed(motorFspeed, motorRspeed):
	if (motorFspeed < minspeed):
		motorFspeed = minspeed

	if (motorFspeed > maxspeed):
		motorFspeed = maxspeed

	if (motorRspeed < minspeed):
		motorRspeed = minspeed

	if (motorRspeed > maxspeed):
		motorRspeed = maxspeed

	return motorFspeed, motorRspeed

# Set Min Max Speed
def getMinMaxSpeed():
	minspeed = 0
	maxspeed = 90
	return minspeed, maxspeed

# Get the motor speed
def getMotorSpeed():
	global motorFspeed
	global motorRspeed

	return motorFspeed, motorRspeed

def getMotorSpeedStep():
	return 10

def ButtonForward():
	fowardAcc = 0
	fowardAcc = getMotorSpeedStep()

	setacceleration(fowardAcc)

	motorFspeed, motorRspeed = getMotorSpeed()

	# percent calculation
	valueF = float(motorFspeed)/100
	valueR =  float(motorRspeed)/100

	GPIO.pwmWrite(motorFdPin, valueF)
	GPIO.pwmWrite(motorRdPin, valueR)

def ButtonReverse():
	backwardAcc = 0
	backwardAcc = getMotorSpeedStep()

	setacceleration((backwardAcc*-1))

	motorFspeed, motorRspeed = getMotorSpeed()

	# percent calculation
	valueF = float(motorFspeed)/100
	valueR =  float(motorRspeed)/100

	GPIO.pwmWrite(motorFdPin, valueF)
	GPIO.pwmWrite(motorRdPin, valueR)


def ButtonTurnLeft():
	stear_left()
	#print("LEFT: ",valueL,valueR,spotturn)

def ButtonTurnRight():
	stear_right()
	#print("RIGHT: ",valueL,valueR, spotturn)

def ButtonStop():
	center()
	stop()

try:
	print 'Press [ESC] to quit'
	while True:
		time.sleep(0.1)
		ButtonForward()
		time.sleep(2)
		ButtonStop()


	ButtonStop()
except KeyboardInterrupt:
	ButtonStop()

initiate()
GPIO.cleanup()
