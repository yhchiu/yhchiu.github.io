from machine import Pin
import time, network, urequests

# 請在以下變數設定 LINE Notify 的權杖
line_token  = ""

# 連線 Wifi 網路 
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Wifi基地台", "Wifi密碼")
while not sta_if.isconnected():
    pass
print("Wifi已連上")

# 建立 16 號腳位的 Pin 物件, 設定為輸入腳位, 並命名為 shock
shock = Pin(16, Pin.IN)

while True:
    if shock.value() == 1:
        print("感應到振動! 發送LINE通知!")

        # 連線 LINE API 發送 LINE 通知
        headers = {
          "Authorization": "Bearer " + line_token, 
          "Content-Type" : "application/x-www-form-urlencoded"
        }
        # 因為 MicroPython 沒有 urlencode 函式, 所以必須先使用其他工具將訊息字串 urlencode
        payload = 'message=%E6%9C%89%E4%BA%BA%E6%89%93%E9%96%8B%E4%BF%9D%E9%9A%AA%E7%AE%B1%E5%9C%A8%E7%BF%BB%E6%89%BE%E6%9D%B1%E8%A5%BF%2C%E8%B6%95%E5%BF%AB%E5%8E%BB%E6%8A%93%E5%B0%8F%E5%81%B7'
        r =urequests.post("https://notify-api.line.me/api/notify",
                      headers = headers, data = payload)
        print(r.json())
    
        # 暫停 60 秒, 避免短時間內一直收到重複的警報
        time.sleep(60)
    else:
        time.sleep(1)

