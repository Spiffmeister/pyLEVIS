'''
Class for initalising the data file. All defaults set here
'''

import os
import re



class data():
    """
    Data file class for VENUS-LEVIS simulations, calling data() will inialise a default data config.
    
    Internal methods:
    default_dicts(), write(), read(), fill_data()
    """
    def __init__(self,npart=4):
        self.simulation, self.collisions, self.equilibrium, self.diagnostics, self.postprocessing = self.__default_dicts()

        self.simulation["nparts"] = npart

    def __default_dicts(self):
        headers = ['simulation','collisions','equilibrium','diagnostics','postprocessing']
        simulation     = {"simulation_duration":int(42069),\
            "tfin":float(1.0e-5),\
            "nparts":int(4),\
            "ninjection":int(1),\
            "fixed_timestep":float(-1),\
            "generate_distribution":bool(0),\
            "cartesian_surface":bool(0)}
        collisions     = {"orbit":bool(1),\
            "variation_threshold":[float(0.0),float(0.0)],\
            "coulomb":bool(0),\
            "cx":bool(0),\
            "fusion":bool(0),\
            "nturns":bool(0),\
            "icrh":bool(0),\
            "rotation":bool(0),\
            "nbi":bool(0),\
            "alphas":bool(0),\
            "Ethreshold":float(2.0),\
            "anomalous":bool(0)}
        equilibrium    = {"animec":bool(1),\
            "backup_equilibrium":bool(0),\
            "recover_equilibrium":bool(0),
            "force_axisymmetry":bool(0),\
            "externalfield":bool(0)}
        diagnostics    = {"ndiagnostics":int(2),\
            "dump_fields":int(5),\
            "dump_particles":int(2),\
            "bounce_tip_recording":bool(0)}
        postprocessing = {"dump_fullf":bool(1),\
            "dump_neutron_camera":bool(1)}
        return simulation, collisions, equilibrium, diagnostics, postprocessing


    def optional_params(self):
        pass

    def __typecheck(self,var,vartype):
        # When writing we need to check the type of each variable is correct
        if type(var) != type(vartype):
            return type(vartype)(var)
        else:
            return var
    
    def properties(self):
        for key in list(self.__dict__.keys()):
            print(key)
            for subkey in getattr(self,key).items():
                print(subkey)
    
    def write(self,simpath):
        '''
        Writes a data file
        '''
        tmp_sim, tmp_col, tmp_equ, tmp_diag, tmp_post = self.__default_dicts()

        fname = os.path.join(simpath,"data")
        f = open(fname,'w')
        f.write("&simulation\n")
        # for key, val in self.simulation.__dict__.items():
        for key,val in self.simulation.items():
            if type(val) != bool:
                f.write(key+"="+str(val)+"\n")
            else:
                f.write(key+"="+str(int(val))+"\n")
        f.write("/\n")
        
        f.write("&collisions\n")
        for key, val in self.collisions.items():
            if type(val) != list:
                if type(val) != bool:
                    f.write(key+"="+str(val)+"\n")
                else:
                    f.write(key+"="+str(int(val))+"\n")
            else:
                f.write(key+"="+str(val[0])+","+str(val[1])+"\n")
        f.write("/\n")

        f.write("&equilibrium\n")
        for key, val in self.equilibrium.items():
            if type(val) != bool:
                f.write(key+"="+str(val)+"\n")
            else:
                f.write(key+"="+str(int(val))+"\n")
        f.write("/\n")

        f.write("&diagnostics\n")
        for key, val in self.diagnostics.items():
            if type(val) != bool:
                f.write(key+"="+str(val)+"\n")
            else:
                if val:
                    f.write(key+"=.TRUE.\n")
                else:
                    f.write(key+"=.FALSE.\n")
        f.write("/\n")

        f.write("&postprocessing\n")
        for key, val in self.postprocessing.items():
            if type(val) != bool:
                f.write(key+"="+str(val)+"\n")
            else:
                f.write(key+"="+str(int(val))+"\n")
        f.write("/\n")
        f.close()
        print("Data file written")
    

    def read(self,simpath):
        '''
        Reads a data file
        '''
        # keys_data_float = ["tfin","dump_fullf","dump_distribution","dump_neutron_camera","Ethreshold","fixed_timestep","ninjection","anomalous","transport_model"]
        # keys_data_int = ["ndiagnostic","nparts","dump_particles"]
        keylist = ['simulation','collisions','equilibrium','diagnostics','postprocessing']
        headerlist = ['&'+key for key in keylist]

        # Generate a list of all available fields
        headerkey = dict()
        for key in keylist:
            headerkey[key] = list(getattr(self,key).__dict__.keys())

        # Read in a data file
        fname = os.path.join(simpath,"data")
        f_open = open(fname,'r')
        # This is a really disgusting way of doing this and I am ashamed
        for line in f_open: #loop over lines
            for header in headerlist: #check if header found
                if header in line:
                    attr = getattr(self,header[1:]).__dict__.keys()
                    for subline in f_open: #push inner lines forward
                        for key in attr:
                            if key in subline: #if key found
                                add = re.split("=|!",subline)
                                add = add[1]
                                addstring = 'self.'+header+'['+key+']='+add
                                exec(addstring)
                            else: #delete the key otherwise
                                remstring = 'self.'+header+'['+key+']=nan'
                                exec(remstring)
        f_open.close()


    # Remove unfilled fields

    def fill_data():
        '''
        If required data is missing, fill it
        '''
        pass

