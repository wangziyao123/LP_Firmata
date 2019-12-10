from pymata_aio.constants import Constants
import Romeo
import sys
import time

board = Romeo.Romeo()

SERVO_PIN = 10


def setup():
    board.servo_config(SERVO_PIN)
    board.sleep(0.2);
    board.analog_write(SERVO_PIN, 0)
    board.sleep(0.5);
    
def loop():
    print("Servo sweep ( 0  to 180 degree )")
    sys.stdout.flush()
    # The range of motion for some servos isn't all the way from 0 degrees to 180 degrees, change as needed.
    for pos in range(0, 180, 5): # Start=0 degrees, Finish=180 degree, (Increment=1 degree which is the default)
        board.analog_write(SERVO_PIN, pos)
        board.sleep(0.1)
    print("Servo sweep ( 180 to 0 degree )")
    sys.stdout.flush()
    for pos in range(180, 0, -5): # Start=180 degrees, Finish=0 degrees, Increment=-1 degrees (moving down)
        board.analog_write(SERVO_PIN, pos)
        board.sleep(0.1)


if __name__ == "__main__":
    setup()
    while True:
        loop()
