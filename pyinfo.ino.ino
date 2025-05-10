const int ledPins[] = {15, 5, 18, 22, 23};
const int numLeds = sizeof(ledPins) / sizeof(ledPins[0]);

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 Ready");

  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int level = input.toInt();
    level = constrain(level, 0, numLeds);

    for (int i = 0; i < numLeds; i++) {
      digitalWrite(ledPins[i], i < level ? HIGH : LOW);
    }
  }
}