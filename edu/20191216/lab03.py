import paho.mqtt.client as mqtt
import Adafruit_DHT
import time

mqtt_username = ""  # Adafruit IO 帳號
mqtt_password = ""  # Adafruit IO 金鑰

mqtt_broker_server = "io.adafruit.com"
mqtt_topic = mqtt_username + "/feeds/temp_humi"  # 頻道名稱 

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_broker_server, 1883)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        if humidity is not None and temperature is not None:
            temp_humi = "%2d ℃/%2d%%" % (temperature, humidity)
            print(temp_humi)
            client.publish(mqtt_topic, temp_humi)
        else:
            print('Failed to get reading. Try again!')

        time.sleep(3)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

