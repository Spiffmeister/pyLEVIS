'''
Plotting anything to do with moments
'''

from .support import *


# Public functions
__all__ = ['plot_energy_density']


'''
PLOTTING FNS
'''

def plot_energy_density(LEVIS,scale=False):
    ped = plt.figure()

    rhotor = LEVIS.moments.rhotor
    plt.plot(rhotor,LEVIS.energy.hot_tail,label=r'W_{fast}')
    plt.plot(rhotor,LEVIS.energy.thermal,label=r'W_{thermal}')
    plt.plot(rhotor,LEVIS.energy.thermal+LEVIS.energy.hot_tail,label=r'W_{total}')
    
    plt.legend()
    plt.grid
    plt.xlabel(r'\rho~r/a')
    plt.ylabel(r'Energy density $J/m^3$')

    return ped


