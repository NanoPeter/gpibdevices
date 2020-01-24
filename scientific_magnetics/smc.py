#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alfons Schuck'
__version__ = '0.2'


import gpib
import time
#import virtual_visa as visa

#assert visa.__version__ >= '1.5', 'visa should be 1.5 or newer'


class SMC(object):
    """
    Scientific Magnetic / Twickenham Super Conducting Magnet Controller (SMC) 5.52
    Operating Manual: http://www.twicksci.co.uk/manuals/pdf/smc552+.pdf
    """

    def __init__(self, GPIBPort: str = 'GPIB0::4::INSTR'):
        """
        Inititialisiert SMC
        :param GPIBPort: Example: 'GPIB0::12::INSTR'
        :type GPIBPort: str
        """
        data = GPIBPort.split('::')

        try:
            board = int(data[0][-1])
        except:
            board = 0
        instrument = int(data[1])

        self.inst = gpib.dev(board, instrument)



        # Initial Values
        self._ampsPerTesla = 9.755555  # A/T
        self._bRate = 0.005  # T/s, max: 0.006
        self._iRate = self._bRate * self._ampsPerTesla
        self._unit = 0  # A
        self._rampTarget = 0
        self._direction = 2 # Unknown
        self._changeDir = False

        # Max Values
        self._TMax = 8  # T
        self._IMax = self._TMax * self._ampsPerTesla
        self._bRateMax = 0.006  # T/s
        self._iRateMax = self._bRateMax * self._ampsPerTesla  # A/s

        # Initialize Instrument
        self.unit = 0
        self.pause = 0
        self.direction = 0
        self.iRate = self.iRate  # Set I-Rate

    def query(self, query: str) -> str:
        try:
            gpib.write(self.inst, '{}'.format(query+'\r\n'))
            return  str(gpib.read(self.inst,512).decode())
        except Exception as e:
            error1, error2 = self.currentStatus
            raise Exception('{}\nFehler Magnetcontroller:\n {}\n{}'.format(e, error1, error2))


    def command(self, command: str):
        try:
            gpib.write(self.inst, '{}'.format(command+'\r\n'))
        except:
            error1, error2 = self.currentStatus
            raise Exception('Fehler Magnetcontroller:\n {}\n{}'.format(error1, error2))


    @property
    def unit(self) -> int:
        return int(self.setPoint['unit'])

    @unit.setter
    def unit(self, value: int):
        assert (value == 0) or (value == 1), 'Value should be 0 (A) or 1(T)!'
        self._unit = value
        self.command('T{:1d}'.format(self._unit))

    @property
    def pause(self) -> int:
        return self._pause

    @pause.setter
    def pause(self, value:int):
        assert (value == 0) or (value == 1), 'Value should be 0 (off) or 1(on)!'
        self._pause = value
        self.command('P{:1d}'.format(self.pause))

    @property
    def apt(self) -> float:
        return self._ampsPerTesla

    @property
    def bRate(self) -> float:
        return self._bRate

    @bRate.setter
    def bRate(self, value: float):
        assert abs(value) <= self._bRateMax, "Absolute B-Rate should be lower than {}".format(self._bRateMax)
        self._bRate = value / self.apt
        self.command('A{:08.5f}'.format(self._bRate))

    @property
    def iRate(self) -> float:
        return self._iRate

    @iRate.setter
    def iRate(self, value: float):
        assert abs(value) <= self._iRateMax, "Absolute I-Rate should be lower than {}".format(self._iRateMax)
        self._iRate = value
        self.command('A{:08.5f}'.format(self._iRate))

    @property
    def amps(self) -> float:
        self.unit = 0
        return float(self.query('G')[1:9])

    @amps.setter
    def amps(self, value: float):
        oldA = self.amps
        self.pause = 0
        self.unit = 0  # AMPERE!
        self.upperSetPoint = value  # Set upper SetPoint
        self.rampTarget = 2  # Ramp to upper SetPoint
        time.sleep(abs(value - oldA) / self._iRate)

    @property
    def tesla(self) -> float:
        tesla = self.amps / self.apt
        self.unit = 1
        return tesla

    @tesla.setter
    def tesla(self, value):
        oldB = self.tesla
        self.pause = 0
        self.unit = 1
        self.upperSetPoint = value
        self.rampTarget = 2
        time.sleep(abs(value-oldB)/self._bRate + 10)
        for i in range(0,10):
            if abs(value-self.tesla) > i/100:
                time.sleep(2)
            else:
                break


    @property
    def setPoint(self) -> dict:
        valueString = self.query('S')
        setPoint = {'unit': int(valueString[1]),
                    'upper': float(valueString[3:10]),
                    'lower': float(valueString[11:18])}

        return setPoint

    @property
    def upperSetPoint(self) -> float:
        return self.setPoint['upper']

    @upperSetPoint.setter
    def upperSetPoint(self, value: float):
        if (value >= 0) & (self.direction != 0):
            self.direction = 0
            print('Direction changed (positive)')
        elif (value < 0) &  (self.direction != 1):
            self.direction = 1
            print('Direction changed (negative)')
        else:
            pass

        if self.unit == 0:
            assert abs(value) < self._IMax
            self.command('U{:07.3f}'.format(abs(value)))
        elif self.unit == 1:
            assert abs(value) < self._TMax, 'Maximales Feld ist {}, gewähltes Feld ist {}'.format(self._TMax, value)
            self.command('U{:07.4f}'.format(abs(value)))
        else:
            pass



    @property
    def lowerSetPoint(self) -> float:
        return self.setPoint['lower']

    @lowerSetPoint.setter
    def lowerSetPoint(self, value: float):
        self.pause = 1
        if self.unit == 0:
            assert abs(value) < self._IMax
            self.command('L{:07.3f}'.format(value))
        elif self.unit == 1:
            assert abs(value) < self._TMax, 'Maximales Feld ist {}, gewähltes Feld ist {}'.format(self._TMax, value)
            self.command('L{:07.4f}'.format(value))
        else:
            pass

        if value >= 0:
            self.direction = 0
        elif value < 0:
            self.direction = 1


    @property
    def rampTarget(self) -> int:
        return self._rampTarget

    @rampTarget.setter
    def rampTarget(self, value:int):
        assert (value == 0) or (value == 1) or (value ==2), 'Value should be 0 (Zero), 1(Lower) or 2(Upper)!'
        self._rampTarget = value
        self.command('R{:1d}'.format(self.rampTarget))

    @property
    def currentStatus(self):
        query_string = self.query('K')
        ec1 = int(query_string[16:17])
        ec2 = int(query_string[17:18])

        edict1 = {0: 'No Error',
                  1: 'Error 1',
                  2: 'Error 2',
                  3: 'Error 3'}
        edict2 = {0: 'No Error',
                  1: 'Quench Trip', 2:' Error 2', 3:'Error 3', 4:'Error 4', 5:'Error 5', 6:'Error 6', 7:'Error 7'}
        return edict1[ec1], edict2[ec2]

    @property
    def direction(self) -> int:
        return int(self._direction)

    @direction.setter
    def direction(self, value:int):
        assert (value == 0) or (value == 1), 'Value should be 0 (Forward) or 1 (Reverse)!'
        self._changeDir = True
        print('change Dir, value= {}'.format(value))
        actualField = self.tesla
        if (value != self.direction) and (actualField != 0): # Sweep to Zero before changing direction
            self.rampTarget = 0
            while actualField != 0:
                time.sleep(1)
                actualField = self.tesla
                print('Goto 0, actual field = {}'.format(actualField))
        self._direction = value
        self.command('D{:1d}'.format(self._direction))
        self._changeDir = False



if __name__ == '__main__':
    dev = SMC()
    print(dev.currentStatus)
