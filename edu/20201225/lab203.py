from machine import Pin
import time, network, urequests
from umqtt.robust import MQTTClient

# 連線 Wifi 網路 
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Wifi基地台", "Wifi密碼")
while not sta_if.isconnected():
    pass
print("Wifi已連上")

 client = MQTTClient(
     client_id="weather", 
     server="io.adafruit.com", 
     user="帳戶名稱", 
     password="填入你的金鑰",
     ssl=False)
client.connect()

# 建立 16 號腳位的 Pin 物件, 設定為輸入腳位, 並命名為 shock
shock = Pin(16, Pin.IN)

shock_value = "0"
shock_value_last = "0"
while True:
    if shock.value() == 1:
        shock_value = "1"
    else:
        shock_value = "0"

    if not shock_value == shock_value_last:
        print("發送到MQTT伺服器: " + shock_value)
        client.publish(
            b"帳戶名稱/feeds/sleep",
            shock_value.encode())
        time.sleep(10)
    
    shock_value_last = shock_value

