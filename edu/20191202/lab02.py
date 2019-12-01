#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import requests

username = ""  #簡訊服務帳號
passwd = ""    #簡訊服務密碼
phone = ""     #接收簡訊的手機號碼
message = "有小偷!超音波感測器偵測到有人接近!" #請勿輸入空格

GPIO.setmode(GPIO.BOARD)
TRIGGER_PIN = 16
ECHO_PIN    = 18
GPIO.setup(TRIGGER_PIN,  GPIO.OUT)
GPIO.setup(ECHO_PIN,     GPIO.IN)
GPIO.output(TRIGGER_PIN, GPIO.LOW)
v = 343		# (331 + 0.6*20)

def measure() :
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)	# 10uS 
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    pulse_start = None
    pulse_end   = None

    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    t = pulse_end - pulse_start

    d = t * v
    d = d/2

    return d*100

def measure_average() :
    d1 = measure()
    time.sleep(0.05)
    d2 = measure()
    time.sleep(0.05)
    d3 = measure()
    distance = (d1 + d2 + d3) / 3
	
    return distance

try :
    while True:
        distance = measure_average()
        print("Distance: %.1f (cm)" % distance)

        if distance <= 50:
            print("感應到有人接近,發送訊息!")
        
            # 連線簡訊服務發送簡訊通知
            requests.get(
                "http://api.message.net.tw/send.php?mtype=G&id="
                + username + "&encoding=utf8&password=" + passwd
                + "&tel=" + phone + "&msg=" + message)
        
            # 暫停 60 秒, 避免短時間內一直收到重複的警報
            time.sleep(60)
        else:
            time.sleep(1)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

finally:
    GPIO.cleanup()          
