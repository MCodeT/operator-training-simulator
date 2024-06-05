// Define the pin for the limit switch
const int switchPin = 2;
// Define the pin for the LED
const int ledPin = 13;

// Define variables for timer and switch state
unsigned long startTime = 0;
unsigned long elapsedTime = 0;
bool switchState = false;
bool timerStarted = false;
const unsigned long timeoutPeriod = 10000; // Timeout period in milliseconds (10 seconds)

void setup() {
  // Set the switch pin as input
  pinMode(switchPin, INPUT);
  // Set the LED pin as output
  pinMode(ledPin, OUTPUT);
  
  // Initialize Serial communication for debugging
  Serial.begin(9600);
}

void loop() {
  // Read the state of the switch
  switchState = digitalRead(switchPin);

  // Check if the switch is turned on
  if (switchState == HIGH) {
    // Record the start time if it's the first time the switch is on
    if (!timerStarted) {
      startTime = millis();
      timerStarted = true;
      Serial.println("Timer started!");
    }
    // Calculate elapsed time since the switch was turned on
    elapsedTime = millis() - startTime;
    // Blink the LED while the switch is on
    digitalWrite(ledPin, HIGH);
  } else {
    // Reset the timer if the switch is turned off
    startTime = 0;
    elapsedTime = 0;
    timerStarted = false;
    // Turn off the LED
    digitalWrite(ledPin, LOW);
  }

  // Check if the switch has been turned on within the timeout period
  if (timerStarted && elapsedTime >= timeoutPeriod) {
    Serial.println("Timeout reached!");
    timerStarted = false; // Reset timer
  }

  // Check if the switch has been on for at least 5 seconds
  if (timerStarted && elapsedTime >= 5000) {
    Serial.println("Well done!");
    timerStarted = false; // Reset timer
  }

  // Delay to control loop execution speed
  delay(100);
}

