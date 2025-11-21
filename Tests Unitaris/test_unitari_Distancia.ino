
const int trigPin = 4;
const int echoPin = 5;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.println("test unitari ultrasons iniciat");

}

void loop() {
  delay(500);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // timeout 30 ms

  if (duration == 0) {
    Serial.println("Error: No hi ha ECO (sensor o connexió incorrecta)");
    return;
  }

  float distance = duration * 0.0343 / 2.0;

  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.println(" cm");

  if (distance < 2 || distance > 400) {
    Serial.println("Advertencia: valor fora del rang del sensor");
  }
}
