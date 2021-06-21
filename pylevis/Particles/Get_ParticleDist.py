import os
import numpy
import glob
import h5py
import warnings

import matplotlib.pyplot as plt #TODO: MUST BE A BETTER OPTION

from .ext_fns import ext_rhotor, ext_v, ext_vpar, ext_vperp


class particle_dist():
    def __init__(self,LEVIS):
        if "dat" in fname:
            self.Read_Particle_dat(fname)
        elif "h5" in fname:
            self.Read_Particle_h5(fname)
    

    '''
    Reading in data files - should work for both init and final distributions 
    TODO: TEST ON FINAL
    '''
    def Read_Particle_dat(self,equilibrium_type,fname):
        # single.particle.dat reading for initial data
        # also handles the InitDist file

        # Get the # of parts
        f_open = open(fname)
        self.np = int(f_open.readline())
        f_open.close()
        # read in the rest
        data = numpy.loadtxt(fname,skiprows=1)
        if fname == "InitDist":
            i = 2
        else:
            i = 0
            self.mass      = data[:,0-i]
            self.charge    = data[:,1-i]
        self.s         = data[:,2-i]
        self.th        = data[:,3-i]
        self.ph        = data[:,4-i]
        self.lam       = data[:,5-i]
        self.E         = data[:,6-i]
        self.w         = data[:,7-i]
        if equilibrium_type == "spec":
            self.lvol  = data[:,8-i]

    def Read_Particle_h5(self,equilibrium_type,fname):
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
        # Generated distribution or final data
        try:
            self.Ptor = numpy.array(f_open["Ptor"])
            self.muOqp = numpy.array(f_open["muOqp"])
        except:
            warnings.warn('Not a generated distribution')
    
    def read_tauparticle(self,fdir):
        # TODO: what does this file look like???
        f_turn = os.path.join(fdir,"TauParticle")
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
    
    def read_EcrossB(self,fdir):
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
    
    def read_fusionalpha(self,fdir):
        # TODO: what is the point of this???
        f_alpha = os.path.join(fdir,"fusion_alpha.out")
        if os.path.exists(f_alpha):
            # alphaprob = numpy.loadtxt(f_alpha)
            self.wc = self.w
            # TODO: two lines missing from matlab code (also commented out there)
    
    # TODO: Must be a better way of doing this
    # tmp = plt.hist(self.rhotor,weights=self.w)
    # dN = tmp.bins
    # dV = 2*numpy.pi*equilib.r0 * 2*numpy.pi*equilib.a**2 * tmp.dx
    # rhoj = tmp.x
    # n0 = dN/dV

    def rhotor(self):
        return numpy.sqrt(self.s)

    def v(self):
        return numpy.sqrt(2*self.charge*self.E/self.mass)

    def vpar(self):
        return self.v()*self.lam
    
    def vperp(self):
        return self.v()*numpy.sqrt(1-self.lam**2)
    
    def x(self):
        return self.R*numpy.cos(self.ph)
    
    def y(self):
        return self.R*numpy.sin(self.ph)
    
    def z(self):
        return self.Z
    
    def dN(self):
        pass

    def dV(self):
        pass
        # TODO: this uses R_0 and a from the equilib class
        # (2*numpy.pi*r0) * (a**2 * 2*numpy.pi * )
    
    def rhoj(self):
        pass

    def n0(self):
        pass
        # return self.dN/self.dV