from osgeo import gdal
import numpy as np
import os
import matplotlib.pyplot as plt

#RUTA IMAGEN (de donde vamos a leer la imagen)
path = "D:/USUARIO/Desktop/CanSat/LoraTests/LandSat"
#os.chdir(path)
t = np.float32
#Seleccionar archivo (ex: "asd.tif") TODO CONVERTIR IMAGEN A TIF
satImage = "multi_ban.tif"
satImage2 = "LC08_L2SP_227080_20220801_20220806_02_T1_SR_B4.TIF"
#Lectura con gdal (geospatial data abstraction library)
img = gdal.Open(satImage)
img1 = gdal.Open(satImage2)

print(img.RasterCount) #Numero de bandas
print(img.RasterXSize) #Numero de pixeles en fila
print(img.RasterYSize) #Numero de pixeles en columna

#Matplot graph.


nir = img.GetRasterBand(1).ReadAsArray(0,0, img.RasterXSize, img.RasterYSize) #Pasar como parametro la banda NIR (Near InfraRed)
red = img1.GetRasterBand(1).ReadAsArray(0,0, img1.RasterXSize, img1.RasterYSize) #Pasar como parametro la banda RED 
# Convert the 16-bit Landsat 8 values to floats for the division operation:
nir = nir.astype(t)
red = red.astype(t)
#NDVI Calc
np.seterr(invalid='ignore')
ndvi = (nir - red)/(nir + red)
# The ndvi value is in the range -1..1, but we want it to be displayable, so:
# Make the value positive and scale it back up to the 16-bit range:
ndvi = (ndvi + 1) * (2**15 - 1)
#Mejorar contraste
ndvi[ndvi < -0] = 0
plt.figure(figsize=(12,10))
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar()
plt.title("NDVI TEST")
plt.xlabel('Column #')
plt.ylabel('Row #')
plt.show()
#plt.savefig('foo.png', bbox_inches='tight') saves the image