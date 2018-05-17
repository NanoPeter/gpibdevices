

class Multimeter2000(object):
    def __init__(self, device):
        self.dev = device

        self.dev.write('*RST')

    def fourwire(self):
        self.dev.write(":sense:function \"FRES\"")

    def twowire(self):
        self.dev.write(":sense:function \"RES\"")

    @property
    def resistance(self):
        return self.read()

    def read(self):
        return float(self.dev.query(':read?'))


if __name__=='__main__':
    from visa import ResourceManager
    from time import sleep

    rm = ResourceManager('@py')
    dev = rm.open_resource('GPIB::9::INSTR')

    nv = Multimeter2000(dev)
    for i in range(1000):
        print(nv.read())
        sleep(1)

