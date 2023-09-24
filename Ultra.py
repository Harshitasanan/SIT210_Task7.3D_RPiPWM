import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED = 18
GPIO_TRIGGER = 14
GPIO_ECHO = 15

MAX_DISTANCE = 10

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

led = GPIO.PWM(LED, 100)
led.start(0)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2  # Speed of sound is approximately 34300 cm/s
    
    return distance

try:
    while True:
        dist = distance()
        print("Measured Distance = %.1f cm" % dist)

        if dist <= MAX_DISTANCE and dist > 0:
            duty_cycle = (MAX_DISTANCE - dist) * 6.25
            led.ChangeDutyCycle(duty_cycle)
        else:
            led.ChangeDutyCycle(0)
        time.sleep(0.1)  # Add a small delay to control the update rate
except KeyboardInterrupt:
    print("Measurement stopped by user")

led.stop()
GPIO.cleanup()
