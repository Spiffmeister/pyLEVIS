from .LEVISClass import simulation

from .sim.Init_Simulation import new_simulation

from . import visualisation as vis

# from .auxil.Init_ParticleDistribution import 

# import pyLEVIS.


'''
    Some global setup stuff
'''
global pylevis_settings
class __pylevis_settings():
    def __init__(self,dir=""):
        self.levis_directory = dir

pylevis_settings = __pylevis_settings()
