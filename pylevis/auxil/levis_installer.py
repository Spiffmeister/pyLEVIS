


import os
import subprocess
import warnings
import pylevis
import shutil



class levis_installer:
    def __init__(self):
        self.source = {"LEVIS":"",\
            "futils":"utils/futils",\
            "hdf5":"/apps/hdf5/1.10.5p",\
            "netcdf":"/apps/netcdf/4.6.3p"}
        self.eqtype = "SPEC"
        self.machine = "this_machine"
        if "SPEC" in eqtype:
            self.source["SPEC_field_reader"] = "utils/SPEC-field-reader"
        self.machine_settings()


    ''' VENUS-LEVIS MACHINE FILES '''
    def machine_settings(self,debugging=True):
        ### Set the compiler settings ###
        # Compiler settings
        self.compiler_settings = {"FC":"mpif90",\
            "PREPROC":["cpp","save-temps"],\
            "PREPROCSUFFIX":[".f90"],\
            "PROPROCPREFIX":[""]
            }
        # Compiler options
        self.compiler_options = {"DEBUGGING":[""],\
            "PROFILING":["p"],\
            "WARNINGS":["Wall","pedantic"],\
            "OPTIM":["O3"],\
            "PRECISION":["fdefault-real-8","ffree-line-length-none"],\
            "MODULES":["-J$(M)"]
        }
        if debugging:
            self.compiler_options["DEBUGGING"] = ["g","fbounds-check","fbacktrace","fcheck=all","fimplicit-none",\
            "ffpe-trap=invalid,zero,overflow","finit-real=nan","fstack-protector"]
    
    def get_machine(self,machine=""):
        ### Get the data in a machine file ###
        if machine == "":
            fname = os.path.join(pylevis.pylevis_settings.levis_directory,machine+".mk")
        else:
            fname = os.path.join(pylevis.pylevis_settings.levis_directory,self.machine+'.mk')
        f = open(fname,'r')
        f.close()

    def generate_machine(self):
        ### Write a compiler settings file for a computer ###
        fname = os.path.join(pylevis.pylevis_settings.levis_directory,"machines",self.machine+".mk")
        f = open(fname,"w")
        # Write compiler settings
        f.write("## compiler")
        f.write("FC = "+self.compiler_settings["FC"])
        f.write("PREPROC = -"+" -".join(self.compiler_settings))
        # Write compiler options
        f.write("## options")
        for key, val in self.compiler_options.items():
            f.write(key+"   = -"+' -'.join(val))
        # Write locations of external modules
        f.write("## external modules")
        for key, val in self.source.items():
            if val != "":
                f.write(key,"   = ",val)
        f.close()

    ''' COMPILATION METHODS FOR UTILITIES '''
    def compile_futils(self):
        ### Compile futils ###
        os.chdir(os.path.join(self.source["LEVIS"],self.source["futils"],"src"))
        shutil.copy2("Makefile.gadi","Makefile")
        subprocess.Popen(["make"])

    def compile_spec_reader(self):
        ### Compile the spec_field_reader ###
        os.chdir(os.path.join(self.source["LEVIS"],self.source["spec_field_reader"]))
        subprocess.Popen(["make"])

    def make(self,prog="all"):
        ### Compile VENUS-LEVIS and utilities ###
        if "MACHINE" not in os.environ:
            os.environ["MACHINE"] = self.machine
        else:
            # raise Exception("Environmental variable $MACHINE already set")
            pass
        
        if prog == "all":
            if self.eqtype == "SPEC":
                self.compile_spec_reader(self)
            self.compile_futils(self)

        make_command = "make MAG_EQ="+eqtype+" install"
        subprocess.Popen([make_command],shell=False)



def spec_field_reader_settings(self):
    self.SFR_settings = {"FFLAGS":"-fdefault-real-8",\
        "MACRO":"",\
        "HDF5compile":"/usr/include/hdf5/openmpi",\
        "HDF5link":["/usr/lib/x86_64-linux-gnu/hdf5/openmpi","lhdf5_hl","hdf5"]}