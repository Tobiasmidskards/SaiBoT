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


UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
STOP = 'stop'

def runGame():
	direction = STOP
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == KEYDOWN:
				if event.key == (K_LEFT or K_a):
					direction = LEFT

				elif event.key == K_RIGHT:
					direction = RIGHT

				elif event.key == K_UP:
					direction = UP

				elif event.key == K_DOWN:
					direction = DOWN
		
		if direction == UP:
			print ('UP') 


GPIO.cleanup()
















