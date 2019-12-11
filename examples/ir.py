"""
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc
"""

# from pymata_aio.constants import Constants
# from pymata_aio.pymata_serial import PymataSerial
# from DFRobot_NFC import DFRobot_PN532_IIC
import Leonardo
import sys
import time

board = Leonardo.Leonardo()
IR_SENSOR = 7


def setup():
    board.ir_config(IR_SENSOR)
    board.sleep(1)


def loop():
    key = board.ir_getKey()
    if key:
        print(key)
        sys.stdout.flush()
    board.sleep(0.5)


if __name__ == "__main__":
    setup()
    while True:
        loop()
