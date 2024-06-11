int ir = 7;
int led = 13; // You can change this to the pin you connected your LED to
bool holeDetected = false;
bool appRunning = false;

#define ARDUINO_TYPE "Counter" // Define a unique identifier for this Arduino

void setup() {
  pinMode(ir, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  appRunning = false;
}

void loop() {
  // Check for incoming serial data
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any extra whitespace or newlines

    // Respond to the IDENTIFY command
    if (command == "IDENTIFY" || command == "RUNNING") {
      appRunning = true;
      if (command == "IDENTIFY") {
        Serial.println(ARDUINO_TYPE);
      }
    } else if (command == "CLOSE") {
      appRunning = false;
    }
  }

  if (appRunning) {
    if (digitalRead(ir) == HIGH) {
      if (!holeDetected) {
        Serial.println("Hole detected");
        digitalWrite(led, HIGH); // Turn on the LED
        holeDetected = true;
      }
    } else {
      holeDetected = false;
      digitalWrite(led, LOW); // Turn off the LED
    }
  }

  delay(10);
}
