#include <SoftwareSerial.h>
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
int i;

long nextMillis1;
long nextMillis2;
const long interval1 = 3000;
const long interval2 = 5000;

int Pausa2 = 0;

int modo_Media_temperatura =0;

const int led = 7;
bool stateLed = LOW;

const int buzzer = 4;
bool stateBuzzer = LOW;
SoftwareSerial mySerial(10, 11); // RX, TX 
void setup() {
   nextMillis1 = millis() + interval1;
   nextMillis2 = millis() + interval2;
   pinMode(led, OUTPUT);
   Serial.begin(9600);
   mySerial.begin(9600);
   mySerial.println("Empezamos");
   dht.begin();

}
void loop() {

  if (Pausa2 == 0 && (millis() >= nextMillis1)){
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      float temperaturas[100];
      int suma =0;
      float m =0;
      int i =0;
      mySerial.print("1:");
      mySerial.print(t);
      mySerial.print(":2:");
      mySerial.print(h);
      temperaturas[i]=t;
      if (modo_Media_temperatura == 1){
         if (i>9){
            suma=suma+temperaturas[i]-temperaturas[(i-10)];
            m = (suma)/10;
            mySerial.print("4:");
            mySerial.println(m);
         }
         else if (i<=9){
            suma=suma+temperaturas[i];
            m = (suma)/10;
            mySerial.print("4:");
            mySerial.println(m);
         }
      }
      i=i+1;
      nextMillis1 = millis() + interval1;
  }

   if (mySerial.available()) {
      char Pausa = mySerial.read();
      if (Pausa == '1'){
         Pausa2 = 1;
         Serial.println("Parar");
      }
      if (Pausa == '0'){
         Pausa2 = 0;
         Serial.println("Reanudar");
      }
      if (Pausa == '2'){
         modo_Media_temperatura =1; //Cambia el modo de media de temperatura 
         Serial.println("Satelite");
      }
      if (Pausa == '3'){
         modo_Media_temperatura =0;
         Serial.println("Tierra");
      }
   }
}
