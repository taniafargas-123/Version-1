# Benvinguts al nostre Sistema Satel·lital!!!
### *Projecte del Grup 12 — Antoni Ruiz · Marc Conill · Tània Fargas*

Aquest projecte és el nostre viatge a l’espai: creem el prototip funcional d’un sistema satel·lital, format per un satèl·lit i una estació de terra que cooperen per captar, enviar i visualitzar dades en temps real.

---

## 🛰️ El Satèl·lit  
El nostre satèl·lit està impulsat per un **Arduino** que recull dades de temperatura, humitat i proximitat, i pot orientar sensors mitjançant servomotors. Processa la informació, envia missatges a terra i respon a ordres del usuari. Tot està programat en **C**.

---

## 🌍 L’Estació de Terra  
Format per un altre Arduino i un portàtil, aquest sistema rep i processa les dades enviades des del satèl·lit, activa alarmes i les mostra mitjançant una interfície gràfica creada en **Python**. També permet enviar ordres al satèl·lit, com modificar la freqüència d’enviament o orientar sensors.

---

## 📡 Comunicació  
La comunicació entre satèl·lit i terra utilitza **LoRa** per transmissions de llarg abast, tot i que durant el desenvolupament també s’ha treballat amb connexió per cable per evitar interferències.

---

##  Versions del Sistema  

### **Versió 1**  
- Enviament de dades de temperatura i humitat.  
- Processament bàsic i alarmes inicials a l’estació de terra.

Link del video demostratiu: 

### **Versió 2**  
- Afegit sensor d’ultrasons i servomotor orientable.  
- Gràfiques informatives i capacitat d’enviar ordres des de terra.

Link del video demostratiu: https://drive.google.com/file/d/1L44LO0Di6GdR4LK3FuMZSn6tWgFo8nDT/view?usp=sharing 

### **Versió 3**  
- Obtenció de la posició orbital del satèl·lit.  
- Visualització en mapa, guardat i recuperació de dades des de la interfície.  

---

## ✨ Objectiu Final  
Construir un **ecosistema satel·lital didàctic i funcional** que combini electrònica, comunicació, programació i visualització de dades. Una experiència completa de “terra a òrbita”.

