import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, True)
time.sleep(2)
GPIO.output(27, False)
time.sleep(2)
GPIO.cleanup()