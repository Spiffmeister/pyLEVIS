# Use for initialising particles

# from re import M
import numpy
from pylevis.particles.InitialParticleData import initial_particle_dist




def create_particle_distribution(npart,s,pol,tor,vpar,E,
    mass_ratio=1,charge_ratio=1,weight=1,
    eqtype='spec',distfn="uniform",seed=None):
    '''
    Create a distribution of n particles
    R, E, vpar and vol are lists of [Rmin,Rmax] for example
    Optional arguments: M, C, weight, volmax, eqtype, distfn

    eqtype - if spec then also generate lvol
    distfn - allows sampling from different distribution functions, default is uniform
    '''
    if eqtype != 'spec':
        if any(s-2.0 >= 0.0):
            raise ValueError('s must be between 0 and 2')
    
    # Set up distribution function for sampling
    rng = getattr(numpy.random.default_rng(),distfn)
    def gen(param):
        # Generating function for values
        if type(param) in [int,float]:
            return param
        if distfn == "standard_normal":
            return rng(npart)
        else:
            return rng(low=param[0],high=param[1],size=npart)
    
    if eqtype == 'spec':
        init = initial_particle_dist(1,1,1,1,1,1,1,1,1)
    else:
        init = initial_particle_dist(1,1,1,1,1,1,1,1)

    init.mass    = gen(mass_ratio)    # mass ratio to proton
    init.charge  = gen(charge_ratio)  # charge ratio to proton
    init.s       = gen(s)         # Radial position (in s)
    if eqtype=='spec':
        # If eqtype is spec, resolve issues with the lvol
        s = numpy.array(s)
        init.lvol= numpy.floor(s/2.0)+1
        init.s   = numpy.mod(init.s,2.0)
    init.th  = gen(pol)       # Poloidal angle
    init.ph  = gen(tor)       # Toroidal angle
    init.lam = gen(vpar)      # v_parallel/v
    init.E   = gen(E)         # Energy [eV]
    init.w   = gen(weight)    # Statistical weight

    
    return init


