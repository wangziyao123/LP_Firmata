
from DFRobot_NFC import DFRobot_PN532_IIC
import Leonardo
import sys
import time

board = Leonardo.Leonardo()
board.i2c_config()
board.sleep(1)

nfc = DFRobot_PN532_IIC(board)

def setup():
    nfc.begin()
    board.sleep(1)


def loop():
    if nfc.scan():
        print(nfc.read_uid())
    # print(nfc.scan('861b89d4'))
        sys.stdout.flush()
    time.sleep(0.2)


if __name__ == "__main__":
    setup()
    while True:
        loop()
