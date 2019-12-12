import sys
import time
from pymata_aio.constants import Constants
from Lib import Leonardo
from Lib.DFRobot_SSD1306 import SSD1306_I2C

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

"""
this example need 1 leonardo board, 1 infrared sensor, 1 motor fan, 1 128*64 LCD
infrared sensor connect with Digital Pin 7
motor fan connect with Digital Pin 5(PWM)
128*64 LCD connect with I2C 
"""

board = Leonardo.Leonardo()
board.i2c_config()
board.sleep(0.1)
IR_SENSOR = 7  # ir sensor must connect digital pin in [0, 1, 2, 3, 7]
FAN_PIN = 5
START_STOP = '0xfd00ff'
UP = '0xfd50af'
DOWN = '0xfd10ef'
lcd = SSD1306_I2C(128, 64, board)

def setup():
    board.ir_config(IR_SENSOR)
    board.sleep(1)
    board.set_pin_mode(FAN_PIN, Constants.PWM)
    lcd.fill(0)
    lcd.text('power off', 30, 10)
    lcd.show()

def loop():
    power_flag = False
    speed = {'off': 0, 'low': 60, 'middle': 80, 'high': 128, 'ultra': 255}
    statement = ['off', 'low', 'middle', 'high', 'ultra']
    index = 1
    while 1:
        key = board.ir_getKey(IR_SENSOR)
        if key:
            if key == START_STOP and not power_flag:
                lcd.fill(0)
                lcd.text('power on', 30, 10)
                lcd.text('speed: %s' % statement[index], 15, 30)
                lcd.show()
                power_flag = True
                index = 1
                board.analog_write(FAN_PIN, speed['low'])
            elif key == START_STOP and power_flag:
                lcd.fill(0)
                lcd.text('power off', 30, 10)
                lcd.show()
                power_flag = False
                index = 1
                board.analog_write(FAN_PIN, speed['off'])
            elif key == UP and power_flag:
                if index < 4:
                    index += 1
                    lcd.fill_rect(15, 30, 127, 63, 0)
                    lcd.text('speed: %s' % statement[index], 15, 30)
                    lcd.show()
                    board.analog_write(FAN_PIN, speed[statement[index]])
                else:
                    lcd.fill_rect(15, 30, 127, 63, 0)
                    lcd.text('max speed!', 15, 30)
                    lcd.show()
            elif key == DOWN and power_flag:
                if index > 1:
                    index -= 1
                    lcd.fill_rect(15, 30, 127, 63, 0)
                    lcd.text('speed: %s' % statement[index], 15, 30)
                    lcd.show()
                    board.analog_write(FAN_PIN, speed[statement[index]])
                else:
                    lcd.fill_rect(15, 30, 127, 63, 0)
                    lcd.text('min speed!', 15, 30)
                    lcd.show()
        board.sleep(0.5)


if __name__ == "__main__":
    setup()
    while True:
        loop()
