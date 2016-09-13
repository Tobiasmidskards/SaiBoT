import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

for x in range (0,1):
  GPIO.output(7,True)
  print "Motor 1-7 is running"
  time.sleep(1)
  GPIO.output(7,False)
  GPIO.output(11,True)
  print "Motor 2-11 is running"
  time.sleep(1)
  GPIO.output(11,False)
  GPIO.output(13,True)
  print "Motor 3-13 is running"
  time.sleep(1)
  GPIO.output(13,False)
  GPIO.output(15,True)
  print "Motor 4-15 is running"
  time.sleep(1)
  GPIO.output(15,False)
  
GPIO.cleanup()

print "Test is complete."
