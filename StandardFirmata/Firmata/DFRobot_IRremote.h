#include <WString.h>
#include <Arduino.h>
#include <IRremoteInt.h>

#ifndef DFROBOT_IRRMEMOTE_H
#define DFROBOT_IRRMEMOTE_H

#define RAWBUF 100 // Length of raw duration buffer

#if defined(NRF5) || defined(ESP_PLATFORM)
#define IRwrite(pin, value) digitalWrite(pin, value)
#else
#define IRwrite(pin, value) pinMode(pin,OUTPUT);digitalWrite(pin, value)
#endif

typedef void (*IRCallback)(uint8_t val);

class IRremote_Receive
{
    public:

    IRremote_Receive();

    void begin(int recvpin1);

    bool keyPressed(char *expected);

    void resume();

    int getPin();

    uint32_t getData();

    String getIrCommand();
#if defined(ARDUINO_AVR_MEGA2560)
    String getIrCommand(int pin);
#endif

    bool available();

    void setCallback(IRCallback cb);

    IRCallback IRcb = NULL;

    private:

    void enableIRIn();

    uint8_t recvpin;

    bool enable;

};

class IRremote_Send 
{
    public:

    IRremote_Send();

    void begin(int recvpin1);

    int getPin();

    void sendNEC(unsigned long data, int nbits);

    void sendWhynter(unsigned long data,  int nbits);

    void sendSony(unsigned long data, int nbits);

    void sendRC5(unsigned long data, int nbits);
  
    void sendRC6(unsigned long data, int nbits);

    void sendDISH(unsigned long data,  int nbits);

    void sendSharpRaw(unsigned long data,  int nbits);

    void sendSAMSUNG(unsigned long data,  int nbits);


    void sendRaw(unsigned int buf[], int len, int hz);

    void sendPanasonic(unsigned int address, unsigned long data);
  
    void sendJVC(unsigned long data, int nbits, int repeat);


    private:

    void space(int time);

    void mark(int time);

    void enableIROut(uint8_t khz);

    uint8_t recvpin;

};


#endif