#include <NewPing.h>

#define TRIGGER_PIN  9  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 20 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

#define max_speed  150

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

void Forward(int a, int b) {
  digitalWrite(5, LOW);
  analogWrite(6, b);
  digitalWrite(10, LOW);
  analogWrite(11, a);
}

void Backward() {
  digitalWrite(5, HIGH);
  digitalWrite(6, LOW);
  digitalWrite(10, HIGH);
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
  
  if (action == false || (0 < dist && dist <= 15)) {
    Stop();
  }

  if (Serial.available()) {
    action = true;
    int cmd = Serial.read();

    if (cmd == 'm') {
      Stop();
      delay(1000);
      action = false;
    }

    else if (cmd >= 0 && cmd < 50) {
      int speed_pwm = map(cmd, 0, 49, 0, max_speed); //位置轉換成左輪速度      越中間速度越快
      Forward(speed_pwm, max_speed);

    }
    else if (cmd >= 50 && cmd <= 100) {
      int speed_pwm = map(cmd, 100, 50, 0, max_speed); //位置轉換成右輪速度     越中間速度越快
      Forward(max_speed, speed_pwm);
    }


    //delay(5);
  }

}

