#include <Servo.h>

Servo myservo;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // Attach the servo to pin 9
}

void loop() {
  if (Serial.available() > 0) {
    char receivedData = Serial.read();
    if (receivedData == 'R') {
      // Move servo to predefined position for red
      myservo.write(0); // Set servo angle (adjust this value as per your servo's requirements)
    } else if (receivedData == 'G') {
      // Move servo to predefined position for green
      myservo.write(90); // Set servo angle (adjust this value as per your servo's requirements)
    } else if (receivedData == 'B') {
      // Move servo to predefined position for blue
      myservo.write(180); // Set servo angle (adjust this value as per your servo's requirements)
    }
  }
}
