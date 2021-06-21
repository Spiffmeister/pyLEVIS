'''
'''
import os
from numpy import squeeze, linspace, meshgrid, cos, sin
import h5py
import warnings




'''
BINDING TO LEVIS
'''
def Get_Backup_Equilibrium(self):
    fname = os.path.join(self.dirrun,"BackupEquilibrium.h5")

    if os.path.exists(fname):

        print("Processing backup equilibrium")
        # Read in backup eq file
        f_data = h5py.File('fname')
        # Get the dimensions
        f_grid  = [int(x) for x in f_data["grid/eq_dim"]] #Grid dimensions
        ns      = f_grid[1]
        nth     = f_grid[2]
        nph     = f_grid[3]
        # Try to interpret the equilibrium type
        try:
            eq_type = f_data["mag_type"]
        except:
            eq_type = "UNKNOWN"
        # Try to reconstruct
        try:
            # Form the grid and if it works do not generate
            s   = f_data["grid/s"]
            th  = f_data["grid/th"]
            ph  = f_data["grid/ph"]
            generate_grid = False
        except:
            warnings.warn("No grid found, generating grid")
            generate_grid = True
        
        # Generate the equilibrium data
        if eq_type in ["ANIMEC","VMEC","SATIRE","SPEC"]:
            # Read in the things we need
            tmpread     = f_data["data/half_scalar"]
            # TODO: is this right???
            B       = tmpread[:,:,:,0]
            jac     = tmpread[:,:,:,4]
            sigma   = tmpread[:,:,:,1]
            tau     = tmpread[:,:,:,2]
            # full scalar
            tmpread     = f_data["data/full_scalar"]
            R       = tmpread[:,:,:,0]
            Z       = tmpread[:,:,:,1]
            dRds    = tmpread[:,:,:,2]
            dRdu    = tmpread[:,:,:,3]
            dZds    = tmpread[:,:,:,4]
            dZdu    = tmpread[:,:,:,5]
            lam     = tmpread[:,:,:,6] #lambda
            dlds    = tmpread[:,:,:,7]
            dldu    = tmpread[:,:,:,8]
            dldv    = tmpread[:,:,:,9]
            # half vector
            tmpread     = f_data["data/half_vector"]
            grad_Bs = tmpread[:,:,:,0]
            grad_Bu = tmpread[:,:,:,1]
            grad_Bv = tmpread[:,:,:,2]
            Bu      = tmpread[:,:,:,3]
            Bv      = tmpread[:,:,:,4]
            Hs      = tmpread[:,:,:,5]
            Hu      = tmpread[:,:,:,6]
            Hv      = tmpread[:,:,:,7]
            Ks      = tmpread[:,:,:,8]
            Ku      = tmpread[:,:,:,9]
            Kv      = tmpread[:,:,:,10]
            Bx      = tmpread[:,:,:,11]
            By      = tmpread[:,:,:,12]
            Bz      = tmpread[:,:,:,13]
            Kx      = tmpread[:,:,:,14]
            Ky      = tmpread[:,:,:,15]
            Kz      = tmpread[:,:,:,16]
            # half flux
            tmpread     = f_data["data/half_flux"]
            Phip    = tmpread[:,1]
            Psip    = tmpread[:,2]
            Phi     = tmpread[:,3]
            Psi     = tmpread[:,4]
            
            phcorr  = 0. #What is this??

            Vrad        = f_data["data/Vrad"]

            if generate_grid:
                ds2     = 0.5/float(ns)
                s       = [0, linspace(ds2,1-ds2,num=float(ns)-1,endpoint=True)]
                th      = linspace(0,2*pi,num=nth+1,endpoint=True)[1:-1]
                ph      = linspace(0,2*pi,num=nth+1,endpoint=True)[1:-1]

    else:
        # If file not found
        raise FileNotFoundError('No backup equilibrium found.')
    
    # Construct grids
    rhotor  = sqrt(s)    
    thg, phg, sg    = meshgrid(th,ph,s,indexing="ij")

    x = R * cos(phg)
    y = R * sin(phg)

    # What is fillup??

