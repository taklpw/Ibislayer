#include <SharpIR.h>

const int numReadings = 10;

int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0;

int irfront = A0;
int irleft = A1;
int irback = A2;
int irright = A3;
int irtop = A4;
int valFIR = 0;
int valLIR = 0;
int valBIR= 0;
int valRIR = 0;
int valTIR = 0;
int last_time = 0;
int current_time = 0;
unsigned long dataCount = 0;

void setup() {
  Serial.begin(9600);

  for (int thisReading =0; thisReading < numReadings; thisReading++){
    readings[thisReading]=0;
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

  Serial.println("");
  Serial.print(dataCount);
  Serial.print(",");
  valFIR = averageReading(irfront);
  Serial.print(valFIR);
  Serial.print(",");
  //delay(1000);

  valLIR = averageReading(irleft);
  Serial.print(valLIR);
  Serial.print(",");
  //delay(1000);

  valBIR = averageReading(irback);
  Serial.print(valBIR);
  Serial.print(",");

  valRIR = averageReading(irright);
  Serial.print(valRIR);
  Serial.print(",");

  valTIR = averageReading(irtop);
  Serial.print(valTIR);
  Serial.print(",");
  last_time = millis()-current_time;
  Serial.print(last_time);
  current_time = millis();

  dataCount++;
  delay(50);

}

int averageReading (int inputPin){
  for (int i = 0; i < numReadings; i++){
    total = total - readings[readIndex];
    readings[readIndex] = analogRead(inputPin);
    total = total + readings[readIndex];
    readIndex = readIndex + 1;
  }
  readIndex = 0;
  
  average = total/numReadings;
  average = 60.374*pow(map(average, 0, 1023, 0, 5000)/1000.0, -1.058);
  return average;
}

