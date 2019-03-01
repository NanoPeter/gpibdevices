
class Sourcemeter2400(object):
    def __init__(self, device):
        self._dev = device

    def voltage_driven(self, voltage, current_limit=1e-6, nplc=1):
        self._dev.write('*RST')
        self._dev.write(':sense:function "current"')
        self._dev.write(':source:function voltage')
        self._dev.write(':source:voltage:range:auto on')
        self._dev.write(':sense:current:range:auto on')
        self._dev.write(':sense:current:protection {0}'.format(current_limit))
        self._dev.write(':sense:current:nplcycles {}'.format(nplc))
        self._dev.write(':sense:average off')
        self._dev.write(':output:state 0')
        self._dev.write(':source:voltage:level {0}'.format(voltage))
        self._dev.write(":format:elements voltage, current")

    def current_driven(self, current, voltage_limit=1, nplc=1):
        self._dev.write('*RST')
        self._dev.write(':sense:function "voltage"')
        self._dev.write(':source:function current')
        self._dev.write(':source:current:range:auto on')
        self._dev.write(':sense:voltage:range:auto on')
        self._dev.write(':sense:voltage:protection {0}'.format(voltage_limit))
        self._dev.write(':sense:voltage:nplcycles {}'.format(nplc))
        self._dev.write(':sense:average off')
        self._dev.write(':output:state 0')
        self._dev.write(':source:current:level {0}'.format(current))
        self._dev.write(":format:elements voltage, current")

    def init_beeper(self):
        self._dev.write(":system:beeper:stat 1")

    def beep(self, frequency:float, duration:float):
        frequency = min([2e6, max([65, frequency]))
        duration = min([7.9, max([0, duration])])
        
        self._dev.write(f":system:beeper:immediate {frequency},{duration}")

    def arm(self):
        self._dev.write(':output:state 1')

    def disarm(self):
        self._dev.write(':output:state 0')

    def set_voltage(self, voltage):
        self._dev.write(':source:voltage:level {0}'.format(voltage))

    def set_current(self, current):
        self._dev.write(':source:current:level {0}'.format(current))

    def read(self):
        voltage, current = self._dev.query_ascii_values(':read?')
        return float(voltage), float(current)

    def __str__(self):
        return  'Sourcemeter2400 {}'.format(self._dev.resource_name)

