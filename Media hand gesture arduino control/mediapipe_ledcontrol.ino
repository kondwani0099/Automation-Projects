const int ledPin = 13;  // Replace this with the GPIO pin connected to your LED
char signal;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    signal = Serial.read();
    if (signal == '1') {
      digitalWrite(ledPin, HIGH);  // Turn on the LED
    } else if (signal == '0') {
      digitalWrite(ledPin, LOW);  // Turn off the LED
    }
  }
}
