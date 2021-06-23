

import os
import h5py



class moment():
    def __init__(self):
        pass

    def Get_MomentData(self,LEVIS):
        fname = os.path.join(LEVIS.dirrun,"Moments.h5")
        
        try: 
            f_open = open(fname,'r')
        except:
            raise FileNotFoundError('No Moments.h5 file found in {}'.format(LEVIS.dirrun))



class trapped():
    def __init__(self):
        pass





