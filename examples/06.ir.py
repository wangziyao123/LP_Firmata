
import Leonardo
import sys
import time
"""
keyBuf[
0xFD00FF,//power
0xFD807F,//VOL+
0xFD40BF,//FUNC/STOP
0xFD20DF,//back
0xFDA05F,//Start/pause
0xFD609F,//next
0xFD10EF,//down
0xFD906F,//vol-
0xFD50AF,//up
0xFD30CF,//0
0xFDB04F,//EQ
0xFD708F,//ST/REPT
0xFD08F7,//1
0xFD8877,//2
0xFD48B7,//3
0xFD28D7,//4
0xFDA857,//5
0xFD6897,//6
0xFD18E7,//7
0xFD9867,//8
0xFD58A7 //9
]
"""
board = Leonardo.Leonardo()
IR_SENSOR = 7  # ir sensor must connect digital pin in [0, 1, 2, 3, 7]


def setup():
    board.ir_config(IR_SENSOR)
    board.sleep(1)


def loop():
    key = board.ir_getKey(IR_SENSOR)
    if key:
        print(key)
        sys.stdout.flush()
    board.sleep(0.5)


if __name__ == "__main__":
    setup()
    while True:
        loop()
