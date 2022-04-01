# pyLEVIS

!!! THIS README IS STILL INCOMPLETE -- WILL BE COMPLETE SOON !!!

Python implementation of the VENUS-LEVIS matlab routines. Most of the routines have the same names so if you've used the matlab routines before most things will be familiar.



# Examples

## Example of reading in some data and plotting if pylevis is in the same directory

```py
    # Import the package from the python command line as
    import pylevis
```

We can then read in the simulation. Note that we no longer use `Mercury` to read data in, also that reading in the simulation will still work if we append "prob" to the name, or we can choose to omit it.
```py
    # Read in some simulation
    sim = pylevis.simulation("probSPEC.0")
    # which is equivalent to
    sim = pylevis.simulation("SPEC.0")
```

Next we want to read in the particles as we would with the matlab routines, this is exactly the same, and accessing the particles is identical to matlab.
```py
    sim.GetParticle()
    # or only some particles (for instance particles 1 5 and 6) as
    sim.GetParticle(parts=[1,5,6])
```

We can then plot the energy and momentum conservation in the same way as with the MATLAB routines.
```
    sim.plot_spconservation()
```
Note: If a particle number does not exist in `sim.sp` it will be skipped, rather than returning an error like MATLAB.



## Creating a new simulation

A new simulation can be initialised by calling,
```py
    import pylevis
    f = pylevis.new_simulation('SimulationName',nparts,'path/to/equilibrium')
```
You can optionally change the equilibrium type by specifying `eqtype=""` (default is `"spec"`) and the machine you are running the simulation on with `machine=""` (`"local"` is default, more on this below). By default, `new_simulation` will set up default simulation settings in `new_simulation.data`, you can check the current config with,
```py
    f.data.properties()
```
All properties are stored in dictionaries, for instance if we wanted to change the simulation duration we would set `f.data["tfin"]=1e-5` (_do not change `f.data["nparts"]` as this isn't actually used except to generate the data file and will be overwritten upon write_).
A distribution (only uniformly sampled at the moment) of particles with `f.nparts` number of particles and and by specifying the range or value of input values (call help(f.generate_particles) for input list),
```py
    f.generate_particles(srng,polrng,torrng,vparrng,Erng,massrng,chargerng,weightrng,numvols)
```
for instance the following,
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



---
# Config

## Current machine configs
- local (calls `./mercury.x < data`)



# If LEVIS is not in the current directory

If VENUS-LEVIS **is not** in the same directory as `pylevis` then you can run
```py
    pylevis.pylevis_settings.levis_directory = "/path/to/levis"
```
to update the configuration, this will automatically update the path to VENUS-LEVIS any future calls to `pylevis.simulation`.

## Changed functions


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





### Long term
- Paralleisation for large data sets?
