#!/usr/bin/python3
import Adafruit_DHT
import time
import requests

aio_username = ""  # Adafruit IO 帳號
aio_key = ""       # Adafruit IO 金鑰
aio_feed = "temp"  # Adafruit IO feed 名稱

try :
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(
                temperature, humidity), end=', ')
        
            data = {"value": temperature}

            # 設定 Adafruit IO 上傳資料的 API 網址
            url = ("https://io.adafruit.com/api/v2/" + aio_username +
                   "/feeds/" + aio_feed + "/data?X-AIO-Key=" + aio_key)

            # 用 POST 上傳 JSON 資料
            r = requests.post(url, json=data)

            if r.status_code == 200:
                print("已成功上傳")
            else:
                print("無法上傳: " + r.text)
        
            # 暫停 2 秒, 避免送出太多資料超過 Adafruit IO 免費額度
            time.sleep(2)
        else:
            time.sleep(1)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

