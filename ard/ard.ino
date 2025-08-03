#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;

const int RELAY1_PIN = 7;
const int RELAY2_PIN = 8;
const float TINGGI_ALAT = 51.0; // cm, dari sensor ke permukaan tanah

String inputSerial = "";

void setup() {
  Serial.begin(9600);
  Wire.begin();

  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);

  digitalWrite(RELAY1_PIN, HIGH); // relay mati (aktif low)
  digitalWrite(RELAY2_PIN, HIGH);

  if (!sensor.init()) {
    Serial.println("VL53L0X tidak terdeteksi");
    while (1);
  }

  sensor.setTimeout(500);
  sensor.startContinuous();
}

void loop() {
  // Hitung tinggi tanaman
  uint16_t jarak = sensor.readRangeContinuousMillimeters();
  float jarak_cm = jarak / 10.0;
  float tinggi_tanaman = TINGGI_ALAT - jarak_cm;
  if (tinggi_tanaman < 0) tinggi_tanaman = 0;

  // Kirim data tinggi ke serial
  Serial.print("TINGGI:");
  Serial.println(tinggi_tanaman);

  // Baca perintah dari Python
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      inputSerial.trim();

      if (inputSerial == "RELAY1_ON") {
        digitalWrite(RELAY1_PIN, LOW);
      } else if (inputSerial == "RELAY1_OFF") {
        digitalWrite(RELAY1_PIN, HIGH);
      } else if (inputSerial == "RELAY2_ON") {
        digitalWrite(RELAY2_PIN, LOW);
      } else if (inputSerial == "RELAY2_OFF") {
        digitalWrite(RELAY2_PIN, HIGH);
      }

      inputSerial = ""; // Reset setelah command
    } else {
      inputSerial += c;
    }
  }

  delay(500);
}
