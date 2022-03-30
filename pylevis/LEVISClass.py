import os
## BINDING EXTERNAL ROUTINES TO LEVIS CLASS
from .directories import Set_Directories

'''
BINDINGS FROM READING
'''
from .reading.Get_InitialParams import Get_SimulationParameters
from .reading.Get_ParticleData import BIND_Get_Particle
from .reading.Get_PlasmaVolume import BIND_Get_Volume
from .reading.Get_InitialParticleData import initial_particle_dist
from .reading.Get_Collisions import Get_Particle_Collisions
from .reading.Get_Scenic import Get_ScenicData
'''
BINDINGS FROM EQUILIBRIA
'''
from .equilibria.Get_BackupEquilibrium import BIND_Get_Backup_Equilibrium

from .visualisation import plots_single_particle

class simulation:
    '''
    Class for loading completed VENUS-LEVIS simulations. Inputs:
    - runid = "name of run"
    Optional Inputs:
    - light_version
    - simcomplete
    - scenic
    '''
    def __init__(self,runid,light_version=False,simcomplete=True,scenic=False):
        # Simulation properties
        self.simcomplete = simcomplete
        self.light_version = light_version
        self.scenic = scenic        #SHOULD BE REMOVED AND ONLY BE PRESENT AS DICT???
        self.runid = runid
        self.equilibrium_type = "spec" #TODO rewrite for auto-detection

        ''' Functions '''
        # Set directories
        self.SetDir()

        # Reading in initialised parameters
        self.params = Get_SimulationParameters(self) #Get.Params
        self.init = initial_particle_dist(self)

        # Get plasma properties
        # self.magnetic = backupequilibrium(self) #DecryptEquilibrium in matlab

        if self.scenic:
            self.scenicdata = Get_ScenicData(self)
        
        # self.GetBackgroundProfiles
        self.GetVolume()

        # self.GetLostParticles

        # if simcomplete:
        #     self.GetMoments
    

    ''' --- EXTERNAL BINDINGS --- '''
    GetParticle = BIND_Get_Particle ##TODO: ensure particles with no data do not interrupt other routines.
    SetDir = Set_Directories

    GetVolume = BIND_Get_Volume #Get_PlasmaVolume

    # Particle collision data
    GetCollisions = Get_Particle_Collisions

    def GetBackupEquilibrium(self):
        self.magnetic = BIND_Get_Backup_Equilibrium(self)


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





