import pygame
import RPi.GPIO as GPIO
import time

# Controls the PWM speed.
global level
level = 0
speed = 33

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
	Hastighed = input ('skriv hastigheden:')
	if hastighed == 1:
		speed(1)

	while True:
		print(speed)
except KeyboardInterrupt:
	GPIO.cleanup()
