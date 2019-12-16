#include <NewPing.h>

#define TRIGGER_PIN  9  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 20 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

#define max_speed  200
int speed_step = max_speed/5;

bool action = false;
int dist = 100;

void setup() {
  Serial.begin(115200);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(13, OUTPUT);
  Stop();
}

void Forward(int left, int right) {
  digitalWrite(5, LOW);
  analogWrite(6, right*speed_step);
  digitalWrite(10, LOW);
  analogWrite(11, left*speed_step);
}

void Backward(int left, int right) {
  analogWrite(5, right*speed_step);
  digitalWrite(6, LOW);
  analogWrite(10, left*speed_step);
  digitalWrite(11, LOW);
}

void Stop() {
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(10, LOW);
  digitalWrite(11, LOW);
}

void loop() {
  dist = sonar.ping_cm();
  
  if (0 < dist && dist <= 15) {
    Stop();
  }
  else {
    if (Serial.available()) {
      //action = true;
      int cmd = Serial.read();
  
      if (cmd == 0) {
        Stop();
        delay(1000);
        //action = false;
      }
  
      else if (cmd >= 1 && cmd <= 55) {
        //int speed_pwm = map(cmd, 0, 49, 0, max_speed); //位置轉換成左輪速度      越中間速度越快
        Forward(cmd/10, cmd%10);
  
      }
      else if (cmd >= 101 && cmd <= 155) {
        //int speed_pwm = map(cmd, 100, 50, 0, max_speed); //位置轉換成右輪速度     越中間速度越快
        cmd = cmd - 100;
        Backward(cmd/10, cmd%10);
      }    

      //delay(5);
    }
  }
}

