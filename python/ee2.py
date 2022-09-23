import datetime
import threading
import ee
import ee.mapclient
import json
from ee.batch import Export
import requests

startDate = '2022-01-01'
endDate = '2022-11-01'


def execute():
  ee.Initialize()
  mizona = ee.Geometry.Point([-59.6731005, -28.4191146])
  Landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(mizona).filterDate(startDate, endDate).first()
  Landsat.resample('bicubic')


  url = Landsat.getDownloadUrl({
      
      'bands': ['SR_B4','SR_B5','SR_B7','SR_B3'],
      'region': Landsat.geometry(),
      'scale': 115,
      'maxPixels':1000,
      'format': 'GEO_TIFF'
  })
  response = requests.get(url)
  with open('multi_bands.tif', 'wb') as fd:
    fd.write(response.content)


def downloadImages(Landsat):
  imageWithNDVI = Landsat.addBands(Landsat.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI'))

  url = imageWithNDVI.getDownloadUrl({
      'bands': ['SR_B4','SR_B5','SR_B7','SR_B3'],
      'region': Landsat.geometry(),
      'scale': 115,
      'maxPixels':1000,
      'format': 'GEO_TIFF'
  })
  response = requests.get(url)
  with open('multi_bands.tif', 'wb') as fd:
    fd.write(response.content)

class EEProcess():
  def __init__(self, coordlat, coordlong):
    self.coordlat = coordlat
    self.coordlong = coordlong

  def start(self):
    
    ee.Initialize()
    mizona = ee.Geometry.Point([self.coordlong, self.coordlat])
    Landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(mizona).filterDate(startDate, endDate).first()
    downloadImages(Landsat)
    

