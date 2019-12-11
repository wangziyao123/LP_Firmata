import Leonardo
import sys
import time

board = Leonardo.Leonardo()

dht_pin = 2

def setup():
    board.dht_config(dht_pin)
    board.sleep(1)

def loop():
    temp = board.dht_Temperature()
    print(temp)
    sys.stdout.flush()
    board.sleep(0.5)
    hum = board.dht_Humidity()
    print(hum)
    sys.stdout.flush()
    board.sleep(0.5)

if __name__ == "__main__":
    setup()
    while True:
        loop()
