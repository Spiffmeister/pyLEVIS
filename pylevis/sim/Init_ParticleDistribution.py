# Use for initialising particles

# from re import M
import numpy
import warnings
import h5py
import os



def create_particle_distribution(npart,R,pol,tor,vpar,E,M,C,weight,volmax=1000):
    '''
    Create a distribution of n particles
    R, E, vpar and vol are lists of [Rmin,Rmax] for example
    '''
    npartchk(npart)
    parts = numpy.zeros([npart, 9])
    for i in range(npart):
        parts[i,:] = createpart(R,pol,tor,vpar,E,M,C,weight,volmax=volmax)
    
    return parts


def write_distribution(loc,dist,type='dat'):
    '''
    Writes the distribution file to the location given
    '''
    npart = dist.numpy.shape[0]
    if type not in ['dat','h5']:
        type = 'dat'
        warnings.warn('Type not recognised, outputting .dat file.')
    # Write files
    fname = os.path.join(loc,'single.part.'+type)
    if type == 'h5':
        create_particle_h5(fname,npart,dist)
    else:
        create_particle_dat(fname,npart,dist)



'''
INTERNAL FUNCTIONS
'''
# PARTICLE CREATION
def createpart(R,pol,tor,vpar,E,Mrat,Crat,weight,volmax=0):
    '''
    Create a single particle
    '''
    # radial position
    r = numpy.random.uniform(low=R[0],high=R[1]*volmax)
    s = r%2 #Ensure the particle is within the computational volume
    # L_vol -- for SPEC equilibria
    if volmax > 0:
        for i in range(volmax):
            if r/(i+1)<2:
                lvol = i+1
    # v_parallel/v
    pol = numpy.random.uniform(low=pol[0],high=pol[1])
    tor = numpy.random.uniform(low=tor[0],high=tor[1])
    vpar = numpy.random.uniform(low=vpar[0],high=vpar[1])
    # Energy (eV)
    E = numpy.random.uniform(low=E[0],high=E[1])
    M = numpy.random.uniform(low=Mrat[0],high=Mrat[1])
    C = numpy.random.uniform(low=Crat[0],high=Crat[1])
    
    # mass ratio to proton | charge ratio to proton | radial position | poloidal angle | toroidal angle | v_parallel/v | energy [eV] | statistical weight | lvol
    if volmax > 0:
        return numpy.array([M,C,s,pol,tor,vpar,E,weight,lvol])
    else:
        return numpy.array([M,C,s,pol,tor,vpar,E,weight])



# CHECK NPARTS VS NCPUS
def npartchk(npart,machine):
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

def create_particle_dat(fname,npart,parts):
    '''
    Create a .dat file for particle distribution, serial read by LEVIS only
    '''
    # Write the distribution
    format = "%f    %f  %f  %f  %f  %f  %f  %f  %i"
    numpy.savetxt(fname,parts,fmt=format)
    # Append the number of particles to the start of the file
    with open(fname,'r') as read_f, open(fname+"bak",'w') as write_f:
        write_f.write(str(npart)+'\n')
        for line in read_f:
            write_f.write(line)
    # Remove trash
    os.remove(fname)
    os.rename(fname+"bak",fname)




