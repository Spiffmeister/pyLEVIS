from .ext_fns import _ext_rhotor, _ext_v, _ext_vpar, _ext_vperp


class initial_particle_dist:
    """
    initial_particle_dist(simulation)

    Class containing the initial particle distribution

    Inputs
    ----------
    simulation class from Mercury

    Returns
    ----------
    initial_particle_dist class containing initial particle data
    """
    def __init__(self,mass,charge,s,th,ph,lam,E,w,lvol=None,wc=None):
        self.mass = mass
        self.charge = charge
        self.s = s
        self.th = th
        self.ph = ph
        self.lam = lam
        self.E = E
        self.w = w
        if lvol != None:
            self.lvol = lvol
        if wc != None:
            self.wc = wc
    
        self.rhotor = _ext_rhotor(self)
        self.v = _ext_v(self)
        self.vpar = _ext_vpar(self)
        self.vperp = _ext_vperp(self)

    '''
    INTERNAL FNS -- Do not store
    '''
    # def rhoj(self):
    #     return 



