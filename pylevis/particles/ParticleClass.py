'''
PARTICLE CLASS
'''
import os
import numpy

from .ext_fns import _ext_rhotor, _ext_v, _ext_vpar, _ext_vperp

class single_particle:
    """
    single_particle(simulation,index=-1)

    Class for particles including methods for reading in and pulling attributes.

    Inputs
    ----------
    - simulation
        the simulation class from LEVISClass
    Optional Inputs
    ----------
    - index = -1 (default)
        Which particle to read in
    - lite = False (default)
        If false, values such as x,y,z will be computed and stored. If true, these will remain as functions i.e. self.x()

    Returns
    ----------
    particle class:
        Either a complete particle object or an empty particle
    """
    def __init__(self,simulation,index=-1,lite=False):
        n_ele = 24
        if simulation.equilibrium_type == "spec":
            n_ele += 1
        if simulation.params["lorentzian"]:
            n_ele += 2  ### TODO
            raise("Lorentzian particles are currently not implemented for reader")
        # Generate path to particle file
        particle_file = os.path.join(simulation.dirdiag,"particle_data","particle."+str(index+1))
        if os.path.isfile(particle_file):
            # If the file exists read it
            fulldata = numpy.loadtxt(particle_file)
            if numpy.size(fulldata)!=0:
                # If data exists read in
                self._read_single_particle(fulldata,n_ele)
                self.missing = False
                if simulation.params["nparts"] > 1:
                    self.mass = simulation.init.mass[index]
                    self.charge = simulation.init.charge[index]
                else:
                    self.mass = simulation.init.mass
                    self.charge = simulation.init.charge
            else:
                # Otherwise create empty particle
                self._empty_particle()
        else:
            raise("Read failed: Particle "+str(index)+" does not exist.")
        
        if not lite:
            # If read-in is not in low memory mode construct and store the data
            self.nt = self.nt()
            self.passing = self.passing()
            self.larmor = self.larmor()
            self.x = self.x()
            self.y = self.y()
            self.z = self.z()
            self.gc_x =self.gc_x()
            self.gc_y =self.gc_y()
            self.gc_z =self.gc_z()
            

    '''
        Inbuilt functions. Overwritten by stored values if lite=False
    '''
    rhotor = _ext_rhotor
    v = _ext_v
    vpar = _ext_vpar
    vperp = _ext_vperp
    # def v(self): #Velocity
    #     return numpy.sqrt(2*self.E*self.charge/self.mass)
    # def vpar(self): #v parallel to B
    #     return self.v()*self.lam
    # def vperp(self): #v perpendicular to B
    #     return self.v()*numpy.sqrt(1-self.lam**2)
    
    def nt(self):
        return len(self.t)
    
    def passing(self): #If particle is passing/counterpassing
        return int(max(0,numpy.sign(max(self.lam)*min(self.lam))))
    
    def larmor(self): #Larmor radius
        return self.mass*self.vperp()/(self.modB*self.charge)
    
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
    
    def crossing(self):
        try:
            return any(self.lvol != self.lvol[1])
        except:
            return False
    

    def _read_single_particle(self,fulldata,n_ele=25):
        # The file format expected
        """
        _read_single_particle(self,fulldata,n_ele=25)

        Returns
        ----------
        Particle data from particle.i data file
        """
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
    
    def _empty_particle(self,equilibrium_type="spec"):
        """
        _empty_particle(self,equilibrium_type="spec")

        Returns
        ----------
        Missing particle object for lost particles
        """
        self.mass   = 0
        self.charge = 0
        self.t      = numpy.array([])
        self.s      = numpy.array([])
        self.th     = numpy.array([])
        self.zeta   = numpy.array([])
        self.gy     = numpy.array([])
        # self.rhotor = numpy.array([])
        self.ph     = numpy.array([])
        self.lam    = numpy.array([])
        self.E      = numpy.array([])
        self.R      = numpy.array([])
        self.Z      = numpy.array([])
        # self.nt     = 0
        self.missing= True
        if equilibrium_type == "spec":
            self.lvol   = numpy.array([])
    







    


