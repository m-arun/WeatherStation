#include <ESP8266WiFi.h>
#include <Ticker.h>  //Ticker Library

Ticker vaneTimer;

#define averagingTime 5000
#define cupSizeMPH 1.492
#define cupSizeKMPH 2.4
#define bucketSizeINCH 0.011
#define bucketSizeMM 00.2794

#define windSensorPin (4) //D2 in ESP
#define rainSensorPin (5) //D1 in ESP

//#define windSensorPin (2)   //Arduino Uno
//#define rainSensorPin (3)   //Arduino Uno

#define offset 0

volatile unsigned long Rotations;
volatile unsigned long windContactBounceTime;

volatile unsigned long Tips;
volatile unsigned long rainContactBounceTime;

volatile int Heading[8] = {0};

float windSpeed;
float Speed;
float Precipitation;
int vaneValue;              // raw analog value from wind vane
int Direction;              // translated 0 - 360 direction
int calDirection;           // converted value with offset applied
int Maximum;
int cardinalPoint;
int Degree;

String weatherMeasures;


void windDirection() {
  vaneValue = analogRead(A0);
  Direction = map(vaneValue, 0, 1023, 0, 360);

  calDirection = Direction + offset;
  if (calDirection > 360)
    calDirection = calDirection - 360;
  if (calDirection < 0)
    calDirection = calDirection + 360;


  if (calDirection < 51)        //East
    Heading[2]++;
  else if (calDirection < 87)   //South-East
    Heading[3]++;
  else if (calDirection < 126)  //South
    Heading[4]++;
  else if (calDirection < 189)  //North-East
    Heading[1]++;
  else if (calDirection < 249)  //South-West
    Heading[5]++;
  else if (calDirection < 305)  //North
    Heading[0]++;
  else if (calDirection < 340)  //North-West
    Heading[7]++;
  else if (calDirection < 360)  //West 
    Heading[6]++;
}

void setup() {  
  Serial.begin(9600);

  pinMode(windSensorPin, INPUT);
  pinMode(rainSensorPin, INPUT);
  vaneTimer.attach(1, windDirection);

  attachInterrupt(digitalPinToInterrupt(windSensorPin), isr_rotation, FALLING);
  attachInterrupt(digitalPinToInterrupt(rainSensorPin), isr_tip, FALLING);
}

void loop() {
  int i;
  Rotations = 0;
  Tips = 0;

  sei();
  delay (averagingTime);
  cli();

  windSpeed = (Rotations * cupSizeMPH) / (averagingTime/1000);
  Speed = (Rotations * cupSizeKMPH) / (averagingTime/1000);
  Precipitation = (Tips * bucketSizeMM) / (averagingTime/1000);

  Maximum = Heading[0];
  cardinalPoint = 1;
  for (i = 0; i < 8; i++)
  {
    if (Heading[i] > Maximum)
    {
      Maximum  = Heading[i];
      cardinalPoint = i+1;
    }
  }
//  Serial.println(i);
//  Serial.println(cardinalPoint);
  if (cardinalPoint == 1)
    Degree = 0;
  else if (cardinalPoint == 2)
    Degree = 45;
  else if (cardinalPoint == 3)
    Degree = 90;
  else if (cardinalPoint == 4)
    Degree = 135;
  else if (cardinalPoint == 5)
    Degree = 180;
  else if (cardinalPoint == 6)
    Degree = 225;
  else if (cardinalPoint == 7)
    Degree = 270;
  else if (cardinalPoint == 8)
    Degree = 315;
  else
    Degree = 404;

  for (i = 0; i < 8; i++)
    Heading[i] = 0;
//
//  Serial.print(Rotations);
//  Serial.print("\t\t\t\t");
//  Serial.print(windSpeed);
//  Serial.print("\t\t\t");
//  Serial.print(Speed);
//  Serial.print("\t\t");
//  Serial.print(Tips);
//  Serial.print("\t\t");
//  Serial.print(Precipitation);
//  Serial.print("\t\t\t");
//  Serial.print("Degree");
//  Serial.println(Degree);
  weatherMeasures += String(Speed);
  weatherMeasures += ",";
  weatherMeasures += String(Degree);
  weatherMeasures += ",";
  weatherMeasures += String(Precipitation);
  Serial.println(weatherMeasures);
  weatherMeasures = "";
}

void isr_rotation () {
  if ((millis() - windContactBounceTime) > 15 ) {
    Rotations++;
    windContactBounceTime = millis();
  }
}

void isr_tip () {
  if ((millis() - rainContactBounceTime) > 15 ) {
    Tips++;
    rainContactBounceTime = millis();
  }
}

