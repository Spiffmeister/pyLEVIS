

import os
import h5py
import numpy
from ..particles.ext_fns import _ext_rhotor
from ..constants import charge


class moment:
    """
    moment(self,fname,ndiagnostic=-1)

    Input
    ----------
    fname: the path/name of the moments file
    ndiagnostic: number of diagnostics, needed if not a h5 file

    Output
    ----------
    Moment class with
    """
    def __init__(self,fpath,vol):

        fname = os.path.join(fpath,'Moments.h5')

        if os.path.exists(fname):
            f_open = h5py.File(fname)

            self.nrad = f_open['radial_dim'][0]
            self.t = f_open['time'][0]
            self.curr_onion = f_open['flux_averages/curr_onion']*charge
            self.hist_onion = f_open['flux_averages/hist_onion']
            self.erg_onion = f_open['flux_averages/erg_onion']*charge

            self.trapped = trapped()
            self.trapped.nrad = self.nrad
            self.trapped.curr_onion = f_open['trapped/curr_onion']*charge
            self.trapped.hist_onion = f_open['trapped/hist_onion']
            self.trapped.erg_onion = f_open['trapped/erg_onion']*charge

            f_open.close()
            
        else:
            f_open = open(fname)
            
            self.nrad = float(f_open.readline())

            for j in range(self.params.ndiagnostic):
                self.curr_onion[:,j] = float(f_open.readline(self.nrad))
                self.hist_onion[:,j] = float(f_open.readline(self.nrad))
                self.erg_onion[:,j]  = float(f_open.readline(self.nrad))
            
            f_open.close()

            time = numpy.linspace(0,self.params.tfin,self.params.ndiagnostic+1)
            self.t = time[1:]


            fname = os.path.join(fpath,'Moments_trapped')
            if os.path.exists(fname):
                self.trapped = trapped()
                f_open = open(fname)
                self.trapped.nrad = float(f_open.readline())
                for i in range(1,self.params.ndiagnostic):
                    self.trapped.curr_onion[:,i]    = float(f_open.readline(self.nrad))
                    self.trapped.hist_onion[:,i]    = float(f_open.readline(self.nrad))
                    self.trapped.erg_onion[:,i]     = float(f_open.readline(self.nrad))
           

        s = numpy.linspace(0,1,self.nrad+1)
        self.s = s[:-1] + numpy.diff(s)/2

        onion_vol = numpy.repeat(vol.dV,[1,numpy.size(self.hist_onion)[1]])
        
        self.ntot = sum(self.hist_onion)
        self.jtot = sum(self.curr_onion/(2*numpy.pi))
        self.ptot = sum(self.erg_onion)

        self.dens  = self.hist_onion/onion_vol
        self.press = self.erg_onion/onion_vol
        self.curr  = self.curr_onion/onion_vol
        self.idens = numpy.cumsum(self.hist_onion,1)
        self.ierg  = numpy.cumsum(self.erg_onion,1)
        self.icurr = numpy.cumsum(self.curr_onion/(2*numpy.pi),1)
        self.navg = numpy.mean(self.dens[:,numpy.floor(len(self.dens)/2):],2)
        self.javg = numpy.mean(self.curr[:,numpy.floor(len(self.curr)/2):],2)
        self.pavg = numpy.mean(self.press[:,numpy.floor(len(self.press)/2):],2)
        self.Navg = numpy.mean(self.idens[:,numpy.floor(len(self.idens)/2):],2)
        self.Iavg = numpy.mean(self.icurr[:,numpy.floor(len(self.icurr)/2):],2)
        self.Eavg = numpy.mean(self.ierg[:,numpy.floor(len(self.ierg)/2):],2)

        rhotor = _ext_rhotor



class trapped():
    def __init__(self):
        self.nrad = 0
        self.curr_onion = 0
        self.hist_onion = 0
        self.erg_onion = 0

