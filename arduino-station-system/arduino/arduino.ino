#include <Servo.h>

Servo servoverti; //vertical servo(TOP SERVO) 
int servov = 0; 
Servo servohori; //vertical servo(TOP SERVO) 
int servoh = 0; 

int ldrtopr = A2; //top right LDR A1 pin
int ldrtopl = A3; //top left LDR A2 pin

int ldrbotr = A1; // bottom right LDR A0 pin
int ldrbotl = A0; // bottom left LDR A3 pin

int i;
int j;

void setup () {
  servohori.attach(10);
  delay(5000);
  servoverti.attach(9);
  delay(5000); //delay
  servoverti.write(0);
  delay(5000);
  servohori.write(0);
  Serial.begin(9600);
  delay(5000);
  for (i=0; i<=180; i++){
    servov = servoverti.read();
    Serial.println(servov);
    servoverti.write(i);
    delay(50);
  }
  delay(3000);
  for (i=180; i>=0; i--){
    servov = servoverti.read();
    Serial.println(servov);
    servoverti.write(i);
    delay(50);
  }
  delay(3000);
  for (i=0; i<=180; i++){
    servoh = servohori.read();
    Serial.println(servoh);
    servohori.write(i);
    delay(50);
  }
  delay(3000);
  for (i=180; i>=0; i--){
    servoh = servohori.read();
    Serial.println(servoh);
    servohori.write(i);
    delay(50);
  }
  delay(3000);
}

void loop() {
  servov = servoverti.read();
  servoh = servohori.read();
  float topl = analogRead(ldrtopl); //read analog values from top left LDR
  float topr = analogRead(ldrtopr); //read analog values from top right LDR
  float botl = analogRead(ldrbotl); //read analog values from bottom left LDR
  float botr = analogRead(ldrbotr); //read analog values from bottom right LDR

  Serial.print("Vert: ");
  Serial.println(servov);
  Serial.print("Hori: ");
  Serial.println(servoh);
  Serial.print("Top L: ");
  Serial.println(topl);
  Serial.print("Top R: ");
  Serial.println(topr);
  Serial.print("Bot L: ");
  Serial.println(botl);
  Serial.print("Bot R: ");
  Serial.println(botr);
  Serial.println("--------");
  
  
  int avgtop = (topl + topr) / 2; //average of top LDRs
  int avgbot = (botl + botr) / 2; //average of bottom LDRs
  int avgleft = (topl + botl) / 2; //average of left LDRs
  int avgright = (topr + botr) / 2; //average of right LDRs

  if (avgtop > avgbot){
    servoverti.write(servov + 1);
    delay(10);
  } else if (avgbot > avgtop) {
    servoverti.write(servov - 1);
    delay(10);
  } else {
    servoverti.write(servov);
    delay(10);
  }

  if (avgright > avgleft) {
    servohori.write(servoh + 1);
    delay(10);
  } else if (avgleft > avgright) {
    servohori.write(servoh - 1);
    delay(10);
  } else {
    servohori.write(servoh);
    delay(10);
  }
  delay(50);
}