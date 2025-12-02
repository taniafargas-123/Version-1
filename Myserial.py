import serial
import threading
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import numpy as np
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import difflib
import sys
import plotly.graph_objects as go
from collections import deque

# --- CONFIGURACIÓN SERIAL ---
device = 'COM5'
mySerial = serial.Serial(device, 9600, timeout=1)

# --- GLOBALS ---
angles = np.linspace(0, np.pi, 181)     # radians, length 181 (0°..180°)
distancies = np.full(len(angles), np.nan)
running = False
ventana_abierta = True

# Time series
temperaturas = []
humedades = []
temperaturas_medias = []
eje_x = []
posicionx_vals = []
posiciony_vals = []
i = 0

Grafica_izquierda = "Temperatura"   # "Temperatura" or "Humedad"
Grafica_derecha = "Distancia"       # "Distancia" or "Posición"
modo_Media_temperatura = 0

# Small helpers / constants
R_EARTH = 6371000  # meters
ALTITUDE = 400000.0  # Altitud (metres)
ORBIT_RADIUS = R_EARTH + ALTITUDE

# Paràmetres del Dibuix
MAX_POINTS = 500  # Nombre màxim de punts per dibuixar la trajectòria de l'òrbita
scale_factor = ORBIT_RADIUS / 1.5 # Escala visual: centre el rang de la gràfica
refresh_interval = 2 # Actualitza la gràfica cada 2 segons (ajusta si cal)
regex_position = re.compile(r"Position: \(X: ([\d\.-]+) m, Y: ([\d\.-]+) m, Z: ([\d\.-]+) m\)")

# --- GUI functions ---
def Parar():
    global running
    if mySerial:
        try:
            mySerial.write(b'1:0')
        except Exception as e:
            print("Serial write error:", e)
    running = False
    print("⏸ Comunicación detenida")

def Reanudar():
    global running
    if mySerial:
        try:
            mySerial.write(b'1:1')
        except Exception as e:
            print("Serial write error:", e)
    running = True
    print("▶ Comunicación reanudada")

def nada():
    print("nada")

def Enter_pressed(event=None):
    """Parse user text for 'periodo temperatura N' or 'periodo distancia N' (fuzzy)."""
    global periodo_temp, periodo_dist
    user_text = Texto.get().lower().strip()

    numeros = re.findall(r"\d+", user_text)
    numero = int(numeros[0]) if numeros else None
    if numero is None:
        print("No se encontró número.")
        Texto.delete(0, "end")
        return

    comandos = ["periodo temperatura", "periodo distancia"]
    match = difflib.get_close_matches(user_text, comandos, n=1, cutoff=0.4)
    if match:
        cmd = match[0]
        if cmd == "periodo temperatura":
            periodo_temp = numero
            print("Periodo de TEMPERATURA =", periodo_temp)
            if mySerial:
                try:
                    mySerial.write(str(periodo_temp).encode())
                except Exception as e:
                    print("Serial write error:", e)
        elif cmd == "periodo distancia":
            periodo_dist = numero
            print("Periodo de DISTANCIA =", periodo_dist)
            if mySerial:
                try:
                    mySerial.write(str(periodo_dist).encode())
                except Exception as e:
                    print("Serial write error:", e)
    else:
        print("Comando no reconocido:", user_text)
    Texto.delete(0, "end")

def IniciarComunicacion():
    global running
    running = True
    threadRecepcion = threading.Thread(target=IniciarComunicacion2, daemon=True)
    threadRecepcion.start()

def checksum(mensaje):
    sumaa = 0
    for i in mensaje:
        sumaa = sumaa+ord(i)
    sumaa = sumaa % 256
    return sumaa

def Comprueva(frase,respuesta):
    sumaa = 0
    for i in frase:
        sumaa = sumaa+ord(i)
    sumaa = sumaa%256
    if sumaa == respuesta:
        return 1
    else:
        return 0

def IniciarComunicacion2():
    global i, ventana_abierta, distancies, punt, linea
    suma = 0
    Temperatura_media = 0
    while ventana_abierta:
        if running and mySerial.in_waiting > 0:
            try:
                linea = mySerial.readline().decode('utf-8').strip()
                datos = {}

                # Cada par es: clave:valor, concatenados así: TEMP:23.5:HUM:40.2:DIST:122
                # Recorrer de 2 en 2
                parts = linea.split(":")
                j = 0
                while j < len(parts) - 1:  # -1 para no salirnos del rango
                    clave = parts[j].strip()
                    valor = parts[j+1].strip()
                    try:
                        datos[clave] = float(valor)
                    except ValueError:
                        datos[clave] = float('nan')
                        print(f"⚠ Valor no numérico para {clave}: {valor}")
                    j += 2  # saltar al siguiente par


                respuesta = checksum(linea)
                print(f"{linea}|{respuesta}")
                respuesta2 = Comprueva(linea,respuesta)
                if respuesta2 ==1:
                    print("El cheksum coincide")
                else:   
                    print("El cheksum no coincide")
                
                temperatura         = datos.get("TEMP", float("nan"))
                humedad             = datos.get("HUM",  float("nan"))
                dist                = datos.get("DIST", float("nan"))
                ang                 = datos.get("ANG",  float("nan"))
                posiciónx           = datos.get("X",    float("nan"))
                posicióny           = datos.get("Y",    float("nan"))
                posiciónz           = datos.get("Z",    float("nan"))

                eje_x.append(i)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                posicionx_vals.append(posiciónx)
                posiciony_vals.append(posicióny)
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
                    Temperatura_media   = datos.get("M",    float("nan"))
                    print(Temperatura_media)
                temperaturas_medias.append(Temperatura_media)
                i += 1
                actualizar_grafica(i)
                actualitza(posiciónx, posicióny, posiciónz)
            except Exception as e:
                print("Error:", e)
        if not running and time.time()%3000 == 1:
            try:
                eje_x.append(i)
                temperaturas.append(np.nan)
                humedades.append(np.nan)    
                i += 1
        
                actualizar_grafica(i)
                actualitza(posiciónx, posicióny, posiciónz)
            except Exception as e:
                print("Error:", e)

# Toggle left graph
def cambiar_modo_izquierda():
    global Grafica_izquierda
    if Grafica_izquierda == "Temperatura":
        Grafica_izquierda = "Humedad"
        cambiarButtonizquierda.config(text="Mostrar Temperatura")
    else:
        Grafica_izquierda = "Temperatura"
        cambiarButtonizquierda.config(text="Mostrar Humedad")
    actualizar_grafica(i)

# Toggle right graph (distance <-> position)
def cambiar_modo_derecha():
    global Grafica_derecha
    if Grafica_derecha == "Distancia":
        Grafica_derecha = "Posición"
        cambiarButtonderecha.config(text="Mostrar Distancia")
    else:
        Grafica_derecha = "Distancia"
        cambiarButtonderecha.config(text="Mostrar Posición")
    # show/hide axes accordingly
    polar_ax.set_visible(Grafica_derecha == "Distancia")
    cart_ax.set_visible(Grafica_derecha == "Posición")
    canvas_polar.draw_idle()

def cambiar_modomedia():
    global modo_Media_temperatura
    if modo_Media_temperatura == 0:
        modo_Media_temperatura = 1
        cambiarmediaButton.config(text="Media Tierra")
        if mySerial:
            try:
                mySerial.write(b'2:1')
            except Exception as e:
                print("Serial write error:", e)
    else:
        modo_Media_temperatura = 0
        cambiarmediaButton.config(text="Media Sat")
        if mySerial:
            try:
                mySerial.write(b'2:0')
            except Exception as e:
                print("Serial write error:", e)

# --- Update left plot ---
def actualizar_grafica(x):
    ax.clear()
    if Grafica_izquierda == "Temperatura":
        ax.set(xlim=(max(0, x-50), x+5), ylim=(0, 50))
        ax.plot(eje_x, temperaturas, label='Temperatura (°C)')
        ax.plot(eje_x, temperaturas_medias, label='Media temperaturas')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Gráfica de Temperatura')
    else:
        ax.set(xlim=(max(0, x-50), x+5), ylim=(0, 100))
        ax.plot(eje_x, humedades, label='Humedad (%)')
        ax.set_ylabel('Humedad (%)')
        ax.set_title('Gráfica de Humedad')
    ax.set_xlabel('Muestras')
    ax.legend()
    canvas.draw_idle()

# --- Update right plot (polar or cartesian) ---
def actualitza(posx, posy, posz):
    # Distance mode (polar)
    if Grafica_derecha == "Distancia":
        # update polar line and point
        linea_polar.set_data(np.radians(np.arange(0, 181)), distancies)
        # update current point if punt defined
        try:
            if 'punt' in globals() and punt is not None:
                r = min(punt[1][0], polar_ax_rmax)
                punt_polar.set_data([punt[0][0]], [r])
            else:
                punt_polar.set_data([], [])
        except Exception:
            punt_polar.set_data([], [])
    else:
        # Position mode: update orbit plot
        if len(posicionx_vals) > 0:
            # update orbit line and last point
            orbit_plot.set_data(posicionx_vals, posiciony_vals)
            # scatter last point
            last_point_plot.set_offsets([[posicionx_vals[-1], posiciony_vals[-1]]])

            # remove only temporary Earth-slice patches (do not clear all patches)
            # use remove() to safely delete patches from the axis
            try:
                # iterate over a copy to avoid modifying the list while iterating
                for p in list(cart_ax.patches):
                    if getattr(p, "_temp_slice", False):
                        p.remove()
            except Exception:
                pass



            # expand limits if needed
            curx = posicionx_vals[-1]
            cury = posiciony_vals[-1]
            xlim = cart_ax.get_xlim()
            ylim = cart_ax.get_ylim()
            if abs(curx) > max(abs(xlim[0]), abs(xlim[1])) or abs(cury) > max(abs(ylim[0]), abs(ylim[1])):
                new_xlim = max(abs(xlim[0]), abs(xlim[1]), abs(curx)) * 1.1
                new_ylim = max(abs(ylim[0]), abs(ylim[1]), abs(cury)) * 1.1
                cart_ax.set_xlim(-new_xlim, new_xlim)
                cart_ax.set_ylim(-new_ylim, new_ylim)
    canvas_polar.draw_idle()

def create_earth_sphere():
    """Crea la malla de l'esfera de la Terra per a Plotly."""
    # Genera una esfera de 50x50 punts per simular la Terra
    # L'esfera s'utilitza per fer-la semblar 'més real'
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]
    x = R_EARTH * np.cos(u) * np.sin(v)
    y = R_EARTH * np.sin(u) * np.sin(v)
    z = R_EARTH * np.cos(v)
    
    # Crea el gràfic de l'esfera
    earth_sphere = go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, 'rgb(0,0,150)'], [1, 'rgb(0,100,255)']],  # Color de l'aigua
        showscale=False,
        opacity=0.8,
        name='Terra'
    )
    return earth_sphere
def plot_orbit(earth_sphere, orbit_trail):
    """Actualitza i mostra el gràfic 3D amb l'òrbita i la Terra."""
    
    if not orbit_trail:
        return
        
    # Extreu les coordenades X, Y, Z de la cua
    x_orbit, y_orbit, z_orbit = zip(*orbit_trail)
    
    # 1. Traçat de l'Òrbita (La Línia)
    orbit_trace = go.Scatter3d(
        x=x_orbit, y=y_orbit, z=z_orbit,
        mode='lines',
        line=dict(color='yellow', width=5),
        name='Òrbita del Satèl·lit'
    )
    
    # 2. Posició Actual del Satèl·lit (El Punt)
    sat_point = go.Scatter3d(
        x=[x_orbit[-1]], y=[y_orbit[-1]], z=[z_orbit[-1]],
        mode='markers',
        marker=dict(size=8, color='red', symbol='circle'),
        name='Satèl·lit'
    )
    
    # 3. Traçat de l'Òrbita de Referència (Cercle en el pla X-Y)
    # Només dibuixem l'òrbita de referència si la inclinació és zero
    angle = np.linspace(0, 2 * np.pi, 100)
    x_ref = ORBIT_RADIUS * np.cos(angle)
    y_ref = ORBIT_RADIUS * np.sin(angle)
    z_ref = np.zeros_like(x_ref)
    
    ref_orbit = go.Scatter3d(
        x=x_ref, y=y_ref, z=z_ref,
        mode='lines',
        line=dict(color='gray', width=1, dash='dash'),
        name='Òrbita de Referència'
    )

    # Crea la figura
    fig = go.Figure(data=[earth_sphere, ref_orbit, orbit_trace, sat_point])
    
    # Configuració del Layout
    fig.update_layout(
        title='Simulació d\'Òrbita Circular de Satèl·lit (Arduino/Python)',
        scene=dict(
            xaxis=dict(title='Eix X (metres)', range=[-scale_factor, scale_factor]),
            yaxis=dict(title='Eix Y (metres)', range=[-scale_factor, scale_factor]),
            zaxis=dict(title='Eix Z (metres)', range=[-scale_factor, scale_factor]),
            aspectmode='cube' # Mantenir la relació d'aspecte per a una correcta visualització 3D
        )
    )
def cerrar_programa():
    global running, ventana_abierta
    if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
        ventana_abierta = False
        running = False
        try:
            if mySerial and mySerial.is_open:
                mySerial.close()
                print("Puerto serial cerrado correctamente.")
        except:
            pass
        window.destroy()
        sys.exit(0)



# --- TKINTER UI SETUP ---
window = Tk()
window.title("Monitor Serial - Temperatura y Humedad")
window.geometry("1200x620")
window.configure(bg="lightpink")

# Grid layout
window.rowconfigure(1, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)

tituloLabel = Label(window, text="Monitor Serial", font=("Times New Roman", 22, "italic"), bg='pink')
tituloLabel.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

frame_botones = Frame(window, bg="lightpink", bd=2)
frame_botones.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

frame_botones_dos = Frame(window, bg="lightpink", bd=2)
frame_botones_dos.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

row2frame = Frame(window, bg="lightpink")
row2frame.grid(row=2, column=0, columnspan=4, pady=10, sticky="nsew")
row2frame.columnconfigure(1, weight=1)

# Input box with placeholder
input_user = StringVar()
def set_placeholder(event=None):
    if Texto.get() == "":
        Texto.insert(0, "Escribe el periodo de temperatura y humedad o el periodo de la distancia")
        Texto.config(fg="grey")
def clear_placeholder(event=None):
    if Texto.get() == "Escribe el periodo de temperatura y humedad o el periodo de la distancia":
        Texto.delete(0, "end")
        Texto.config(fg="black")

Texto = Entry(row2frame, textvariable=input_user, width=60, font=("Arial", 12), fg="grey")
Texto.grid(row=0, column=1, padx=10, pady=5, sticky="nsew", ipady=8)
Texto.bind("<Return>", Enter_pressed)
Texto.bind("<FocusIn>", clear_placeholder)
Texto.bind("<FocusOut>", set_placeholder)
set_placeholder()

# Buttons
boton_style = {"font": ("Arial", 11), "width": 15, "height": 2}
IniciarButton = Button(frame_botones, text="Iniciar", bg='thistle', fg="black", command=IniciarComunicacion, **boton_style)
PararButton = Button(frame_botones, text="Parar", bg='lightblue', fg="black", command=Parar, **boton_style)
ReanudarButton = Button(frame_botones, text="Reanudar", bg='lightyellow', fg="black", command=Reanudar, **boton_style)
cambiarButtonizquierda = Button(frame_botones, text="Mostrar Humedad", bg='lightgreen', fg="black", command=cambiar_modo_izquierda, **boton_style)
cambiarmediaButton = Button(frame_botones, text="Media Sat", bg='lightyellow', fg="black", command=cambiar_modomedia, **boton_style)

IniciarButton.grid(row=0, column=0, padx=5, pady=5)
PararButton.grid(row=1, column=0, padx=5, pady=5)
ReanudarButton.grid(row=2, column=0, padx=5, pady=5)
cambiarButtonizquierda.grid(row=3, column=0, padx=5, pady=5)
cambiarmediaButton.grid(row=4, column=0, padx=5, pady=5)

PararButtonPolar = Button(frame_botones_dos, text ="Parar",bg ='lightblue',fg ="black",command =nada, **boton_style)
ReanudarButtonPolar = Button(frame_botones_dos, text="Reanudar", bg='lightyellow', fg="black", command=nada, **boton_style)
cambiarButtonderecha = Button(frame_botones_dos, text="Mostrar Posición", bg='lightgreen', fg="black", command=cambiar_modo_derecha, **boton_style)

PararButtonPolar.grid(row=1, column=0, padx=5, pady=5)
ReanudarButtonPolar.grid(row=2, column=0, padx=5, pady=5)
cambiarButtonderecha.grid(row=3, column=0, padx=5, pady=5)

# --- Left graph (time series) ---
frame_grafica = LabelFrame(window, bg="white", bd=2, text="Gráfica en tiempo real", font=("Arial", 11))
frame_grafica.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
frame_grafica.rowconfigure(0, weight=1)
frame_grafica.columnconfigure(0, weight=1)

fig = matplotlib.figure.Figure(figsize=(6,4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# --- Right graph (polar or position) ---
frame_grafica_polar = LabelFrame(window, bg="white", bd=2, text="Gráfica en tiempo real", font=("Arial", 11))
frame_grafica_polar.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
frame_grafica_polar.rowconfigure(0, weight=1)
frame_grafica_polar.columnconfigure(0, weight=1)

fig_polar = matplotlib.figure.Figure(figsize=(6,4))
# create two axes: one polar and one cartesian; toggle visibility
polar_ax = fig_polar.add_subplot(1,1,1, polar=True)
cart_ax = fig_polar.add_subplot(1,1,1, polar=False, frame_on=True)  # will overlap; we will toggle visibility

# configure polar axis
polar_ax.set_theta_zero_location("E")
polar_ax.set_theta_direction(1)
polar_ax.set_thetalim(0, np.pi)
polar_ax_rmax = 50
polar_ax.set_rmax(polar_ax_rmax)
polar_ax.set_rticks([10,20,30,40,50])
polar_ax.set_rlabel_position(180)
polar_ax.set_title("Radar de Ultrasonidos", va='bottom')

# configure cartesian axis (for satellite position)
cart_ax.set_xlabel("X (meters)")
cart_ax.set_ylabel("Y (meters)")
cart_ax.set_title("Satellite Equatorial Orbit (View)")

# Set sensible initial limits for cartesian axis so Earth circle doesn't dominate
lim = R_EARTH * 1.2
cart_ax.set_xlim(-lim, lim)
cart_ax.set_ylim(-lim, lim)
cart_ax.set_aspect('equal', 'box')

# initial artists (polar mode)
linea_polar, = polar_ax.plot(np.radians(np.arange(0,181)), distancies, lw=2, label="Distancia")
punt_polar, = polar_ax.plot([], [], "go", markersize=8, label="haz actual")
beam_polar, = polar_ax.plot([], [], lw=3, label="BEAM")
polar_ax.legend(loc='upper right')

# initial artists (cartesian mode)
orbit_plot, = cart_ax.plot([], [], 'bo-', markersize=2, label='Satellite Orbit')
last_point_plot = cart_ax.scatter([], [], color='red', s=30, label='Last Point')

# Add Earth surface as a patch on the correct axis (cart_ax) using patches (not plt.Circle)
earth_circle = mpatches.Circle((0, 0), R_EARTH, fill=False, edgecolor='orange', linewidth=1.5, zorder=0)
cart_ax.add_patch(earth_circle)

# Start with polar visible and cart hidden
polar_ax.set_visible(True)
cart_ax.set_visible(False)

canvas_polar = FigureCanvasTkAgg(fig_polar, master=frame_grafica_polar)
canvas_polar.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# protocol
window.protocol("WM_DELETE_WINDOW", cerrar_programa)

# Start tkinter mainloop
window.mainloop()
