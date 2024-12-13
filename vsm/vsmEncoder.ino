#include <Arduino.h>
#define ENCODER_OPTIMIZE_INTERRUPTS
#include <Encoder.h>
#include <RunningAverage.h>


// Nutze Interrupt Pins 2 und 3
// um hohe Auslesegeschwindigkeiten zu erreichen
Encoder enc(2,3);
int oldPosition = 0;
int newPosition = 0;
int maximum = 0;
int newMax = 0;
int minimum = 0;
int newMin = 0;
byte risingEdge = false;
byte newMaxValue = false;
byte newMinValue = false;
byte ch;

int currentAmplitude = 0;
RunningAverage amplitude(60);


void setup() {
  amplitude.clear();
  Serial.begin(115200);
}

void loop() {
  newPosition = enc.read();
  calcPeak();
  calcAmplitude();
  input();

}

void input(){
  ch = 0;
  while (Serial.available()>0){
    ch = Serial.read();
    if (ch == 'A'){
      Serial.println(amplitude.getAverage());
    }
    if (ch == 'P'){
      Serial.println(newPosition);
    }
    if (ch == 'M'){
      Serial.println(maximum);
    }
    if (ch == 'm'){
      Serial.println(minimum);
    }
    else if (ch == 'V'){
      Serial.println("ENCODER");
    }
  }
}

void calcPeak(){
  if (newPosition > oldPosition){
    risingEdge = true;
    newMaxValue = true;
    maximum = newPosition;

  }
  else if (newPosition < oldPosition){
    newMinValue = true;
    risingEdge = false;
    minimum = newPosition;
  }
  oldPosition = newPosition;
}

void calcAmplitude(){

  if (risingEdge == true && newMinValue == true){
    newMinValue = false;
    newMin = minimum;
    currentAmplitude = newMax - newMin;
    amplitude.addValue(currentAmplitude);
  }
  else if (risingEdge == false  && newMaxValue == true){
  newMaxValue = false;
  newMax = maximum;
  currentAmplitude = newMax - newMin;
  amplitude.addValue(currentAmplitude);
  }
}
