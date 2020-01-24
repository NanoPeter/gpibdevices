# -*- coding = utf-8 -*-
__AUTHOR__ = "Alfons Schuck"

from serial import Serial
import time


class VsmEncoder(object):

    def __init__(self, SerialPort= 'dev/ttyACM1'):
        self._inst = Serial(SerialPort, 115200)
        time.sleep(2)

    def query(self, value: str):
        self._inst.write(value.encode('ascii'))
        time.sleep(0.5)
        return self._inst.readline().decode().strip('\r\n')


    @property
    def amplitude(self) -> float:
        return float(self.query('A'))

    @property
    def maximum(self) -> float:
        return float(self.query('M'))

    @property
    def minimum(self) -> float:
        return float(self.query('m'))

    @property
    def position(self) -> float:
        return float(self.query('P'))

    @property
    def idn(self) -> str:
        return self.query('V')


if __name__ == '__main__':
    dev = VsmEnc('/dev/ttyACM1')
    print(dev.idn)