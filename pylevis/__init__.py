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

    Directory settings for pylevis. Set using pylevis.pylevis_settings.set_levis_directory("/path/to/levis")
    """
    def __init__(self):
        self.update()
    
    def update(self):
        """
        update(self)
        
        Update the directory settings (use new settings)
        """
        import configparser
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.levis_directory = config.get('Paths','levis_directory')
        self.runs_directory = config.get('Paths','runs_directory')

    def set_levis_directory(self,dir):
        """
        set_levis_directory(dir)
        
        Set 'dir' as the location of VENUS-LEVIS - writes config and updates setting
        """
        self.levis_directory = dir
        import configparser
        import os
        config = configparser.ConfigParser()
        config.read('settings.ini')
        config.set('Paths','levis_directory',dir)
        if self.runs_directory == '': #If the runs directory is unset, try and set it now
            runsdir = os.path.join(os.pathself.levis_directory,'runs')
            if os.path.exists(runsdir):
                config.set('Paths','runs_directory',runsdir)
        with open('settings.ini','w') as configfile:
            config.write(configfile)

    def set_runs_directory(self,dir):
        """
        set_runs_directory(dir)

        Set 'dir' as the location of the outputs from VENUS-LEVIS - writes config and updates setting
        """
        self.runs_directory = dir
        config = configparser.ConfigParser()
        config.read('settings.ini')
        config.set('Paths','runs_directory',dir)
        with open('settings.ini','w') as configfile:
            config.write(configfile)


pylevis_settings = __pylevis_settings()
