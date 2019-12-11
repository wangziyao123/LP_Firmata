from pymata_aio.constants import Constants
import Leonardo
import sys
import time

board = Leonardo.Leonardo()

def setup():
    for i in range(6,14):
        board.set_pin_mode(i, Constants.OUTPUT)

def loop():
    print("display 1")
    sys.stdout.flush()
    board.display(1)
    time.sleep(2)

    print("display 2")
    sys.stdout.flush()
    board.display(2)
    time.sleep(2)

    print("display 3")
    sys.stdout.flush()
    board.display(3)
    time.sleep(2)

    print("display 4")
    sys.stdout.flush()
    board.display(4)
    time.sleep(2)

    print("display 5")
    sys.stdout.flush()
    board.display(5)
    time.sleep(2)

    print("display 6")
    sys.stdout.flush()
    board.display(6)
    time.sleep(2)

    print("display 7")
    sys.stdout.flush()
    board.display(7)
    time.sleep(2)
    print("repeat...")

if __name__ == "__main__":
    setup()
    while True:
        loop()

