# import os
import os
import pylevis
import warnings

'''
EXTERNAL METHODS - BOUND TO LEVIS CLASS
'''

def Set_Directories(simulation):
    if pylevis.pylevis_settings.levis_directory == "":
        #If global settings not set attempt to use cwd
        simulation.levisdir = Getlevisdir()
        warnings.warn("pylevis.pylevis_settings.levis_directory set temporarily, check help(pylevis.pylevis_settings) to set directories permanently")
    else:
        simulation.levisdir = pylevis.pylevis_settings.levis_directory
    
    def testpath(fpath):
        return os.path.join(simulation.levisdir,fpath)

    if os.path.exists("prob"+simulation.runid):
        simulation.dirrun = testpath("prob"+simulation.runid)
    elif os.path.exists(simulation.runid):
        simulation.dirrun = testpath(simulation.runid)
    else:
        raise Exception("simulation not found, check pylevis.pylevis_settings")


    simulation.dirdiag = os.path.join(simulation.dirrun,"Diag")
    simulation.dirrun = dirrun
    

'''
INTERNAL METHODS
'''

def Getlevisdir():
    return os.getcwd()


