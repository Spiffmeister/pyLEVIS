'''
These functions are bound to other routines, this avoids double coding when possible
'''

from numpy import sqrt

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

