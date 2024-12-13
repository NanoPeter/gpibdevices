#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alfons Schuck'
__version__ = '0.1'


import gpib
import time



class SMU(object):
    """
    Keithley SMU als MagnetController
    """

    def __init__(self, GPIBPort: str = 'GPIB0::10::INSTR'):
        """
        Inititialisiert SMU
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
        self._amps = 0

        # Max Values
        self._TMax = 0.03  # T
        self._IMax = self._TMax * self._ampsPerTesla
        self._bRateMax = 0.0005  # T/s
        self._iRateMax = self._bRateMax * self._ampsPerTesla  # A/s

        self.initInstrument()

    def sweepToZero(self):
        self.sweepToValue(0)

    def sweepToValue(self, value:float):
        assert abs(value) <= self._IMax, 'Absolute IMax should be lower than {} A'.format(self._IMax)
        magnet_sleep_time = 0.005
        self.command("magnetcurrent = smua.source.leveli")
        I_start = self.query("printnumber(magnetcurrent)")
        B_start = float(I_start) / self.apt
        field = B_start
        step = 1e-5

        while (field < value - step) or (field > value + step):
            if (field > value +step):
                field = field - step
            elif (field < value-step):
                field = field + step
            elif (abs(field - value) < 2*step):
                field = value
            magnetcurrent = field * self.apt
            self.command("smua.source.leveli = {:.8f}".format(magnetcurrent))
            self._amps = magnetcurrent
            #print("field: " + str(field) + "T")
            time.sleep(magnet_sleep_time)


    def initInstrument(self):
        self.sweepToZero()
        NPLC = 1
        VLimit = 1
        self.command("smua.reset()")
        self.command("smua.source.func = smua.OUTPUT_DCAMPS")
        self.command("smua.source.autorangei = smua.AUTORANGE_ON")
        self.command("smua.source.limitv = {}".format(VLimit))
        self.command("smua.source.leveli = 0.0")
        self.command("smua.measure.autorangev = smua.AUTORANGE_ON")
        self.command("smua.measure.nplc = {}".format(NPLC))
        self.command("display.smua.measure.func = display.MEASURE_DCVOLTS")
        self.command("smua.source.offmode = smua.OUTPUT_NORMAL")
        self.command("smua.source.output = smua.OUTPUT_ON")

    def query(self, query: str) -> str:
        gpib.write(self.inst, '{}'.format(query+'\r\n'))
        return  str(gpib.read(self.inst,512).decode())

    def command(self, command: str):
        gpib.write(self.inst, '{}'.format(command+'\r\n'))


    @property
    def unit(self) -> int:
        return int(0)

    @unit.setter
    def unit(self, value: int):
        assert (value == 0), 'Value should be 0 (A)!'
        self._unit = value
        self.command('T{:1d}'.format(self.unit))

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

    @property
    def iRate(self) -> float:
        return self._iRate

    @iRate.setter
    def iRate(self, value: float):
        assert abs(value) <= self._iRateMax, "Absolute I-Rate should be lower than {}".format(self._iRateMax)
        self._iRate = value

    @property
    def amps(self) -> float:
        return float(self._amps)

    @amps.setter
    def amps(self, value: float):
        self.sweepToValue(value)

    @property
    def tesla(self) -> float:
        return self.amps / self.apt

    @tesla.setter
    def tesla(self, value):
        self.amps = value


if __name__ == '__main__':
    dev = SMU()
    dev.amps = -0.1
    time.sleep(5)
    print(dev.tesla)
    dev.amps = 0.1
    time.sleep(5)
    print(dev.tesla)
    dev.rampTarget = 0









