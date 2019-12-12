import DFRobot_SSD1306

from pymata_aio.constants import Constants
from pymata_aio.pymata_serial import PymataSerial
import Leonardo
import sys
import time


board = Leonardo.Leonardo()
board.i2c_config()
lcd = DFRobot_SSD1306.SSD1306_I2C(128, 64, board)

def setup():
    lcd.hline(0, 24, 32, 1)  # hline(x, y, width, color)
    lcd.show()
    board.sleep(0.5)

    lcd.line(9, 10, 98,30, 1)  # line(x1, y1, x2, y2, color)
    lcd.show()
    board.sleep(0.5)

    lcd.rect(1, 10, 120, 10, 1)  # rect(x, y, width, height, color)
    lcd.show()
    board.sleep(0.5)
    time.sleep(1)

    lcd.circle(63,32,10,1)  # circle(x, y, radius, color)
    lcd.circle(63,32,30,1)
    lcd.show()
    board.sleep(0.5)

    lcd.fill_circle(63,32,20,1)  # fill_circle(x, y, radius, color)
    lcd.show()
    board.sleep(0.5)

    lcd.fill(0)
    lcd.show()

    lcd.text('Hello World!')  # text(string, x, y, color)
    lcd.show()
    board.sleep(0.5)


def loop():
    # lcd.fill(1)
    # lcd.show()
    # lcd.fill(0)
    # lcd.show()
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
