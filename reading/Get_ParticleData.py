'''
PARTICLE CLASS
'''
import os
import numpy

from .ext_fns import ext_rhotor, ext_v, ext_vpar, ext_vperp

class single_particle():
    '''
    Class for single particles including methods for reading in and pulling attributes
    '''
    def __init__(self,LEVIS,index=-1):
        n_ele = 24
        if LEVIS.equilibrium_type == "spec":
            n_ele += 1
        if LEVIS.params["lorentzian"]:
            n_ele += 2  ### TODO
            raise("Lorentzian particles are currently not implemented for reader")
        # Generate path to particle file
        particle_file = os.path.join(LEVIS.dirdiag,"particle_data","particle."+str(index))
        if os.path.isfile(particle_file):
            fulldata = numpy.loadtxt(particle_file)
            if numpy.size(fulldata)!=0:
                # If data exists read in
                self.read_single_particle(fulldata,n_ele)
                self.missing = False
                self.mass = LEVIS.init.mass[index]
                self.charge = LEVIS.init.charge[index]
            else:
                # Otherwise create empty particle
                self.empty_particle()

        else:
            raise("Read failed: Particle "+str(index)+" does not exist.")

    def read_single_particle(self,fulldata,n_ele=25):
        '''Read in particle data from particle.n data file'''
        self.t              = fulldata[0:-1:n_ele]
        self.s              = fulldata[1:-1:n_ele]
        self.th             = fulldata[2:-1:n_ele]
        self.zeta           = fulldata[3:-1:n_ele]
        self.gy             = fulldata[4:-1:n_ele]
        self.R              = fulldata[5:-1:n_ele]
        self.Z              = fulldata[6:-1:n_ele]
        self.ph             = fulldata[7:-1:n_ele]
        self.E              = fulldata[8:-1:n_ele]
        self.lam            = fulldata[9:-1:n_ele]
        self.Ptor           = fulldata[10:-1:n_ele]
        self.Ppol           = fulldata[11:-1:n_ele]
        self.muOqp          = fulldata[12:-1:n_ele]
        self.modB           = fulldata[13:-1:n_ele]
        self.gc_s           = fulldata[14:-1:n_ele]
        self.gc_th          = fulldata[15:-1:n_ele]
        self.gc_zeta        = fulldata[16:-1:n_ele]
        self.gc_R           = fulldata[17:-1:n_ele]
        self.gc_Z           = fulldata[18:-1:n_ele]
        self.gc_ph          = fulldata[19:-1:n_ele]
        self.field_variation= fulldata[20:-1:n_ele]
        self.norm_curv      = fulldata[21:-1:n_ele]
        self.geod_curv      = fulldata[22:-1:n_ele]
        self.w              = fulldata[23:-1:n_ele]
        if n_ele == 25:
            self.lvol           = fulldata[24:-1:n_ele].astype(int)
        

    def empty_particle(self,equilibrium_type="spec"):
        self.mass   = 0
        self.charge = 0
        self.t      = numpy.array([])
        self.s      = numpy.array([])
        self.th     = numpy.array([])
        self.zeta   = numpy.array([])
        self.gy     = numpy.array([])
        self.rhotor = numpy.array([])
        self.ph     = numpy.array([])
        self.lam    = numpy.array([])
        self.E      = numpy.array([])
        self.R      = numpy.array([])
        self.Z      = numpy.array([])
        # self.nt     = 0
        self.missing= True
        if equilibrium_type == "spec":
            self.lvol   = numpy.array([])
        
    
    '''
        Calculate these values when required rather than storing them
    '''
    rhotor = ext_rhotor
    v = ext_v
    vpar = ext_vpar
    vperp = ext_vperp
    # def v(self): #Velocity
    #     return numpy.sqrt(2*self.E*self.charge/self.mass)
    # def vpar(self): #v parallel to B
    #     return self.v()*self.lam
    # def vperp(self): #v perpendicular to B
    #     return self.v()*numpy.sqrt(1-self.lam**2)
    
    def nt(self):
        return len(self.t)
    
    def passing(self): #If particle is passing/counterpassing
        return numpy.sign(max(self.lam)*min(self.lam))
    
    def larmor(self): #Larmor radius
        return self.mass*self.vperp/(self.modB*self.charge)
    
    ## CARTESIAN COORDINATES
    def x(self):
        return self.R*numpy.cos(self.ph)
    def y(self):
        return self.R*numpy.sin(self.ph)
    def z(self):
        return self.Z

    def gc_x(self):
        return self.gc_R*numpy.cos(self.gc_ph)
    def gc_y(self):
        return self.gc_R*numpy.sin(self.gc_ph)
    def gc_z(self):
        return self.gc_Z




'''
    BINDING TO LEVIS CLASS
'''

def Get_Particle(self,index=-1,parts=[]):
    '''
    Method bound to LEVIS class for reading in particles
    - SELF is LEVIS class
    '''
    if self.params["dump_particles"]==0:
        # If there is no particle data abort
        raise("single particle dumping is off, aborting read.")

    if (index==-1) & (parts == []):
        # If index is -1 and no list of parts is specified read all
        np = len(os.listdir(os.path.join(self.dirdiag,"particle_data")))
        self.sp = dict.fromkeys(range(np))
        for i in self.sp:
            self.sp[i] = single_particle(self,i+1)
    elif parts != []:
        # Read only the list of particles provided
        for i in parts:
            self.sp[i-1] = single_particle(self,i)
    elif index != -1:
        # Read only a single particle
        self.sp[index-1] = single_particle(self,index)
    
        


    

