#include <AccelStepper.h>

#define DIR_PIN 2         // Direction pin for the stepper driver
#define STEP_PIN 5        // Step pin for the stepper driver
#define LIMIT_SWITCH_1 7  // Limit switch 1 (Bottom)
#define ALWAYS_HIGH_PIN 8 // Pin D8 should always be HIGH

// Create an AccelStepper object in DRIVER mode (for A4988)
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);
//max step = stepsPerRevolution * revolutionToMove * 7

const int stepsPerRevolution = 200;  // Number of steps per revolution for the stepper motor
const int revolutionsToMove = 100;     // Number of revolutions you want to move
long targetPosition;                 // Target position in steps
const int lowSpeed = 2000;
const int highSpeed = 3500;
long currPos;

const long max_height = stepsPerRevolution * revolutionsToMove * 7;

void setup() {
  Serial.begin(9600); // For debugging (optional)


  // Initialize limit switch pins
  pinMode(LIMIT_SWITCH_1, INPUT);

  // Initialize pin D8 to always be HIGH
  pinMode(ALWAYS_HIGH_PIN, OUTPUT);
  digitalWrite(ALWAYS_HIGH_PIN, HIGH); // Ensure D8 is always HIGH

  // Initialize stepper settings
  stepper.setMaxSpeed(3600);    // Set max speed in steps per second
  stepper.setAcceleration(1500); // Set acceleration in steps per second^2

  calibrate();

}

void loop() {
  if(Serial.available() > 0) {
    char command = Serial.read();
    long val = Serial.parseInt();
    if (command == 'P') {
      Serial.println("LOG:Setting Position");
      setPos(val);
    } else if (command == 'V') {
      Serial.println("LOG:Setting Velocity");
      setVel(val);
    } else if (command == 'S') {
      Serial.println("LOG:Emergency Stop");
      stop();
    } else if (command == 'C') {
      Serial.println("LOG:Calibration");
      calibrate();
    }
  }


    // Check if limit switch 1 is pressed (HIGH)

  currPos = getPos();
  Serial.println("POS:" + String(currPos));

  if (currPos <= 0 || currPos > max_height) {
    Serial.println("LOG:Reached Min/Max Pos");
    stop();
  }
  delay(200);
}


void setPos(long val) {
  stepper.move(val);
  Serial.println("LOG:setPos Completed");
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
  stepper.setSpeed(-1*lowSpeed);
  if (digitalRead(LIMIT_SWITCH_1) == HIGH) {
    stepper.stop();
    Serial.println("LOG:Calibration Completed");
    stepper.setCurrentPosition(0);
  }

}


