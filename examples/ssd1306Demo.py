import DFRobot_SSD1306

from pymata_aio.constants import Constants
from pymata_aio.pymata_serial import PymataSerial
import Romeo
import sys
import time
# import DFRobot_NFC


board = Romeo.Romeo()
board.i2c_config()
lcd = DFRobot_SSD1306.SSD1306_I2C(128, 64, board)
# nfc = DFRobot_NFC.DFRobot_PN532_IIC(board)

def setup():
    # board.nfc_begin()
    # nfc.begin()
    # time.sleep(1)
    # print(nfc.scan())
    # lcd.hline(12,24,32,1)
    # board.sleep(2)
    # lcd.line(9, 10, 98,30, 1)
    # lcd.rect(1, 10, 120, 10, 1)
    # lcd.show()
    # time.sleep(3)
    # lcd.fill(1)
    # lcd.circle(63,32,50,1)
    # lcd.fill_circle(63,32,20,1)
    # lcd.text('Hello World!')
    # lcd.line(9, 10, 98,30, 1)
    # lcd.pixel(1, 0, 1)
    # lcd.show()
    pass


def loop():
    lcd.fill(1)
    lcd.show()
    lcd.fill(0)
    lcd.show()
    '''lcd.poweron()
    y_axis = 0
    x_axis = 0
    while y_axis < 64:
        while x_axis < 128:
            lcd.pixel(x_axis, y_axis, 1)
            lcd.show()
            x_axis += 1
            # board.sleep(0.1)
        y_axis += 1
        x_axis = 0
        # board.sleep(0.1)'''
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
