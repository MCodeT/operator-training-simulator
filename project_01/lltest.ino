int ir = 7;
int count = 0;
bool holeDetected = false;
unsigned long startTime;
unsigned long gameTime = 50000; // 50 seconds in milliseconds
bool gameStarted = false;

void setup() {
  pinMode(ir, INPUT);
  Serial.begin(9600);
  
  // Countdown
  Serial.println("Get ready...");
  for (int i = 5; i > 0; i--) {
    Serial.print(i);
    Serial.println("...");
    delay(1000);
  }
  Serial.println("Go!");

  // Start the game
  startTime = millis();
  gameStarted = true;
}

void loop() {
  if (gameStarted) {
    if (millis() - startTime <= gameTime) {
      if (digitalRead(ir) == HIGH) {
        if (!holeDetected) {
          count++;
          Serial.print("Number of turns: ");
          Serial.println(count);
          holeDetected = true;
        }
      } else {
        holeDetected = false;
      }
      delay(100); // Debounce delay to avoid multiple counts in a single detection
    } else {
      gameStarted = false;
      Serial.print("Game over! Total turns: ");
      Serial.println(count);
    }
  }
}
