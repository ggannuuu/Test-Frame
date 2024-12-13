#include "HX711.h"

#define calibration_factor -129450.0 // This value is obtained using the SparkFun_HX711_Calibration sketch

#define DOUT  3
#define CLK   2

HX711 scale;

const int numReadings = 5;   // Number of readings to average
float readings[numReadings]; // Array to store the readings
int readIndex = 0;           // Index for the readings array
float total = 0;             // Sum of the readings
float average = 0;           // Average of the readings
unsigned long previousMillis = 0;
const long interval = 100;    // Interval for averaging and printing (ms)

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 scale demo");

  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor); // This value is obtained by using the SparkFun_HX711_Calibration sketch
  scale.tare(); // Assuming there is no weight on the scale at startup, reset the scale to 0

  Serial.println("Readings:");
}

void loop() {
  unsigned long currentMillis = millis();

  // Check if 500 ms have passed
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Subtract the last reading from the total
    total -= readings[readIndex];

    // Read the new value from the scale and add it to the total
    readings[readIndex] = scale.get_units(1); // Get a single reading
    total += readings[readIndex];

    // Advance to the next index in the array (circular buffer)
    readIndex = (readIndex + 1) % numReadings;

    // Calculate the average of the readings
    average = total / numReadings;

    // Output the average reading with a label to serial
    Serial.print("Load_Cell: ");  // Label for the plot
    Serial.println(average, 3);   // Print the average reading with 3 decimal places
  }
}