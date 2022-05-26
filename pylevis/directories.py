# import os
import os
import pylevis
import warnings

'''
EXTERNAL METHODS - BOUND TO LEVIS CLASS
'''

def Set_Directories(simulation):

    pwd = os.getcwd()

    if "prob" in pwd:
        simulation.dirrun = pwd
    elif os.path.exists(os.path.join(pwd,"prob"+simulation.runid)):
        simulation.dirrun = os.path.join(pwd,"prob"+simulation.runid)
    elif os.path.exists(os.path.join(pwd,simulation.runid)):
        simulation.dirrun = os.path.join(pwd,simulation.runid)
    else:
        raise Exception("simulation not found check runid")

    simulation.dirdiag = os.path.join(simulation.dirrun,"Diag")
    if not os.path.exists(simulation.dirdiag):
        warnings.warn("no /Diag folder found, no VENUS-LEVIS outputs present in run directory")
    

