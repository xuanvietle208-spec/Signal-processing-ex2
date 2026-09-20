#include "HX711.h"

HX711 scale;
const int dtPin = 3;
const int sckPin = 2;

void setup() {
  Serial.begin(9600);
  scale.begin(dtPin, sckPin);
}
void loop() {
  if (scale.is_ready()) {
    Serial.print(millis());
    Serial.print(",");
    Serial.println(scale.read()); // Đọc trực tiếp 24-bit thô
  }
}