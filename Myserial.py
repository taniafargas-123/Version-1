import serial
import threading
import matplotlib.pyplot as plt
import time
import numpy as np
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# --- CONFIGURACIÓN SERIAL ---
device = 'COM3'
mySerial = serial.Serial(device, 9600, timeout=1)

# --- VARIABLES GLOBALES ---
angles = np.linspace(0, np.pi, 181)  
distancies = np.zeros_like(angles)
running = False
ventana_abierta = True
temperaturas = []
humedades = []
temperaturas_medias =[]
eje_x = []
i = 0
modo_actual = "Temperatura"  # Puede ser "Temperatura" o "Humedad"
modo_Media_temperatura = 0
punt=0
linea=0

# --- FUNCIONES DE CONTROL SERIAL ---
def Parar():
    global running
    mySerial.write(b'1')
    if running == True:
      print("⏸ Comunicación detenida")
    running = False

def Reanudar():
    global running
    mySerial.write(b'0')
    if running == False:
      print("▶ Comunicación reanudada")
    running = True

def IniciarComunicacion():
    global running
    running = True
    threadRecepcion = threading.Thread(target=IniciarComunicacion2, daemon=True)
    threadRecepcion.start()

def IniciarComunicacion2():
    global i, ventana_abierta, distancies, punt, linea
    suma = 0
    Temperatura_media = 0
    while ventana_abierta:
        if running and mySerial.in_waiting > 0:
            try:
                linea = mySerial.readline().decode('utf-8').strip()
                if ':' not in linea:
                    continue
                trozos = linea.split(':')
                temperatura = float(trozos[1])
                humedad = float(trozos[3])
                dist = float(trozos[5])
                ang = float(trozos[7])
                print(linea)

                eje_x.append(i)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                if 0 <= ang <= 180:
                    # Guardar la distància en l'array (index per grau)
                    distancies[int(ang)] = dist

                    # Actualitzar punt (Matplotlib polar espera radians per l'angle)
                    theta_rad = np.radians(ang)
                    punt = ([theta_rad], [dist])   # variable global usada per actualitza()
                    beam_polar.set_data([np.radians(ang),np.radians(ang)],[0,dist])

                if modo_Media_temperatura == 0:
                    if (i>9):
                        suma=suma+temperaturas[i]-temperaturas[(i-10)]
                        Temperatura_media = (suma)/10
                        print(Temperatura_media)
                    elif (i<=9):
                        suma=suma+temperaturas[i]
                        Temperatura_media = (suma)/10
                        print(Temperatura_media)
                if modo_Media_temperatura == 1:
                    Temperatura_media = float(trozos[9])
                    print(Temperatura_media)
                temperaturas_medias.append(Temperatura_media)
                i += 1
                actualizar_grafica(i)
                actualitza()
            except Exception as e:
                print("Error:", e)
        if not running and time.time()%3000 == 1:
            try:
                eje_x.append(i)
                temperaturas.append(np.nan)
                humedades.append(np.nan)    
                i += 1
        
                actualizar_grafica(i)
            except Exception as e:
                print("Error:", e)
        
# --- FUNCIÓN PARA CAMBIAR DE GRÁFICA ---
def cambiar_modo():
    global modo_actual
    if modo_actual == "Temperatura":
        modo_actual = "Humedad"
        cambiarButton.config(text="Mostrar Temperatura")
    else:
        modo_actual = "Temperatura"
        cambiarButton.config(text="Mostrar Humedad")
    actualizar_grafica()
    
# --- FUNCIÓN PARA CAMBIAR MEDIA TEMPERATURA
def cambiar_modomedia():
    global modo_Media_temperatura
    if modo_Media_temperatura == 0:
        modo_Media_temperatura = 1
        cambiarmediaButton.config(text="Media Tierra")
        mySerial.write(b'2')
    else:
        modo_Media_temperatura = 0
        cambiarmediaButton.config(text="Media Sat")
        mySerial.write(b'3')

# --- FUNCIÓN PARA ACTUALIZAR LA GRÁFICA ---
def actualizar_grafica(x):
    ax.clear()
    if modo_actual == "Temperatura":
        ax.set(xlim=(x-10,x+10),ylim=(0,50))
        ax.plot(eje_x, temperaturas, color='red', label='Temperatura (°C)')
        ax.plot(eje_x, temperaturas_medias, color="magenta",label='media temepraturas')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Gráfica de Temperatura')
        
        
    else:
        ax.set(xlim=(x-10,x+10),ylim=(0,100))
        ax.plot(eje_x, humedades, color='blue', label='Humedad (%)')
        ax.set_ylabel('Humedad (%)')
        ax.set_title('Gráfica de Humedad')

    ax.set_xlabel('Tiempo (s)')
    ax.legend()
    canvas.draw()
# --- FUNCIÓ PER ACTUALITZAR NOMÉS LES DADES (NO netejar l'eix) ---
def actualitza():
    # Actualitza la línia (angles ja en radians)
    linea_polar.set_data(angles, distancies)

    # Actualitza el punt si té dades vàlides
    try:
        RMAX = 50
        if punt is not None:
            r = min(punt[1][0], RMAX)
            punt_polar.set_data([punt[0][0]], [r])
        else:
            punt_polar.set_data([], [])

    except Exception:
        punt_polar.set_data([], [])

    # Forçar redraw del canvas polar
    canvas_polar.draw()
def cerrar_programa():
    """Se ejecuta al cerrar la ventana con la X."""
    global running, ventana_abierta
    if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
        ventana_abierta = False   # ← Esto detiene el bucle del hilo
        running = False           # ← Detiene la lectura
        try:
            if mySerial.is_open:
                mySerial.close()
                print("Puerto serial cerrado correctamente.")
        except:
            pass
        window.destroy()
        import sys
        sys.exit(0)

# --- INTERFAZ TKINTER ---
window = Tk()
window.title("Monitor Serial - Temperatura y Humedad")
window.geometry("1200x550")
window.configure(bg="lightpink")

# Configuración de rejilla principal
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)

# --- Título ---
tituloLabel = Label(window, text="Monitor Serial", font=("Times New Roman", 22, "italic"), bg='pink')
tituloLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# --- Frame de botones ---
frame_botones = Frame(window, bg="lightpink", bd=2)
frame_botones.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configurar filas y columnas del frame de botones
for r in range(5):
    frame_botones.rowconfigure(r, weight=1)
frame_botones.columnconfigure(0, weight=1)

# --- Botones ---
boton_style = {"font": ("Arial", 11), "width": 15, "height": 2}

IniciarButton = Button(frame_botones, text="Iniciar", bg='thistle', fg="black", command=IniciarComunicacion, **boton_style)
IniciarButton.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

PararButton = Button(frame_botones, text="Parar", bg='lightblue', fg="black", command=Parar, **boton_style)
PararButton.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

ReanudarButton = Button(frame_botones, text="Reanudar", bg='lightyellow', fg="black", command=Reanudar, **boton_style)
ReanudarButton.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

cambiarButton = Button(frame_botones, text="Mostrar Humedad", bg='lightgreen', fg="black", command=cambiar_modo, **boton_style)
cambiarButton.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

cambiarmediaButton = Button(frame_botones, text="Media Sat", bg='lightyellow', fg="black", command=cambiar_modomedia, **boton_style)
cambiarmediaButton.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

# --- Frame para la gráfica ---
frame_grafica = LabelFrame(window, bg="white", bd=2, text="Gráfica en tiempo real", font=("Arial", 11))
frame_grafica.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
frame_grafica.rowconfigure(0, weight=1)
frame_grafica.columnconfigure(0, weight=1)
# --- Frame para la gráfica polar
frame_grafica_polar = LabelFrame(window, bg="white", bd=2, text="Gráfica en tiempo real", font=("Arial", 11))
frame_grafica_polar.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
frame_grafica_polar.rowconfigure(0, weight=1)
frame_grafica_polar.columnconfigure(0, weight=1)

# --- Figura de Matplotlib ---
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# --- FIGURA POLAR (SUBSTITUEIX AQUEST BLOQ) ---
# angles ja era: np.linspace(0, np.pi, 181)  # radians de 0 a pi
figur = plt.figure(figsize=(6, 4))
axp = plt.subplot(111, polar=True)

# CONFIGURACIÓ FIXA
axp.set_theta_zero_location("E")   # 0° a la dreta
axp.set_theta_direction(1)        # sentit antihorari visual com a radar (opcional: -1 o 1)
axp.set_thetalim(0, np.pi)         # semicercle 0–180°
axp.set_rmax(50)                   # màxim fix
axp.set_rticks([10, 20, 30, 40, 50])
axp.set_rlabel_position(180)
axp.set_title("Radar d'Ultrasons", va='bottom')

# INICIALITZA distancies amb np.nan perquè la línia no "saltin" valors inicals
distancies = np.full_like(angles, np.nan)  # assegura que no dibuixi línia abans de dades

# Crear la línia i el punt només UNA vegada
linea_polar, = axp.plot(angles, distancies, color="yellow", lw=2, label="Distància")
punt_polar, = axp.plot([], [], "go", markersize=8, label="Feix actual")
beam_polar, = axp.plot(angles,distancies,color="blue",lw=3,label ="BEAM")

axp.legend(loc='upper right')

# Canvas dins la UI (substitueix la teva variable 'ani' per 'canvas_polar')
canvas_polar = FigureCanvasTkAgg(figur, master=frame_grafica_polar)
canvas_polar.get_tk_widget().grid(row=0, column=0, sticky="nsew")


window.protocol("WM_DELETE_WINDOW", cerrar_programa)

window.mainloop()
