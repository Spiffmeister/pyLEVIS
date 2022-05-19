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
    """
    simulation(runid,light_version=False,simcomplete=True,scenic=False)

    Class for loading completed VENUS-LEVIS simulations.

    Inputs
    ----------
    - runid: "NameOfRun" 
        String of name of LEVIS run (example "probSPEC.0")
    Optional Inputs
    ----------
    - light_version: True (default), False
    - simcomplete: True (default), False 
        Was the simulation completed or aborted?
    - scenic: True, False (default)

    Returns
    ----------
    simulation class with contents:
        simcomplete, light_version, scenic, runid, equilibrium_type, params, init
        params: initial simulation parameters

    Internal/Bound Functions
    ----------
    GetParticle() - loads particle output data from LEVIS simulation
    GetVolume()
    GetCollisions()

    plot_spconservation() - plots the conservation of energy and momentum and a 2D projection of orbits

    """
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
        # self.magnetic = BackupEquilibrium(self) #DecryptEquilibrium in matlab

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





