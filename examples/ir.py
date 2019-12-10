"""
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc
"""

# from pymata_aio.constants import Constants
# from pymata_aio.pymata_serial import PymataSerial
# from DFRobot_NFC import DFRobot_PN532_IIC
import Romeo
import sys
import time

board = Romeo.Romeo()
# board.i2c_config()
# board.sleep(1)

BOARD_LED = 13
IR_SENSOR = 7
neo_pixel = 13
SERVO_PIN = 10
dht_pin = 2

# nfc = DFRobot_PN532_IIC(board)

def setup():
    # board.set_pin_mode(neo_pixel, Constants.OUTPUT)
    # board.set_pin_mode(IR_SENSOR)
    # board.neo_pixel(neo_pixel, 20, 20, 20)
    # time.sleep(1)
    # board.dht_config(dht_pin)
    # board.sleep(1)
    # board.i2c_config()
    # nfc.begin()
    # time.sleep(0.1)
    board.ir_config(IR_SENSOR)

    # board.nfc_begin()
    # time.sleep(2)
    #board.get_temp(dht_pin)
    # board.enable_digital_reporting(neo_pixel)
    # board.enable_analog_reporting(neo_pixel)
    # board.neo_pixel(SERVO_PIN)
    # board.analog_write(SERVO_PIN, 0)AS
    pass


def loop():
    # temp = board.dht_Temperature()
    key = board.ir_getKey()
    if key:
        print(key)
        sys.stdout.flush()
    # print(nfc.scan('861b89d4'))
    # sys.stdout.flush()
    time.sleep(1)
    # print(nfc.read_data(2))
    # sys.stdout.flush()
    # time.sleep(2)
    # nfc.begin()
    # hum = board.dht_Humidity()
    # print(hum)
    # sys.stdout.flush()
    # board.sleep(1)
    # print(board.get_message())
    # temp = board.get_temp(dht_pin)
    # print(temp)
    # sys.stdout.flush()
    # print(board.dfrobot_map)

    # board.sleep(0.1)
    # # code = board.digital_read(BOARD_LED)
    # sys.stdout.flush()
    # for pos in range(0, 180, 5): # Start=0 degrees, Finish=180 degree, (Increment=1 degree which is the default)
    #     board.analog_write(SERVO_PIN, pos)
    #     board.sleep(0.1)
    # for pos in range(180, 0, -5): # Start=180 degrees, Finish=0 degrees, Increment=-1 degrees (moving down)
    #     board.analog_write(SERVO_PIN, pos)
    #     board.sleep(0.1)
    pass


if __name__ == "__main__":
    setup()
    while True:
        loop()
