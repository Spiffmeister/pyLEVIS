# pyLEVIS

!!! THIS README AND PACKAGE IS STILL INCOMPLETE !!!

Python implementation of the VENUS-LEVIS MATLAB routines. Most of the routines have the same names so the functions should be familiar.

You should be in the direction in which your runs are located to read them in, for instance `path/to/levis/runs`.



# Examples

## Example: Reading in a simulation and plotting

```py
    # Import the package from the python command line as
    import pylevis
```

Reading the simulation is similar to the old scripts, except we no longer use `Mercury` to read data in, also that reading in the simulation will still work if we append "prob" to the name, or we can choose to omit it:
```py
    # Read in some simulation
    sim = pylevis.simulation("probSPEC.0")
    # which is equivalent to
    sim = pylevis.simulation("SPEC.0")
```
_A warning that if you have two runs, one called "probSPEC" and another called "SPEC", this may cause issues reading them in._

Retrieving the particles data is the same as with the matlab routines:
```py
    sim.GetParticle()
```
although we can now also choose to read in only certain particles (indexed from 1, since that's how the file naming convention is):
```py
    sim.GetParticle(parts=[1,5,6])
```
note that to access the particles the indexing starts from 0 as per python, so `sim.sp[0]` is particle 1.


Plotting the energy/momentum conservation is also the same as with the MATLAB routines:
```
    sim.plot_spconservation()
```
Note: If a particle number does not exist in `sim.sp` it will be skipped and the user will be warned that some were not plotted, rather than returning an error like in MATLAB.


## Example: Creating a new simulation (_experimental_)

This is experimental at the moment, but a new simulation can be initialised by calling:
```py
    import pylevis
    f = pylevis.new_simulation('SimulationName',nparts,eqfile="path/to/equilibrium",eqtype="spec",exedir="path/to/mercuryandpostprocessing.x",machine="local")
```
The equilibrium type can be changed by specifying `eqtype=""` (default and only supported at the moment is `"spec"`), the machine you are running the simulation on should be set with `machine=`,if this is your own computer, it should be `"local"` (more info below). By default, `new_simulation` will set up default simulation settings in `new_simulation.data`, you can check the current config with,
```py
    f.data.properties()
```
All properties are stored in dictionaries, for instance if we wanted to change the simulation duration we would set `f.data["tfin"]=1e-5` (_do not change `f.data["nparts"]` as this isn't actually used except to generate the data file and will be overwritten upon write_).
A distribution (only uniformly sampled at the moment) of particles with `f.nparts` number of particles and and by specifying the range or value of input values can be generated, for instance the following:
```py
    f.generate_particles([0.1,1.9],0,0,1,[5e2,2e3],1,1,1)
```
will generate particles, with $s\in[0.1,1.9]$ and $E\in[5e2,2e3]$ randomly generated, and all other values set as given. The required simulation files can then all be created at the location set by `f.simdir` by calling,
```py
    f.create_simulation()
```
If the location already exists you will be prompted to provide the optional input `overwrite=True`, this will delete existing files and remake them. Finally, we can run the simulation from the python tools as well,
```py
    f.run_simulation()
```
How the simulation is called depends on the value of `f.machine=""` (default is `"local"`) (your local machine).


### Config

#### Current machine configs
- local (calls `./mercury.x < data`)




---
# Progress

## TO DO


| Function           | Purpose                                                                                 |
| ------------------ | --------------------------------------------------------------------------------------- |
| Get_Diffusivity    |                                                                                         |
| DecryptEquilibrium | Calls UnfoldEquilibrium?                                                                |
| UnfoldEquilibrium  | Reads in equilibrium? `Equilibrium reconstruction interface for many equilibrium codes` |
| GetParScenic       | Reads in `scenic.in` file                                                               |
| GetBG              | Gets background profiles                                                                |
| GetLostParticles   | What a poorly written file                                                              |
| Get_Moments        | Gets moments(?) and trapped(?) information                                              |
|                    |                                                                                         |

### Incomplete

| Function                     | Subfunctions             |
| ---------------------------- | ------------------------ |
| GetPar                       | `Get_Diffusivity_Params` |
| Get_Dist -> Get_ParticleDist |                          |




## Completed


| Original            | New                    |
|:------------------- |:---------------------- |
| Get_Particle        |                        |



