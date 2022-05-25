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
        simulation.dirlevis = Getdirlevis()
        warnings.warn("pylevis.pylevis_settings.levis_directory set temporarily, use pylevis_settings.set_levis_directory to set permanently")
    else:
        simulation.dirlevis = pylevis.pylevis_settings.levis_directory
    
    if pylevis.pylevis_settings.runs_directory == "":
        simulation.dirrun = os.path.join(simulation.dirlevis,'runs')
        warnings.warn("pylevis_settings.runs_directory set temporarily, use pylevis_settings.set_runs_directory to set permanently")
    else:
        simulation.dirrun = pylevis.pylevis_settings.runs_directory
    
    def testpath(fpath):
        return os.path.join(simulation.dirrun,fpath)

    if os.path.exists(testpath("prob"+simulation.runid)):
        simulation.dirrun = testpath("prob"+simulation.runid)
    elif os.path.exists(testpath(simulation.runid)):
        simulation.dirrun = testpath(simulation.runid)
    else:
        raise Exception("simulation not found, check pylevis.pylevis_settings")

    simulation.dirdiag = os.path.join(simulation.dirrun,"Diag")
    if not os.path.exists(simulation.dirdiag):
        warnings.warn("no /Diag folder found, no VENUS-LEVIS outputs present in run directory")
    

'''
INTERNAL METHODS
'''

def Getdirlevis():
    return os.getcwd()


