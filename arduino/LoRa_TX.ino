#include <TinyWireM.h>
#include <USI_TWI_Master.h>
#include <Wire.h>

#include <LoRa.h>

#include <Adafruit_BusIO_Register.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_I2CRegister.h>
#include <Adafruit_SPIDevice.h>

#include <Adafruit_Sensor.h>  // incluye librerias para sensor BMP280
#include <Adafruit_BMP280.h>
#include <SPI.h>

#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

Adafruit_BMP280 pressure;    // crea objeto con nombre bmp

TinyGPSPlus gps;
SoftwareSerial ss(10, 11); //RX,TX

#define CS 8 // Pin de CS del módulo LoRa
#define RST 4 // Pin de Reset del módulo LoRa
#define IRQ 7 // Pin del IRQ del módulo LoRa
#define LED 13 // Pin del LED onboard
#define SERIAL_BAUDRATE 9600 // Velocidad del Puerto

#define INTERVAL_TIME_TX 500 // Cantidad de milisegundos

// Configuraciones del módulo LoRa. Tener en cuenta que esta

// 433E6 for Asia
// 866E6 for Europe
// 915E6 for North America
// 915E6 to 928E3 for Argentina
#define LORA_FREQUENCY 915000000 // Frecuencia en Hz a

#define LORA_SYNC_WORD 0xB8 // Byte value to use

#define LORA_POWER 17 // TX power in dB,

#define LORA_SPREAD_FACTOR 7 // Spreading factor,

#define LORA_SIG_BANDWIDTH 125E3 // Signal bandwidth in

#define LORA_CODING_RATE 5
double baseline;
double T, P, A;
unsigned int pktNumber = 0;
double bitRate;
void setup()
{

  Serial.begin(SERIAL_BAUDRATE);// Set de Serial a 9600 bps
  ss.begin(9600);
  // Set Led onboard con Output
  pinMode(LED, OUTPUT);
  // Set de pin RST como Output y se pone a High para que
  /* Default settings from datasheet. */
  pressure.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                       Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                       Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                       Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                       Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */
  pinMode(RST, OUTPUT);
  digitalWrite(RST, HIGH);
  //Inicializar módulo LoRa
  LoRa.setPins(CS, RST, IRQ);

  LoRa.begin(LORA_FREQUENCY);
  while (!LoRa.begin(LORA_FREQUENCY))
  {
    delay(1000);
  }
  LoRa.setTxPower(LORA_POWER);
  LoRa.setSpreadingFactor(LORA_SPREAD_FACTOR);
  LoRa.setSignalBandwidth(LORA_SIG_BANDWIDTH);
  LoRa.setCodingRate4(LORA_CODING_RATE);
  LoRa.setSyncWord(LORA_SYNC_WORD);
  // Calculo del BitRate = (SF * (BW / 2 ^ SF)) * (4.0 / CR)
  bitRate = (LORA_SPREAD_FACTOR * (LORA_SIG_BANDWIDTH / pow(2, LORA_SPREAD_FACTOR))) * (4.0 / LORA_CODING_RATE);
  Serial.println("LoRa OK!");
  // Inicializar el BMP280
  bool bmpIsInit = false;
  Serial.println("Iniciando BMP280 ");
  // Si el BMP180 no inicializa, no arranca la placa y el led
  digitalWrite(LED, HIGH);
  pressure.begin();


}
void loop()
{

  // Leer Presion, Temperatura y calcular Altura
  String presion = String(pressure.readPressure() / 100, 0) + ",";
  String temperatura = String(pressure.readTemperature(), 0) + ",";
  String latitud = obtenerDatosGPS("latitud") + ",";
  String longitud = obtenerDatosGPS("longitud") + ",";
  String altitud = obtenerDatosGPS("altitud") + ",";
  String co = String(analogRead(A0)) + ",";
  String met = String(analogRead(A1)) + ",";
  String paquete = String(pktNumber);

  Serial.println(presion +
                 temperatura +
                 latitud +
                 longitud +
                 altitud +
                 co +
                 met +
                 paquete);
  pktNumber++;
  //Send LoRa packet to receiver
  digitalWrite(LED, HIGH);
  LoRa.beginPacket();
  //PONER ACÁ LO QUE SE VA A ENVIAR AL SIG. MODULO
  LoRa.println(presion +
               temperatura +
               latitud +
               longitud +
               altitud +
               co +
               met +
               paquete);
  LoRa.endPacket();
  digitalWrite(LED, LOW);
  // Volver a 0 para que no haga overflow
  if (pktNumber >= 65500)
  {
    pktNumber = 0;
  }

  // Tiempo de espera entre Tx y Tx
  smartDelay(1000);
}

// Send a byte array of UBX protocol to the GPS
void sendUBX(uint8_t *MSG, uint8_t len) {
  for (int i = 0; i < len; i++) {
    Serial.write(MSG[i]);
  }
}

void resetGPS() {

  //Set GPS to backup mode (sets it to never wake up on its own)
  uint8_t GPSoff[] = {0xB5, 0x62, 0x02, 0x41, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x4D, 0x3B};
  sendUBX(GPSoff, sizeof(GPSoff) / sizeof(uint8_t));

  delay(5000);

  //Restart GPS
  uint8_t GPSon[] = {0xB5, 0x62, 0x02, 0x41, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x4C, 0x37};
  sendUBX(GPSon, sizeof(GPSon) / sizeof(uint8_t));


}

String obtenerDatosGPS(String valor) {
  if (millis() > 5000 && gps.charsProcessed() < 10) // uh oh
  {
    resetGPS();
  } else {
    if(valor == "latitud") return String(gps.location.lat(), 6);
    if(valor=="longitud") return String(gps.location.lng(),6);
    if(valor=="altitud") return String(gps.altitude.meters(),2);
  }
  return "0";
}

//Printing the coordinates of GPS
static void printFloat(float val, bool valid, int len, int prec)
{

  if (!valid)
  {
    while (len-- > 1)
      Serial.print('*');
    Serial.print(' ');
  }
  else
  {
    Serial.print(val, prec);
    int vi = abs((int)val);
    int flen = prec + (val < 0.0 ? 2 : 1); // . and -
    flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
    for (int i = flen; i < len; ++i)
      Serial.print(' ');
  }
  delay(1000);
}

void displayGPSInfo()
{
  if (gps.location.isValid())
  {
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(","));
    Serial.print(gps.location.lng(), 6);
    Serial.print(F(","));
    printFloat(gps.altitude.meters(), gps.altitude.isValid(), 5, 2);
  }
  else
  {
    Serial.print(F("INVALID"));
  }

}

static void smartDelay(unsigned long ms)
{
  unsigned long start = millis();
  do
  {
    while (ss.available())
      gps.encode(ss.read());
  } while (millis() - start < ms);
}
