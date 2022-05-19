import os
import numpy
import glob
import h5py
import warnings

from .ext_fns import ext_rhotor, ext_v, ext_vpar, ext_vperp

class initial_particle_dist:
    """
    initial_particle_dist(simulation)

    Class containing the initial particle distribution

    Inputs
    ----------
    simulation class from LEVISClass

    Returns
    ----------
    initial_particle_dist class containing initial particle data
    """
    def __init__(self,simulation):
        self.Get_InitialParticle(simulation)

        # self.__read_tauparticle(simulation.dirrun)

    def Get_InitialParticle(self,simulation):
        """
        See initial_particle_dist(simulation)
        """
        # Check the init particle distribution type and call reading fn
        exts = ["dat","h5"]
        for ext in exts:
            try:
                fname = glob.glob(os.path.join(simulation.dirrun,"single.particle."+ext))[0]
                break
            except IndexError:
                #Make sure if this fails it doesn't try to read nothing
                ext = "" 
        # Read in file
        if ext == "dat":
            self.__read_init_dat(simulation.equilibrium_type,fname)
        elif ext == "h5":
            self.__read_init_h5(fname)
        else:
            raise FileNotFoundError("No h5 or dat single particle file found")
        

        # TODO: what does this file look like???
        f_alpha = os.path.join(simulation.dirrun,"fusion_alpha.out")
        if os.path.exists(f_alpha):
            # TODO: Does nothing in MATLAB routines
            # alphaprob = numpy.loadtxt(f_alpha)
            self.wc = self.w
        
        



    def __read_init_dat(self,equilibrium_type,fname):
        """
        __read_init_dat(self,equilibrium_type,fname)

        Open single.particle.dat and read in data
        """
        # Get the # of parts
        f_open = open(fname)
        self.np = int(f_open.readline())
        f_open.close()
        # read in the rest
        data = numpy.loadtxt(fname,skiprows=1,max_rows=self.np)
        self.mass      = data[:,0]
        self.charge    = data[:,1]
        self.s         = data[:,2]
        self.th        = data[:,3]
        self.ph        = data[:,4]
        self.lam       = data[:,5]
        self.E         = data[:,6]
        self.w         = data[:,7]
        if equilibrium_type == "spec":
            self.lvol  = data[:,8]
    
    def __read_init_h5(self,fname):
        """
        __read_init_h5(self,fname)

        Open single.particle.h5 and read in data
        """
        # single.particle.h5 reading
        f_open = h5py.File(fname)
        self.np = int(f_open["nparts"])
        self.s = numpy.array(f_open["u1"])
        self.th = numpy.array(f_open["u2"])
        self.ph = numpy.array(f_open["u3"])
        self.lam = numpy.array(f_open["lambda"])
        self.E = numpy.array(f_open["energy"])
        self.w = numpy.array(f_open["weight"])
        self.mass = numpy.array(f_open["mass"])
        self.charge = numpy.array(f_open["charge"])
        self.R = numpy.array(f_open["R"])
        self.Z = numpy.array(f_open["Z"])
        # NBI distribution
        try:
            self.vx = numpy.array(f_open["vx"])
            self.vy = numpy.array(f_open["vy"])
            self.vz = numpy.array(f_open["vz"])
        except:
            warnings.warn('No NBI distribution')
        # Generated distribution
        try:
            self.Ptor = numpy.array(f_open["Ptor"])
            self.muOqp = numpy.array(f_open["muOqp"])
        except:
            warnings.warn('Not a generated distribution')
        
    def __read_tauparticle(self,dirname):
        """
        __read_tauparticle(self,dirname)

        Open TauParticle file and read in data
        """
        # TODO: what does this file look like???
        f_turn = os.path.join(dirname,"TauParticle")
        if os.path.exists(f_turn):
            tmpfile = numpy.loadtxt(f_turn)
            index_final = tmpfile[:,0]
            th_final = tmpfile[:,1]
            ph_final = tmpfile[:,2]
            t_final = tmpfile[:,3]

            nup = (ph_final - th_final)/2/numpy.pi/t_final #more descriptive name?? also what the hell is this

            self.nup = numpy.zeros(self.np)
            self.th_final = numpy.zeros(self.np)
            self.ph_final = numpy.zeros(self.np)

            self.nup[index_final] = nup
            self.th_final[index_final] = th_final
            self.ph_final[index_final] = ph_final
            self.index_final = index_final
    
    def __read_EcrossB(self,fdir):
        """
        __read_EcrossB(self,fdir)

        Open EcrossB.in file and read in data
        """
        # TODO
        # Get initial potential energy data
        fname = os.path.join(fdir,"EcrossB.in")
        if os.path.exists(fname):
            f_open = open(fname,'r')
            # ns = f_open.readline()
            # self.Epot = self.charge
            f_open.close()
        else:
            raise FileNotFoundError('No ExB file found')
    

    '''
    INTERNAL FNS -- Do not store
    '''
    # def rhoj(self):
    #     return 

    '''
    Bind to ext_fns since same as single_particle class
    '''
    rhotor = ext_rhotor
    v = ext_v
    vpar = ext_vpar
    vperp = ext_vperp


