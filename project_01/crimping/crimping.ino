
// Define the pin numbers
const int buttonPin = 2;       // Pin where the main switch is connected
const int ledPin = 13;         // Pin for the green LED
const int wirePin = 4;         // Pin where one side of the wire switch is connected
const int redLedPin = 11;      // Pin for the red LED
const int otherWirePin = 7;    // Pin where the other side of the wire switch is connected
const int buzzerPin = 10;      // Pin where the buzzer is connected

int buttonState = 0;           // Variable to store the state of the main switch
int wireState = 0;             // Variable to store the state of the wire switch
int buzzerState = 0;           // Variable to store the state of the buzzer sound
bool wasPressed = false;

void setup() {
  // Initialize the pins
  pinMode(buttonPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(wirePin, INPUT);
  pinMode(redLedPin, OUTPUT);
  pinMode(otherWirePin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the state of the main switch
  buttonState = digitalRead(buttonPin);
  
  // Read the state of the wire switches
  wireState = digitalRead(wirePin);
  int otherWireState = digitalRead(otherWirePin);
  
  // Check if the main switch is pressed
  if (buttonState == LOW) {
    // Main switch is pressed
    // Check the state of the wire switches
    if (wireState == HIGH && otherWireState == HIGH) {
      // Both wires are not touching
      if(!wasPressed){
        Serial.println("GREEN");
        wasPressed = true;
      }
      digitalWrite(ledPin, HIGH);    // Turn on the green LED
      digitalWrite(redLedPin, LOW);  // Turn off the red LED
      buzzerState = 1;               // Set buzzer state to play sound 1
    } else {
      // At least one wire is touching
      Serial.println("RED");
      digitalWrite(ledPin, LOW);     // Turn off the green LED
      digitalWrite(redLedPin, HIGH); // Turn on the red LED
      buzzerState = 2;               // Set buzzer state to play sound 2
    } 
  } else {
    // Main switch is not pressed
    wasPressed = false;
    digitalWrite(ledPin, LOW);       // Turn off the green LED
    digitalWrite(redLedPin, LOW);   // Turn off the red LED
    noTone(buzzerPin);              // Stop any ongoing buzzer sound
  }
  
  // Play buzzer sound based on buzzerState
  if (buzzerState == 1) {
    // Play sound 1 when wires are not touching and switch is pressed
    tone(buzzerPin, 1000);  // Play a 1000Hz tone
  } else if (buzzerState == 2) {
    // Play sound 2 when wires are touching and switch is pressed
    tone(buzzerPin, 2000);  // Play a 2000Hz tone
  }
  
  // Delay to avoid reading the switches too quickly
  delay(100);
}
