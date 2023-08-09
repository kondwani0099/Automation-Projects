/* 
***************************Code Description********************************************
This code is used to move the robotic arm clockwise ,anti clockwise and neutral position.
The micro controller receives the information from the camera through the computer vision 
algorithm to manipulate the arm based on the color detected.

************************* Instructions **************************************************
1. Choose the type of board and connect the   IDE port to the microcontroller board
2. Compile and upload the code into the microcontroller 
3. Connect the L298N motor driver ,ultra Sonic sensor and servo motor to the  pins below
*/
#include <Servo.h> //servo motor library

//Intialization of the servo object
Servo myservo;

const int trigPin = 2;  // Trig pin of ultrasonic sensor
const int echoPin = 3;  // Echo pin of ultrasonic sensor

long duration;
int distance;

// Motor control pins
int in1Pin = 9;
int in2Pin = 10;
int enablePin = 11; // Connect to the ENA pin on the L298N

void setup() {
   // Set motor control pins as OUTPUT
  pinMode(in2Pin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  
  Serial.begin(9600);//serial communication baud rate
  myservo.attach(5);  // Attach the servo to pin 5

  // Setting ultra sonic pins as OUTPUT and INPUT 
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  //this part of the code enables the ultra sonic to detect objects on the convey belt
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  ///Serial.print("Distance: ");
  //Serial.print(distance);
  //Serial.println(" cm");
  
if (distance > 10 && distance < 80) { 
  // If an object is detected above 10cm the convey continues moving 
  
    digitalWrite(in2Pin, HIGH);
    digitalWrite(in1Pin, LOW);
    analogWrite(enablePin, 210);
    delay(50);
   
} else {
  // If an object is detected within 10 cm
  // This part switches off the convey  belt motor 
   digitalWrite(in2Pin, HIGH);
    digitalWrite(in1Pin, LOW);
    analogWrite(enablePin, 0);
    delay(50);
}
  if (Serial.available() > 0) {
      char receivedData = Serial.read();// gets the information from the serial communication port ,receiving data from a python algorithm
      if (receivedData == 'R') {
         myservo.writeMicroseconds(2000); // Set servo angle for red
        
      } else if (receivedData == 'G') {
         myservo.writeMicroseconds(1000);  // Set servo angle for green
      
      } else if (receivedData == 'B') {
         myservo.writeMicroseconds(1500);  // Set servo angle for blue
        
      }
  }

  
}
  

