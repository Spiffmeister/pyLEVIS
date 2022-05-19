

import os
import h5py
import numpy



class moment():
    """
    moment(self)

    
    """
    def __init__(self):
        self.ntot = sum(self.hist_onion)
        self.jtot = sum(self.curr_onion/(2*numpy.pi))
        self.ptot = sum(self.erg_onion)

        self.nrad =  fscanf(fid,'%d',1)
        for j in range(self.par.ndiagnostic):
            self.mom.curr_onion[:,j] = fscanf(fid,'%f',nrad)
            self.mom.hist_onion[:,j] = fscanf(fid,'%f',nrad)
            self.mom.erg_onion[:,j]  = fscanf(fid,'%f',nrad)

        onion_vol = numpy.repmat(self.vol.dV[:],[1,numpy.size(self.hist_onion,2)])

        self.dens  = self.hist_onion/onion_vol
        self.press = self.erg_onion/onion_vol
        self.curr  = self.curr_onion/onion_vol
        self.idens = self.cumsum(self.hist_onion]
        self.ierg  = self.cumsum(self.erg_onion]
        self.icurr = self.cumsum(self.curr_onion/(2*numpy.pi),1]
        self.navg = numpy.mean[self.dens[:,numpy.floor(end/2):end],2]
        self.javg = numpy.mean[self.curr[:,numpy.floor(end/2):end],2]
        self.pavg = numpy.mean[self.press[:,numpy.floor(end/2):end],2]
        self.Navg = numpy.mean[self.idens[:,numpy.floor(end/2):end],2]
        self.Iavg = numpy.mean[self.icurr[:,numpy.floor(end/2):end],2]
        self.Eavg = numpy.mean[self.ierg[:,numpy.floor(end/2):end],2]
    




class trapped():
    def __init__(self):
        self.nrad = 0
        self.curr_onion = 0
        self.hist_onion = 0
        self.erg_onion = 0


def Get_MomentData(self,simulation):
    fname = os.path.join(simulation.dirrun,"Moments.h5")
    
    try: 
        f_open = open(fname,'r')
    except:
        raise FileNotFoundError('No Moments.h5 file found in {}'.format(simulation.dirrun))
    
