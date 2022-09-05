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

char Version[] = "v2.5 - 27/05/2022";
//Defino los pines a ser usados por el modulo transceptor LoRa
#define CS    8      // Pin de CS del módulo LoRa
#define RST   4      // Pin de Reset del módulo LoRa
#define IRQ   7      // Pin del IRQ del módulo LoRa

#define LED   13     // Pin del LED onboard
#define SERIAL_BAUDRATE 9600   // Velocidad del Puerto Serie

// Configuraciones del módulo LoRa. Tener en cuenta que esta configuración debe 


// 433E6 for Asia
// 866E6 for Europe
// 915E6 for North America 

// 915E6 to 928E3 for Argentina
#define LORA_FREQUENCY      915000000  // Frecuencia en Hz a la que se quiere 


#define LORA_SYNC_WORD      0xB8       // Byte value to use as the sync word, 
#define LORA_POWER          17         // TX power in dB, defaults to 17. 
#define LORA_SPREAD_FACTOR  7          // Spreading factor, defaults to 7. 
#define LORA_SIG_BANDWIDTH  125E3      // Signal bandwidth in Hz, defaults to 
#define LORA_CODING_RATE    5          // Denominator of the coding rate, 

double bitRate;
void setup() 
{  
  // Set Led onboard con Output
  pinMode(LED, OUTPUT);
  //Incializo el Serial Monitor
  Serial.begin(SERIAL_BAUDRATE);
  while (!Serial) 
  {

    // Mientras el COM no esté disponible el LED onbooard encendido
    digitalWrite(LED, HIGH);  
  }
  // Apaga el LED si se conecta al COM
  digitalWrite(LED, LOW);  
  
  // Inicializar módulo LoRa
  LoRa.setPins(CS, RST, IRQ);
  while (!LoRa.begin(LORA_FREQUENCY)) 

  {
    Serial.println(".");
    delay(500);

  }
  // Change sync word (0xF3) to match the receiver
  // The sync word assures you don't get LoRa messages from other LoRa 

  // ranges from 0-0xFF

  LoRa.setSyncWord(LORA_SYNC_WORD);
  LoRa.setTxPower(LORA_POWER);              
  LoRa.setSpreadingFactor(LORA_SPREAD_FACTOR);           
  LoRa.setSignalBandwidth(LORA_SIG_BANDWIDTH);
  LoRa.setCodingRate4(LORA_CODING_RATE);  
  // Calculo del BitRate = (SF * (BW / 2 ^ SF)) * (4.0 / CR)
  bitRate = (LORA_SPREAD_FACTOR * (LORA_SIG_BANDWIDTH / pow(2,LORA_SPREAD_FACTOR))) * (4.0 / LORA_CODING_RATE);
  
}
void loop() 
{
  // Version v2.5 - 27/05/2022
  // LoRa BitRate: 5468.75 bps

  // Telemetria RAW Recibida 530,1014.66,1014.56,0.81,22.15
  // Packet Number: 530
  // Presion Base: 1014.66
  // Presion Absoluta: 1014.56

  // Altura: 0.81
  // Temperatura: 22.15
  // Nivel de señal [RSSI]: -45

  // =====================================================================
  // Trato de parsear el paquete  
  int packetSize = LoRa.parsePacket();
  if (packetSize) 
  {     
    // Encender LED onboard
    digitalWrite(LED, HIGH);  
    // Paquete recibido
    // Lectura del paquete
    //[pres, . , temp]

    while (LoRa.available()) 
    {
      String LoRaData = LoRa.readString();
      Serial.print(LoRaData);
    }
    // Apagar LED onboard
    digitalWrite(LED, LOW); 
  }

}
