import datetime
import ee
import ee.mapclient
import json
from ee.batch import Export
import requests

startDate = '2022-01-01'
endDate = '2022-11-01'
def downloadImages(Landsat):
  imageWithNDVI = Landsat.addBands(Landsat.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI'))

  url = imageWithNDVI.getDownloadUrl({
      'bands': ['NDVI'],
      'region': imageWithNDVI.geometry(),
      'scale': 80,
      'format': 'GEO_TIFF'
  })
  response = requests.get(url)
  with open('multi_ban.tif', 'wb') as fd:
    fd.write(response.content)

class EEProcess:
  def __init__(self, coordlat, coordlong):
    self.coordlat = coordlat
    self.coordlong = coordlong

  def start(self):
    
    ee.Initialize()
    mizona = ee.Geometry.Point([self.coordlong, self.coordlat])
    Landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(mizona).filterDate(startDate, endDate).first()
    downloadImages(Landsat)
    

