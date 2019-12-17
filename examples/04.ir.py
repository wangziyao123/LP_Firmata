import sys
import time
from Lib import Leonardo
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
使用时需讲英文字母换成小写，并且使用字符串格式如 power 键 对应 '0xfd00ff'
"""
board = Leonardo.Leonardo()
IR_SENSOR = 7  # ir sensor must connect digital pin in [0, 1, 2, 3, 7]

def setup():
    board.ir_config(IR_SENSOR)
    board.sleep(1)
    board.set_pin_mode(FAN_PIN, Constants.PWM)

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
