import os
from ..particles.ParticleClass import single_particle


def _BIND_Get_Particle(self,parts=[]):
    """
    _BIND_Get_Particle(simulation,parts=[])

    Method bound to simulation class for reading in particles.

    Inputs
    ----------
    - simulation
        Called from self.GetParticle(), self in simulation class
    Optional Inputs
    ----------
    - parts=[]
        If parts is empty, read all particles
        Otherwise read in the particles listed in parts (indexing from 1) [convention from LEVIS]
    
    Returns
    ----------
    Particle class
    """
    if self.params["dump_particles"]==0:
        # If there is no particle data abort
        raise("single particle dumping is off, aborting read.")
    
    if (parts == []):
        # If index is -1 and no list of parts is specified read all
        np = len(os.listdir(os.path.join(self.dirdiag,"particle_data")))
        self.sp = dict.fromkeys(range(np))
        for i in self.sp:
            self.sp[i] = single_particle(self,i,self.lite)
    elif parts != []:
        if type(parts) == int:
            parts = [parts]
        # Read only the list of particles provided
        parts = [x-1 for x in parts]
        self.sp = dict.fromkeys(parts)
        for i in parts:
            self.sp[i] = single_particle(self,i,self.lite)

