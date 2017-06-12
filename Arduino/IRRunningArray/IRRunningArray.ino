// number of readings before
const int numReadings = 10;

// values for readings
int readings[numReadings];
int readIndex = 0;
int total = 0;
int average = 0;

// input pins for corresponding IRs
int irfront = A0;
int irleft = A1;
int irback = A2;
int irright = A3;
int irtop = A4;

// values for correspinding IR sensors
int valFIR = 0;
int valLIR = 0;
int valBIR= 0;
int valRIR = 0;
int valTIR = 0;

//values for time between loops
int last_time = 0;
int current_time = 0;

//array value
int IR_sensor_values[7] = {0, 0, 0, 0, 0, 0, 0};

// value for number of the data string
unsigned long dataCount = 0;

void setup() {
  // start serial
  Serial.begin(9600);
  // creates an array for readings that is completely empty
  for (int thisReading =0; thisReading < numReadings; thisReading++){
    readings[thisReading]=0;
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

  // starts a new line/string
  Serial.println("");
  // prints value of string
  IR_sensor_values[0] = dataCount;
  Serial.print(IR_sensor_values[0]);
  Serial.print(",");
  // gets average value for front IR sensor
  IR_sensor_values[1] = averageReading(irfront);
  // prints value for front IR sensor
  Serial.print(IR_sensor_values[1]);
  Serial.print(",");

  // gets average value for left IR sensor
  IR_sensor_values[2] = averageReading(irleft);
  // prints value for left IR sensor
  Serial.print(IR_sensor_values[2]);
  Serial.print(",");

  // gets average value for back IR sensor
  IR_sensor_values[3] = averageReading(irback);
  // prints value for back IR sensor
  Serial.print(IR_sensor_values[3]);
  Serial.print(",");

  // gets average value for right IR sensor
  IR_sensor_values[4] = averageReading(irright);
  // prints value for right IR sensor
  Serial.print(IR_sensor_values[4]);
  Serial.print(",");

  // gets average value for top IR sensor
  IR_sensor_values[5] = averageReading(irtop);
  //prints value for top IR sensor
  Serial.print(IR_sensor_values[5]);
  Serial.print(",");

  //calculates value for time between now and last loop
  IR_sensor_values[6] = millis()-last_time;
  //prints value of time between loops
  Serial.print(IR_sensor_values[6]);
  //changes value of previous time to new time value
  last_time = millis();

  //increase dataCount value
  dataCount++;
  delay(10);

  

}

//function for determining the average reading of an IR sensor
int averageReading (int inputPin){
  //loop fothe number of readings
  for (int i = 0; i < numReadings; i++){
    //remove current total from the value total
    total = total - readings[readIndex];
    //get reading from input pin
    readings[readIndex] = analogRead(inputPin);
    //get new total value to equal the readings
    total = total + readings[readIndex];
    readIndex = readIndex + 1;
  }
  readIndex = 0;
  //get the average of totals
  average = total/numReadings;
  //convert value to cm
  average = 60.374*pow(map(average, 0, 1023, 0, 5000)/1000.0, -1.058);
  return average;
}

