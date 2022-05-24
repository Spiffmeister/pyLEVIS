

import os
import h5py
import numpy



class moment():
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
    def __init__(self,fname,par=-1):
        charge = 1.0

        if '.h5' in fname:
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

            for j in range(par.ndiagnostic):
                self.curr_onion[:,j] = float(f_open.readline(self.nrad))
                self.hist_onion[:,j] = float(f_open.readline(self.nrad))
                self.erg_onion[:,j]  = float(f_open.readline(self.nrad))
            
            f_open.close()

            time = numpy.linspace(0,par.tfin)

            self.ntot = sum(self.hist_onion)
            self.jtot = sum(self.curr_onion/(2*numpy.pi))
            self.ptot = sum(self.erg_onion)


            onion_vol = numpy.repmat(self.vol.dV[:],[1,numpy.size(self.hist_onion,2)])

            self.dens  = self.hist_onion/onion_vol
            self.press = self.erg_onion/onion_vol
            self.curr  = self.curr_onion/onion_vol
            self.idens = self.cumsum(self.hist_onion)
            self.ierg  = self.cumsum(self.erg_onion)
            self.icurr = self.cumsum(self.curr_onion/(2*numpy.pi),1)
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

    if os.path.exists(os.path.join(simulation.dirrun,"Moments.h5")):
        pass
    elif os.path.exists(os.path.join(simulation.dirrun,"Moments")):
        pass
    elif os.path.exists(os.path.join(simulation.dirrun,"current.out")):
        pass
    else:
        raise FileNotFoundError('No Moments file found in {}'.format(simulation.dirrun))
    
