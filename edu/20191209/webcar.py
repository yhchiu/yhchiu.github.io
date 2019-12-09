#!/usr/bin/python3
import serial
import time

#初始化序列通訊埠
#ser=serial.Serial('/dev/ttyUSB0',115200)
ser=serial.Serial('/dev/ttyAMA0',115200)

import socket
def get_localip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
   return render_template('webcar.html')

@app.route("/run/<left>/<right>")
def run(left, right):
    left = int(left)
    right = int(right)
    if left == 0 and right == 0:
        offset = 109
        print("停車")
        #ser.write(b'm')  #要求停車
    elif left == right:
        offset = 50  
        print("前進")
    elif left > right:
        if right > 0 and right >= 2:
            offset = 25
            print("左前")
        else:
            offset = 0  
            print("左轉")
    elif left < right:
        if left > 0 and left >= 2:
            offset = 75
            print("右前")
        else:
            offset = 100  
            print("右轉")

    #ser.write(chr(offset).encode('utf-8'))   #傳送數值給 Arduino
    return "OK"


if __name__ == "__main__":
    print("Web server 網址 http://" + get_localip())
    app.run(host='0.0.0.0', port=80, debug=True)
    ser.close()      #關閉序列埠

