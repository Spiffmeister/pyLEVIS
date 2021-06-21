'''
EXPORT DATA FROM pyLEVIS.simulation
'''
import os
import datetime
import h5py
import pickle

def Export(LEVIS,fname,etype="pickle"):
    intype = str(type(LEVIS))
    if "simulation" in intype:
        go = True
    else:
        pass
        # TODO: read in sim
        # Read in the simulation
        # LEVIS = 

    os.mkdir(os.path.join(LEVIS.dirrun,"export"))
    if go:
        if etype == "pickle":
            # Write to pickle file
            export_pickle(LEVIS,fname)
        elif etype == "h5":
            export_h5(LEVIS,fname)



def export_pickle(sim,fname):
    # Write a python pickle file
    p_file = open(fname,'rb')
    pickle.dump(sim,p_file)
    p_file.close()
    if os.path.exists(fname+".pickle"):
        print("Pickle file written.")



def export_h5(LEVIS,fname):
        # Ensure that particle orbits are loaded
        try:
            LEVIS.sp
        except AttributeError:
            LEVIS.GetParticle
        # Ensure the initial data is loaded
        try:
            LEVIS.init
        except:
            pass
        # Check if backup equilibrium data is loaded
        try:
            LEVIS.magnetic
        except:
            pass
        
        # Make export directory under run
        os.mkdir(os.path.join(LEVIS.dirrun,"export"))

        f_data = h5py.File('export','w')
        
        init = f_data.create_group('init')
        init.create_dataset('s',        data=LEVIS.init.s,      dtype=float)
        init.create_dataset('rho',      data=LEVIS.init.rhotor, dtype=float)
        init.create_dataset('th',       data=LEVIS.init.th,     dtype=float)
        init.create_dataset('ph',       data=LEVIS.init.ph,     dtype=float)
        init.create_dataset('lambda',   data=LEVIS.init.lam,    dtype=float)
        init.create_dataset('E',        data=LEVIS.init.E,      dtype=float)
        init.create_dataset('mass',     data=LEVIS.init.mass,   dtype=float)
        init.create_dataset('charge',   data=LEVIS.init.charge, dtype=float)
        init.create_dataset('R',        data=LEVIS.init.R,      dtype=float)
        init.create_dataset('Z',        data=LEVIS.init.Z,      dtype=float)
        init.create_dataset('x',        data=LEVIS.init.x,      dtype=float)
        init.create_dataset('y',        data=LEVIS.init.y,      dtype=float)
        init.create_dataset('vpar',     data=LEVIS.init.vpar,   dtype=float)
        init.create_dataset('vperp',    data=LEVIS.init.vperp,  dtype=float)
        init.create_dataset('muOqp',    data=LEVIS.init.muOqp,  dtype=float)

        f_data.create_dataset('nparts',         data=LEVIS.param["nparts"])
        f_data.create_dataset('tfin',           data=LEVIS.param["tfin"])
        f_data.create_dataset('basedir',        data=LEVIS.rundir)
        f_data.create_dataset('creation_date',  data=datetime.date.today())

        eq = f_data.create_group('eq')
        # eq.create_dataset('R',)




