#include <SoftwareSerial.h>
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial mySerial(10, 11); // RX, TX (azul, naranja)
unsigned long nextMillis = 500;

void setup() {
   Serial.begin(9600);
   mySerial.begin(9600);
   dht.begin();
}
void loop() {
   if (mySerial.available()) {
      String data = mySerial.readString();
      Serial.print(data);
      
   }
   if (Serial.available()){
   char Pausa = Serial.read();
   if (Pausa == ('1')){
      mySerial.println('1');
   }
   if (Pausa == ('0')){
      mySerial.println('0');
   }
   }
}
