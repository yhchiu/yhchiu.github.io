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

shock_time = 0
while True:
    if shock.value() == 1:
        shock_time = time.time()
        print("感應到振動")

    if shock_time and (time.time() - shock_time) > 60:
        print("很久沒有動了! 發送LINE通知!")

        # 連線 LINE API 發送 LINE 通知
        headers = {
          "Authorization": "Bearer " + line_token, 
          "Content-Type" : "application/x-www-form-urlencoded"
        }
        # 因為 MicroPython 沒有 urlencode 函式, 所以必須先使用其他工具將訊息字串 urlencode
        payload = 'message=%E5%B0%8F%E5%AD%A9%E7%9D%A1%E8%A6%BA%E5%BE%88%E4%B9%85%E6%B2%92%E6%9C%89%E5%8B%95%E4%BA%86%EF%BC%8C%E8%B6%95%E5%BF%AB%E5%8E%BB%E7%9C%8B%E7%9C%8B!'
        urequests.post("https://notify-api.line.me/api/notify",
                      headers = headers, data = payload)
    
        shock_time = 0
