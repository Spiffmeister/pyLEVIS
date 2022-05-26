
import matplotlib.pyplot as plt
import numpy




def plt_particleq(sim,eq):
    
    if type(sim) == pylevis.simulation:
        sim = [sim]
    if type(eq) == pyspec.spec:
        eq = [eq]
    
    qfig = plt.figure()

    for i in range(len(sim)):
        nparts = len(sim.sp[i])

        # boundary of SPEC volume
        # bound = get_spec_rzarr(S[1],1,[1],[0],[0])
        R = numpy.zeros(nparts)
        Q = numpy.zeros(nparts)
        crossing = numpy.zeros(nparts)

        for j in nparts:
            R[j] = sim[i].sp[j].s[1]
            Q[j] = sim[i].sp[j].zeta[-1]/sim[i].sp[j].th[-1]
            crossing[j] = sum(abs(numpy.diff(sim[i].sp[j].lvol)))
        
        R[R>=2] -= 2

        plt.plot(R,Q,'-o')
        plt.plot(R[crossing!=0],Q[crossing!=0])

        plt.axvline(0,'--','r')







def plt_gyro(sim):

    gfig = plt.figure()

    n = len(sim.sp)
    R = numpy.zeros(1,n)
    gyro = numpy.zeros(1,n)
    crossing = numpy.zeros(1,n)

    for i in range(n):
        R[i] = sim.sp[i].R(1)

        g_r = numpy.sqrt(sim.sp[i].gc_x()**2 + sim.sp[i].gc_y()**2 + sim.sp[i].gc_z()**2)
        gyro[i] = numpy.mean(g_r)

        crossing[i] = sum(abs(numpy.diff(sim.sp[i].lvol)))
    
    plt.plot(R,gyro,'-o')
    plt.plot(R[crossing!=0],gyro[crossing!=0],'x')
    





