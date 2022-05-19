'''
Check the collisions between particles
'''
import os
from numpy import loadtxt


'''
Collision subclass
'''
class collisions():
    """
    collisions(fname)

    Inputs
    ----------
    - fname: name of file to read in

    Returns
    ----------
    Class for collisional data
    """
    def __init__(self,fname):
        data = loadtxt(fname)
        
        self.rho        = data[:,0]
        self.nud        = data[:,1]
        self.tsi        = data[:,2]
        self.tse        = data[:,3]
        self.dnuedei    = data[:,4]
        self.dnuedee    = data[:,5]
        self.Ade        = data[:,6]
        self.Adi        = data[:,7]
        self.Be         = data[:,8]
        self.Ce         = data[:,9]
        self.Bi         = data[:,10]
        self.Ci         = data[:,11]
        self.lni        = data[:,12]
        self.lne        = data[:,13]


'''
BINDING TO LEVIS
'''

def Get_Particle_Collisions(self):
    """
    Get_Particle_Collisions(self)

    Inputs
    ----------
    simulation class from LEVISClass

    Returns
    ----------
    collision class object
    """
    fname = os.path.join(self.dirdiag,"CheckCollisions.Radial")

    if os.path.exists(fname):
        return collisions(fname)
    else:
        raise FileNotFoundError('No collision file found')