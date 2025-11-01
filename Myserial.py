import serial
import threading
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- CONFIGURACIÓN SERIAL ---
device = 'COM6'
mySerial = serial.Serial(device, 9600, timeout=1)

# --- VARIABLES GLOBALES ---
running = False
ventana_abierta = True
temperaturas = []
humedades = []
eje_x = []
i = 0
modo_actual = "Temperatura"  # Puede ser "Temperatura" o "Humedad"

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
    global i ,ventana_abierta
    while ventana_abierta:
        if running and mySerial.in_waiting > 0:
            try:
                linea = mySerial.readline().decode('utf-8').strip()
                if ':' not in linea:
                    continue
                trozos = linea.split(':')
                temperatura = float(trozos[1])
                humedad = float(trozos[3])
                print(linea)

                eje_x.append(i)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                i += 1
        
                actualizar_grafica()
            except Exception as e:
                print("Error:", e)
        else:
            try:
                linea = mySerial.readline().decode('utf-8').strip()
                if ':' not in linea:
                    continue
                trozos = linea.split(':')
                temperatura = float(trozos[1])
                humedad = float(trozos[3])
                print(linea)

                eje_x.append(i)
                temperaturas.append()
                humedades.append()
                i += 1
        
                actualizar_grafica()
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

# --- FUNCIÓN PARA ACTUALIZAR LA GRÁFICA ---
def actualizar_grafica():
    ax.clear()
    if modo_actual == "Temperatura":
        ax.plot(eje_x, temperaturas, color='red', label='Temperatura (°C)')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Gráfica de Temperatura')
    else:
        ax.plot(eje_x, humedades, color='blue', label='Humedad (%)')
        ax.set_ylabel('Humedad (%)')
        ax.set_title('Gráfica de Humedad')

    ax.set_xlabel('Tiempo (s)')
    ax.legend()
    canvas.draw()

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
window.geometry("900x550")
window.configure(bg="lightpink")

# Configuración de rejilla principal
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)

# --- Título ---
tituloLabel = Label(window, text="Monitor Serial", font=("Times New Roman", 22, "italic"), bg='pink')
tituloLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# --- Frame de botones ---
frame_botones = Frame(window, bg="lightpink", bd=2)
frame_botones.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configurar filas y columnas del frame de botones
for r in range(4):
    frame_botones.rowconfigure(r, weight=1)
frame_botones.columnconfigure(0, weight=1)

# --- Botones ---
boton_style = {"font": ("Arial", 12), "width": 15, "height": 2}

IniciarButton = Button(frame_botones, text="Iniciar", bg='thistle', fg="black", command=IniciarComunicacion, **boton_style)
IniciarButton.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

PararButton = Button(frame_botones, text="Parar", bg='lightblue', fg="black", command=Parar, **boton_style)
PararButton.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

ReanudarButton = Button(frame_botones, text="Reanudar", bg='lightyellow', fg="black", command=Reanudar, **boton_style)
ReanudarButton.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

cambiarButton = Button(frame_botones, text="Mostrar Humedad", bg='lightgreen', fg="black", command=cambiar_modo, **boton_style)
cambiarButton.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

# --- Frame para la gráfica ---
frame_grafica = LabelFrame(window, bg="white", bd=2, text="Gráfica en tiempo real", font=("Arial", 11))
frame_grafica.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
frame_grafica.rowconfigure(0, weight=1)
frame_grafica.columnconfigure(0, weight=1)

# --- Figura de Matplotlib ---
fig, ax = plt.subplots(figsize=(7, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

window.protocol("WM_DELETE_WINDOW", cerrar_programa)

window.mainloop()

