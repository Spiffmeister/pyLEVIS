# Used for initialising simulations

from matplotlib.style import available
import numpy
import os
import shutil
import warnings
import pylevis
from pylevis.Equilibria.Get_BackupEquilibrium import backupequilibrium
from Init_ParticleDistribution import create_particle_distribution, write_distribution, npartchk


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
        self.simdir = os.path.join(self.levdir,"runs",self.simname)
        self.equilibrium_type = "spec"
        self.eqfile = eqfile

        self.levdir = pylevis.pylevis_settings.levis_directory

        self.nparts = nparts
        self.ncpus = 1

        self.data = pylevis.data()
        self.data.simulation['nparts'] = self.nparts
        print("Default simulation config loaded, nparts set, check simulation.data.properties() to see settings")


        self.created = False
        self.avail_machines = ['local']
        print("Config for new simulation created")
        print("Use simulation.create_simulation() to generate files")


    ### BINDING TO EXTERNAL FUNCTIONS ###
    def generate_particles(self,R,pol,tor,vpar,E,M,C,weight,volmax=1000):
        self.particles = create_particle_distribution(self.npart,R,pol,tor,vpar,E,M,C,weight,volmax=volmax)
    

    machine_npartchk = npartchk
    write_particles = write_distribution



    def create_simulation(self,filetype='dat',overwrite=False):
        '''
        Creates files required to run simulation. Optional inputs:
        filetype = 'dat' or 'h5' - particle file
        overwrite = True or False - if the folder exists, overwrite it
        '''
        # Create directory for simulation
        if not os.path.exists(self.simdir):
            os.mkdir(self.simdir)
        elif os.path.exists(self.simdir) and not overwrite:
            os.rmdir(self.simdir)
        else:
            raise Exception('Path already exists use overwrite flag')

        # Grab equilibrium file
        simeq = os.path.join(self.simdir,"eq.spec.h5")
        shutil.copy2(self.eqfile,simeq)


        # Get the LEVIS program and postprocessing program
        bindir = os.path.join(self.levdir,"bin")
        shutil.copy2(os.path.join(bindir,"mercury.x"),self.simdir)
        shutil.copy2(os.path.join(bindir,"postprocessing.x"),self.simdir)

        # Create data file
        self.data.create(self.simname)
        # Create particle distribution file
        try:
            if (self.nparts > 1000) & ('dat' in filetype):
                warnings.warn('Large number of particles, recommend creating h5 file for parallel reading')
            self.write_particles(self.simdir,self.particles,filetype)
            self.created = True
            # raise Exception("In-built LEVIS generator not finished yet")
        except NameError:
            raise Exception("Particles have not been generated, call new_simulation.generate_particles()")
        else:
            raise Exception("Something went wrong")



    # create simulation setting/readme file
    # def create_readme(self):
        # pass

    def run_simulation(self):
        if not self.created:
            raise Exception('Simulation files not yet created, run simulation.create_simulation() first')
        if self.machine == "local":
            #execute ./mercury.x < data and echo output
            pass




def copy_simulation(LEVIS):
    '''
    Creates a new simulation from an existing one
    '''
    runname = LEVIS.rundir+".copy"
    tmpsim = new_simulation(runname,LEVIS.params["nparts"],eqtype=LEVIS.equilibrium_type)
    return tmpsim
