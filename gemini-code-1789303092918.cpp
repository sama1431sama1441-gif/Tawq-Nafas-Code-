#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Initializing Tawq Nafas Sensor...");

  // Initialize sensor using default I2C pins for XIAO ESP32-S3 (D4-SDA, D5-SCL)
  Wire.begin();

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found. Please check wiring/power!");
    while (1);
  }
  
  Serial.println("MAX30102 online!");
  particleSensor.setup(); // Configure sensor with default settings
  particleSensor.setPulseAmplitudeRed(0x0A); // Turn Red LED to low to indicate
  particleSensor.setPulseAmplitudeGreen(0); // Disable Green LED
}

void loop() {
  long irValue = particleSensor.getIR();

  if (irValue > 50000) {
    Serial.print("IR Value: ");
    Serial.print(irValue);
    Serial.println(" - Finger Detected (Active Monitoring)");
  } else {
    Serial.println("No finger detected. Please place finger on sensor.");
  }
  
  delay(500);
}