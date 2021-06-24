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

We can then plot the energy and momentum conservation as with matlab.
```
    sim.plot_spconservation()
```
Note: If a particle number does not exist in `sim.sp` it will be skipped, rather than returning an error like matlab.




## If LEVIS is not in the current directory

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
