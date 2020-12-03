from machine import Pin
import time
import network, urequests
import dht

ifttt_key = "IFTTT的金鑰"
ifttt_event = "weather"

sensor = dht.DHT11(Pin(0))                # 使用 D3 腳位取得溫溼度物件

sta_if = network.WLAN(network.STA_IF)     # 取得無線網路介面
sta_if.active(True)                       # 啟用無線網路
sta_if.connect('無線網路名稱', '密碼')      # 連結無線網路
while not sta_if.isconnected():           # 等待無線網路連上
    pass
print("connected")

while True:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    urequests.get("https://maker.ifttt.com/trigger/%s/"
                  "with/key/%s?value1=%2d&value2=%2d" % (
                  ifttt_event, ifttt_key, temperature, humidity))
    print("發送溫溼度紀錄")

    time.sleep(3)