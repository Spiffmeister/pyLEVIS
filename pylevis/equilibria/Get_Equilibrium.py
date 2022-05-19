'''
Get Equilibrium
'''

class equilibrium:
    def __init__(self):
        equilibrium.raxis    =1.
        equilibrium.r0       =1.
        equilibrium.a        =0.1
        equilibrium.plasmaR  =1.1
        equilibrium.plasmaZ  =0.1
        
        

def GetEquilibrium(simulation):
    """
    GetEquilibrium(simulation)

    Returns
    ----------
    equilibrium class
    """
    # equilibrium = ReconstructEquilibrium() #Unfold equilibrium from matlab

    # How the equilibrium is read in depends on the actual equilibrium code
    if simulation.equilibrium_type == "spec":
        # TODO: defer to SPEC routines
        pass
    elif simulation.equilibrium_type == "terps":
        pass
    elif simulation.equilibrium_type == "animec":
        pass
    elif simulation.equilibrium_type == "satire":
        pass
    elif simulation.equilibrium_type == "terph5":
        pass
    elif simulation.equilibrium_type == "netcdf":
        pass

    if simulation.light_version:
        # TODO: what is light version???
        if equilibrium.dim > 2:
            # equilibrium = ReconstructEquilibrium(self.dirrun,true,false,32,32)
            pass
        else:
            # equilibrium = ReconstructEquilibrium(self.dirrun,true,false,256)
            pass
    else:
        # Failing finding the profiles
       pass
        
