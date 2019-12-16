import paho.mqtt.client as mqtt

mqtt_username = "emailtest777"  # Adafruit IO 帳號
mqtt_password = "52696a2ea66e4968b0ca27cdf2208b82"  # Adafruit IO 金鑰

mqtt_broker_server = "io.adafruit.com"
mqtt_topic = mqtt_username + "/feeds/temp_humi"  # 頻道名稱

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc):
    print("已經連上 MQTT 伺服器!")
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    data = msg.payload.decode("utf-8")
    print( "Topic: ", msg.topic + "\nMessage: " + data)

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_server, 1883)

client.loop_forever()
client.disconnect()

