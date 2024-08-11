import adafruit_dht #pip install Adafruit_CircuitPython_DHT --break-system-package
import board
import time

# Initialize the DHT device, with data pin connected to GPIO14:
dht_device = adafruit_dht.DHT11(board.D14)

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature:.1f} C  Humidity: {humidity:.1f}%")
    except RuntimeError as error:
        # Errors happen fairly often with DHT sensors, just keep going
        print(error.args[0])
    except Exception as error:
        dht_device.exit()
        raise error

    # Wait for a while before attempting to read again
    time.sleep(2.0)
