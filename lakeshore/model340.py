
import gpib
from enum import Enum

class Sensor(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    
class Loop(Enum):
    ONE = '1'
    TWO = '2'

class RampStatus(Enum):
    Ramping = '1'
    NotRamping = '0'

class Model340:
    
    TERM_CHARS = '\r\n'
    
    def __init__(self, address, board=0):
        self._dev = gpib.dev(board, address)
        
    def _read(self):
        return gpib.read(self._dev, 512)

    def _write(self, message):
        number_of_bytes = gpib.write(self._dev, message + self.TERM_CHARS)
        return number_of_bytes
        
    def _query(self, message):
        self._write(message)
        return self._read().strip().decode()
        
    def get_set_point(self, loop:Loop=Loop.ONE):
        return float(self._query('SETP? {}'.format(loop.value)))
        
    def set_set_point(self, loop:Loop, temperature):
        return self._write('SETP {loop}, {temperature}'.format(loop=loop.value,
                                                              temperature=temperature))
        
    def get_temperature(self, sensor:Sensor=Sensor.A):
        return float(self._query('KRDG? {}'.format(sensor.value)))
        
    def get_ramp(self, loop:Loop=Loop.ONE):
        answer = self._query('RAMP? {}'.format(loop.value))
        split = answer.split(',', maxsplit=1)
        
        return {'enabled': bool(split[0]), 'rate': float(split[1])}
        
    def set_ramp(self, loop:Loop, enable: bool, rate: float):
            
        self._write('RAMP {loop}, {enable}, {rate}'.format(loop=loop.value,
                                                            enable=int(enable),
                                                            rate=rate))
    def get_rampstatus(self, loop:Loop=Loop.ONE):
        return RampStatus(self._query('RAMPST? {}'.format(loop.value)))
        
        
    @property
    def identifier(self):
        return self._query('*IDN?')
    
        
if __name__ == '__main__':
    
    temperature_controller = Model340(12)
    
    print(temperature_controller.identifier)
    
    print(temperature_controller.get_temperature())
    
    print(temperature_controller.get_ramp())
    
    print(temperature_controller.get_rampstatus())
    
    
        
