'''
GET INITIAL SIMULATION PARAMETERS
'''

import os
import warnings
import re

def Get_SimulationParameters(simulation):
    """
    Get_SimulationParameters(simulation)

    GetPar in MATLAB routines.

    Returns
    ----------
    dictionary 'params' with initial simulation params
    """
    #Initialise parameters
    params = dict()

    # Add data parameters
    params.update(Get_data(simulation))
    # Is the simulation using lorentzian
    params.update(Get_Lorentzian(simulation))
    # Get the number of processors used
    params.update(Get_Parallel_Env(simulation))
    # Get the diffusivity parameters ## TODO
    params["anom"] = Get_Diffusivity_Params(simulation) #FIX: nested dicts are bad to access

    if simulation.scenic:
        params.update(Get_ScenicData(simulation))
   
    return params


'''
SUPPORT
'''
"""
class sim_data:
    def __init__(self,simulation):
        # Construct file name
        fname = os.path.join(simulation,dirrun,"data")
        # Possible keys in the parameter files
        # Keys for floats
        keys_data_float = ["tfin","dump_fullf","dump_distribution","dump_neutron_camera","Ethreshold","fixed_timestep","ninjection","anomalous","transport_model"]
        # Keys for ints
        keys_data_int = ["ndiagnostic","nparts","dump_particles"]
        
        # Try to open the data file
        if os.path.exists(fname):
            f_open = open(fname,'r')
            # Check the datafile for parameters and add to params
            for line in f_open:
                for key in keys_data_float:
                    if key in line:
                        add = re.split("=|!",line)
                        setattr(self,key,float(add))
                for key in keys_data_int:
                    if key in line:
                        add = re.split("=|!",line)
                        setattr(self,key,int(add[1]))
            f_open.close()
"""
        




def Get_data(simulation):
    """
    Get_data(simulation)

    Reads in the 'data' file in a LEVIS run

    Returns
    ----------
    Dictionary of inputs from run/<run ID>/data
    """
    # Construct file name
    filename = os.path.join(simulation.dirrun,"data")

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
        raise FileNotFoundError('No data file found in {}'.format(simulation.dirrun))
    
    return data


def Get_Lorentzian(simulation):
    """
    Get_Lorentzian(simulation)

    Returns
    ----------
    True or false if file runs/<run ID>/lorentz_orbits exist
    """
    filename = os.path.join(simulation.dirdiag,"lorentz_orbits")
    if os.path.exists(filename):
        return {"lorentzian":True}
    else:
        return {"lorentzian":False}


def Get_Parallel_Env(simulation):
    """
    Get_Parallel_Env(simulation)

    Returns
    ----------
    Get number of processors from runs/<run ID>/ParaEnv
    """
    filename = os.path.join(simulation.dirdiag,"ParaEnv")
    if os.path.exists(filename):
        with open(filename,'r') as f_open:
            return {"nprocs":int(f_open.readline())}
    else:
        warnings.warn("Number of processors unknown, statistics may be incorrect.")
        return {"nprocs":1}


def Get_Diffusivity_Params(simulation):
    """
    Get_Diffusivity_Params(simulation)

    Returns
    ----------
    Diffusivity parameters from file runs/<run ID>/diffusivity.parameters
    """
    filename = os.path.join(simulation.dirdiag,"diffusivity.parameters")
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



def Get_ScenicData(simulation):
    """
    Get_ScenicData(simulation)

    Returns
    ----------
    Dictionary containing data from <run ID>/scenic.in
    """
    fname = os.path.join(simulation.dirrun,"scenic.in")

    try:
        f_open = open(fname)
        keys_data_float = ["antenna_power","toroidal_mode","power_partition","icrh_nr","icrh_nz","icrh_nphi","splitting_factor","density_avg","coarse_grain_bin","charge_majority","mass_majority","Zeff","charge_ratio","mass_ratio"]

        data = dict()

        for line in f_open:
            for key in keys_data_float:
                if key in line:
                    add = re.split("=|!",line)
                    data[key] = float(add[1])
        f_open.close()

    except:
        raise FileNotFoundError('No scenic.in file found in {}'.format(simulation.dirrun))

    return data
