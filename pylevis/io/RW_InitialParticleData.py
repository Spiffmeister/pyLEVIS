import os
import glob
import numpy
import warnings
import h5py

from pylevis.particles.InitialParticleData import initial_particle_dist


def Get_initial_particle_dist(simulation):
    # Check the init particle distribution type and call reading fn
    exts = ["dat","h5"]
    for ext in exts:
        try:
            fname = glob.glob(os.path.join(simulation.dirrun,"single.particle."+ext))[0]
            break
        except IndexError:
            #Make sure if this fails it doesn't try to read nothing
            ext = "" 
    # Read in file
    if ext == "dat":
        init = _read_init_dat(fname,simulation.equilibrium_type)
    elif ext == "h5":
        init = _read_init_h5(fname)
    else:
        raise FileNotFoundError("No h5 or dat single particle file found")
    

    # TODO: what does this file look like???
    f_alpha = os.path.join(simulation.dirrun,"fusion_alpha.out")
    if os.path.exists(f_alpha):
        # TODO: Does nothing in MATLAB routines
        # alphaprob = numpy.loadtxt(f_alpha)
        self.wc = self.w
    
    return init
    
        
        



def _read_init_dat(fname,equilibrium_type):
    """
    _read_init_dat(self,equilibrium_type,fname)

    Open single.particle.dat and read in data
    """
    # Get the # of parts
    f_open = open(fname)
    np = int(f_open.readline())
    f_open.close()
    # read in the rest
    data = numpy.loadtxt(fname,skiprows=1,max_rows=np)
    if np > 1:
        mass      = data[:,0]
        charge    = data[:,1]
        s         = data[:,2]
        th        = data[:,3]
        ph        = data[:,4]
        lam       = data[:,5]
        E         = data[:,6]
        w         = data[:,7]
        if equilibrium_type == "spec":
            lvol  = data[:,8]
    else:
        mass      = data[0]
        charge    = data[1]
        s         = data[2]
        th        = data[3]
        ph        = data[4]
        lam       = data[5]
        E         = data[6]
        w         = data[7]
        if equilibrium_type == "spec":
            lvol  = data[8]
        

    if equilibrium_type == "spec":
        init = initial_particle_dist(mass,charge,s,th,ph,lam,E,w,lvol)
    else:
        init = initial_particle_dist(mass,charge,s,th,ph,lam,E,w)
    
    return init


def _read_init_h5(self,fname):
    """
    _read_init_h5(self,fname)

    Open single.particle.h5 and read in data
    """
    # single.particle.h5 reading
    f_open = h5py.File(fname)
    np = int(f_open["nparts"])
    s = numpy.array(f_open["u1"])
    th = numpy.array(f_open["u2"])
    ph = numpy.array(f_open["u3"])
    lam = numpy.array(f_open["lambda"])
    E = numpy.array(f_open["energy"])
    w = numpy.array(f_open["weight"])
    mass = numpy.array(f_open["mass"])
    charge = numpy.array(f_open["charge"])
    R = numpy.array(f_open["R"])
    Z = numpy.array(f_open["Z"])

    try:
        lvol = numpy.array(f_open["lvol"])
        init = initial_particle_dist(mass,charge,s,th,ph,lam,E,w,lvol)
    except:
        init = initial_particle_dist(mass,charge,s,th,ph,lam,E,w)
        
    # NBI distribution
    try:
        init.vx = numpy.array(f_open["vx"])
        init.vy = numpy.array(f_open["vy"])
        init.vz = numpy.array(f_open["vz"])
    except:
        warnings.warn('No NBI distribution')
    # Generated distribution
    try:
        init.Ptor = numpy.array(f_open["Ptor"])
        init.muOqp = numpy.array(f_open["muOqp"])
    except:
        warnings.warn('Not a generated distribution')


def _read_tauparticle(init,np,dirname):
    """
    _read_tauparticle(self,dirname)

    Open TauParticle file and read in data
    """
    # TODO: what does this file look like???
    fname = os.path.join(dirname,"TauParticle")
    if os.path.exists(fname):
        tmpfile = numpy.loadtxt(fname)
        index_final = tmpfile[:,0]
        th_final = tmpfile[:,1]
        ph_final = tmpfile[:,2]
        t_final = tmpfile[:,3]

        nup = (ph_final - th_final)/2/numpy.pi/t_final #more descriptive name?? also what the hell is this

        init.nup = numpy.zeros(np)
        init.th_final = numpy.zeros(np)
        init.ph_final = numpy.zeros(np)

        init.nup[index_final] = nup
        init.th_final[index_final] = th_final
        init.ph_final[index_final] = ph_final
        init.index_final = index_final


def _read_EcrossB(init,fdir):
    """
    _read_EcrossB(self,fdir)

    Open EcrossB.in file and read in data
    """
    # TODO
    # Get initial potential energy data
    fname = os.path.join(fdir,"EcrossB.in")
    if os.path.exists(fname):
        f_open = open(fname,'r')
        # ns = f_open.readline()
        # self.Epot = self.charge
        f_open.close()
    else:
        raise FileNotFoundError('No ExB file found')


# WRITING #
def write_distribution(dist,fpath,filetype='dat'):
    '''
    Writes the distribution file to the location given as either .dat or .h5 depending on filetype
    '''
    print(fpath)
    print(dist)
    npart = len(dist.s)
    if filetype not in ['dat','h5']:
        filetype = 'dat'
        warnings.warn('Type not recognised, outputting .dat file.')
    # Write files
    fname = os.path.join(fpath,'single.particle.'+filetype)
    if filetype == 'h5':
        _create_particle_h5(fname,npart,dist)
    else:
        _create_particle_dat(fname,npart,dist)


    
def _create_particle_h5(fname,npart,dist,eqtype='spec'):
    '''
    Create a hdf5 file for particle distribution, parallel read by LEVIS
    '''
    hf = h5py.File(fname,'w')
    dset = hf.create_dataset('nparts', data=npart, dtype='i')
    dset = hf.create_dataset('mass',   data=dist.mass)
    dset = hf.create_dataset('charge', data=dist.charge)
    dset = hf.create_dataset('u1',     data=dist.s)
    dset = hf.create_dataset('u2',     data=dist.th)
    dset = hf.create_dataset('u3',     data=dist.ph)
    dset = hf.create_dataset('lambda', data=dist.lam)
    dset = hf.create_dataset('energy', data=dist.E)
    dset = hf.create_dataset('weight', data=dist.w)
    if eqtype == 'spec':
        dset = hf.create_dataset('lvol', data=dist.lvol, dtype='i')
    hf.close()

def _create_particle_dat(fname,npart,dist,eqtype='spec'):
    '''
    Create a .dat file for particle distribution, serial read by LEVIS
    '''
    # Write the distribution
    fields = ["mass","charge","s","th","ph","lam","E","w"]
    if eqtype == 'spec':
        format = "%f    %f  %f  %f  %f  %f  %f  %f  %i"
        fields.append("lvol")
    else:
        format = "%f    %f  %f  %f  %f  %f  %f  %f"
    
    parts = numpy.zeros(len(fields))
    for i in range(len(fields)):
        parts[i] = getattr(dist,fields[i])

    numpy.savetxt(fname,parts,fmt=format)
    # Append the number of particles to the start of the file
    with open(fname,'r') as read_f, open(fname+"bak",'w') as write_f:
        write_f.write(str(npart)+'\n')
        for line in read_f:
            write_f.write(line)
    # Remove trash
    os.remove(fname)
    os.rename(fname+"bak",fname)

