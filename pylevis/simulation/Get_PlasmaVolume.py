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
    """
    volume(self,fname,ns)

    Reads in the data from <run ID>/Diag/Volume

    Returns
    ----------
    Volume class with contents:
        s: radial array of points
        dV: \Delta V at radial points
    """
    def __init__(self,fname,ns):
        # Read in all rows skipping first
        self.dV = numpy.loadtxt(fname,skiprows=1)
        # Create radial points
        s = numpy.linspace(0,1,num=ns+1,endpoint=True)
        self.s = s[:-1] + numpy.diff(s)



'''
BINDING TO LEVIS CLASS
'''

def BIND_Get_Volume(self):
    """
    volume(self,fname,ns)

    Method bound to simulation class for reading in plasma volume data.

    Returns
    ----------
    Volume class
    """
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

    

