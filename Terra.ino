#include <SoftwareSerial.h>
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial mySerial(10, 11); // RX, TX (azul, naranja)
unsigned long nextMillis = 500;

int angulo = 90;
int joyX = A0;      
int valX = 0;
float velMotor = 0;

int pinBoton = 3;  
int aut = 0;
bool botonAnterior = HIGH;  // para detectar cambios
int sentido = 0;   // 0 = izquierda, 1 = derecha


void setup() {
   Serial.begin(9600);
   mySerial.begin(9600);
   dht.begin();
   pinMode(pinBoton, INPUT_PULLUP);  // LOW cuando se presiona

}
void loop() {
   if (mySerial.available()) {
      String data = mySerial.readString();
      Serial.print(data);
      
   }
   int estadoBoton = digitalRead(pinBoton);

  // Detectar flanco de bajada (cuando el botón pasa de HIGH a LOW)
  if (botonAnterior == HIGH && estadoBoton == LOW) {
      aut = !aut;          // alternar el modo
      if (aut == 1){
         mySerial.println("4:");
         delay(200);          // debounce
      }
      else{
         mySerial.println("5:");
         delay(200);  
      }
  }
  botonAnterior = estadoBoton;  // actualizar estado
   // ---- MODO MANUAL ----
  if (!aut) {
      valX = analogRead(joyX);
      velMotor = abs(((valX - 500) / 500.00) * 4.00);
      if (valX < 490 && angulo < 180) {
         angulo += velMotor;
      }else if (valX > 510 && angulo > 0) {
         angulo -= velMotor;
      } 
      if (angulo < 0){ 
         angulo = 0;
      }else if (angulo > 180){
         angulo = 180;
      }
   }
  
  // ---- MODO AUTOMATICO ----
  else {
      if (angulo >= 180) sentido = 0;
      if (angulo <= 0) sentido = 1;

      if (sentido == 0) angulo -= 2;
      else angulo += 2;
  }
   if (Serial.available()){
   char Pausa = Serial.read();
   if (Pausa == ('1')){
      mySerial.println("1:");
   }
   if (Pausa == ('0')){
      mySerial.println("0:");
   }
   if (Pausa == ('2')){
      mySerial.println("2:"); //Cambia el modo de media de temperatura para el satelite
   }
   if (Pausa == ('3')){
      mySerial.println("3:");//Cambia el modo de media de temperatura para tierra
   }
   mySerial.print("6:");
   mySerial.println(angulo);
   delay(2000);
   }
}
