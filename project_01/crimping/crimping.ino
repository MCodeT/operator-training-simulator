
// Define the pin numbers
const int buttonPin = 2;       // Pin where the main switch is connected
const int greenLedPin = 12;    // Pin for the green LED
const int wirePin = 3;         // Pin where one side of the wire switch is connected
const int redLedPin = 11;      // Pin for the red LED
const int buzzerPin = 10;      // Pin where the buzzer is connected

int buttonState = 0;           // Variable to store the state of the main switch
int wireState = 0;             // Variable to store the state of the wire switch
bool wasPressed = false;

void setup() {
  // Initialize the pins
  pinMode(buttonPin, INPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(wirePin, INPUT_PULLUP);  // Enable internal pull-up resistor
  pinMode(redLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the state of the main switch
  buttonState = digitalRead(buttonPin);
  
  // Read the state of the wire switch
  wireState = digitalRead(wirePin);
  
  // Check if the main switch is pressed
  if (buttonState == LOW) {
    // Main switch is pressed
    // Check the state of the wire switch
    if (wireState == LOW) {
      // Wire is touching (LOW state due to pull-up)
      if(!wasPressed){
        Serial.println("GREEN");
        wasPressed = true;
      }

      digitalWrite(greenLedPin, HIGH);  // Turn on the green LED
      digitalWrite(redLedPin, LOW);     // Turn off the red LED
      tone(buzzerPin, 1000);             // Play a 500Hz tone
    } else {
      // Wire is not touching
      Serial.println("RED");
      digitalWrite(greenLedPin, LOW);   // Turn off the green LED
      digitalWrite(redLedPin, HIGH);    // Turn on the red LED
      tone(buzzerPin, 2000);             // Play a 300Hz tone
    }
  } else {
    // Main switch is not pressed
    digitalWrite(greenLedPin, LOW);     // Turn off the green LED
    digitalWrite(redLedPin, LOW);       // Turn off the red LED
    noTone(buzzerPin);                  // Stop any ongoing buzzer sound
    wasPressed = false;
  }
  
  // Delay to avoid reading the switches too quickly
  delay(150);
}
