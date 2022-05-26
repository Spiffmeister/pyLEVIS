'''
EXPORT DATA FROM pylevis.simulation
'''
import os
import datetime
import h5py
import pickle

def Export(simulation,fname,etype="pickle"):
    intype = str(type(simulation))
    if "simulation" in intype:
        go = True
    else:
        pass
        # TODO: read in sim
        # Read in the simulation
        # simulation = 

    os.mkdir(os.path.join(simulation.dirrun,"export"))
    if go:
        if etype == "pickle":
            # Write to pickle file
            export_pickle(simulation,fname)
        elif etype == "h5":
            export_h5(simulation,fname)



def export_pickle(sim,fname):
    # Write a python pickle file
    p_file = open(fname,'rb')
    pickle.dump(sim,p_file)
    p_file.close()
    if os.path.exists(fname+".pickle"):
        print("Pickle file written.")



def export_h5(simulation,fname):
        # Ensure that particle orbits are loaded
        try:
            simulation.sp
        except AttributeError:
            simulation.GetParticle
        # Ensure the initial data is loaded
        try:
            simulation.init
        except:
            pass
        # Check if backup equilibrium data is loaded
        try:
            simulation.magnetic
        except:
            pass
        
        # Make export directory under run
        os.mkdir(os.path.join(simulation.dirrun,"export"))

        f_data = h5py.File('export','w')
        
        init = f_data.create_group('init')
        init.create_dataset('s',        data=simulation.init.s,      dtype=float)
        init.create_dataset('rho',      data=simulation.init.rhotor, dtype=float)
        init.create_dataset('th',       data=simulation.init.th,     dtype=float)
        init.create_dataset('ph',       data=simulation.init.ph,     dtype=float)
        init.create_dataset('lambda',   data=simulation.init.lam,    dtype=float)
        init.create_dataset('E',        data=simulation.init.E,      dtype=float)
        init.create_dataset('mass',     data=simulation.init.mass,   dtype=float)
        init.create_dataset('charge',   data=simulation.init.charge, dtype=float)
        init.create_dataset('R',        data=simulation.init.R,      dtype=float)
        init.create_dataset('Z',        data=simulation.init.Z,      dtype=float)
        init.create_dataset('x',        data=simulation.init.x,      dtype=float)
        init.create_dataset('y',        data=simulation.init.y,      dtype=float)
        init.create_dataset('vpar',     data=simulation.init.vpar,   dtype=float)
        init.create_dataset('vperp',    data=simulation.init.vperp,  dtype=float)
        init.create_dataset('muOqp',    data=simulation.init.muOqp,  dtype=float)

        f_data.create_dataset('nparts',         data=simulation.param["nparts"])
        f_data.create_dataset('tfin',           data=simulation.param["tfin"])
        f_data.create_dataset('basedir',        data=simulation.dirrun)
        f_data.create_dataset('creation_date',  data=datetime.date.today())

        eq = f_data.create_group('eq')
        # eq.create_dataset('R',)




