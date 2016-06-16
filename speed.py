import pygame
import RPi.GPIO as GPIO
import time

# Controls the PWM speed.
global level
global current
level = 0
current = 33

def setboard():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)  # MOTOR 1-7
	GPIO.setup(11,GPIO.OUT)  # MOTOR 2-11
	GPIO.setup(13,GPIO.OUT)  # MOTOR 3-13
	GPIO.setup(15,GPIO.OUT)  # MOTOR 4-15

setboard()

def speed(level):
	global current
	first = GPIO.PWM(7, 100)
	second = GPIO.PWM(11, 100)
	third = GPIO.PWM(13, 100)
	fourth = GPIO.PWM(15, 100)
	
	first.start(33)
	second.start(33)
	third.start(33)
	fourth.start(33)

	if level == 0:
		current = 33
	elif level == 1:
		current = 66
	elif level == 2:
		current = 100
	else:
		print('doesnt work')

	first.ChangeDutyCycle(current)
	second.ChangeDutyCycle(current)
	third.ChangeDutyCycle(current)
	fourth.ChangeDutyCycle(current)

try:
	print(current)

	while True:
		hastighed = input ('skriv hastigheden:')
		if hastighed == 0:
			speed(0)
		elif hastighed == 1:
			speed(1)
		else:
			speed(2)
		print(current)
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
