from pymata_aio.constants import Constants
from Lib import Leonardo
import sys
import time

board = Leonardo.Leonardo()

FAN_PIN = 5

def setup():
    board.set_pin_mode(FAN_PIN, Constants.PWM)

def loop():

    print('low speed')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 60)
    time.sleep(4)

    print('middle speed')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 80)
    time.sleep(4)

    print('high speed')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 128)
    time.sleep(4)

    print('ultra speed')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 255)
    time.sleep(4)

    print('low speed')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 60)
    time.sleep(4)

    print('stop')
    sys.stdout.flush()
    board.analog_write(FAN_PIN, 0)
    time.sleep(4)

if __name__ == "__main__":
    setup()
    while True:
        loop()
