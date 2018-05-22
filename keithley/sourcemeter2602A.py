from enum import Enum


class SMUChannel(Enum):
    channelA = 'a'
    channelB = 'b'

class Sourcemeter2602A(object):
        def __init__(self, device, sub_device: SMUChannel = SMUChannel.channelA):
                self._dev = device
                self.__channel_string = 'smu{}'.format(sub_device.value)
                self.__channel_token = sub_device.value
                self._dev.write('smua.reset()')

        def voltage_driven(self, voltage, current_limit=1e-6, nplc = 3):

                self._dev.write('{}.reset()'.format(self.__channel_string))
                self._dev.write("{}.source.func = smua.OUTPUT_DCVOLTS".format(self.__channel_string))
                self._dev.write("{}.source.levelv = 0.0".format(self.__channel_string))
                self._dev.write("{}.source.autorangev = smua.AUTORANGE_ON".format(self.__channel_string))
                self._dev.write("{}.source.limiti = {}".format(self.__channel_string, current_limit))
                self._dev.write("{}.measure.autorangei = smua.AUTORANGE_ON".format(self.__channel_string))
                self._dev.write("{}.measure.nplc = {}".format(self.__channel_string, nplc))

        def current_driven(self, current, voltage_limit=1):
                raise NotImplementedError('you fool!')

        def arm(self):
                self._dev.write("{}.source.output = smua.OUTPUT_ON".format(self.__channel_string))

        def disarm(self):
                self._dev.write("{}.source.output = smua.OUTPUT_OFF".format(self.__channel_string))

        def set_voltage(self, voltage):
                self._dev.write("{}.source.levelv = {}".format(self.__channel_string, voltage))

        def set_current(self, current):
                raise NotImplementedError('you fool!')

        def read(self):
                self._dev.write("ireading{0}, vreading{0} = {1}.measure.iv()".format(self.__channel_token, self.__channel_string))
                return self._dev.query_ascii_values("printnumber(vreading{0},ireading{0})".format(self.__channel_token))



if __name__ == '__main__':
        from visa import ResourceManager as RM

        rm = RM('@py')

        dev = rm.open_resource('GPIB0::10::INSTR')

        smu = Sourcemeter2602A(dev)
        smu.voltage_driven(0)
        smu.arm()
        smu.set_voltage(1e-3)
        print(smu.read())
        smu.set_voltage(0)
        smu.disarm()

