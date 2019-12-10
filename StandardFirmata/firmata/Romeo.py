from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import time
import sys



class Romeo(PyMata3):
  def __init__(self):
    retry = 2;
    self.segment = [0xFC,0x60,0xDA,0xF2,0x66,0xB6,0xBE,0xE0,0xFE,0xF6,0xEE,0x3E,0x9C,0x7A,0x9E,0x8E,0x00]
    sys.stdout.flush()
    while retry >0:
        try:
            super().__init__()
            return
        except Exception as err:
            print(err)
            print("please burn StandardFirmata.hex file")
            sys.stdout.flush()
            retry = retry -1;
            time.sleep(0.5);

  def display(self,val):
    if(val >= len(self.segment)):
      return;
    x=self.segment[val]
    for i in range(0,8):
      self.digital_write(13-i, 1 if (x>>(7-i))&1 else 0)
