import pygame
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# Controls the PWM speed.
global level
level = 0
speed = 33

def setboard():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(18, GPIO.OUT) # LED WHITE
	GPIO.setup(40, GPIO.OUT) # LED RED

	GPIO.setup(7, GPIO.OUT)  # MOTOR 1-7
	GPIO.setup(11,GPIO.OUT)  # MOTOR 2-11
	GPIO.setup(13,GPIO.OUT)  # MOTOR 3-13
	GPIO.setup(15,GPIO.OUT)  # MOTOR 4-15

	GPIO.setup(12,GPIO.OUT)  # DISTANCE TRIGGER
	GPIO.setup(16, GPIO.IN)  # DISTANCE ECHO

def speed(level):

	first = GPIO.PWM(7, 100)
	second = GPIO.PWM(11, 100)
	third = GPIO.PWM(13, 100)
	fourth = GPIO.PWM(15, 100)

	if level == 0:
		speed = 33
	elif level == 1:
		speed = 66
	elif level == 2:
		speed = 100

	first.ChangeDutyCycle(speed)
	second.ChangeDutyCycle(speed)
	third.ChangeDutyCycle(speed)
	fourth.ChangeDutyCycle(speed)

try:
	print(speed)
	hastighed = input ('skriv hastigheden:')
	if hastighed == 1:
		speed(1)

	while True:
		print(speed)
except KeyboardInterrupt:
	GPIO.cleanup()
