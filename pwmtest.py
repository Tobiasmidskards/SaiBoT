import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep  # pull in the sleep function from time module

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes. I use BCM

GPIO.setup(7, GPIO.OUT)# set GPIO 25 as output for white led
GPIO.setup(11, GPIO.OUT)# set GPIO 24 as output for red led
GPIO.setup(13, GPIO.OUT)# set GPIO 25 as output for white led
GPIO.setup(15, GPIO.OUT)# set GPIO 24 as output for red led

leftf = GPIO.PWM(7, 100)    # create object white for PWM on port 25 at 100 Hertz
leftb = GPIO.PWM(11, 100)      # create object red for PWM on port 24 at 100 Hertz

rightf = GPIO.PWM(13, 100)    # create object white for PWM on port 25 at 100 Hertz
rightb = GPIO.PWM(15, 100)      # create object red for PWM on port 24 at 100 Hertz

leftf.start(0)              # start white led on 0 percent duty cycle (off)
leftb.start(100)              # red fully on (100%)

rightf.start(0)              # start white led on 0 percent duty cycle (off)
rightb.start(100)              # red fully on (100%)

# now the fun starts, we'll vary the duty cycle to
# dim/brighten the leds, so one is bright while the other is dim

pause_time = 0.02           # you can change this to slow down/speed up

try:
    while True:
        for i in range(0,101):      # 101 because it stops when it finishes 100
            leftf.ChangeDutyCycle(i)
            rightf.ChangeDutyCycle(i)
            #red.ChangeDutyCycle(100 - i)
            sleep(pause_time)
        leftf.ChangeDutyCycle(0)
        rightf.ChangeDutyCycle(0)
        sleep(1)
        for i in range(100,-1,-1):      # from 100 to zero in steps of -1
            #white.ChangeDutyCycle(i)
            leftb.ChangeDutyCycle(100 - i)
            rightb.ChangeDutyCycle(100 - i)
            sleep(pause_time)
        leftb.ChangeDutyCycle(0)
        rightb.ChangeDutyCycle(0)
        sleep(1)

except KeyboardInterrupt:
    white.stop()            # stop the white PWM output
    red.stop()              # stop the red PWM output
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
