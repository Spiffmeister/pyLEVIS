# import os
import os

'''
EXTERNAL METHODS - BOUND TO LEVIS CLASS
'''

def Set_Directories(self):
    self.mercurydir = GetMercuryDir()

    if "prob" in self.runid:
        tmpid = self.runid
    else:
        tmpid = "prob"+self.runid

    runpath = os.path.join(self.mercurydir,"runs",tmpid)
    self.dirrun = runpath
    self.dirdiag = os.path.join(self.dirrun,"Diag")
    

'''
INTERNAL METHODS
'''

def GetMercuryDir():
    return os.getcwd()


