import os
## BINDING EXTERNAL ROUTINES TO LEVIS CLASS
from .directories import Set_Directories

'''
BINDINGS FROM READING
'''
from .reading.Get_InitialParams import Get_SimulationParameters
from .reading.Get_ParticleData import Get_Particle
from .reading.Get_PlasmaVolume import Get_Volume
from .reading.Get_InitialData import initial_particle_dist
from .reading.Get_Collisions import Get_Particle_Collisions

from .visualisation import plots_single_particle

class simulation:
    def __init__(self,runid,light_version=False,simcomplete=True,scenic=False):
        # Simulation properties
        self.simcomplete = simcomplete
        self.light_version = light_version
        self.scenic = scenic
        self.runid = runid
        self.equilibrium_type = "spec"

        ''' Functions '''
        # Set directories
        self.SetDir()

        # Reading in initialised parameters
        self.params = Get_SimulationParameters(self) #Get.Params
        self.init = initial_particle_dist(self)

        # Get plasma properties
        # self.GetEquilibrium(self) #DecryptEquilibrium in matlab

        # if scenic:
        #     self.GetParScenic ##TODO
        
        # self.Get_BackgroundProfiles
        self.GetVolume()

        # self.GetLostParticles

        # if simcomplete:
        #     self.GetMoments
    

    ''' --- EXTERNAL BINDINGS --- '''
    GetParticle = Get_Particle ##TODO: ensure particles with no data do not interrupt other routines.
    SetDir = Set_Directories

    GetVolume = Get_Volume

    # Particle collision data
    GetCollisions = Get_Particle_Collisions



    '''
    Visualisation
    '''
    plot_spconservation = plots_single_particle.plot_spconservation


    '''
    INTERNAL ROUTINES
    '''
    def select_eqtype(self):
        # if 
        self.equilibrium_type = "spec"





