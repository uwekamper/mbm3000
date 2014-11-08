#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
 
int potpin = 0;  // analog pin used to connect the potentiometer
int val = 46;    // variable to read the value from the analog pin 
 
int step = 1;
int min = 30;
int max = 110;

void setup() 
{ 
  myservo.attach(3);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  val = val + step;
  myservo.write(val);                  // sets the servo position according to the scaled value 
  delay(8);                           // waits for the servo to get there 
  if (val >= max || val <= min) {
    step = -step;
  }
} 
