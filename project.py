from gpiozero import LED
import RPi.GPIO as GPIO
import adafruit_dht
import board
import time

# LED Setup
led1 = LED(14)
led2 = LED(15)
led3 = LED(27)
led4 = LED(22)
led5 = LED(2)
led6 = LED(3)

# Ultrasonic Sensor GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# IR Sensor GPIO Pin
IR_PIN = 16

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# DHT Sensor Setup
dht_device = adafruit_dht.DHT11(board.D20)

def US():
    # Set the trigger to high
    GPIO.output(GPIO_TRIGGER, True)

    # Wait for a short time and then set the trigger to low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Wait for the echo pin to go high and then start a timer
    start_time = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Wait for the echo pin to go low and then stop the timer
    stop_time = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Calculate the time difference and convert to distance in centimeters
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    print(f"Distance: {distance:.2f} cm")
    
    return distance

def IR():
    if GPIO.input(IR_PIN):
        led3.on()
        led4.off()
    else:
        led4.on()
        led3.off()

def DTH():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature:.1f} °C  Humidity: {humidity:.1f}%")
        
        if temperature > 28:
            led5.on()
            led6.off()
        else:
            led5.off()
            led6.on()

    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(f"Runtime Error: {error.args[0]}")
    except Exception as error:
        dht_device.exit()
        raise error

# Main loop
try:
    while True:
        # Read the distance measured by the ultrasonic sensor
        dist = US()

        # Turn the LED on or off based on the distance
        if dist < 20:
            led1.on()
            led2.off()
        else:
            led2.on()
            led1.off()

        IR()
        DTH()
        
        # Wait a short time before measuring the distance again
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
