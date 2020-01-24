#include <Bounce2.h>
#include <Arduino.h>
#include <Stepper.h>
#include <EEPROM.h>
#define endButton 7

const byte motorSteps = 200; // Steps per Revolution
const byte pwmA = 3;
const byte pwmB = 11;
const byte brakeA = 9;
const byte brakeB = 8;
const byte dirA = 13;
const byte dirB = 12;


byte escape = 0;
byte motorRunning = LOW;
byte intInput = LOW;
byte button = LOW;
char ch;
int newPos;
int steps;
int a;


// maximum position = 2600 * 0.012192 mm = 31,7
int pos  = 0;
const int zmax = 2500;

// Function Prototypes
/*
void readEEPROM(void);
void writeEEPROM(void);
void motorUp(void);
void motorDown(void);
void pickUp(void);
void reference(void);
void checkButton(void);
*/

//Initialize Stepper class
Stepper myStepper(motorSteps, dirA, dirB);

Bounce debouncer = Bounce();

void setup() {
    myStepper.setSpeed(40);

    // turn on pulse width modulation
    pinMode(endButton,INPUT_PULLUP);
    pinMode(pwmA, OUTPUT);
    digitalWrite(pwmA, HIGH);
    pinMode(pwmB, OUTPUT);
    digitalWrite(pwmB, HIGH);

    // turn off the brakes
    pinMode(brakeA, OUTPUT);
    digitalWrite(brakeA, LOW);
    pinMode(brakeB, OUTPUT);
    digitalWrite(brakeB, LOW);

    debouncer.attach(endButton);
    debouncer.interval(50);

    Serial.begin(115200);

    readEEPROM();

}
void loop(){
    checkButton();
    input();
}


void goUp(int newPos){
  motorRunning = HIGH;
  escape = 0;
  while ((pos > newPos) && (escape == 0)){
    input();
    motorUp();
  }
  motorRunning = LOW;
}

void goDown(int newPos){
  motorRunning = HIGH;
  escape = 0;
  while ((pos < newPos) && (escape == 0)){
    input();
    motorDown();
  }
  motorRunning = LOW;
}

void input(){
  ch = 0;
  a = 0;
  escape = false;
  // Serial.flush();
  while (Serial.available()>0){
    ch = Serial.read();
    if ((motorRunning == LOW) && (intInput == LOW)){
      // gehe zu position N####
      if (ch == 'N'){
        intInput = HIGH;
        newPos = 0;
      }
      // up
      else if (ch == 'U'){
        motorUp();
        Serial.println(pos);
      }
      // down
      else if (ch == 'D'){
        motorDown();
        Serial.println(pos);
      }
      // position?
      else if (ch == 'P'){
        Serial.println(pos);
      }
      // save
      else if (ch == 'S'){
        writeEEPROM();
        Serial.println(pos);
      }
      // reference position;
      else if (ch == 'R'){
        reference();
      }
      // Button pressed?
      else if (ch == 'B'){
        debouncer.update();
        button = debouncer.read();
        Serial.println(button);
      }
      // Identification
      else if (ch == 'V'){
        Serial.println("MOTOR");
      }
      // pickUp
      else if (ch == 'G'){
        grab();
      }
      else if (ch == 'O'){
        pos = 0;
      }
    }
    else if ((motorRunning == HIGH) && (intInput == LOW)){
      // Emergency stop
      if (ch == 'E'){
        escape = 1;
      }
      else if (ch == 'P'){
        Serial.println(pos);
      }
  }
  else if (intInput == HIGH){
      if (isDigit(ch)){
        newPos = newPos * 10;
        a=ch-'0';
        newPos = newPos + a;
      }

      else if ((ch == 'X') && (newPos > pos) && (newPos < 2600)){
        intInput = LOW;
        goDown(newPos);
      }
      else if ((ch == 'X') && (newPos < pos) && (newPos > 100)){
        intInput = LOW;
        goUp(newPos);
      }
      else{
        intInput = LOW;
      }
}
}
}

void checkButton(){
    if (pos < 100){
      debouncer.update();
      button = debouncer.read();
      if (button == LOW){
        pos = 0;
      }
    }
    else{
      button = HIGH;
    }
  }

// EEPROM only supports 100'000 W
void writeEEPROM(){
  byte z0 = pos / 256;
  byte z1 = pos % 256;

  EEPROM.write(2,z0);
  EEPROM.write(3,z1);
}

void readEEPROM(){
  byte z0 = EEPROM.read(2);
  byte z1 = EEPROM.read(3);

  pos = z1 + (z0 * 256);
}

void motorUp(){
  checkButton();
  if (button == HIGH){
    myStepper.step(-1);
    pos--;
  }
}

void motorDown(){
  checkButton();
  if (pos < zmax){
    myStepper.step(1);
    if (button == HIGH){
      pos++;
    }
  }
}

void grab(){
  motorRunning = HIGH;
  escape = 0;
  while ((pos < zmax) && (escape == 0)){
    input();
    motorDown();
  }
  motorRunning = LOW;
}

void reference(){
  escape = 0;
  motorRunning = HIGH;
  while ((button == HIGH) && (escape == 0)){
    checkButton();
    input();
    if ((button == HIGH) && (escape == 0)){
      motorUp();
    }
  }
  motorRunning = LOW;
}



