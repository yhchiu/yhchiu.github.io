#!/usr/bin/python3

import datetime

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
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO Flask',
      'time': timeString
      }
   return render_template('lab01.html', **templateData)

if __name__ == "__main__":
   print("Web server 網址 http://" + get_localip())
   app.run(host='0.0.0.0', port=80, debug=True)

