# -*- coding = utf-8 -*-
__AUTHOR__ = "Alfons Schuck"

from serial import Serial
import time

class VsmMotor(object):

    def __init__(self, SerialPort= 'dev/ttyACM1'):
        self._inst = Serial(SerialPort, 115200)
        time.sleep(2)
        self.mmPerStep = 0.012192/4

    def query(self, value: str):
        self._inst.write(value.encode('ascii'))
        time.sleep(0.5)
        return self._inst.readline().decode().strip('\r\n')

    def command(self, value: str):
        self._inst.write(value.encode('ascii'))
        time.sleep(0.5)


    @property
    def position(self) -> int:
        return int(self.query('P'))

    @position.setter
    def position(self, value: int):
        assert (value >= 0) and (value <= 2500), 'Position should be between 0 and 2500 steps'
        self.command('N{:d}X'.format(value))

    @property
    def positionMM(self) -> float:
        return float(self.position * self.mmPerStep)

    @positionMM.setter
    def positionMM(self, value: float):
        assert (value >= 0) and (value <= 30), 'Position should be between 0 and 30 mm'
        self.position = int(round(value * 4 * self.mmPerStep, 0))

    @property
    def idn(self) -> str:
        return self.query('V')


    def stop(self):
        self.command('E')

    def _reference(self):
        self.command('R')

    def _grab(self):
        self.command('G')

    def _resetPosition(self):
        self.command('O')

    def save(self):
        self.command('S')


if __name__ == '__main__':
    dev = VsmMC('/dev/ttyACM1')
    print(dev.idn)
    print(dev.position)
    dev.position=2500
    time.sleep(10)
    dev.save()
    print(dev.position)