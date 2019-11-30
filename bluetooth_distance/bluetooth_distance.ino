#include <NewPing.h>
#include <SoftwareSerial.h>

/* Example code for HC-SR04 ultrasonic distance sensor with Arduino. No library required. More info: https://www.makerguides.com */
#define USONIC_DIV 58.0
// Define Trig and Echo pin:
const int trigPin1 = 2;
const int echoPin1 = 3;

const int trigPin2 = 4;
const int echoPin2 = 5;

const int trigPin3 = 6;
const int echoPin3 = 7;

const int rxPin = 8;
const int txPin = 9;


const int MEASURE_SAMPLES = 10;
const int MEASURE_SAMPLE_DELAY = 10;
/*
#define trigPin1 2
#define echoPin1 3

#define trigPin2 4
#define echoPin2 5
*/

// Define variables:
long durationx;
long durationy;
float distancex;
float distancey;

NewPing sensor(trigPin1, echoPin1, 200);
NewPing sensor2(trigPin2, echoPin2, 200);
NewPing sensor3(trigPin3, echoPin3, 200);

SoftwareSerial BT_Serial(9, 8);

void setup() {
  // Define inputs and outputs:
  //pinMode(trigPin1, OUTPUT);
  //pinMode(echoPin1, INPUT);

  /*
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  */
  //Begin Serial communication at a baudrate of 9600:
  Serial.begin(9600);
  BT_Serial.begin(9600);
}
void loop() {
  delay(MEASURE_SAMPLE_DELAY);
  //BT_Serial.println("Bluetooth man");
  //Serial.println(measure(trigPin1, echoPin1));
  BT_Serial.print(singleMeasurement2());
  BT_Serial.print("\t");
  BT_Serial.print(singleMeasurement(trigPin1, echoPin1));
  BT_Serial.print("\t");
  BT_Serial.println(singleMeasurement3());
  /*
  Serial.print(singleMeasurement2());
  Serial.print("\t");
  Serial.print(singleMeasurement(trigPin1, echoPin1));
  Serial.print("\t");
  Serial.println(singleMeasurement3());
  */
}

float measure(int trigPin, int echoPin){
  float measureSum = 0;
  float samples = MEASURE_SAMPLES;
  float single = 0;
  for(int i = 0; i < MEASURE_SAMPLES; i++){
    delay(MEASURE_SAMPLE_DELAY);
    single = singleMeasurement(trigPin, echoPin);
    if(single > 20000){
      samples--;
    }
    else{
      measureSum += single;
    }
  }
  if(samples == 0){
    return 0;
  }
  else{
    return measureSum / samples;
  }
}

float singleMeasurement(int trigPin, int echoPin){
  float time_taken = sensor.ping();
  return int(time_taken / 57.0 * 10);
}

float singleMeasurement2(){
  float time_taken = sensor2.ping();
  return int(time_taken / 57.0 * 10);
}

float singleMeasurement3(){
  float time_taken = sensor3.ping();
  return int(time_taken / 57.0 * 10);
}
