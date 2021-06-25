'''
GET VOLUME DATA
'''
import os
import warnings
import numpy


'''
VOLUME SUB-CLASS
'''
class volume():
    def __init__(self,fname,ns):
        
        self.dV = numpy.loadtxt(fname,skiprows=1)

        s = numpy.linspace(0,1,num=ns+1,endpoint=True)
        self.s = s[:-1] + numpy.diff(s)



'''
BINDING TO LEVIS CLASS
'''

def BIND_Get_Volume(self):
    fname = os.path.join(self.dirdiag,"Volume")
    
    if os.path.exists(fname):
        with open(fname) as f_open:
            # Read in the first line
            ns = int(f_open.readline())###TODO: more useful name
        # vol = volume(fname,ns)
        # Construct the volume
        self.vol = volume(fname,ns)
    else:
        warnings.warn('No volume data')
        self.vol = -1

    

