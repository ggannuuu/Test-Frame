#include <AccelStepper.h>

#define DIR_PIN 2         // Direction pin for the stepper driver
#define STEP_PIN 5        // Step pin for the stepper driver
#define LIMIT_SWITCH_1 7  // Limit switch 1 (Bottom)
#define ALWAYS_HIGH_PIN 8 // Pin D8 should always be HIGH

// Create an AccelStepper object in DRIVER mode (for A4988)
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

const int stepsPerRevolution = 200;  // Number of steps per revolution for the stepper motor
const int revolutionsToMove = 100;  // Number of revolutions you want to move
const long max_height = stepsPerRevolution * revolutionsToMove * 7;

const int lowSpeed = 2000;
const int highSpeed = 3500;
long currPos;

void setup() {
  Serial.begin(9600); // Initialize serial communication

  // Initialize limit switch pins
  pinMode(LIMIT_SWITCH_1, INPUT);

  // Initialize pin D8 to always be HIGH
  pinMode(ALWAYS_HIGH_PIN, OUTPUT);
  digitalWrite(ALWAYS_HIGH_PIN, HIGH); // Ensure D8 is always HIGH

  // Initialize stepper settings
  stepper.setMaxSpeed(3600);    // Set max speed in steps per second
  stepper.setAcceleration(1500); // Set acceleration in steps per second^2

  if (digitalRead(LIMIT_SWITCH_1) == HIGH) {
    escapeLimitSwitch();
  }

  calibrate();
  moveToDefaultPosition(); // Move to default position after calibration
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n'); // Read until newline
    inputString.trim(); // Remove any leading/trailing spaces
    processCommand(inputString);
  }

  stepper.run();

  // Periodically send the current position
  static unsigned long lastReport = 0;
  if (millis() - lastReport > 500) { // Every 500ms
    currPos = getPos();
    Serial.println("POS:" + String(currPos));
    lastReport = millis();
  }

  // Check if position is out of bounds

}

void processCommand(String command) {
  if (command.startsWith("#P:")) {
    long val = command.substring(3).toInt();
    Serial.println("LOG:Move command received");
    setPos(val);
  } else if (command.startsWith("#V:")) {
    long val = command.substring(3).toInt();
    Serial.println("LOG:Velocity command received");
    setVel(val);
  } else if (command.startsWith("#S")) {
    Serial.println("LOG:Emergency Stop");
    stop();
  } else if (command.startsWith("#C")) {
    Serial.println("LOG:Calibration");
    calibrate();
    moveToDefaultPosition();
  } else {
    Serial.println("LOG:Invalid command");
  }
}

void setPos(long val) {
  stepper.moveTo(currPos + val);
  Serial.println("LOG:setPos Completed");
  if (currPos + val < 0 || currPos + val > max_height) {
    Serial.println("LOG:Reached Min/Max Pos");
    stop();
  }
}

void setVel(long val) {
  stepper.setSpeed(val);
  Serial.println("LOG:setVel Completed");
}

void stop() {
  stepper.stop();
  Serial.println("LOG:STOP Completed");
}

long getPos() {
  return stepper.currentPosition();
}

void calibrate() {
  stepper.setSpeed(-1 * highSpeed);
  while (digitalRead(LIMIT_SWITCH_1) != HIGH) {
    stepper.runSpeed();
  }

  stepper.stop();
  stepper.setCurrentPosition(0);
  Serial.println("LOG:Calibration Completed");
}

void moveToDefaultPosition() {
  stepper.moveTo(1000);
  Serial.println("LOG:Moved to default position (1000)");
}

void escapeLimitSwitch() {
  Serial.println("LOG:Escaping limit switch");
  stepper.setSpeed(highSpeed); // Move in the opposite direction
  for (int i = 0; i < 200; i++) { // Move a small number of steps away from the switch
    stepper.runSpeed();
  }
  stepper.stop();
  Serial.println("LOG:Escaped limit switch");
}
