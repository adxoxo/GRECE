#include <Wire.h>

// Sensor data buffers
char sensordata[30];
byte sensor_bytes_received = 0;
byte code = 0;
byte in_char = 0;

// Sensor configuration
#define TOTAL_CIRCUITS 2
int channel_ids[] = {99, 100};  // PH and EC sensor IDs
float ph_value = 0.0;
float ec_value = 0.0;

void setup() {
  Serial.begin(9600);
  Wire.begin();
}

// Function to read a specific sensor
float readSensor(int sensor_id) {
  Wire.beginTransmission(sensor_id);
  Wire.write('r');
  Wire.endTransmission();
  
  delay(1000);  // Wait for reading to be ready
  
  sensor_bytes_received = 0;
  memset(sensordata, 0, sizeof(sensordata));
  
  Wire.requestFrom(sensor_id, 48, 1);
  code = Wire.read();
  
  while (Wire.available()) {
    in_char = Wire.read();
    if (in_char == 0) {
      Wire.endTransmission();
      break;
    }
    else {
      sensordata[sensor_bytes_received] = in_char;
      sensor_bytes_received++;
    }
  }
  
  // Convert reading to float if valid
  if (code == 1) {
    return atof(sensordata);
  }
  return -1.0;  // Return -1 if reading failed
}

void loop() {
  // Read PH sensor (ID 99)
  ph_value = readSensor(99);
  
  // Read EC sensor (ID 100)
  ec_value = readSensor(100);
  
  // Send data in a structured format: PH:value,EC:value
  Serial.print("PH:");
  if (ph_value >= 0) {
    Serial.print(ph_value, 2);  // 2 decimal places
  } else {
    Serial.print("ERROR");
  }
  Serial.print(",EC:");
  if (ec_value >= 0) {
    Serial.print(ec_value, 2);  // 2 decimal places
  } else {
    Serial.print("ERROR");
  }
  Serial.println();  // End the line
  
  delay(1000);  // Wait 1 second before next reading
}