'''
READING FIELD LINES
'''
import numpy
import scipy.ndimage

class fieldline():
    def __init__(self,LEVIS,rho0=0.5,th0=0,ph0=0,nph=1e3,ph_lim=2*numpy.pi*5,qvalue=1):
        self.q      = qvalue
        self.rho    = rho0
        self.ph     = numpy.linspace(ph0,ph_lim,num=nph,endpoint=True)
        self.th     = th0 + (self.ph - ph0)/self.q

        # Map coordinates does the same as interp2 in MATLAB
        Rl = scipy.ndimage.map_coordinates(LEVIS.equilib.chi,LEVIS.equilib.rhotor,LEVIS.equilib.R[:,:,0],[numpy.angle(self.th),self.rho])
        # Cartesian coordinates
        self.z = scipy.ndimage.map_coordinates(LEVIS.equilib.chi,LEVIS.equilib.rhotor,LEVIS.equilib.Z[:,:,0],[numpy.angle(self.th),self.rho])
        self.x = Rl*numpy.cos(self.ph)
        self.y = Rl*numpy.sin(self.ph)



# def GetFieldLine(self,rho0=0.5,th0=0,ph0=0,nph=1e3,ph_lim=2*numpy.pi*5,qvalue=1):
    
    
    