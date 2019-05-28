
import gpib
from enum import Enum


class SweepMode(Enum):
    HOLD = 'A0'
    TO_SET_POINT = 'A1'
    TO_ZERO = 'A2'
    CLAMPED = 'A4'

class ControlMode(Enum):
    LOCAL_AND_LOCKED = 'C0'
    REMOTE_AND_LOCKED = 'C1'
    LOCAL_AND_UNLOCKED = 'C2'
    REMOTE_AND_UNLOCKED = 'C3'

class CommunicationProtocol(Enum):
    NORMAL = 'Q0'
    LF_AND_CR = 'Q2'
    EXTENDED_RESOLUTION = 'Q4'
    EXTENDED_RESOLUTION_AND_LF_AND_CR = 'Q6'

class SwitchHeaterMode(Enum):
    OFF_AT_ZERO = 'H0'
    ON = 'H1'

class IPS120_10:
    def __init__(self, address: int = 25):
        assert (1 <= address <= 32), 'address out of range'

        self._device_handler = gpib.dev(0, address)
        gpib.config(self._device_handler, gpib.IbaEOSrd, 1)
        gpib.config(self._device_handler, gpib.IbaEOSchar, 13)

    def clear(self):
        gpib.clear(self._device_handler)

    def _query(self, message: str):
        self._write(message)
        return self._read()

    def _write(self, message: str):
        gpib.write(self._device_handler, message + '\r')
        
    def _read(self) -> str:
        return gpib.read(self._device_handler, 512).rstrip()

    def set_control_mode(self, mode: ControlMode):
        self._query(mode.value)

    def set_communication_protocol(self, protocol: CommunicationProtocol):
        self._write(protocol.value)

    def set_sweep_mode(self, mode: SweepMode):
        self._query(mode.value)

    def set_switch_heater(self, mode: SwitchHeaterMode):
        self._query(mode.value)

    def set_current_sweep_rate(self, amps_per_minute: float):
        assert (0 <= amps_per_minute <= 5), 'rate is out of range'
        command = 'S{:.04f}'.format(amps_per_minute)
        self._query(command)

    def set_field_sweep_rate(self, tesla_per_minute: float):
        assert (0 <= tesla_per_minute <= 0.3), 'rate is out of range'
        command = 'T{:.04f}'.format(tesla_per_minute)
        self._query(command)

    def set_target_current(self, target_amps: float):
        assert abs(target_amps) < 120, 'target current is too damn high'
        command = 'I{:.04f}'.format(target_amps)
        self._query(command)

    def set_target_field(self, target_tesla: float):
        assert abs(target_tesla) < 8.0, 'target field is too damn high'
        command = 'J{:.04f}'.format(target_tesla)
        self._query(command)

    def get_current(self):
        return self._query('R0')

    def get_field(self):
        return self._query('R7')

    @property
    def field(self):
        field_bytes = self.get_field()

        field_string = field_bytes.decode('utf-8')

        if field_string[0] != 'R':
            return float('nan')
        else:
            try:
                return float(field_string[1:])
            except:
                return float('inf')

        



        

