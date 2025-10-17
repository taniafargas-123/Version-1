import serial
import threading
import matplotlib.pyplot as plt
from tkinter import *

device = 'COM3'
mySerial = serial.Serial(device, 9600)

def Parar ():
   mySerial.write(b'1')
   print("Parar")
def Reanudar():
   mySerial.write(b'0')
   print("Reanudar")
def IniciarComunicacion ():
   threadRecepcion = threading.Thread (target = IniciarComunicacion2)
   threadRecepcion.start()

def IniciarComunicacion2 ():
  
   try:
      plt.ion()
      plt.axis([0,100,20,30])
      temperaturas=[]
      humedades = []
      eje_x =[]
      i = 0
      while True:
         if mySerial.in_waiting > 0:
            linea = mySerial.readline().decode('utf-8').rstrip()
            trozos= linea.split(':')
            print(linea)
            eje_x.append(i)
            temperatura=float(trozos[1])
            humedad = float(trozos[3])
            temperaturas.append (temperatura)
            humedades.append(humedad)
            plt.plot(eje_x,temperaturas)
            plt.title(str(i))
            i=i+1
            plt.draw()
            plt.pause(0.5) 
         
   except KeyboardInterrupt:
      print("saliendo...")
   finally:
      mySerial.close()
   
window = Tk()
window.geometry("400x400")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

tituloLabel = Label(window, text = "Mi programa", font=("<TimesNewRoman", 20, "italic"), bg='pink')
tituloLabel.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky=N + S + E + W)

IniciarButton = Button(window, text="Iniciar", bg='thistle', fg="black",command=IniciarComunicacion)
IniciarButton.grid(row=1, column=0,rowspan=2, padx=5, pady=5, sticky=N + S + E + W)
PararButton = Button(window, text="Parar", bg='lightblue', fg="black",command=Parar)
PararButton.grid(row=1, column=1,rowspan=2, padx=5, pady=5, sticky=N + S + E + W)
ReanudarButton = Button(window, text="Reanudar", bg='lightyellow', fg="black", command=Reanudar)
ReanudarButton.grid(row=1, column=2,rowspan=2, padx=5, pady=5, sticky=N + S + E + W)

window.mainloop()
   
