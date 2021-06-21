'''
ENERGY SUBCLASS
'''
import os
from numpy import array, loadtxt, diff, isnan
import h5py

class Energy():
    def __init__(self,dirname,lost_particle,charge):
        if os.path.exists(os.path.join(dirname,"Moments.h5")):
            f_data = h5py.File(os.path.join(dirname,"Moments.h5"),'r')
            self.read_h5(f_data,lost_particle,charge)

        elif os.path.exists(os.path.join(dirname,"Energy")):
            fname = os.path.join(dirname,"Energy")
            self.read_dat(fname)
    
    '''
    READING FNS
    '''
    def read_h5(self,f_data,lost_particle,charge):
        self.t      = array(f_data['time'])
        self.Etot   = array(f_data['Totals/E'])#TODO: *charge)
        self.Ntot   = array(f_data['Totals/w'])
        
        out = lost_particle.index > 0

        self.Elost  = sum(lost_particle.E(out) * lost_particle.w(out))
        self.Nlost  = sum(lost_particle.w(out))

    def read_dat(self,fname):
        f_data = loadtxt(fname)
        self.t      = f_data[:,0]
        self.Etot   = f_data[:,1]
        self.Ntot   = f_data[:,2]
        self.Elost  = f_data[:,3]
        self.Nlost  = f_data[:,4]

    def read_mino(self,LEVIS,fname):
        f_data = h5py.File(fname,'r')
        
        self.hot_energy     = f_data['flux_averages/hot_energy_dens']
        self.thermal_energy = f_data['flux_averages/thermal_energy_dens']

        

    
    '''
    INBUILT FNS -- avoid storage
    '''

    def dt(self):
        # Time steps
        return self.t[0] - self.t[1]
    
    def Emean(self):
        # Mean energy
        Em = self.Etot/self.Ntot
        Em[isnan(Em)] = 0
        return Em




'''
BINDING TO LEVIS
'''

def Get_Energy(self):
    # Read in the energy class
    fname = os.path.join(self.dirrun,"Moments.h5")
    try:
        return Energy(self.dirrun,self.lost_particle,self.sp.charge)

    except:
        return Energy(self.dirrun)


def Get_EnergyDensity(self):
    fname = os.path.join(self.dirrun,"Mino_Moments.h5")
    if os.path.exists(fname):
        pass
