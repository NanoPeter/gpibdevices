
class Sourcemeter2602A(object):
        def __init__(self, device):
                self.__dev = device
                self.__dev.write('smua.reset()')
               
        def voltage_driven(self, voltage, current_limit=1e-6, nplc = 3):

                self.__dev.write('smua.reset()')
                self.__dev.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                self.__dev.write("smua.source.levelv = 0.0")
                self.__dev.write("smua.source.autorangev = smua.AUTORANGE_ON")
                self.__dev.write("smua.source.limiti = {}".format(current_limit))
                self.__dev.write("smua.measure.autorangei = smua.AUTORANGE_ON")
                self.__dev.write("smua.measure.nplc = {}".format(nplc))
                
        def current_driven(self, current, voltage_limit=1):
                raise NotImplementedError('you fool!')
            
        def arm(self):
                self.__dev.write("smua.source.output = smua.OUTPUT_ON")

        def disarm(self):
                self.__dev.write("smua.source.output = smua.OUTPUT_OFF")
           
        def set_voltage(self, voltage):
                self.__dev.write("smua.source.levelv = {}".format(voltage))

        def set_current(self, current):
                raise NotImplementedError('you fool!')

        def read(self):
                self.__dev.write("ireading, vreading = smua.measure.iv()")
                return self.__dev.query_ascii_values("printnumber(vreading,ireading)")



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
        
