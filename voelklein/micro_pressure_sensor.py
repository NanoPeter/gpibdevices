from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

from typing import Tuple

class MicroPressureSensor:
    BAUD_RATE = 9600
    TIMEOUT = 1

    MAX_VALUE = 51150
    MIN_VALUE = 0

    MESSAGE = 'A\n'.encode()

    #sensor parameter
    P0 = 7.77571e-3
    D = 1.0 / 1.21503756

    def __init__(self, serial_path -> str):
        self._serial = Serial(serial_path,
                              baudrate = MicroPressureSensor.BAUD_RATE,
                              timeout = MicroPressureSensor.TIMEOUT,
                              bytesize = EIGHTBITS,
                              stopbits = STOPBITS_ONE,
                              xonxoff=0,
                              rtscts=0)
        #reset device and serial buffer
        self._serial.setDTR(False)
        self._serial.flushInput()
        self._serial.setDTR(True)

        self._lower_bound = MicroPressureSensor.MIN_VALUE #lowest possible value
        self._upper_bound = MicroPressureSensor.MAX_VALUE #highest possible value

    def _calculate_pressure(self, value: int) -> float:
        if value > C:
            radicand = self._upper_bound / (value - self._lower_bound) - 1.0
            if radicand < 0:
                return float('-inf')
            else:
                return MicroPressureSensor.P0 * radicand**MicroPressureSensor.D
        else:
            return float('inf')

    def _get_raw_value(self):
        s.write(MicroPressureSensor.MESSAGE)
        answer = s.readline()
        text = answer.decode('utf-8')

        if len(text) > 0:
            value = int(text[:-2])
            pressure = self._calculate_pressure(value)
            return pressure, value
        else:
            raise IOError('no answer from device')

    @property
    def pressure(self) -> Tuple[float, int]:
        try:
            value = self._get_raw_value()
        except IOError:
            return float('nan'), -1
        else:
            return self._calculate_pressure(value), value

    def calibrate_lower_bound(self):
        try:
            self._lower_bound = self.get_raw_value()
        except IOError:
            self._lower_bound = MicroPressureSensor.MIN_VALUE

    def calibrate_upper_bound(self):
        try:
            self._upper_bound = self.get_raw_value()
        except IOError:
            self._upper_bound = MicroPressureSensor.MAX_VALUE

