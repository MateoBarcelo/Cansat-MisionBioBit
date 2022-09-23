from osgeo import gdal
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from imageresize import Resize
t = np.float32

satImage = "multi_bands.tif"

def processImages():
    #Lectura con gdal (geospatial data abstraction library)
    img = gdal.Open(satImage)

    #Matplot graph
    red = img.GetRasterBand(1).ReadAsArray(0,0, img.RasterXSize, img.RasterYSize) #Pasar como parametro la banda RED 
    nir = img.GetRasterBand(2).ReadAsArray(0,0, img.RasterXSize, img.RasterYSize) #Pasar como parametro la banda NIR (Near InfraRed)
    swir = img.GetRasterBand(3).ReadAsArray(0,0, img.RasterXSize, img.RasterYSize) #Banda 7 swir
    green = img.GetRasterBand(4).ReadAsArray(0,0, img.RasterXSize, img.RasterYSize) #Banda 2 green
    #CONVERTIR 16 bits a float para poder hacer la division:
    nir = nir.astype(t)
    red = red.astype(t)
    swir = swir.astype(t)
    green.astype(t)
    #NDVI Calc
    np.seterr(invalid='ignore')
    ndvi = (nir - red)/(nir + red)
    nbr = (nir - swir)/(nir + swir)
    ndwi = (green - nir)/(green + nir)
    # El valor de ndvi esta entre -1 y 1, hay que hacerlo visible
    # Entonces hacemos el valor positivo para eliminar los negativos y lo escalamos a 16 bits:
    ndvi = (ndvi + 1) * (2**15 - 1)
    nbr = (nbr + 1) * (2**15 - 1)
    ndwi = (ndwi + 1) * (2**15 - 1) 
    #Mejorar contraste
    ndvi[ndvi < -0] = 0
    nbr[nbr < -0] = 0

    #Seteo de figuras
    figndvi = plt.figure(figsize=(12,10))
    plt.imshow(ndvi, cmap="RdYlGn")
    cbar = plt.colorbar()
    plt.title("INDICE NDVI")
    plt.xlabel('Pixeles')
    plt.ylabel('Pixeles')
    fignbr = plt.figure(figsize=(12,10))
    plt.imshow(nbr, cmap="PiYG")
    cbar1=plt.colorbar()
    plt.title("INDICE NBR")
    plt.xlabel('Pixeles')
    plt.ylabel('Pixeles')
    figndwi = plt.figure(figsize=(12,10))
    plt.imshow(ndwi, cmap="RdBu")
    cbar2=plt.colorbar()
    plt.title("INDICE NDWI")
    plt.xlabel('Pixeles')
    plt.ylabel('Pixeles')
    #Cambiar color de texto
    cbar.ax.tick_params(axis='y',labelcolor='white')
    figndvi.gca().tick_params(axis='both',labelcolor='white')

    cbar1.ax.tick_params(axis='y',labelcolor='white')
    fignbr.gca().tick_params(axis='both',labelcolor='white')

    cbar2.ax.tick_params(axis='y',labelcolor='white')
    figndwi.gca().tick_params(axis='both',labelcolor='white')

    plt.show()
    figndvi.savefig('ndvi.png', bbox_inches='tight', transparent=True) 
    fignbr.savefig('nbr.png', bbox_inches='tight', transparent=True)
    figndwi.savefig('ndwi.png', bbox_inches='tight',transparent=True)

    resize = Resize(400)
    resize.resizeImage('ndvi.png')
    resize.resizeImage('nbr.png')
    resize.resizeImage('ndwi.png')