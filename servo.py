import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BOARD)


GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50)

GPIO.setup(13,GPIO.OUT)
servo2 = GPIO.PWM(13,50)

servo1.start(7)
servo2.start(7)

time.sleep(2)


GPIO.cleanup()
print("eol")
