

class NanovoltMeter34420A(object):
    def __init__(self, device):
        self.dev = device
        self.dev.write('*RST')
        #self.dev.write('SENS:VOLT:RANG:AUTO')

    def get_voltage(self):
        return float(self.dev.ask(':read?'))


if __name__=='__main__':
    from visa import ResourceManager

    rm = ResourceManager('@py')

    dev = rm.open_resource('GPIB::11::INSTR')

    nv = NanovoltMeter34420A(dev)
    for i in range(1000):
        print(nv.get_voltage())

