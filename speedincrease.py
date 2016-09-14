import pygame
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def MotorOff():
	GPIO.output(DRIVE_1, GPIO.LOW)
	GPIO.output(DRIVE_2, GPIO.LOW)
	GPIO.output(DRIVE_3, GPIO.LOW)
	GPIO.output(DRIVE_4, GPIO.LOW)

def speed(level):
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
