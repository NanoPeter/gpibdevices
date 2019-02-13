from enum import Enum

from typing import Union

class SenseMethod(Enum):
    voltage_dc = 'VOLT:DC'
    voltage_ac = 'VOLT:AC'
    current_dc = 'CURR:DC'
    current_ac = 'CURR:AC'
    two_probe_resistance = 'RES'
    four_probe_resistance = 'FRES'

class MinMaxValue(Enum):
    MIN = 'MIN'
    MAX = 'MAX'

class Multimeter34401A(object):
    def __init__(self, device):
        self.dev = device
        self.dev.write('*RST')

    def set_sense(self, method: SenseMethod,
            range: Union[float, MinMaxValue] = MinMaxValue.MAX,
            resolution: Union[float, MinMaxValue] = MinMaxValue.MIN,
            integration_time_nplc: float = 10,
            auto_range: bool = False):
        """ sets all sense settings for a measurement
            nplc will be set near the following numbers
            [0.02, 0.2, 1, 10, 100]
        """

        method_string = method.value

        resolution_parameter = str(resolution) if type(resolution) is float else resolution.value
        range_parameter = str(range) if type(range) is float else range.value
        auto_range_parameter = 'ON' if auto_range else 'OFF'

        integration_time = min([time for time in [0.02, 0.2, 1, 10, 100]
                                if time >= integration_time_nplc])

        self.dev.write('SENS:FUNC "{:s}"'.format(method_string))
        self.dev.write('SENS:FUNC:{:s}:RANG {:s}'.format(method_string, range_parameter))
        self.dev.write('SENS:FUNC:{:s}:RANG:AUTO {:s}'.format(method_string, auto_range_parameter))
        self.dev.write('SENS:FUNC:{:s}:RES {:s}'.format(method_string, resolution_parameter))
        self.dev.write('SENS:FUNC:{:s}:NPLC {:f}'.format(method_string, integration_time))

    def get_errors(self):
        return self.dev.query('SYST:ERR?')


    def read(self):
        return self.dev.query('READ?')

    @property
    def resistance(self) -> float:
        return float(self.read())


if __name__=='__main__':
    from visa import ResourceManager
    from time import sleep

    rm = ResourceManager('@py')

    dev = rm.open_resource('GPIB0::9::INSTR')

    mux = Multimeter34401A(dev)

    mux.set_sense(SenseMethod.four_probe_resistance)

    print(dev.read())


