import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)

pwm = GPIO.PWM(13, 50)

pwm.start(0)

pwm.ChangeDutyCycle(10)
time.sleep(1)

pwm.stop()
GPIO.cleanup()