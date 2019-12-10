#include "DFRobot_IRremote.h"
#ifdef NRF5
#include <avr/interrupt.h>
#include <basic.h>
#endif
#if CONFIG_FREERTOS_UNICORE
#define ARDUINO_RUNNING_CORE_IR 0
#else
#define ARDUINO_RUNNING_CORE_IR 1
#endif
#include <Arduino.h>

volatile uint32_t tmp=0;
volatile int counter=0;
volatile unsigned long ts;
volatile uint32_t data;
volatile bool iravailable;
long micr = 0;

IRremote_Receive *IRremote_dal_pt = NULL;
bool task_init;

#ifdef NRF5
void loopEvent(){
#else
void loopEvent(void *param){
#endif
    while(true){
        uint32_t val = IRremote_dal_pt->getData();
        if(val != 0){
            //if(((val&0xff)^((val>>8)&0xff)) == 0xff){
                if(IRremote_dal_pt->IRcb != NULL){
                    IRremote_dal_pt->IRcb(val&0xff);
                }
            //}
        }
#ifdef NRF5
        fiber_sleep(50);
#elif defined(ESP_PLATFORM)
        delay(50);
#endif
    }
}

IRremote_Receive::IRremote_Receive() {
    IRremote_dal_pt = this;
    data = 0;
    iravailable = false;
    task_init = false;
    enable = false;
}


void IRremote_Receive::setCallback(IRCallback cb){
    IRcb = cb;
    if(!task_init){
#ifdef NRF5
        create_fiber(loopEvent);
#elif defined(ESP_PLATFORM)
        xTaskCreatePinnedToCore(loopEvent, "loopEvent", 2048, NULL, 1, NULL, ARDUINO_RUNNING_CORE_IR);
#endif
        task_init = true;
    }
}


void IRremote_Receive::begin(int recvpin1) {
    recvpin = recvpin1;
    this->enableIRIn();
    this->enable = true;
}

int IRremote_Receive::getPin() {
    return recvpin;
}

uint32_t IRremote_Receive::getData(void) {
    uint32_t _data = data;
    data = 0;
    return _data;
}

String IRremote_Receive::getIrCommand()
{
    uint32_t command = this->getData();
    char string[20];

    memset(string,'\0',20);
    sprintf(string,"%lX",command);
    return (String)string;
}

#if defined(ARDUINO_AVR_MEGA2560)
String IRremote_Receive::getIrCommand(int pin)
{
    if(this->enable == false){
        begin(pin);
    }
    uint32_t command = this->getData();
    char string[20];

    memset(string,'\0',20);
    sprintf(string,"%lX",command);
    return (String)string;
}
#endif

void IRremote_Receive::resume() {
#if defined(NRF5)
    detachInterrupt(recvpin);
#else
    detachInterrupt(digitalPinToInterrupt(recvpin));
#endif
}

// TIMER2 interrupt code to collect raw data.
// Widths of alternating SPACE, MARK are recorded in rawbuf.
// Recorded in ticks of 50 microseconds.
// rawlen counts the number of entries recorded so far.
// First entry is the SPACE between transmissions.
// As soon as a SPACE gets long, ready is set, state switches to IDLE, timing of SPACE continues.
// As soon as first MARK arrives, gap width is recorded, ready is cleared, and new logging starts
void decode(uint32_t code) {  
    //byte add = (code>>24)&0xff;
    data = (code)&0xffffffff;
    iravailable = true;
}
//long p=0;
bool IRremote_Receive::available() {
    if(iravailable) {
        //p++;
        //if(p>14000){ this->resume();
            iravailable = false;
           // p = 0; this->enableIRIn();
            return true;
       // }
    }
    return false;
}

void IR_INT() {

    iravailable = false;

    unsigned long long x = micros();
    unsigned long interval = x-ts;

    ts = x;

    if(interval > 3000){
        counter = 0;
        tmp = 0;
        return;
    }

    if((interval > 2000) && (interval<2500)){
        tmp <<= 1;
        tmp |=  1;
    }else{
        tmp <<= 1;
    }

    counter++;

    if(counter == 32){
        //Serial.print("tmp= ");Serial.println(tmp);
        decode(tmp); 
        counter = 0;
    }

}

// initialization
void IRremote_Receive::enableIRIn() {

#if defined(NRF5)
    pinMode(recvpin,INPUT);
    attachInterrupt(recvpin,IR_INT,RISING);
#else
    pinMode(recvpin,INPUT);
    attachInterrupt(digitalPinToInterrupt(recvpin),IR_INT,RISING);
#endif
}

bool IRremote_Receive::keyPressed(char *expected) {

    uint32_t number = data;
    char string[20];
    char *p = string;

    memset(string,'\0',20);
    //itoa(16580863,string,10);Serial.println(string);
    sprintf(string,"%lX",number);

    while(*expected!='\0') {
        if(*expected != *p)
            break;
        expected++;
        p++;
    }

    if(*expected != '\0')
        return false;
    if(*p!= '\0')
        return false;

    data = 0;
    return true;

}

IRremote_Send::IRremote_Send() {

}

void IRremote_Send::begin(int recvpin1) {
    recvpin = recvpin1;
}

int IRremote_Send::getPin() {
    return recvpin;
}

void IRremote_Send::sendNEC(unsigned long data, int nbits) {

    //data = data << (32 - nbits);

    enableIROut(38);

   // noInterrupts();

    this->mark(NEC_HDR_MARK);
    this->space(NEC_HDR_SPACE);

    for (int i = 0; i < nbits; i++) {
        if (data & TOPBIT) {
            this->mark(NEC_BIT_MARK);
            this->space(NEC_ONE_SPACE);
        } else {
            this->mark(NEC_BIT_MARK);
            this->space(NEC_ZERO_SPACE);
        }
        data <<= 1;
    }

    this->mark(NEC_BIT_MARK);
    this->space(0);

   // interrupts();
}

void IRremote_Send::sendSony(unsigned long data, int nbits) {

    enableIROut(40);

    noInterrupts();

    this->mark(SONY_HDR_MARK);
    this->space(SONY_HDR_SPACE);

    //data = data << (32 - nbits);

    for (int i = 0; i < nbits; i++) {
        if (data & TOPBIT) {
            this->mark(SONY_ONE_MARK);
            this->space(SONY_HDR_SPACE);
        } else {
            this->mark(SONY_ZERO_MARK);
            this->space(SONY_HDR_SPACE);
        }
        data <<= 1;
    }
    interrupts();
}

void IRremote_Send::sendRaw(unsigned int buf[], int len, int hz) {

    enableIROut(hz);
    noInterrupts();
    for (int i = 0; i < len; i++) {
        if (i & 1) {
            this->space(buf[i]);
        } else {
            this->mark(buf[i]);
        }
    }

    space(0); // Just to be sure
    interrupts();
}

// Note: first bit must be a one (start bit)
void IRremote_Send::sendRC5(unsigned long data, int nbits) {

    enableIROut(36);
    noInterrupts();
    //data = data << (32 - nbits);

    this->mark(RC5_T1); // First start bit
    this->space(RC5_T1); // Second start bit
    this->mark(RC5_T1); // Second start bit

    for (int i = 0; i < nbits; i++) {
        if (data & TOPBIT) {
            this->space(RC5_T1); // 1 is this->space, then mark
            this->mark(RC5_T1);
        } else {
            this->mark(RC5_T1);
            this->space(RC5_T1);
        }
        data <<= 1;
    }

    this->space(0); // Turn off at end
    interrupts();
}

// Caller needs to take care of flipping the toggle bit
void IRremote_Send::sendRC6(unsigned long data, int nbits) {

    enableIROut(36);
    noInterrupts();
    //data = data << (32 - nbits);

    this->mark(RC6_HDR_MARK);
    this->space(RC6_HDR_SPACE);
    this->mark(RC6_T1); // start bit
    this->space(RC6_T1);

    int t;
    for (int i = 0; i < nbits; i++) {
        if (i == 3) {
            // double-wide trailer bit
            t = 2 * RC6_T1;
        } else {
            t = RC6_T1;
        }
        if (data & TOPBIT) {
            this->mark(t);
            this->space(t);
        } else {
            this->space(t);
            this->mark(t);
        }

        data <<= 1;
    }

    this->space(0); // Turn off at end
    interrupts();
}
void IRremote_Send::sendPanasonic(unsigned int address, unsigned long data) {

    enableIROut(35);
    noInterrupts();
    this->mark(PANASONIC_HDR_MARK);
    this->space(PANASONIC_HDR_SPACE);
    
    for(int i=0;i<16;i++)
    {
        this->mark(PANASONIC_BIT_MARK);
        if (address & 0x8000) {
            this->space(PANASONIC_ONE_SPACE);
        } else {
            this->space(PANASONIC_ZERO_SPACE);
        }
        address <<= 1;
    }

    for (int i=0; i < 32; i++) {
        this->mark(PANASONIC_BIT_MARK);
        if (data & TOPBIT) {
            this->space(PANASONIC_ONE_SPACE);
        } else {
            this->space(PANASONIC_ZERO_SPACE);
        }
        data <<= 1;
    }

    this->mark(PANASONIC_BIT_MARK);
    this->space(0);
    interrupts();
}
void IRremote_Send::sendJVC(unsigned long data, int nbits, int repeat) {

    enableIROut(38);
    noInterrupts();
    data = data << (32 - nbits);

    if (!repeat){
        this->mark(JVC_HDR_MARK);
        space(JVC_HDR_SPACE); 
    }

    for (int i = 0; i < nbits; i++) {
        if (data & TOPBIT) {
            this->mark(JVC_BIT_MARK);
            space(JVC_ONE_SPACE); 
        } else {
            this->mark(JVC_BIT_MARK);
            space(JVC_ZERO_SPACE); 
        }
        data <<= 1;
    }

    this->mark(JVC_BIT_MARK);
    space(0);
    interrupts();
}

void IRremote_Send::sendWhynter(unsigned long data,  int nbits) {

    // Set IR carrier frequency
    enableIROut(38);
    noInterrupts();
    // Start
    mark(WHYNTER_ZERO_MARK);
    space(WHYNTER_ZERO_SPACE);

    // Header
    mark(WHYNTER_HDR_MARK);
    space(WHYNTER_HDR_SPACE);

    // Data
    for (unsigned long  mask = 1UL << (nbits - 1);  mask;  mask >>= 1) {
        if (data & mask) {
            mark(WHYNTER_ONE_MARK);
            space(WHYNTER_ONE_SPACE);
        } else {
            mark(WHYNTER_ZERO_MARK);
            space(WHYNTER_ZERO_SPACE);
        }
    }

    // Footer
    mark(WHYNTER_ZERO_MARK);
    space(WHYNTER_ZERO_SPACE);  // Always end with the LED off
    interrupts();

}

void IRremote_Send::sendDISH(unsigned long data,  int nbits) {

    // Set IR carrier frequency
    enableIROut(56);
    noInterrupts();
    mark(DISH_HDR_MARK);
    space(DISH_HDR_SPACE);

    for (unsigned long  mask = 1UL << (nbits - 1);  mask;  mask >>= 1) {
        if (data & mask) {
            mark(DISH_BIT_MARK);
            space(DISH_ONE_SPACE);
        } else {
            mark(DISH_BIT_MARK);
            space(DISH_ZERO_SPACE);
        }
    }
    mark(DISH_HDR_MARK);
    interrupts();
}

void IRremote_Send::sendSharpRaw(unsigned long data,  int nbits) {

    enableIROut(38);
    noInterrupts();
    // Sending codes in bursts of 3 (normal, inverted, normal) makes transmission
    // much more reliable. That's the exact behaviour of CD-S6470 remote control.
    for (int n = 0;  n < 3;  n++) {
        for (unsigned long  mask = 1UL << (nbits - 1);  mask;  mask >>= 1) {
            if (data & mask) {
                mark(SHARP_BIT_MARK);
                space(SHARP_ONE_SPACE);
            } else {
                mark(SHARP_BIT_MARK);
                space(SHARP_ZERO_SPACE);
            }
        }

        mark(SHARP_BIT_MARK);
        space(SHARP_ZERO_SPACE);
        delay(40);

        data = data ^ SHARP_TOGGLE_MASK;
    }
    interrupts();
}

void IRremote_Send::sendSAMSUNG(unsigned long data,  int nbits) {

    // Set IR carrier frequency
    enableIROut(38);
    noInterrupts();
    // Header
    mark(SAMSUNG_HDR_MARK);
    space(SAMSUNG_HDR_SPACE);

    // Data
    for (unsigned long  mask = 1UL << (nbits - 1);  mask;  mask >>= 1) {
        if (data & mask) {
            mark(SAMSUNG_BIT_MARK);
            space(SAMSUNG_ONE_SPACE);
        } else {
            mark(SAMSUNG_BIT_MARK);
        space(SAMSUNG_ZERO_SPACE);
        }
    }

    // Footer
    mark(SAMSUNG_BIT_MARK);
    space(0);  // Always end with the LED off
    interrupts();
}

void IRremote_Send::enableIROut(uint8_t khz) {
    pinMode(recvpin, OUTPUT);
#if defined(NRF5)
    micr = 1000 * (float)(1/khz);
#else
    micr = 1000 * (float)(1/khz) + 6;
#endif
}

void IRremote_Send::mark(int time) {

    long time1 = micros();

    while(1){
        IRwrite(recvpin, HIGH);
        delayMicroseconds(micr);
        IRwrite(recvpin,  LOW);
        delayMicroseconds(micr);

        if((micros() - time1) >= time){
            return;
        }
    }
}

void IRremote_Send::space(int time) {

    long time1 = micros();

    IRwrite(recvpin,  LOW);

    while(1){
        if((micros() - time1) >= time){
            return;
        }
    }
}
