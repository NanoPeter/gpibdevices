from enum import Enum


class SMUChannel(Enum):
    channelA = 'a'
    channelB = 'b'


class Sourcemeter2602A(object):
    def __init__(self, device, sub_device: SMUChannel = SMUChannel.channelA):
        self._dev = device
        self._channel_string = 'smu{}'.format(sub_device.value)
        self._channel_token = sub_device.value
        self._channel = sub_device
        self._dev.write('{0}.reset()'.format(self._channel_string))

    def voltage_driven(self, voltage, current_limit=1e-6, nplc = 3, range=1e-8):
        #self._dev.write('{}.reset()'.format(self._channel_string))
        self._dev.write('{0}.source.offmode = {0}.OUTPUT_HIGH_Z'.format(self._channel_string))
        self._dev.write("{0}.source.func = {0}.OUTPUT_DCVOLTS".format(self._channel_string))
        self._dev.write("{}.source.levelv = 0.0".format(self._channel_string))
        self._dev.write("{0}.source.autorangev = {0}.AUTORANGE_ON".format(self._channel_string))
        self._dev.write("{}.source.limiti = {}".format(self._channel_string, current_limit))
        self._dev.write("{0}.measure.autorangei = {0}.AUTORANGE_ON".format(self._channel_string))
        self._dev.write("{}.measure.nplc = {}".format(self._channel_string, nplc))
        self._dev.write("{}.measure.lowrangei = {}".format(self._channel_string, range))

    def current_driven(self, current, voltage_limit=1, nplc = 3, range=1e-8):
        #self._dev.write('{}.reset()'.format(self._channel_string))
        self._dev.write('{0}.source.offmode = {0}.OUTPUT_HIGH_Z'.format(self._channel_string))
        self._dev.write("{0}.source.func = {0}.OUTPUT_DCAMPS".format(self._channel_string))
        self._dev.write("{}.source.leveli = {}".format(self._channel_string, current))
        self._dev.write("{0}.source.autorangei = {0}.AUTORANGE_ON".format(self._channel_string))
        self._dev.write("{}.source.limitv = {}".format(self._channel_string, voltage_limit))
        self._dev.write("{0}.measure.autorangev = {0}.AUTORANGE_ON".format(self._channel_string))
        self._dev.write("{}.measure.nplc = {}".format(self._channel_string, nplc))
        #self._dev.write("{}.measure.lowrangev = {}".format(self._channel_string, range))

    def arm(self):
        self._dev.write("{0}.source.output = {0}.OUTPUT_ON".format(self._channel_string))

    def disarm(self):
        self._dev.write("{0}.source.output = {0}.OUTPUT_OFF".format(self._channel_string))

    def set_voltage(self, voltage):
        self._dev.write("{}.source.levelv = {}".format(self._channel_string, voltage))

    def set_current(self, current):
        self._dev.write("{}.source.leveli = {}".format(self._channel_string, current))

    def read(self):
        self._dev.write("ireading{0}, vreading{0} = {1}.measure.iv()".format(self._channel_token, self._channel_string))
        return self._dev.query_ascii_values("printnumber(vreading{0},ireading{0})".format(self._channel_token))

    def __str__(self):
        return 'Sourcemeter 2602A {} {}'.format(self._channel, self._dev.resource_name)


if __name__ == '__main__':
    from visa import ResourceManager as RM

    rm = RM('@py')

    dev = rm.open_resource('GPIB0::10::INSTR')

    smu = Sourcemeter2602A(dev)
    smu.voltage_driven(0, 1e-9, 1, range=1e-12)


