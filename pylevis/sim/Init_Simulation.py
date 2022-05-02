# Used for initialising simulations

from matplotlib.style import available
import numpy
import os
import shutil
import warnings
import pylevis
import subprocess
from ..directories import Set_Directories
from .class_data import data
from .Init_ParticleDistribution import create_particle_distribution, write_distribution, npartchk


class new_simulation:
    '''
    Set up new simulation object. Inputs are:
    simname = name of simulation - will prefix with prob if not added by user
    nparts = number of particles in simulation
    eqfile = path/to/equilibrium/file
    Optional input:
    eqtype = type of equilibrium file, default "spec"
    machine = computer user is running simulation on, alters function of run_simulation()
        method, default is 'local'
    Internal methods:
    generate_particles(), create_simulation(), run_simulation()

    Simulation settings stored in simulation.data object
    '''
    
    def __init__(self,simname,nparts,eqfile,eqtype="spec",machine='local'):
        if "prob" not in simname:
            simname = "prob"+simname

        self.simname = simname
        self.levdir = pylevis.pylevis_settings.levis_directory
        self.simdir = os.path.join(self.levdir,"runs",self.simname)
        self.equilibrium_type = eqtype
        self.eqfile = eqfile

        self.levdir = pylevis.pylevis_settings.levis_directory

        self.nparts = nparts
        self.ncpus = 1

        self.data = data()
        self.data.simulation['nparts'] = self.nparts
        print("Default simulation config loaded, nparts set, check simulation.data.properties() to see settings")


        self.created = False
        self.machine = machine
        self.avail_machines = ['local']
        print("Config for new simulation created")
        print("Use simulation.create_simulation() to generate files")


    ### BINDING TO EXTERNAL FUNCTIONS ###
    def generate_particles(self,R,pol,tor,vpar,E,M=1,C=1,weight=1,volmax=1):
        '''
        radial position, poloidal angle, toroidal angle, v_parallel/v, energy [eV], mass ratio to proton, charge ratio to proton, statistical weight, number of volumes in equilibrium (spec only)
        '''
        self.particles = create_particle_distribution(self.nparts,R,pol,tor,vpar,E,M=M,C=C,weight=weight,volmax=volmax)
        avs = numpy.mean(self.particles[:,2])
        avp = numpy.mean(self.particles[:,3])
        avt = numpy.mean(self.particles[:,4])
        print("Particle distribution generated. Average [s,theta,zeta] position: [%3.5f,%3.5f,%3.5f]"%(avs,avp,avt))
    

    # machine_npartchk = npartchk
    # write_particles = write_distribution

    def machineconfiguration(self):
        if self.machine == 'gadi':
            self.machine_config = {"ncpus":1,\
            "ngpus":0,\
            "mem":"4GB",\
            "jobfs":"4GB",\
            "queue":"normal",\
            "project":"y08",\
            "walltime":"02:00:00",\
            "storage":"gdata/y08+scratch/y08",\
            "enter_job_directory":"wd",\
            "email":"",
            "alerts":"bea",\
            "jobname":"LEVIS"}



    def create_simulation(self,ftype='dat',overwrite=False):
        '''
        Creates files required to run simulation. Optional inputs:
        filetype = 'dat' or 'h5' - particle file
        overwrite = True or False - if the folder exists, overwrite it
        '''
        # Create directory for simulation
        if not os.path.exists(self.simdir):
            os.mkdir(self.simdir)
        elif os.path.exists(self.simdir) and overwrite:
            shutil.rmtree(self.simdir)
            os.mkdir(self.simdir)
        else:
            raise Exception('Path already exists use overwrite flag')

        # Grab equilibrium file
        if not os.path.exists(self.eqfile):
            raise
        simeq = os.path.join(self.simdir,"eq.spec.h5")
        shutil.copy2(self.eqfile,simeq)


        # Get the LEVIS program and postprocessing program
        bindir = os.path.join(self.levdir,"bin")
        shutil.copy2(os.path.join(bindir,"mercury.x"),self.simdir)
        shutil.copy2(os.path.join(bindir,"postprocessing.x"),self.simdir)

        # Check to make sure nparts is the same across configs
        if self.particles.shape[0] != self.nparts:
            warnings.warn('Number of particles not the same as nparts, updating nparts to match number of generated particles')
            self.nparts = self.particles.shape[0]
        
        if self.data.simulation["nparts"] != self.nparts:
            warnings.warn('Number of particles in config not the same as number generated, updating config')
            self.data.simulation["nparts"] = self.nparts

        # Create data file
        self.data.write(self.simdir)

        # Create particle distribution file
        try:
            if (self.nparts > 1000) & ('dat' in ftype):
                warnings.warn('Large number of particles, recommend creating h5 file for parallel reading')
            write_distribution(self.simdir,self.particles)
            self.created = True
            # raise Exception("In-built LEVIS generator not finished yet")
        except NameError:
            raise Exception("Particles have not been generated, call new_simulation.generate_particles()")
        print('Simulation data written')



    # create simulation setting/readme file
    # def create_readme(self):
        # pass

    def run_simulation(self,mode="active"):
        if not self.created:
            raise Exception('Simulation files not yet created, run simulation.create_simulation() first')
        if self.machine == "local":
            #execute ./mercury.x < data and echo output
            os.chdir(self.simdir)
            subprocess.run("./mercury.x < data",shell=True)
            # print("Running simulation")
            




def copy_simulation(LEVIS):
    '''
    Creates a new simulation from an existing one
    '''
    runname = LEVIS.rundir+".copy"
    tmpsim = new_simulation(runname,LEVIS.params["nparts"],eqtype=LEVIS.equilibrium_type)
    return tmpsim




def create_machine(machine):
    if machine == "gadi":
        config = {"ncpus":1,\
            "mem":"4GB",\
            "jobfs":"4GB",\
            "queue":"normal",\
            "project":"y08",\
            "walltime":"02:00:00",\
            "storage":"gdata/y08+scratch/y08",\
            "enter_job_directory":"wd",\
            "email":"",
            "alerts":"bea",\
            "jobname":"LEVIS"}
    return config


def write_machine(SIM):
    if SIM.machine == "gadi":
        flags = {"-l":["ncpus","mem","jobfs","walltime","enter_job_directory"],"-q":["normal"],"-P":["project"],"-m":["alerts"],"-M":["email"]}
        f_open = open(new_simulation.simdir,'w')
        f_open.write("#!/bin/bash")
        for key,val in SIM.machine_config:
            for subkey,subval in flags:
                if val in subval:
                    f_open.write("#PBS "+subkey+" "+key+" "+val)

