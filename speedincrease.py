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
	GPIO.output(DRIVE_1, GPIO.LOW)
	GPIO.output(DRIVE_2, GPIO.LOW)
	GPIO.output(DRIVE_3, GPIO.LOW)
	GPIO.output(DRIVE_4, GPIO.LOW)

def speed():
	global current
	current = 0
	first = GPIO.PWM(7, 100)
	second = GPIO.PWM(11, 100)
	third = GPIO.PWM(13, 100)
	fourth = GPIO.PWM(15, 100)
	first.start(33)
	second.start(33)
	third.start(33)
	fourth.start(33)

	time.sleep(3)
	for i in 100:
		current = current + 1
		time.sleep(0.5)
		first.ChangeDutyCycle(current)

	MotorOff()
	PIO.cleanup()

setboard()
speed()
