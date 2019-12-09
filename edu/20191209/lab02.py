#!/usr/bin/python3
import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIGGER_PIN = 16
ECHO_PIN    = 18
GPIO.setup(TRIGGER_PIN,  GPIO.OUT)
GPIO.setup(ECHO_PIN,     GPIO.IN)
GPIO.output(TRIGGER_PIN, GPIO.LOW)
v = 343         # (331 + 0.6*20)

def measure() :
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001) # 10uS
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
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'HELLO Flask',
      'time': timeString
      }
    return render_template('lab01.html', **templateData)

@app.route("/dist")
def distance():
    cm = measure_average()
    return render_template('lab02.html', distance = cm)

if __name__ == "__main__":
    print("Web server 網址 http://" + get_localip())
    app.run(host='0.0.0.0', port=80, debug=True)

