import pygame, sys, terminos, tty
from pygame.locals import *
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# Variabels
speedCount = 0

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


def forward():
	print('Forward')
	acceleration(7)

def backward():
	print('Backward')

def left():
	print('Left')

def right():
	print('Right')

def stop():
	print('Stop')
	GPIO.output(7,False)
	GPIO.output(11,False)
	GPIO.output(13,False)
	GPIO.output(15,False)

# p = GPIO.PWM(7, 50) # Channel = 12 frequency = 50Hz
# p.start(0)

keydown = False

def acceleration(x: int):
	p = GPIO.PWM(x , 50)
	p.ChangeFrequency(100)
	p.start(speedCount)
	global speedCount
	global keydown
	while keydown == True & speedCount < 100:
		speedCount = (speedCount + 10)
		p.ChangeDutyCycle(speedCount)
		time.sleep(0.2)
	while keydown == True & speedCount == 100:
		p.ChangeDutyCycle(100)
		time.sleep(0.2)
	p.stop()
	speedCount = 0
	stop()

pygame.init()
pygame.display.set_mode((300,300))
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
		if event.type == pygame.KEYDOWN:

			global keydown
			keydown = True

			global speedCount
			print(speedCount)

			if event.key == pygame.K_w:
				forward()

			elif event.key == pygame.K_s:
				backward()

			elif event.key == pygame.K_a:
				left()

			elif event.key == pygame.K_d:
				right()

			elif event.key == pygame.K_k:
				stop()

		else: 
			global keydown
			keydown = False

GPIO.cleanup()
















