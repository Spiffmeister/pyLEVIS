import os
import warnings
from numpy import sqrt


'''
BG PROFILE CLASS
'''

class BGProfile():
    def __init__(self,fname):
        f_open = open(fname,'r')
        self.nspec          = int(f_open.readline()) #WHAT IS THIS??
        self.nrad           = f_open.readline()
        self.protons        = -1
        self.deuterium      = -1
        self.tritium        = -1
        
        self.s              = f_open.readline()
        self.rhotor         = sqrt(self.s)

        spec = dict.fromkeys("mass","charge",)
        for i in range(self.nspec):
            # Check the species
            pass
            spec["mass"][i]     = f_open.readline()
            spec["charge"][i]   = f_open.readline()
            spec["n"][i]        = f_open.readline()
            spec["T"][i]        = f_open.readline()





'''
INTERNAL METHODS
'''
def Get_Profiles(fname="",tokamak=[],shot=[]):
    
    if (fname=="") & (tokamak!=[]) & (shot!=[]):
        pass
        # fname = os.path.join(Getlevisdir) ##TODO -- NEEDS DIRECTORY LINKING
    elif (fname==""):
        pass
    
    f_open = open(fname,'r')
    f_open.close()






'''
EXTERNAL METHOD -- BINDING TO LEVIS
'''

def Get_BGProfile(self):
    
    # Check possible files
    fnamechk = ["BackgroundProfiles","profiles.in"]
    for chk in fnamechk:
        fname = os.path.join(self.dirrun,chk)
        if os.path.exists(fname):
            # If it exists go ahead for read
            fname = os.path.join(self.dirrun,chk)
            self.BGProfile = Get_Profiles(fname=fname)
            return
        else:
            chk = False
    
    if not chk:
        # If it failed to find the file return an error
        # raise FileNotFoundError("Specify a profiles.in file or VENUS-LEVIS compatible background profile file")
        warnings.warn("No input background profiles")
    



    