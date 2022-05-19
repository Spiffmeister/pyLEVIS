
__version__ = "0.2"


from .LEVISClass import simulation
from .sim.Init_Simulation import new_simulation
from . import visualisation as vis


"""
    Global settings
"""
global pylevis_settings
class __pylevis_settings():
    """
        __pylevis_settings(dir="")

    Directory settings for pylevis. Set using pylevis.pylevis_settings.levis_directory = "/path/to/levis"
    """
    def __init__(self,dir=""):
        self.levis_directory = dir

pylevis_settings = __pylevis_settings()
