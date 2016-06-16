import pygame
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# Variabels.
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
	GPIO.cleanup()

# p = GPIO.PWM(7, 50) # Channel = 12 frequency = 50Hz
# p.start(0)

keydown = False

def acceleration(x):
	p = GPIO.PWM(x , 50)
	p.ChangeFrequency(100)
	global speedCount
	p.start(speedCount)
	global keydown
	while keydown == True and speedCount < 100:
		speedCount = (speedCount + 10)
		p.ChangeDutyCycle(speedCount)
		time.sleep(0.2)
	while keydown == True and speedCount == 100:
		p.ChangeDutyCycle(100)
		time.sleep(0.2)
	p.stop()
	speedCount = 0
	stop()

global hadEvent
global UP
global DOWN
global LEFT
global RIGHT
global STOP
global QUIT

hadEvent = True
UP = False
DOWN = False
RIGHT = False
LEFT = False
STOP = False
QUIT = False
pygame.init()
screen = pygame.display.set_mode([300, 100])
pygame.display.set_caption("SaiBoT - Press [ESC] to quit")

def runGame(events):
	setboard()
	global hadEvent
	global UP
	global DOWN
	global LEFT
	global RIGHT
	global STOP
	global QUIT
	for event in events:
			if event.type == pygame.QUIT:
				hadEvent = True
				QUIT = True

			elif event.type == KEYDOWN:

				hadEvent = True
				if event.key == K_a:
					UP = True

				elif event.key == K_d:
					RIGHT = True

				elif event.key == K_w:
					UP = True

				elif event.key == K_s:
					DOWN = True

				elif event.key == K_ESCAPE:
					QUIT = True
			elif event.type == KEYUP:
				hadEvent = True

				if event.key == K_a:
					UP = False

				elif event.key == K_d:
					RIGHT = False

				elif event.key == K_w:
					UP = False

				elif event.key == K_s:
					DOWN = False

				elif event.key == K_ESCAPE:
					QUIT = False
		
try:
	print 'Press [ESC] to quit'
	while True:
		runGame(pygame.event.get())
		print('looping')
		if hadEvent:
			hadEvent = False
			print('had event')
			if QUIT:
				break
			elif UP:
				forward()
		time.sleep(0.1)
	stop()
except KeyboardInterrupt:
	stop()



















