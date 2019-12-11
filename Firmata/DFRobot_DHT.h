#ifndef DF_DHT_H
#define DF_DHT_H

#if ARDUINO < 100
  #include <WProgram.h>
#else
  #include <Arduino.h>
#endif

  typedef enum {
    AUTO_DETECT,
    DHT11,
    DHT22,
    AM2302,  // Packaged DHT22
    RHT03    // Equivalent to DHT22
  }
  DHT_MODEL_t;

  typedef enum {
    ERROR_NONE = 0,
    ERROR_TIMEOUT,
    ERROR_CHECKSUM
  }
  DHT_ERROR_t;

class DFRobot_DHT
{
  public:

  DFRobot_DHT();
  void begin(uint8_t _pin, DHT_MODEL_t _model = AUTO_DETECT);
  void resetTimer();

  float getTemperature();
  float getHumidity();

  DHT_ERROR_t getStatus() { return error; };
  String getStatusString();

  DHT_MODEL_t getModel() { return model; }

  int getMinimumSamplingPeriod() { return model == DHT11 ? 1000 : 2000; }

  int8_t getNumberOfDecimalsTemperature() { return model == DHT11 ? 0 : 1; };
  int8_t getLowerBoundTemperature() { return model == DHT11 ? 0 : -40; };
  int8_t getUpperBoundTemperature() { return model == DHT11 ? 50 : 125; };

  int8_t getNumberOfDecimalsHumidity() { return 0; };
  int8_t getLowerBoundHumidity() { return model == DHT11 ? 20 : 0; };
  int8_t getUpperBoundHumidity() { return model == DHT11 ? 90 : 100; };

  static float toFahrenheit(float fromCelcius) { return 1.8 * fromCelcius + 32.0; };
  static float toCelsius(float fromFahrenheit) { return (fromFahrenheit - 32.0) / 1.8; };
protected:
  

private:
  void readSensor();

  float temperature;
  float _temperature;
  float humidity;
  float _humidity;
  
  bool err11_t,err22_t, err11_h,err22_h;

  uint8_t pin;
  
  uint64_t te11;
  uint64_t te22;
  uint64_t hu11;
  uint64_t hu22;
  
  
  DHT_MODEL_t model;
  DHT_ERROR_t error;
  unsigned long lastReadTime;

#if defined(ESP_PLATFORM)
  float mpythonGetTemperature();
  float mpythonGetHumidity();
  float cacheTemperature;
  float cacheHumidity;
  bool first;
static void dhtTick(void *param)
{
  DFRobot_DHT *self = (DFRobot_DHT *)param;
  float t;
  float h;

  while(true){
    t = self->mpythonGetTemperature();
    h = self->mpythonGetHumidity();

    if(t > 0)
      self->cacheTemperature = t;
    if(h > 0)
      self->cacheHumidity = h;
    delay(100);
  }
}
#endif

};

#endif /*dht_h*/
