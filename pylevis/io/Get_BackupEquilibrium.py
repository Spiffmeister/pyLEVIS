'''
'''
import os
import numpy
import h5py
import warnings



'''
simulation
'''

class BackupEquilibrium:
    """
    BackupEquilibrium(simulation)

    Inputs
    ----------
    simulation in LEVISClass

    Returns
    ----------
    BackupEquilibrium class with contents based on the equilibrium type
    """
    def __init__(self,simulation):
        fname = os.path.join(simulation.dirrun,"BackupEquilibrium.h5")
        
        if os.path.exists(fname):
            print("Processing backup equilibrium")
            # Read in backup eq file
            f_data = h5py.File(fname)
            # Get the dimensions
            f_grid  = [int(x) for x in f_data["grid/eq_dim"]] #Grid dimensions
            self.ns      = f_grid[0]
            self.nth     = f_grid[1]
            self.nph     = f_grid[2]
        
            # Try to interpret the equilibrium type
            try:
                self.eq_type = f_data["mag_type"]
            except:
                self.eq_type = "UNKNOWN"
            
            # Check if the equilibrium types match
            if self.eq_type != simulation.equilibrium_type:
                warnings.warn("Warning backup equilibrium type does not match simulation equilibrium type.")

            # Calling readin functions
            if self.eq_type in ["ANIMEC","VMEC","SATIRE","SPEC"]:
                self._read_vmec(f_data)
            elif self.eq_type == "SOLOVEV": #TODO
                pass
            elif self.eq_type == "MINERVA": #TODO
                pass
            elif self.eq_type == "DCON": #TODO
                pass
            elif self.eq_type == "UNKNOWN": #TODO
                    self._read_vmec(f_data)
                # try:
                #     pass
                # except:
                #     pass
        else:
            # If file not found
            raise FileNotFoundError('No backup equilibrium found.')
        

        
               

    def _read_vmec(self,f_data):
        # READ IN ANIMEC, VMEC, SATIRE AND SPEC EQUILIBRIA
        self._read_data_halfscalar(f_data["data/half_scalar"])
        self._read_data_fullscalar(f_data["data/full_scalar"])
        self._read_data_halfvector(f_data["data/half_vector"])
        self._read_data_halfflux(f_data["data/half_flux"])

        self.phcorr     = 0. #What is this??
        self.Vrad       = f_data["data/Vrad"]


    def _read_generic(self,f_data):
        pass

    '''
        READ IN DATA
    '''
    def _read_data_halfscalar(self,half_scalar):
        # TODO: is this right???
        self.B      = half_scalar[:,:,:,0]
        self.jac    = half_scalar[:,:,:,4]
        self.sigma  = half_scalar[:,:,:,1]
        self.tau    = half_scalar[:,:,:,2]
    
    def _read_data_fullscalar(self,full_scalar):
        # full scalar
        self.R      = full_scalar[:,:,:,0]
        self.Z      = full_scalar[:,:,:,1]
        self.dRds   = full_scalar[:,:,:,2]
        self.dRdu   = full_scalar[:,:,:,3]
        self.dZds   = full_scalar[:,:,:,4]
        self.dZdu   = full_scalar[:,:,:,5]
        self.lam    = full_scalar[:,:,:,6] #lambda
        self.dlds   = full_scalar[:,:,:,7]
        self.dldu   = full_scalar[:,:,:,8]
        self.dldv   = full_scalar[:,:,:,9]
    
    def _read_data_halfvector(self,half_vector):            
        # half vector
        self.grad_Bs= half_vector[:,:,:,0]
        self.grad_Bu= half_vector[:,:,:,1]
        self.grad_Bv= half_vector[:,:,:,2]
        self.Bu     = half_vector[:,:,:,3]
        self.Bv     = half_vector[:,:,:,4]
        self.Hs     = half_vector[:,:,:,5]
        self.Hu     = half_vector[:,:,:,6]
        self.Hv     = half_vector[:,:,:,7]
        self.Ks     = half_vector[:,:,:,8]
        self.Ku     = half_vector[:,:,:,9]
        self.Kv     = half_vector[:,:,:,10]
        self.Bx     = half_vector[:,:,:,11]
        self.By     = half_vector[:,:,:,12]
        self.Bz     = half_vector[:,:,:,13]
        self.Kx     = half_vector[:,:,:,14]
        self.Ky     = half_vector[:,:,:,15]
        self.Kz     = half_vector[:,:,:,16]

    def _read_data_halfflux(self,half_flux):
        # half flux
        self.Phip   = half_flux[:,1]
        self.Psip   = half_flux[:,2]
        self.Phi    = half_flux[:,3]
        self.Psi    = half_flux[:,4]


    '''
        GRIDS
    '''
    def Get_Grid(self,f_data):
        # Try to reconstruct
        try:
            # Form the grid and if it works do not generate
            self.s              = f_data["grid/s"]
            self.th             = f_data["grid/th"]
            self.ph             = f_data["grid/ph"]
            self.generate_grid  = False
        except:
            warnings.warn("No grid found, generating grid")
            self.generate_grid  = True


    def gen_grid(self):
        # Generate the grid
        ds2     = 0.5/float(self.ns)
        self.s  = [0, numpy.linspace(ds2,1-ds2,num=float(self.ns)-1,endpoint=True)]
        self.th = numpy.linspace(0,2*numpy.pi,num=self.nth+1,endpoint=True)[1:-1]
        self.ph = numpy.linspace(0,2*numpy.pi,num=self.nth+1,endpoint=True)[1:-1]


    def construct_grid(self):
        # Construct grids
        self.rhotor  = numpy.sqrt(self.s)
        thg, phg, sg    = numpy.meshgrid(self.th,self.ph,self.s,indexing="ij")

        x = self.R * numpy.cos(phg)
        y = self.R * numpy.sin(phg)

        # What is fillup??
    
        



'''
BINDING TO simulation
'''

def BIND_Get_Backup_Equilibrium(self):
    return BackupEquilibrium(self)
