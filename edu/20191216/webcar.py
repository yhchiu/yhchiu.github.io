#!/usr/bin/python3
import serial
import time

#初始化序列通訊埠
#ser=serial.Serial('/dev/ttyUSB0',115200)
ser=serial.Serial('/dev/ttyAMA0',115200)

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
        offset = 0
        print("停車")
    elif left > 0 or right > 0:
        offset = left * 10 + right  
        print("往前, 左馬達:{} 右馬達:{}".format(left, right))
    elif left < 0 or right < 0:
        offset = abs(left) * 10 + abs(right) + 100 
        print("往後, 左馬達:{} 右馬達:{}".format(left, right))

    ser.write(chr(offset).encode('utf-8'))   #傳送數值給 Arduino
    return "OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    ser.close()      #關閉序列埠

