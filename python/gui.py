
from asyncio.windows_events import NULL
from dataclasses import asdict
from datetime import datetime
from functools import partial
from genericpath import exists
import os
from pathlib import Path
from ssl import VERIFY_CRL_CHECK_CHAIN
import sys
import threading
import time
import tkinter
import serial
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import mplcyberpunk
import serial.tools.list_ports
import bandprocessing
from vegcalculation import VegetationCalculation
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import DISABLED, Label, StringVar, Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

from ee2 import EEProcess

import imagegui
global ser
try:
    ser = serial.Serial('COM5', 9600, timeout=1)
except:
    ser = NULL

#VARIABLES GLOBALES
global pressure,temperature,co,met,altitud,latitud,longitud,isNotPlotted, grafico3, isLabelOn

#INCIALIZACION DE VARIABLES BASICAS 
pressure = "0"
temperature = "0"
co = "0"
met = "0"
altitud = "0"

#VARIABLES DE TIEMPO Y VALORES EN VENTANA GRAPHS
tiemp = []
y1 = []
y2 = []
y3 = []
y4 = []

#VARIABLES GRAFICO EMBED EN VENTANA PRINCIPAL
isNotPlotted = True
isLabelOn = False
grafico3 = NULL

#DIRECTORIO PARA ACCEDER A LOS ASSETS
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("build/assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ReadSerial(threading.Thread):
    loop = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.loop = True

    def stop(self):
        self.loop = False
        sys.exit()
        
    def run(self):
        # Read and record the data
        while (self.loop):
            if True:
                
                try:
                    data1=ser.readline().strip().decode("utf-8") #Array de valores
                except:
                    data1="0,0,0,0,0,0,0,0"
                data = data1.split(",")
                print(data)
                try:
                    globals()['pressure'] = data[0] #OBTENER PRESION, INDICE 0
                    globals()['temperature'] = data[1] #OBTENER TEMPERATURA, INDICE 1
                    globals()['latitud'] = data[2]
                    globals()['longitud'] = data[3]
                    globals()['altitud'] = data[4] #OBTENER ALTITUD INDICE 4
                    globals()['co'] = data[5] #OBTENER CO, INDICE 5
                    globals()['met'] = data[6] #OBTENER METANO, INDICE 6
                    pkt = data[7]
                    canvas.itemconfig(presion, text = pressure+"hPa")
                    canvas.itemconfig(temp, text = temperature+"°C")
                    canvas.itemconfig(lat, text = latitud)
                    canvas.itemconfig(long, text = longitud)
                    canvas.itemconfig(alt, text = altitud+"m")
                    canvas.itemconfig(emisionco, text = co+"ppm")
                    canvas.itemconfig(emisionmet, text = met+"ppm")
                    canvas.itemconfig(packetnum, text = pkt)
                except:
                    continue
            
                time.sleep(0.5)
                
class Loop(threading.Thread):
    loop = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.loop = True

    def stop(self):
        self.loop = False
        sys.exit()
    def run(self):
        
        while (self.loop):
            if True:
                try:
                    time.sleep(1)
                    canvas.itemconfig(hora, text = time.strftime("%H:%M:%S"))
                    #Append valores de graficos
                    tiemp.append(next(index))
                    y1.append(pressure)
                    y2.append(temperature)
                    y3.append(int(co))
                    y4.append(int(met))
                except:
                    self.stop()

class downloadImages(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def stop():
        sys.exit()
    def run(self):
        while(True):
            time.sleep(1)
            if(float(altitud) >= 200):
                print("Descargando Imagen...")
                downloadImage()
                break

plt.style.use('cyberpunk')

index = count()

#ANIMAR GRAFICOS
def animate(i):
    graph1, graph2, graph3,graph4 = plt.figure(1).get_axes()
    plt.cla()
    graph1.plot(tiemp, y1, color = "#FE53BB")
    graph2.plot(tiemp, y2, color = "#08F7FE")
    graph3.plot(tiemp, y3, color = '#F5D300')
    graph4.plot(tiemp, y4, color = '#00ff41')
    #SET Y AXIS TITLES
    graph1.set_ylabel("Presion")
    graph2.set_ylabel("Temperatura")
    graph3.set_ylabel("Monóxido CO")
    graph4.set_ylabel("Metano CH4")
    
#PONER LOS GRÁFICOS EN LA VENTANA GRAPHS
def cargarGraficos(graphs1):

    figtp = plt.figure(1) #get current figure
    figtp.set_size_inches(14, 8) #tamaño para que abarque toda la pantalla
    canvas1 = FigureCanvasTkAgg(figtp, master = graphs1) #embed grafico en el canvas graphs
    canvas1.get_tk_widget().grid(column=0, row=1)
    gs = figtp.add_gridspec(4, hspace=0.3) #dividir en 4 subplots 
    gs.subplots(sharex = True) #mismaS propiedades de x para todos
    for axis in figtp.get_axes():
        axis.get_xaxis().set_visible(False)
    plt.gca().autoscale()
    figtp.canvas.draw_idle()

def openGraphWindow(event):
    #GRAPHS WINDOW (Iniciar nueva ventana con TopLevel)
    graphs = Toplevel(window)
    graphs.geometry("1366x768")
    #CANVAS DE LA VENTANA DE GRÁFICOS
    canvas2 = Canvas(
        graphs,
        bg= "#30394A",
        height=768,
        width=1366,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    cargarGraficos(graphs)

def openImageWindow(event):
    imagegui.imageWindow1.createWindow(window)

#MAIN WINDOW
window = Tk()
window.geometry("1366x768")
window.configure(bg="#FFFFFF")

#PORT WINDOW

combo = NULL
comboarr = StringVar()

def showComboBox(event):
    #COMBO VISIBLE
    combo = ttk.Combobox(window, textvariable=comboarr)
    combo['values'] = ("COM5","COM7","COM6","COM11")
    combo.bind('<<ComboboxSelected>>',setComboBoxSelected)
    combo.place(x=820, y=30)

    
def setComboBoxSelected(event):
    
    globals()['ser'] = serial.Serial(str(comboarr.get()), 9600, timeout=1)
    

ani=FuncAnimation(plt.figure(1), animate, 1000)

#CANVAS DE LA VENTANA PRINCIPAL
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=768,
    width=1366,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)


def animate2(i):

    #IF NECESARIO PARA NO GENERAR GRAFICOS INFINITOS
    if(globals()['isNotPlotted']):
        globals()['grafico3'] = plt.figure(2).subplots()
        globals()['isNotPlotted'] = False

    globals()['grafico3'].set_facecolor("#2A3444") #COLOR DE GRAFICO

    globals()['grafico3'].plot(tiemp,y1, color = "#FE53BB", label = "Pres.")
    globals()['grafico3'].plot(tiemp,y2, color = "#08F7FE", label = "Temp.")

    #Poner el label una sola vez y que no se repita infinitamente
    if not (isLabelOn):
        globals()['grafico3'].legend(loc = "upper right")
        globals()['isLabelOn'] = True
        
#GRAFICO EMBED EN VENTANA PRINCIPAL
grafico = plt.figure(2)
grafico.set_size_inches(4.8,3.1)
graficopt = FigureCanvasTkAgg(grafico, master = window) #embed grafico en el canvas graphs
graficopt.get_tk_widget().grid(column=0, row=1)
for axis in grafico.get_axes():
    axis.get_xaxis().set_visible(False)
    
ani2 = FuncAnimation(plt.figure(2), animate2, 1000)

graficopt.get_tk_widget().place(x=810, y=430) # TODO CHECK THIS MAT <-----------------
grafico.canvas.draw_idle()

windowBg=canvas.create_rectangle(
    0.0,
    0.0,
    1366.0,
    768.0,
    fill="#30394A",
    outline="")

canvas.create_rectangle(
    0.0,
    6.103515625e-05,
    1366.0,
    76.00018310546875,
    fill="#2A3444",
    outline="")

canvas.create_text(
    26.0,
    8.0,
    anchor="nw",
    text="Misión BIO-BIT",
    fill="#E9E9E9",
    font=("Varela Round Regular", 48 * -1)
)

canvas.create_rectangle(
    3.0,
    76.0,
    390.0,
    79.0,
    fill="#1FB8BD",
    outline="")

global ndvi    
ndvi = NULL
try:
    globals()["ndvi"] = PhotoImage(file=relative_to_assets("convertedndvi.png"))
except:
    globals()["ndvi"]=PhotoImage(file=relative_to_assets("loadingimage.png"))

image_1 = canvas.create_image(
    1066.0,
    265.0,
    image=ndvi
)
#BOTON GRAPH
graphimg = PhotoImage(file=relative_to_assets("image_3.png"))
graph_button=canvas.create_image(
    600,
    40,
    image=graphimg
)
#BOTON IMAGENES
satimg = PhotoImage(file=relative_to_assets("image_4.png"))
sat_button = canvas.create_image(
    680,
    40,
    image=satimg
)
#BOTON PUERTO
puertoimg= PhotoImage(file=relative_to_assets("image_5.png"))
puerto_button = canvas.create_image(
    770,
    40,
    image=puertoimg
)


#BINDEAR BOTONES A SUS RESP. FUNCIONES
canvas.tag_bind(graph_button, "<Button-1>", openGraphWindow)
canvas.tag_bind(puerto_button, "<Button-1>", showComboBox)
canvas.tag_bind(sat_button, "<Button-1>", openImageWindow)
canvas.create_rectangle(
    26.0,
    136.0,
    384.0,
    314.0,
    fill="#2A3444",
    outline="")

canvas.create_rectangle(
    26.0,
    314.0,
    384.0,
    317.0,
    fill="#00C6BA",
    outline="")

canvas.create_text(
    49.0,
    152.0,
    anchor="nw",
    text="Temperatura:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    206.0,
    anchor="nw",
    text="Presion:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    260.0,
    anchor="nw",
    text="Altitud:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_rectangle(
    423.0,
    136.0,
    781.0,
    314.0,
    fill="#2A3444",
    outline="")

canvas.create_rectangle(
    26.0,
    375.0,
    781.0,
    733.0,
    fill="#2A3444",
    outline="")

canvas.create_text(
    49.0,
    442.0,
    anchor="nw",
    text="Emision CO:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    490.0,
    anchor="nw",
    text="Emision CH4:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    625.0,
    anchor="nw",
    text="Latitud:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    673.0,
    anchor="nw",
    text="Longitud:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)


canvas.create_rectangle(
    26.0,
    733.0,
    781.0,
    736.0,
    fill="#00C6BA",
    outline="")

canvas.create_rectangle(
    423.0,
    314.0,
    780.0,
    317.0,
    fill="#00C6BA",
    outline="")

canvas.create_text(
    446.0,
    152.0,
    anchor="nw",
    text="Tiempo:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    446.0,
    206.0,
    anchor="nw",
    text="Hora:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    446.0,
    260.0,
    anchor="nw",
    text="N° Paquete:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    446.0,
    446.0,
    anchor="nw",
    text="Buen estado:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    446.0,
    487.0,
    anchor="nw",
    text="Mal estado:",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)

canvas.create_text(
    49.0,
    381.0,
    anchor="nw",
    text="Sensores",
    fill="#00E4D6",
    font=("HelveticaRounded-Bold", 32 * -1)
)

canvas.create_text(
    446.0,
    384.0,
    anchor="nw",
    text="Vegetacion",
    fill="#00E4D6",
    font=("HelveticaRounded-Bold", 32 * -1)
)

canvas.create_text(
    49.0,
    568.0,
    anchor="nw",
    text="GPS",
    fill="#00E4D6",
    font=("HelveticaRounded-Bold", 32 * -1)
)

canvas.create_text(
    446.0,
    568.0,
    anchor="nw",
    text="Estado",
    fill="#00E4D6",
    font=("HelveticaRounded-Bold", 32 * -1)
)
# -------------PARAMETROS NUMERICOS----------------

tiempomision = canvas.create_text(
    652.0,
    152.0,
    anchor="nw",
    text="01:00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

buenaveg = canvas.create_text(
    660.0,
    449.0,
    anchor="nw",
    text="N/D",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

malaveg = canvas.create_text(
    660.0,
    490.0,
    anchor="nw",
    text="N/D",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

estado = canvas.create_text(
    446.0,
    627.0,
    anchor="nw",
    text="x",
    fill="#FFFFFF",
    font=("HelveticaRounded-Bold", 28 * -1)
)
downimg= PhotoImage(file=relative_to_assets("image_6.png"))
succimg=PhotoImage(file=relative_to_assets("image_7.png"))
down_button = canvas.create_image(
    600,
    700,
    image=downimg
)
#Check image disponibility
if(exists("multi_bands.tif")):
    canvas.itemconfig(estado,text="Imagen obtenida!")
    canvas.itemconfig(down_button, image=succimg)
else:
    canvas.itemconfig(estado,text="Imagen no obtenida...")
    

def calculateVeg():
    vegPercent = VegetationCalculation.getVegetationPercentage()
    canvas.itemconfig(buenaveg, text=vegPercent + "%")
    canvas.itemconfig(malaveg, text = str((100-float(vegPercent))) + "%")

try:
    calculateVeg()
except:
    ""

def downloadImage():
    canvas.itemconfig(estado,text="Obteniendo imagen...")
    EEProcess(float(lat), float(long)).start()
    canvas.itemconfig(estado,text="Imagen obtenida!")
    canvas.itemconfig(down_button, image=succimg)
    bandprocessing.processImages()
    imagegui.imageWindow1.updateImages()
    calculateVeg()
    globals()["ndvi"] = PhotoImage(file=relative_to_assets("convertedndvi.png"))
    canvas.itemconfig(image_1,image=globals()["ndvi"])
    canvas.update()

def startDownload(event):
    threaddown.start()
    

threaddown = threading.Thread(target=downloadImage) #Empezar thread para descargar la imagen
canvas.tag_bind(down_button, "<Button-1>", startDownload)

lat = canvas.create_text(
    205.0,
    625.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

long = canvas.create_text(
    205.0,
    673.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

hora = canvas.create_text(
    618.0,
    206.0,
    anchor="nw",
    text=datetime.now().strftime("%H:%M:%S"),
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

packetnum = canvas.create_text(
    690.0,
    258.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

emisionco = canvas.create_text(
    255.0,
    442.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

emisionmet = canvas.create_text(
    255.0,
    490.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

presion = canvas.create_text(
    219.0,
    206.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

temp = canvas.create_text(
    255.0,
    152.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

alt = canvas.create_text(
    239.0,
    260.0,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Inter Medium", 28 * -1)
)

window.resizable(True, True)
global serialRead,loopThings,img

def leerSerial():
	globals()['serialRead'] = ReadSerial()
def leerTiempo():
    globals()['loopThings'] = Loop()
def downImage():
    globals()['img'] = downloadImages()
def onClose():
    window.destroy()
    serialRead.stop()
    loopThings.stop()
    img.stop()
    

window.after(0, leerSerial())
window.after(0, leerTiempo())
#window.after(0, cargarGraficos())
window.after(0, downImage())
window.protocol("WM_DELETE_WINDOW", onClose)
window.mainloop()
