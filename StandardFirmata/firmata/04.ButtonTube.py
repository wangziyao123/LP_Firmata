from pymata_aio.constants import Constants
import Romeo
import sys
import time

board = Romeo.Romeo()

BOARD_BUTTON = 3

def setup():
    for i in range(6,14):
        board.set_pin_mode(i, Constants.OUTPUT)
    board.set_pin_mode(BOARD_BUTTON, Constants.INPUT)

def loop():
    if(board.digital_read(BOARD_BUTTON)):
        board.display(1)
    else:
        board.display(0)
    board.sleep(0.1)

if __name__ == "__main__":
    setup()
    while True:
        loop()
