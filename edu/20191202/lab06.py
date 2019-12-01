import Adafruit_DHT
import time
import requests

# 請在以下變數設定 Google App Scripts 網址
app_scripts = ""

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(
                temperature, humidity))
            requests.get("{0}?t={1:0.1f}".format(app_scripts, temperature))
        else:
            print('Failed to get reading. Try again!')

        time.sleep(5)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

