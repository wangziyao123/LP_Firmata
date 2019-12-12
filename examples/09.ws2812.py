import sys
import time
from pymata_aio.constants import Constants
from Lib import Leonardo

board = Leonardo.Leonardo()
neo_pixel1 = 8
neo_pixel2 = 4

def setup():

    board.set_neo_pixel(neo_pixel1, 8, 255)
    board.sleep(1)
    board.setRangeColor(neo_pixel1, 0, 7, 0x12cdff)
    board.sleep(1)
    board.neo_pixel_rainbow(neo_pixel1, 0, 7, 1, 200)
    board.sleep(1)
    # board.set_neo_pixel(neo_pixel2, 7, 255)
    # board.sleep(1)
    # board.setRangeColor(neo_pixel2, 0, 5, board.rgbToColor(0, 0, 0))
    # board.sleep(1)
    board.neo_pixel_clear(neo_pixel1)


def loop():
    time.sleep(1)
    # board.setRangeColor(neo_pixel, 0, 7, color)


if __name__ == "__main__":
    setup()
    while True:
        # color = 0
        loop()
        # color += 30
