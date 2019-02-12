class Multimeter34401A(object):
    """With add-in card Agilent 34901A on channel 1."""
    
    def __init__(self, device):
        self.dev = device
        self.dev.write_termination = "\n"
        self.dev.read_termination = "\n"
        self.dev.write('*RST')

    def four_wire(self):
        #here MEAS:FRES? RANGE, RESOLTION
        # MEAS:FRES? 10000, 0.1
        # meaning: measure resistance in four-wiremode 
        # in the range of 10kOhm with an accuracy of 0.1 Ohm
        self.dev.write('MEAS:FRES? 10000, 0.1')

    def two_wire(self):
        self.dev.write('MEAS:RES? 10000, 0.1')



if __name__=='__main__':
    from visa import ResourceManager
    from time import sleep

    rm = ResourceManager('@py')

    dev = rm.open_resource('GPIB0::9::INSTR')

    mux = Multimeter34401A(dev)
    
    print(dev.four_wire())

    
