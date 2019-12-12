"""
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc
"""

from pymata_aio.constants import Constants
from Lib import Leonardo
import sys
import time

board = Leonardo.Leonardo()
BOARD_LED=13


def setup():
    board.set_pin_mode(BOARD_LED, Constants.OUTPUT)


def loop():
    print("LED On")
    sys.stdout.flush()
    board.digital_write(BOARD_LED, 1)
    board.sleep(1.0)
    print("LED Off")
    sys.stdout.flush()
    board.digital_write(BOARD_LED, 0)
    board.sleep(1.0)


if __name__ == "__main__":
    setup()
    while True:
        loop()
