from .Mercury import simulation
from .newsimulation.Init_Simulation import new_simulation
# from . import visualisation as vis
# from . import reading


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
