# Benvinguts al nostre Sistema Satel·lital!!!
### *Projecte del Grup 12 — Antoni Ruiz · Marc Conill · Tània Fargas*

![WhatsApp Image 2025-12-15 at 19 27 58](https://github.com/user-attachments/assets/088ab4cc-22aa-402e-af4e-4a27c7a0f546)

Aquest projecte és el nostre viatge a l’espai: creem el prototip funcional d’un sistema satel·lital, format per un satèl·lit i una estació de terra que cooperen per captar, enviar i visualitzar dades en temps real.

---

## El Satèl·lit  
El nostre satèl·lit està impulsat per un **Arduino** que recull dades de temperatura, humitat i proximitat, i pot orientar sensors mitjançant servomotors. Processa la informació, envia missatges a terra i respon a ordres del usuari. Tot està programat en **C**.

---

## L’Estació de Terra  
Format per un altre Arduino i un portàtil, aquest sistema rep i processa les dades enviades des del satèl·lit, activa alarmes i les mostra mitjançant una interfície gràfica creada en **Python**. També permet enviar ordres al satèl·lit, com modificar la freqüència d’enviament o orientar sensors.

---

## Comunicació  
La comunicació entre satèl·lit i terra utilitza **LoRa** per transmissions de llarg abast, tot i que durant el desenvolupament també s’ha treballat amb connexió per cable per evitar interferències.

---

##  Versions del Sistema  

### **Versió 1**  
En aquesta primera versió, el satèl·lit captura dades de temperatura i humitat amb precisió i les envia a terra. A l’estació de terra, aquestes dades cobren vida en forma de gràfics i lectures clares, mentre detecta patrons i llança alertes quan el sistema identifica situacions compromeses.

Link del video demostratiu: https://www.canva.com/design/DAG2FDCh28I/qZcI6gRfyIkjfftYRJZoaw/watch?utm_content=DAG2FDCh28I&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf39c88deff 

### **Versió 2**  
En aquesta versió, el satèl·lit amplia la seva percepció incorporant un sensor d’ultrasons capaç de detectar objectes propers que podrien posar-lo en risc. Tota aquesta informació —juntament amb la de la versió anterior— arriba a terra amb precisió i es transforma en gràfics clars que potencien la presa de decisions. Ara, l’operador també pot interactuar amb el satèl·lit enviant ordres que modifiquen tasques, ajusten freqüències o orienten el sensor d’ultrasons mitjançant un servo-motor.

Link del video demostratiu: https://drive.google.com/file/d/1L44LO0Di6GdR4LK3FuMZSn6tWgFo8nDT/view?usp=sharing 

### **Versió 3**  
El satèl·lit adquireix una capacitat clau: determinar i comunicar la seva posició exacta en òrbita. Aquesta informació s’uneix a la resta de dades i s’envia a terra, on l’usuari pot visualitzar la trajectòria sobre mapes intuïtius i gestionar-ho tot des d’una interfície gràfica potent i fàcil d’utilitzar. A més, la plataforma emmagatzema i recupera dades sempre que calgui, convertint el sistema en una eina útil per monitorar i entendre el comportament del satèl·lit.

Link del video demostratiu: https://drive.google.com/file/d/1-j9wdUP3bScsias9G_AwwVxJ__L_HbMh/view?usp=sharing

### **Versió 4**  
En aquesta etapa final del projecte, ens hem concentrat en la consolidació i refinament de totes les funcionalitats desenvolupades anteriorment, assegurant una operació robusta i fiable del sistema. El nostre satèl·lit ara imita l'estructura d'un CubeSat. També, pensant en l'accessibilitat i l'adopció global, hem implementat la traducció de la interfície de visualització de dades a 6 idiomes diferents, una característica clau que fa que la plataforma d'estació de terra sigui adaptable i fàcilment utilitzable per a operadors i investigadors de tot el món, garantint que les dades i gràfiques siguin plenament comprensibles sense barreres lingüístiques. 
Finalment, hem volgut presentar el projecte final d’una manera una mica diferent i divertida. Esperem que el gaudiu!

Link del video demostratiu: https://drive.google.com/file/d/1hRvkniphaLGZRZEO9MF9vkkqmuoNQ8-O/view?usp=sharing 

---

##  Objectiu Final  
Construir un **sistema satel·lital didàctic i funcional** que combini electrònica, comunicació, programació i visualització de dades. Una experiència completa de “terra a òrbita”.

