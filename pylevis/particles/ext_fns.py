'''
These functions are bound to other routines, this avoids double coding when possible
'''

from numpy import sqrt
from ..auxil.constants import charge

'''
Particle and init classes
'''
def ext_rhotor(self): #
    return sqrt(self.s)

def ext_v(self): #Velocity
    return sqrt(2*self.E*self.charge/self.mass)

def ext_vpar(self): #v parallel to B
    return self.v()*self.lam
    
def ext_vperp(self): #v perpendicular to B
    return self.v()*sqrt(1-self.lam**2)

def joule2ev(Ein): #joules to energy
    return Ein/charge

def ev2joule(Ein): #energy to joules
    return Ein*charge