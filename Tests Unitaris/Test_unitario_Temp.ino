#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
void setup() {
   Serial.begin(9600);

   dht.begin();
}
void loop() {
delay (3000);

float h = dht.readHumidity(); //humitat
float t = dht.readTemperature(); //temperatura

Serial.print("Humedad: ");// Escriu les dades
Serial.print(h );
Serial.print(" Temperatura: ");
Serial.println(t );

}
