import RPi.GPIO as GPIO
import time

# Set GPIO mode and pins
GPIO.setmode(GPIO.BCM)
TRIGGER_PIN = 14
ECHO_PIN = 15
LED_PIN = 18

# Set maximum distance and threshold
MAX_DISTANCE = 10  # Maximum distance in centimeters

# Setup GPIO pins
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Create PWM object for LED
led = GPIO.PWM(LED_PIN, 100)
led.start(0)

# Function to measure distance
def measure_distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # Speed of sound is approximately 34300 cm/s

    return distance

try:
    while True:
        dist = measure_distance()
        print("Measured Distance = {:.1f} cm".format(dist))

        if 0 < dist <= MAX_DISTANCE:
            duty_cycle = (MAX_DISTANCE - dist) * 6.25
            led.ChangeDutyCycle(duty_cycle)
        else:
            led.ChangeDutyCycle(0)
        
        time.sleep(0.1)  # Add a small delay to control the update rate

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    led.stop()
    GPIO.cleanup()
