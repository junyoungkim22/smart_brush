/* Example code for HC-SR04 ultrasonic distance sensor with Arduino. No library required. More info: https://www.makerguides.com */
// Define Trig and Echo pin:
#define trigPin1 2
#define echoPin1 3

#define trigPin2 4
#define echoPin2 5

// Define variables:
long durationx;
long durationy;
float distancex;
float distancey;

void setup() {
  // Define inputs and outputs:
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);

  /*
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  */
  //Begin Serial communication at a baudrate of 9600:
  Serial.begin(115200);
}
void loop() {
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

  /*
  // Clear the trigPin by setting it LOW:
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(5);
  // Trigger the sensor by setting the trigPin high for 10 microseconds:
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  // Read the echoPin, pulseIn() returns the duration (length of the pulse) in microseconds:
  durationy = pulseIn(echoPin2, HIGH);
  // Calculate the distance:
  distancey = durationy*0.034/2;
  */

  Serial.println(distancex*10);
  //Serial.print("\t");
  //Serial.println(distancey*10);
  
  delay(50);
}
