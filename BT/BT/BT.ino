#include "BluetoothSerial.h"

String readString;
String getID(String msg);
String getMsg(String msg);

BluetoothSerial SerialBT;

void motorStop();
void motorStaright();
void readMsg();

#define PWM1 15
#define PWM2 2
#define PWM3 4
#define PWM4 5

#define DIR1 18
#define DIR2 19
#define DIR3 21
#define DIR4 22

//motor 1 power
int pwr1 = 60;
int dir1 = 1;

//motor 2 power
int pwr2 = 60;
int dir2 = 1;

//motor 3 power
int pwr3 = 60;
int dir3 = -1;

//motor 4 power
int pwr4 = 60;
int dir4 = 1;

void setup() {                                               
  Serial.begin(115200);
  SerialBT.begin("ESP32_R"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  pinMode(PWM1,OUTPUT);
  pinMode(PWM2,OUTPUT);
  pinMode(PWM3,OUTPUT);
  pinMode(PWM4,OUTPUT);

  pinMode(DIR1,OUTPUT);
  pinMode(DIR2,OUTPUT);
  pinMode(DIR3,OUTPUT);
  pinMode(DIR4,OUTPUT);
}

void loop() {
    //motor 1 power
    pwr1 = 60;
    dir1 = 1;

    //motor 2 power
    pwr2 = 60;
    dir2 = 1;

    //motor 3 power
    pwr3 = 60;
    dir3 = -1;

    //motor 4 power
    pwr4 = 60;
    dir4 = 1;

    readMsg();      
}

void motorStaright() {
    setMotor(dir1, pwr1, PWM1, DIR1);
    setMotor(dir2, pwr2, PWM2, DIR2);
    setMotor(dir3, pwr3, PWM3, DIR3);
    setMotor(dir4, pwr4, PWM4, DIR4);
    
    delay(1000);

    motorStop();    
}

void motorStop() {
    pwr1=0;
    pwr2=0;
    pwr3=0;
    pwr4=0;

    setMotor0(pwr1, PWM1);
    setMotor0(pwr2, PWM2);
    setMotor0(pwr3, PWM3);
    setMotor0(pwr4, PWM4);
}

void readMsg() {
  if (Serial.available()) {    
    while (Serial.available()) { //Check if the serial data is available.
      delay(3);                  // a small delay
      char c = Serial.read();  // storing input data
      readString += c;         // accumulate each of the characters in readString
    }   
    
    if (readString.length() > 0) { //Verify that the variable contains information
      if (getID(readString) == "00619" || getID(readString) == "10619") {
        if (getMsg(readString) == " 1") {
          Serial.println("Robot is moving.");
          motorStaright();
        }
        else if (getMsg(readString) == " 0") {
          Serial.println("Robot is stopping.");
          motorStop();
        }
        else Serial.println("Message: " + getMsg(readString));
      }
      else Serial.println("Unkown Device.");
    }   
    readString = "";    
  }
  delay(20);
}

String getID(String msg) { 
  return msg.substring(1,6);
}

String getMsg(String msg) {
  return msg.substring(8,msg.length()); //was 9  not 8
}

void setMotor(int dir, int pwmVal, int pwm, int dirx){
  analogWrite(pwm, pwmVal);
  if(dir == 1) {
    digitalWrite(dirx,HIGH);
  }
  else if (dir == -1){
    digitalWrite(dirx,LOW);
  }
}

void setMotor0( int pwmVal, int pwm){
  analogWrite(pwm, pwmVal);
}
