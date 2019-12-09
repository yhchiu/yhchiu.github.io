#!/usr/bin/python3
import RPi.GPIO as GPIO
import datetime
import time
import os

pins = {
   23 : {'name' : 'GPIO 23', 'state' : GPIO.LOW},
   24 : {'name' : 'GPIO 24', 'state' : GPIO.LOW}
   }

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

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
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   templateData = {
      'pins' : pins
      }
   return render_template('lab03.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   if action == "on":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   return main()

@app.route("/led/<action>")
def led(action):
   os.system("sudo echo gpio > /sys/class/leds/led0/trigger")
   if action == "on":
     os.system("sudo echo 1 > /sys/class/leds/led0/brightness")
   if action == "off":
     os.system("sudo echo 0 > /sys/class/leds/led0/brightness")

   return main()


if __name__ == "__main__":
   print("Web server 網址 http://" + get_localip())
   app.run(host='0.0.0.0', port=80, debug=True)

