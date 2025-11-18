#include <SoftwareSerial.h>
#include <DHT.h>
#include <Servo.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define trigPin 4
#define echoPin 5
#define servoPin 6
#define joyX A0

DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial mySerial(10, 11); 
Servo servoMotor; 

String input = "";

long nextMillis1;
const long interval1 = 3000;

int Pausa2 = 0;
int modo_Media_temperatura =0;
float suma =0;
float m =0;
int i =0;

float duration=0;
float distance=0;

bool aut = true;
int valX = 0;    
float velMotor = 0;
int angulo=90;

int sentido = 0;   // 0 = izquierda, 1 = derecha


void setup() {
   Serial.begin(9600);
   mySerial.begin(9600);
   dht.begin();
   pinMode(trigPin, OUTPUT);
   pinMode(echoPin, INPUT);
   servoMotor.attach(servoPin);
   mySerial.println("Empezamos");
   servoMotor.write(angulo); // Posición inicial
   nextMillis1 = millis() + interval1;
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
      mySerial.println(angulo);
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
      i++;
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

   duration = pulseIn(echoPin, HIGH, 3000000); // 30ms timeout

   if (duration!=0) {
      distance = duration * 0.0343 / 2.000;
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
