#include "DFRobot_DHT.h"
#if defined(ESP_PLATFORM)
#include "pins_arduino.h"
#if CONFIG_FREERTOS_UNICORE
#define ARDUINO_RUNNING_CORE_DHT 0
#else
#define ARDUINO_RUNNING_CORE_DHT 1
#endif
#endif

DFRobot_DHT::DFRobot_DHT()
{
#if defined(ESP_PLATFORM)
  first = true;
#endif
}

void DFRobot_DHT::begin(uint8_t _pin, DHT_MODEL_t _model)
{
  pin = _pin;
  model = _model;
  resetTimer(); // Make sure we do read the sensor in the next readSensor()
}

void DFRobot_DHT::resetTimer()
{
  err22_h = true;
  err22_t = true;
  err11_h = true;
  err11_t = true;
  DFRobot_DHT::lastReadTime = millis() - 3000;
  if(model == DHT11) {
    te11 = millis();
    hu11 = millis();
  } else {
    te22 = millis();
    hu22 = millis();
  }
}

float DFRobot_DHT::getHumidity()
{
#if defined(ESP_PLATFORM)
  if(first){
    xTaskCreatePinnedToCore(DFRobot_DHT::dhtTick, "dhtTick", 2048, this, 1, NULL, ARDUINO_RUNNING_CORE_DHT);
    first = false;
    long time = 50;
    while(time--) {
      if(cacheHumidity)
        break;
      delay(100);
    }
  }
  return cacheHumidity;
#else
  readSensor();
  if(getStatusString() == "OK")
  {
    (model == DHT11 ? err11_h : err22_h) = false;
    _humidity = humidity;
        (model == DHT11 ? hu11 : hu22) = millis();
    return humidity;
  }

  if( millis() - (model == DHT11 ? hu11 : hu22) > (model == DHT11 ? 1200 : 500)) {
    (model == DHT11 ? err11_h : err22_h) = true;
    if(model == DHT11 ? err11_t : err22_t){
      _humidity = 0;
      (model == DHT11 ? hu11 : hu22) = millis();
    }
  }
  return _humidity;
#endif
}

float DFRobot_DHT::getTemperature()
{
#if defined(ESP_PLATFORM)
  if(first){
    xTaskCreatePinnedToCore(DFRobot_DHT::dhtTick, "dhtTick", 2048, this, 1, NULL, ARDUINO_RUNNING_CORE_DHT);
    first = false;
    long time = 50;
    while(time--) {
      if(cacheTemperature)
        break;
      delay(100);
    }
  }
  return cacheTemperature;
#else
  readSensor();
  if(getStatusString() == "OK")
  {
    (model == DHT11 ? err11_t : err22_t) = false;
    _temperature = temperature;
    (model == DHT11 ? te11 : te22) = millis();
    return temperature;
  }

  if( millis() - (model == DHT11 ? te11 : te22) > (model == DHT11 ? 1200 : 500)) {
    (model == DHT11 ? err11_t : err22_t) = true;
    if(model == DHT11 ? err11_h : err22_h){
      _temperature = 0;
      (model == DHT11 ? te11 : te22) = millis();
    }
  }
  return _temperature;
#endif
}

#ifndef OPTIMIZE_SRAM_SIZE

String DFRobot_DHT::getStatusString()
{
  switch ( error ) {
    case ERROR_TIMEOUT:
      return "TIMEOUT";

    case ERROR_CHECKSUM:
      return "CHECKSUM";

    default:
      return "OK";
  }
}

#else

// At the expense of 26 bytes of extra PROGMEM, we save 11 bytes of
// SRAM by using the following method:

prog_char P_OK[]       PROGMEM = "OK";
prog_char P_TIMEOUT[]  PROGMEM = "TIMEOUT";
prog_char P_CHECKSUM[] PROGMEM = "CHECKSUM";

const char *DFRobot_DHT::getStatusString() {
  prog_char *c;
  switch ( error ) {
    case ERROR_CHECKSUM:
      c = P_CHECKSUM; break;

    case ERROR_TIMEOUT:
      c = P_TIMEOUT; break;

    default:
      c = P_OK; break;
  }

  static char buffer[9];
  strcpy_P(buffer, c);

  return buffer;
}

#endif

void DFRobot_DHT::readSensor()
{
  // Make sure we don't poll the sensor too often
  // - Max sample rate DHT11 is 1 Hz   (duty cicle 1000 ms)
  // - Max sample rate DHT22 is 0.5 Hz (duty cicle 2000 ms)
  delay(1);
  unsigned long startTime = millis();
  //if ( (unsigned long)(startTime - lastReadTime) < (model == DHT11 ? 999L : 1999L) ) {
  //  return;
  //}
  //lastReadTime = startTime;

  temperature = NAN;
  humidity = NAN;

  // Request sample

#ifdef NRF5
  digitalWrite1(pin, LOW); // Send start signal
  pinMode1(pin, OUTPUT);
#else
  pinMode(pin, OUTPUT);
  digitalWrite1(pin, LOW); // Send start signal
  
#endif
  if ( model == DHT11 ) {
    delay(18);
  }
  else {
    // This will fail for a DHT11 - that's how we can detect such a device
    delayMicroseconds(800);
  }
#ifdef NRF5
  pinMode1(pin, INPUT);
  digitalWrite1(pin, HIGH); // Switch bus to receive data
#else
  digitalWrite1(pin, HIGH); // Switch bus to receive data
  pinMode(pin, INPUT);
  
#endif
  // We're going to read 83 edges:
  // - First a FALLING, RISING, and FALLING edge for the start bit
  // - Then 40 bits: RISING and then a FALLING edge per bit
  // To keep our code simple, we accept any HIGH or LOW reading if it's max 85 usecs long

  uint16_t rawHumidity = 0;
  uint16_t rawTemperature = 0;
  uint16_t data = 0;

  for ( int8_t i = -3 ; i < 2 * 40; i++ ) {
    byte age;
    startTime = micros();
    do {
      age = (unsigned long)(micros() - startTime);
      if ( age > 90 ) {
        error = ERROR_TIMEOUT;
        return;
      }
    }
    while ( digitalRead1(pin) == (i & 1) ? HIGH : LOW );

    if ( i >= 0 && (i & 1) ) {
      // Now we are being fed our 40 bits
      data <<= 1;

      // A zero max 30 usecs, a one at least 68 usecs.
      if ( age > 30 ) {
        data |= 1; // we got a one
      }
    }

    switch ( i ) {
      case 31:
        rawHumidity = data;
        break;
      case 63:
        rawTemperature = data;
        data = 0;
        break;
    }
  }

  // Verify checksum

  if ( (byte)(((byte)rawHumidity) + (rawHumidity >> 8) + ((byte)rawTemperature) + (rawTemperature >> 8)) != data ) {
	  
    error = ERROR_CHECKSUM;
    return;
  }

  // Store readings

  if ( model == DHT11 ) {
    humidity = rawHumidity >> 8;
    _humidity = humidity;
    temperature = rawTemperature >> 8;
    _temperature = temperature;
  }
  else {
    humidity = rawHumidity * 0.1;
    _humidity = humidity;

    if ( rawTemperature & 0x8000 ) {
      rawTemperature = -(int16_t)(rawTemperature & 0x7FFF);
    }
    temperature = ((int16_t)rawTemperature) * 0.1;
    _temperature = temperature;
  }

  error = ERROR_NONE;
}

#if defined(ESP_PLATFORM)
float DFRobot_DHT::mpythonGetHumidity()
{
  readSensor();
  if(getStatusString() == "OK")
  {
    (model == DHT11 ? err11_h : err22_h) = false;
    _humidity = humidity;
    (model == DHT11 ? hu11 : hu22) = millis();
    return humidity;
  }

  if( millis() - (model == DHT11 ? hu11 : hu22) > (model == DHT11 ? 1200 : 500)) {
    (model == DHT11 ? err11_h : err22_h) = true;
    if(model == DHT11 ? err11_t : err22_t){
      _humidity = 0;
      (model == DHT11 ? hu11 : hu22) = millis();
    }
  }
  return _humidity;
}

float DFRobot_DHT::mpythonGetTemperature()
{
  readSensor();
  if(getStatusString() == "OK")
  {
    (model == DHT11 ? err11_t : err22_t) = false;
    _temperature = temperature;
    (model == DHT11 ? te11 : te22) = millis();
    return temperature;
  }

  if( millis() - (model == DHT11 ? te11 : te22) > (model == DHT11 ? 1200 : 500)) {
    (model == DHT11 ? err11_t : err22_t) = true;
    if(model == DHT11 ? err11_h : err22_h){
      _temperature = 0;
      (model == DHT11 ? te11 : te22) = millis();
    }
  }
  
  return _temperature;
}
#endif
