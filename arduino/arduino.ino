#include <Wire.h>
#include <VL53L0X.h>

#define SENSOR_PIN A0  // Pin sensor kelembaban
VL53L0X sensor;

// Tinggi alat dari tanah (cm)
const float TINGGI_ALAT = 51.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!sensor.init()) {
    Serial.println("Gagal mendeteksi sensor VL53L0X!");
    while (1);
  }

  sensor.setTimeout(500);
  sensor.startContinuous();
}

void loop() {
  // === BACA Kelembaban ===
  int adc = analogRead(SENSOR_PIN);
  float kelembaban = map(adc, 1023, 300, 0, 100);
  kelembaban = constrain(kelembaban, 0, 100);

  // === BACA Tinggi Tanaman ===
  uint16_t jarak_mm = sensor.readRangeContinuousMillimeters();
  float tinggi_tanaman = 0;

  if (!sensor.timeoutOccurred()) {
    float jarak_cm = jarak_mm / 10.0;
    tinggi_tanaman = TINGGI_ALAT - jarak_cm;
    if (tinggi_tanaman < 0) tinggi_tanaman = 0;
  }

  // === KIRIM SERIAL ===
  Serial.print("LEMBAB=");
  Serial.print(kelembaban);
  Serial.print(";");
  Serial.print("TINGGI=");
  Serial.print(tinggi_tanaman, 2);
  Serial.println(";");

  delay(1000);
}
