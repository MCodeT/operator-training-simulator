int ir = 7;
int led = 13; // You can change this to the pin you connected your LED to
bool holeDetected = false;

void setup() {
  pinMode(ir, INPUT);
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
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
  delay(100); // Debounce delay to avoid multiple counts in a single detection
}
