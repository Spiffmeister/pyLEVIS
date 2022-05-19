# Use for initialising particles

# from re import M
import numpy
import warnings
import h5py
import os



def create_particle_distribution(npart,s,pol,tor,vpar,E,mass_ratio=1,charge_ratio=1,weight=1,vol=[0]):
    '''
    Create a distribution of n particles
    R, E, vpar and vol are lists of [Rmin,Rmax] for example
    Optional arguments: M, C, weight, volmax
    '''
    def gen(param):
        if type(param) in [int,float]:
            return param
        else:
            return numpy.random.uniform(low=param[0],high=param[1],size=npart)
    
    npartchk(npart)

    if (vol[0] == 0) and (len(vol) == 1):
        parts = numpy.zeros([npart, 8])
    else:
        parts = numpy.zeros([npart, 9])
    
    # mass ratio to proton
    parts[:,0] = gen(mass_ratio)
    # charge ratio to proton
    parts[:,1] = gen(charge_ratio)
    # Radial position
    parts[:,2] = gen(s) # s assignment
    # Poloidal angle
    parts[:,3] = gen(pol)
    # Toroidal angle
    parts[:,4] = gen(tor)
    # v_parallel/v
    parts[:,5] = gen(vpar)
    # Energy [eV]
    parts[:,6] = gen(E)
    # Statistical weight
    parts[:,7] = gen(weight)
    # Volumes if 
    if len(vol) > 1:
        parts[:,8] = numpy.random.randint(low=vol[0],high=vol[-1],size=npart)
    elif (len(vol) == 1) and (vol[0] != 0):
        parts[:,8] = vol[0]
    
    return parts


def write_distribution(fpath,dist,filetype='dat'):
    '''
    Writes the distribution file to the location given
    '''
    print(fpath)
    print(dist)
    npart = dist.shape[0]
    if filetype not in ['dat','h5']:
        filetype = 'dat'
        warnings.warn('Type not recognised, outputting .dat file.')
    # Write files
    fname = os.path.join(fpath,'single.particle.'+filetype)
    if filetype == 'h5':
        create_particle_h5(fname,npart,dist)
    else:
        create_particle_dat(fname,npart,dist)



'''
INTERNAL FUNCTIONS
'''

# CHECK NPARTS VS NCPUS
def npartchk(npart,machine='local'):
    '''
    Helper function for checking how many cpus can be called (or should be)
    '''
    if "gadi" in machine:
        node = 48
        if npart >= node:
            if (npart%48 != 0):
                npart = round(npart/48) * 48
                warnings.warn("Gadi can only use nproc multiples of 48 for npart>=48, closest nproc is {}".format(npart))
        if npart < node:
            divisors = [x for x in range(1,npart) if npart%x==0]
            print('Generating ',npart,' particles, for less than 1 node, possible nprocs: ',divisors)
        


# FILE CREATING INTERNALS
def create_particle_h5(fname,npart,parts,eqtype='spec'):
    '''
    Create a hdf5 file for particle distribution, parallel read by LEVIS possible
    '''
    hf = h5py.File(fname,'w')
    dset = hf.create_dataset('nparts', data=npart, dtype='i')
    dset = hf.create_dataset('mass',   data=parts[:,0])
    dset = hf.create_dataset('charge', data=parts[:,1])
    dset = hf.create_dataset('u1',     data=parts[:,2])
    dset = hf.create_dataset('u2',     data=parts[:,3])
    dset = hf.create_dataset('u3',     data=parts[:,4])
    dset = hf.create_dataset('lambda', data=parts[:,5])
    dset = hf.create_dataset('energy', data=parts[:,6])
    dset = hf.create_dataset('weight', data=parts[:,7])
    if eqtype == 'spec':
        dset = hf.create_dataset('lvol', data=parts[:,8])
    hf.close()

def create_particle_dat(fname,npart,parts,eqtype='spec'):
    '''
    Create a .dat file for particle distribution, serial read by LEVIS only
    '''
    # Write the distribution
    if eqtype == 'spec':
        format = "%f    %f  %f  %f  %f  %f  %f  %f  %i"
    else:
        format = "%f    %f  %f  %f  %f  %f  %f  %f"
    numpy.savetxt(fname,parts,fmt=format)
    # Append the number of particles to the start of the file
    with open(fname,'r') as read_f, open(fname+"bak",'w') as write_f:
        write_f.write(str(npart)+'\n')
        for line in read_f:
            write_f.write(line)
    # Remove trash
    os.remove(fname)
    os.rename(fname+"bak",fname)




