import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT) #IN1
GPIO.setup(18, GPIO.OUT) #IN2
GPIO.setup(22, GPIO.OUT) #EN1

pwm = GPIO.PWM(22, 100) #100hz
pwm.start(80) #start pwm with 0 duty so it doesn't run yet
time.sleep(5)
#Move forward    
GPIO.output(16, False)
GPIO.output(18, True)
pwm.ChangeDutyCycle(40)
#GPIO.output(22, True)
time.sleep(5)
pwm.stop()
GPIO.cleanup()