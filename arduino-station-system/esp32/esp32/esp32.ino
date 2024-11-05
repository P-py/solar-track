#include <Wire.h>               //Biblioteca utilizada gerenciar a comunicação entre dispositicos através do protocolo I2C
#include <LiquidCrystal_I2C.h>  //Biblioteca controlar display 16x2 através do I2C

#define col 16     //Define o número de colunas do display utilizado
#define lin 2      //Define o número de linhas do display utilizado
#define ende 0x27  //Define o endereço do display

#define RXp2 16
#define TXp2 17

String stringValue;

LiquidCrystal_I2C lcd(ende, 16, 2);  //Cria o objeto lcd passando como parâmetros o endereço, o nº de colunas e o nº de linhas

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);
  lcd.init();       //Inicializa a comunicação com o display já conectado
  lcd.clear();      //Limpa a tela do display
  lcd.backlight();  //Aciona a luz de fundo do display
}

void loop() {
  lcd.clear();
  stringValue = Serial2.readStringUntil('\n');
  stringValue.trim();
  lcd.print(stringValue);
  Serial.println(stringValue);
  delay(50);
}