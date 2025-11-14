#include <SoftwareSerial.h>
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
#include <Servo.h>

Servo servoMotor; 

DHT dht(DHTPIN, DHTTYPE);
String input = "";

long nextMillis1;
long nextMillis2;
const long interval1 = 3000;
const long interval2 = 5000;

int Pausa2 = 0;
int modo_Media_temperatura =0;
float suma =0;
float m =0;
int i =0;

const int trigPin = 4;
const int echoPin = 5;
float duration;
float distance;

int aut = 1;
int valX = 0;
int joyX = A0;      
float velMotor = 0;

int angulo=90;
int pinBoton = 3;  
bool botonAnterior = HIGH;  // para detectar cambios
int sentido = 0;   // 0 = izquierda, 1 = derecha

SoftwareSerial mySerial(10, 11); // RX, TX 

void setup() {
   nextMillis1 = millis() + interval1;
   nextMillis2 = millis() + interval2;
   Serial.begin(9600);
   mySerial.begin(9600);
   mySerial.println("Empezamos");
   dht.begin();
   servoMotor.attach(6); // Servo conectado al pin 6
   servoMotor.write(angulo); // Posición inicial
   pinMode(trigPin, OUTPUT);
   pinMode(pinBoton, INPUT_PULLUP);
   pinMode(echoPin, INPUT);

}
void loop() {

  if (Pausa2 == 0 && (millis() >= nextMillis1)){
      float h = dht.readHumidity();
      float t = dht.readTemperature();
      float temperaturas[100];
      mySerial.print("1:");
      mySerial.print(t);
      mySerial.print(":2:");
      mySerial.print(h);
      mySerial.print(":3:");
      mySerial.print(distance);
      mySerial.print(":4:");
      mySerial.print(angulo);
      temperaturas[i]=t;
      if (modo_Media_temperatura == 1){
         if (i>9){
            suma=suma+temperaturas[i]-temperaturas[(i-9)];
            m = (suma)/10;
            mySerial.print(":5:");
            mySerial.println(m);
         }
         else if (i<=9){
            suma=suma+temperaturas[i];
            m = (suma)/10;
            mySerial.print(":5:");
            mySerial.println(m);
         }
      }
      i=i+1;
      nextMillis1 = millis() + interval1;
  }
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
  // ---- SUPERSONICOS ----
   digitalWrite(trigPin, LOW);
   delayMicroseconds(2);
   digitalWrite(trigPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(trigPin, LOW);

   duration = pulseIn(echoPin, HIGH, 30000); // 30ms timeout

   if (duration == 0) {
      Serial.println("Sin lectura válida");
   } else {
      distance = duration * 0.0343 / 2;
      Serial.print("Distancia: ");
      Serial.print(distance);
      Serial.println(" cm");
}

servoMotor.write(angulo);

   if (mySerial.available()) {
      input = Serial.readStringUntil('\n'); // Lee hasta el fin del mensaje
      input.trim(); // eliminar saltos de línea y espacios

      int firstColon = input.indexOf(':');
      int comando;

      if (firstColon != -1) {
         comando = input.substring(0, firstColon).toInt();
      } else {
         comando = input.toInt();
      }

      switch (comando) {
    case 1:
      Pausa2 = 1;
      Serial.println("Parar");
      break;

    case 0:
      Pausa2 = 0;
      Serial.println("Reanudar");
      break;

    case 2:
      modo_Media_temperatura = 1;
      Serial.println("Satelite");
      break;

    case 3:
      modo_Media_temperatura = 0;
      Serial.println("Tierra");
      break;

    case 4:
      aut = 1;
      Serial.println("Modo auto");
      break;

    case 5:
      aut = 0;
      Serial.println("Modo manual");
      break;

    case 6:
      // si más adelante quieres enviar un ángulo como "6:123"
      angulo = input.substring(firstColon + 1).toInt();
      Serial.print("Ángulo recibido: ");
      Serial.println(angulo);
      break;

    default:
      Serial.print("Comando no reconocido: ");
      Serial.println(input);
      break;
      }
   }
}
