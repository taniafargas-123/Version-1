#include <SoftwareSerial.h>
#define pinBoton 3
#define pinVRx A0
#define aAmarilla 5
#define aRoja 6
#define aVerde 7
SoftwareSerial mySerial(10, 11); // RX, TX (azul, naranja)

unsigned long nextMillis = 500;
int angulo = 90;     
int valX = 0;
float velMotor = 0;

bool aut = false;
bool botonAnterior = HIGH;  // para detectar cambios
int sentido = 0;   // 0 = izquierda, 1 = derecha


void setup() {
   Serial.begin(9600);
   mySerial.begin(9600);
   pinMode(pinBoton, INPUT_PULLUP);  // LOW cuando se presiona
}

void loop() {
   if (mySerial.available()) {
      String data = mySerial.readString();
      Serial.print(data);
      
   }

   // Detectar flanco de bajada (cuando el botón pasa de HIGH a LOW)
   int estadoBoton = digitalRead(pinBoton);
   if (botonAnterior == HIGH && estadoBoton == LOW) { 
      if (aut){
         aut = false;
         mySerial.println("4:"); 
         delay(200);          // debounce
      }
      else if(!aut){
         aut = true;
         mySerial.println("5:");
         delay(200);  
      }
   }
   botonAnterior = estadoBoton;  

   // ---- MODO MANUAL ----
   if (!aut) {
      valX = analogRead(pinVRx);
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
   else if (aut) {
      if (angulo >= 180) sentido = 0;
      if (angulo <= 0) sentido = 1;
      if (sentido == 0) angulo -= 2;
      else angulo += 2;
   }
   // ---- LECTURA/ENVIO ----
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
