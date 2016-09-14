import pygame
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

def setboard():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)  # MOTOR 1-7
	GPIO.setup(11,GPIO.OUT)  # MOTOR 2-11
	GPIO.setup(13,GPIO.OUT)  # MOTOR 3-13
	GPIO.setup(15,GPIO.OUT)  # MOTOR 4-15

	GPIO.setup(12,GPIO.OUT)  # DISTANCE TRIGGER
	GPIO.setup(16, GPIO.IN)  # DISTANCE ECHO

def MotorOff():
	GPIO.output(7, GPIO.LOW)
	GPIO.output(11, GPIO.LOW)
	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)

def speed():
	global current
	current = 100

	for i in range (0,100):
		first = GPIO.PWM(7, 100)
		second = GPIO.PWM(11, 100)
		third = GPIO.PWM(13, 100)
		fourth = GPIO.PWM(15, 100)
		first.start(33)
		second.start(33)
		third.start(33)
		fourth.start(33)
		current = current - 5
		time.sleep(1)
		first.ChangeDutyCycle(current)
		MotorOff()
		print (current)

	MotorOff()
	PIO.cleanup()

setboard()
speed()
