# Use for initialising particles

import numpy
import os
import h5py
import warnings



# # Params
# npart = 16
# # Range of energies
# Emin = 1.E3
# Emax = 1.E5
# # Radius
# Rmin = 0.
# Rmax = 2.
# # Lvol
# volmin = 1
# volmax = 2
# # v_parallel/v
# vparmin = 0.3
# vparmax = 1.0


def init_createsimulation(simname,npart,R,E,vpar,vol=[]):
    pass


def init_createdist(npart,R,E,vpar,vol=[]):
    '''
    Create a distribution of n particles
    R, E, vpar and vol are lists of [Rmin,Rmax] for example
    '''
    npartchk(npart)
    if vol != []:
        parts = numpy.zeros([npart, 9])
        for i in range(npart):
            parts[i,:] = createpart(R[0],R[1],vpar[0],vpar[1],E[0],E[1],vol[0],vol[1])
    
    return parts




def init_writedist(loc,dist,type='dat'):
    # Writes the distribution file to the location
    npart = dist.numy.shape[0]
    if type not in ['dat','h5']:
        type = 'dat'
        warnings.warn('Type not recognised, outputting .dat file.')
    # Write files
    fname = os.path.join(loc,'single.part.'+type)
    if type == 'h5':
        create_h5(fname,npart,dist)
    else:
        create_dat(fname,npart,dist)



'''
INTERNAL FUNCTIONS
'''
# CHECK INPUTS
def npartchk(npart):
    if npart > 47:
        if (npart%48 != 0):
            npart = round(npart/48) * 48
            warnings.warn("Gadi can only call multiples of 48 for npart>47, closest is {}".format(npart))
    if npart < 47:
        divisors = [x for x in range(1,npart) if npart%x==0]
        print('Generating ',npart,' particles, possible nprocs: ',divisors)
        

# PARTICLE CREATION
def createpart(Rmin,Rmax,vparmin,vparmax,Emin,Emax,volmin,volmax):
    # radial position
    r = numpy.random.uniform(low=Rmin,high=Rmax*volmax)
    s = r%2
    # L_vol
    for i in range(volmax):
        if r/(i+1)<2:
            l = i+1
    # v_parallel/v
    vpar = numpy.random.uniform(low=vparmin,high=vparmax)
    # Energy (eV)
    E = numpy.random.uniform(low=Emin,high=Emax)
    # mass ratio to proton | charge ratio to proton | radial position | poloidal angle | toroidal angle | v_parallel/v | energy [eV] | statistical weight | lvol
    return numpy.array([1,1,s,0,0,vpar,E,1,l])


# FILE CREATING INTERNALS
def create_h5(fname,npart,parts):
    hf = h5py.File(fname,'w')
    dset = hf.create_dataset('nparts', data=npart, dtype='i')
    dset = hf.create_dataset('mass',   data=parts[:,0])
    dset = hf.create_dataset('charge', data=parts[:,1])
    dset = hf.create_dataset('u1',     data=parts[:,2])
    dset = hf.create_dataset('u2',     data=parts[:,3])
    dset = hf.create_dataset('u3',     data=parts[:,4])
    dset = hf.create_dataset('lambda', data=parts[:,5])
    dset = hf.create_dataset('energy', data=parts[:,7])
    dset = hf.create_dataset('weight', data=parts[:,8])
    hf.close()

def create_dat(fname,npart,parts):
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






##### GUESS SIM LENGTH -- WORST CASE
# bspd = 4.5      #Ghz
# bt = 30         #min
# bfin = 1.e-3    #tfin


# gspd = 3.2      #Gadi core speed
# gnode = 48


# tfin = 1.e-3
# gcores = 252


# chunks = []
# gcores = []
# for i in range(10):
#     if (npart/i)%gnode != 0:
#         gcores.append(i)
#         chunks.append(i)


# spd_ratio = gspd/bspd # speed ratio gadi/base case
# spt = bt*(2+spd_ratio) #est 1 particle on gadi for 1.e-3 sim
# sim_ratio = tfin/bfin #ratio of current/base simulation times

# chunks = npart/gcores # no. of simulation chunks

# est_run_time = chunks*spt*sim_ratio
