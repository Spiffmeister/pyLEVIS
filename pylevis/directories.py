# import os
import os
import pylevis

'''
EXTERNAL METHODS - BOUND TO LEVIS CLASS
'''

def Set_Directories(self):
    if pylevis.pylevis_settings.levis_directory == "":
        self.levisdir = Getlevisdir()
    else:
        self.levisdir = pylevis.pylevis_settings.levis_directory

    if "prob" in self.runid:
        tmpid = self.runid
    else:
        tmpid = "prob"+self.runid

    runpath = os.path.join(self.levisdir,"runs",tmpid)
    self.dirrun = runpath
    self.dirdiag = os.path.join(self.dirrun,"Diag")
    

'''
INTERNAL METHODS
'''

def Getlevisdir():
    return os.getcwd()




