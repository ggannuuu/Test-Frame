
/*Includes*/
#include <Dynamixel2Arduino.h>
#include <DynamixelShield.h>
#include <SoftwareSerial.h>
SoftwareSerial soft_serial(7, 8); // DYNAMIXELShield UART RX/TX
#define DEBUG_SERIAL soft_serial


/* Global Constants */

const uint8_t DXL_ID = 1;
const float DXL_PROTOCOL_VERSION = 2.0;
DynamixelShield dxl;

const int DXL_MAX_POS = 4095;
const int DXL_MIN_POS = 0;
const int DXL_DEFAULT_POS = 2047;
const int DXL_DEFAULT_VEL = 20;


void setup() {
  /*Serial Setup*/
  DEBUG_SERIAL.begin(115200);
  /* Basic DXL Setup */
  /*baudrate = 57600, torque is always on*/
  dxl.begin(57600);
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  dxl.torqueOn(DXL_ID);
  


}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char command = Serial.read();
    int val = Serial.parseInt();

    if (command == 'p') {
      Serial.println("Setting Position");
      setPos(val);
    } else if (command == 'v') {
      Serial.println("Setting Velocity");
      setVel(val);
    } else if (command == 'P') {
      Serial.println("Switching to Position Mode");
      setPosMode();
    } else if (command == 'V') {
      Serial.println("Switching to Velocity Mode");
      setVelMode();
    } else if (command == 'C') {
      Serial.println("Calibrating");
      calibrate();
    } else if (command == 'S') {
      Serial.println("Emergency Stop");
      emergencyStop();
    }
  }

}

//Basic Functions
void calibrate() {
  //Set the force and position read to 0
}



//Functions for Dynamixel


void setPos(int pos) {
  //sets the position of the motor
  //Position mode
  int curr = getPos();
  if(curr + pos < DXL_MIN_POS || curr + pos > DXL_MAX_POS) {
    Serial.println("Reached Max/Min Position");
    return;
  } else {
    curr = curr + pos;
  }
  Serial.print("Current position: ");
  Serial.println(curr);
  dxl.setGoalPosition(DXL_ID, curr);
}

void setPosMode() {
  //sets the mode of the motor to Position mode
  dxl.setOperatingMode(DXL_ID, OP_POSITION);
}

void setVel(int vel) {
  //sets the speed of the rotation
  //Velocity mode
  dxl.setGoalVelocity(DXL_ID, vel);
}

void setVelMode() {
  //sets the mode of the motor to Velocity mode
  dxl.setOperatingMode(DXL_ID, OP_VELOCITY);
}

int getPos() {
  return dxl.getPresentPosition(DXL_ID);
}

void emergencyStop() {
  //stop the motor immediately
  setVelMode();
  setVel(0);
}

//Funcitons for Loadcells
void readLC() {
  //read loadcell values
}
