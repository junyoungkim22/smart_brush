#include <NewPing.h>

/* Example code for HC-SR04 ultrasonic distance sensor with Arduino. No library required. More info: https://www.makerguides.com */
#define USONIC_DIV 58.0
// Define Trig and Echo pin:
const int trigPin1 = 2;
const int echoPin1 = 3;

const int trigPin2 = 4;
const int echoPin2 = 5;

const int MEASURE_SAMPLES = 5;
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
}
void loop() {
  /*
  // Clear the trigPin by setting it LOW:
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(5);
  // Trigger the sensor by setting the trigPin high for 10 microseconds:
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  // Read the echoPin, pulseIn() returns the duration (length of the pulse) in microseconds:
  durationx = pulseIn(echoPin1, HIGH);
  // Calculate the distance:
  distancex = durationx*0.034/2;
  */
  //distancex = getDistance(trigPin1, echoPin1);
  //int time_taken = sensor.ping();
  //Serial.println(sensor.convert_mm(time_taken));
  //Serial.println(distancex*10);
  //Serial.print("\t");
  //Serial.println(distancey*10);
  delay(MEASURE_SAMPLE_DELAY);
  //Serial.println(measure(trigPin1, echoPin1));
  Serial.println(singleMeasurement(trigPin1, echoPin1));
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
  return time_taken / 57.0;
  //Serial.println(sensor.convert_mm(time_taken));
  /*
  long duration = 0;
  // Clear the trigPin by setting it LOW:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  // Trigger the sensor by setting the trigPin high for 10 microseconds:
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Read the echoPin, pulseIn() returns the duration (length of the pulse) in microseconds:
  duration = pulseIn(echoPin, HIGH);
  // Calculate the distance:
  return (long) (((float) duration / USONIC_DIV) * 10.0);
  */
}
