// Define pin connections
const int sensorPin = 2; // Pin connected to the output pin of the RC-51 sensor

// Variables to keep track of rotations
volatile int rotationCount = 0;
unsigned long previousMillis = 0;
const unsigned long interval = 10000; // Time period in milliseconds (10 seconds)

// Flag to indicate when the sensor detects a passing mark
volatile bool detected = false;

// Flag to indicate whether counting is active
bool countingActive = true;

void setup() {
  // Initialize the sensor pin as an input
  pinMode(sensorPin, INPUT);

  // Begin serial communication for debugging at 9600 baud
  Serial.begin(9600);

  // Attach an interrupt to the sensor pin
  attachInterrupt(digitalPinToInterrupt(sensorPin), countRotation, FALLING);

  // Save the current time
  previousMillis = millis();
}

void loop() {
  // Get the current time
  unsigned long currentMillis = millis();

  // Check if the interval time has passed
  if (countingActive && currentMillis - previousMillis >= interval) {
    // Save the current time
    previousMillis = currentMillis;

    // Print the number of rotations
    Serial.print("Rotations in the last ");
    Serial.print(interval / 1000);
    Serial.print(" seconds: ");
    Serial.println(rotationCount);

    // Stop the counting
    countingActive = false;
  }
}

// Interrupt service routine to count rotations
void countRotation() {
  if (countingActive && !detected) {
    rotationCount++;
    detected = true;
  } else {
    detected = false;
  }
}
