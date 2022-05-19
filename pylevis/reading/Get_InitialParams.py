'''
GET INITIAL SIMULATION PARAMETERS
'''

import os
import warnings
import re

def Get_SimulationParameters(self):
    """
    Get_SimulationParameters(self)

    GetPar in MATLAB routines.

    Returns
    ----------
    dictionary 'params' with initial simulation params
    """
    #Initialise parameters
    params = dict()

    # Add data parameters
    params.update(Get_data(self))
    # Is the simulation using lorentzian
    params.update(Get_Lorentzian(self))
    # Get the number of processors used
    params.update(Get_Parallel_Env(self))
    # Get the diffusivity parameters ## TODO
    params["anom"] = Get_Diffusivity_Params(self) #FIX: nested dicts are bad to access
   
    return params


'''
SUPPORT
'''
def Get_data(self):
    """
    Get_data(self)

    Reads in the 'data' file in a LEVIS run

    Returns
    ----------
    Dictionary of inputs from run/<run ID>/data
    """
    # Construct file name
    filename = os.path.join(self.dirrun,"data")

    # Possible keys in the parameter files
    # Keys for floats
    keys_data_float = ["tfin","dump_fullf","dump_distribution","dump_neutron_camera","Ethreshold","fixed_timestep","ninjection","anomalous","transport_model"]
    # Keys for ints
    keys_data_int = ["ndiagnostic","nparts","dump_particles"]
    data = dict()
    
    # Try to open the data file
    if os.path.exists(filename):
        f_open = open(filename,'r')
        # Check the datafile for parameters and add to params
        for line in f_open:
            for key in keys_data_float:
                if key in line:
                    add = re.split("=|!",line)
                    data[key] = float(add[1])
            for key in keys_data_int:
                if key in line:
                    add = re.split("=|!",line)
                    data[key] = int(add[1])
        f_open.close()
    else:
        raise FileNotFoundError('No data file found in {}'.format(self.dirrun))
    
    return data


def Get_Lorentzian(self):
    """
    Get_Lorentzian(self)

    Returns
    ----------
    True or false if file runs/<run ID>/lorentz_orbits exist
    """
    filename = os.path.join(self.dirdiag,"lorentz_orbits")
    if os.path.exists(filename):
        return {"lorentzian":True}
    else:
        return {"lorentzian":False}


def Get_Parallel_Env(self):
    """
    Get_Parallel_Env(self)

    Returns
    ----------
    Get number of processors from runs/<run ID>/ParaEnv
    """
    filename = os.path.join(self.dirdiag,"ParaEnv")
    if os.path.exists(filename):
        with open(filename,'r') as f_open:
            return {"nprocs":int(f_open.readline())}
    else:
        warnings.warn("Number of processors unknown, statistics may be incorrect.")
        return {"nprocs":1}


def Get_Diffusivity_Params(self):
    """
    Get_Diffusivity_Params(self)

    Returns
    ----------
    Diffusivity parameters from file runs/<run ID>/diffusivity.parameters
    """

    ''' Check diffusivity parameters '''
    filename = os.path.join(self.dirdiag,"diffusivity.parameters")
    data = dict()
    keys_data_float = ["D0es","x0","sigma_x"]

    if os.path.exists(filename):
        f_open = open(filename)
        for line in f_open:
            for key in keys_data_float:
                if key in line:
                    add = re.split("=|!",line)
                    data[key] = float(add[1])
    return data