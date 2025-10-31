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
      mySerial.print("T:");
      mySerial.print(t);
      mySerial.print(":H:");
      mySerial.println(h);
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
   }
}
