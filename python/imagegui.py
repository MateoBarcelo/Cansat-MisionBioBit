from asyncio.windows_events import NULL
from pathlib import Path
from tkinter import Label, Tk, ttk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
from os.path import exists
import os

#os.chdir("D:/USUARIO/Desktop/CanSat/LoraTests/")
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH

def relative_to_assets(path: str) -> Path:
	return ASSETS_PATH / Path(path)


global nbr,ndvi,ndwi,indicetext
nbr = NULL
ndvi = NULL
ndwi = NULL  
indicetext = NULL
print(relative_to_assets('nbr.png'))
class imageWindow1:

    def __init__(self,  window):
        self.window=window

    def createWindow(window):
        imageWindow = Toplevel(window)
        imageWindow.geometry('1366x768')
        imgcanvas = Canvas(
            imageWindow,
            bg= "#30394A",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        
        imgcanvas.place(x=0,y=0)
        
        try:
            globals()["nbr"]=PhotoImage(file=relative_to_assets("convertednbr.png"))
        except:
            globals()["nbr"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))

        try:
            globals()["ndvi"] = PhotoImage(file=relative_to_assets("convertedndvi.png"))
        except:
            globals()["ndvi"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))

        try:
            globals()["ndwi"] = PhotoImage(file=relative_to_assets("convertedndwi.png"))
        except:
            globals()["ndwi"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))

        globals()["indicetext"] = PhotoImage(file=relative_to_assets("build/assets/indicestext.png"))
        imgcanvas.create_image(
            230.0,
            260.0,
            image=nbr)

        imgcanvas.create_image(
            680.0,
            260.0,
            image=ndvi
        )
        imgcanvas.create_image(
            1100.0,
            260.0,
            image=ndwi
        )

        imgcanvas.create_image(
            610.0,
            600.0,
            image=indicetext
        )
        imgcanvas.create_rectangle(
            0.0,
            6.103515625e-05,
            1366.0,
            76.00018310546875,
            fill="#2A3444",
            outline="")

        imgcanvas.create_text(
            26.0,
            8.0,
            anchor="nw",
            text="Misión BIO-BIT",
            fill="#E9E9E9",
            font=("Varela Round Regular", 48 * -1)
        )

        imgcanvas.create_rectangle(
            3.0,
            76.0,
            390.0,
            79.0,
            fill="#1FB8BD",
            outline="")

    def updateImages():
        try:
            globals()["nbr"]=PhotoImage(file=relative_to_assets("convertednbr.png"))
        except:
            globals()["nbr"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))

        try:
            globals()["ndvi"] = PhotoImage(file=relative_to_assets("convertedndvi.png"))
        except:
            globals()["ndvi"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))

        try:
            globals()["ndwi"] = PhotoImage(file=relative_to_assets("convertedndwi.png"))
        except:
            globals()["ndwi"]=PhotoImage(file=relative_to_assets("build/assets/loadingimage.png"))


        
        
        
        
    
    
