import paho.mqtt.client as mqtt
import time

mqtt_username = ""  # Adafruit IO 帳號
mqtt_password = ""  # Adafruit IO 金鑰

mqtt_broker_server = "io.adafruit.com"
mqtt_topic = mqtt_username + "/feeds/fan"  # 頻道名稱

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc):
    print("已經連上 MQTT 伺服器!")
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    data = msg.payload.decode("utf-8")
    print( "Topic: ", msg.topic + "\nMessage: " + data)

    if data == "on":
        print("開燈")
        os.system("sudo echo gpio > /sys/class/leds/led0/trigger")
        os.system("sudo echo 1 > /sys/class/leds/led0/brightness")
    elif data == "off":
        print("關燈")
        os.system("sudo echo gpio > /sys/class/leds/led0/trigger")
        os.system("sudo echo 0 > /sys/class/leds/led0/brightness")

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_server, 1883)

client.loop_forever()
client.disconnect()


