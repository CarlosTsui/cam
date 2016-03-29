#include <Servo.h> 

Servo hor,ver;
int hordeg=90,verdeg=120;
char action='t';

void cameraMove(int a,int b){
  if(hordeg+a>=0&&hordeg+a<=180)hordeg+=a;
  if(verdeg+b>=45&&verdeg+b<=180)verdeg+=b;
  hor.write(hordeg);
  ver.write(verdeg);
  delay(20);
  Serial.flush();
}
void setup() {
  hor.attach(6);
  ver.attach(0);
  Serial.begin(9600); 
}
bool getChar(char &x){
  if(Serial.available()<=0)return false;
  x=(char)Serial.read();
  Serial.flush();
  return true;
}

void loop() {
  while(action!='s'){while(getChar(action));};
  //confirm here
  while(1){
    if(getChar(action)){
      if(action=='a')cameraMove(0,1);
      if(action=='d')cameraMove(0,-1);
    }
  }
  //confirm here
}