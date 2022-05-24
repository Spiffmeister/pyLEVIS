'''
Plotting the energy and toroidal momentum conservation
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axis3D
import pympl

# plt.rc('text',usetex=True) ## ISSUE WITH SUBPLOTS AND TEX??
plt.rc('text',usetex=True)
# plt.rc('preamble')
# plt.rcParams.update({
# 'text.usetex':True,
# 'pgf.preamble':["\\usepackage"]
# })


def plot_spconservation(self,show=1):
    """
    plot_spconservation(self,show=1)

    Plot the energy (top left) and momentum (top right) conservation and R-Z position of the particles
    """
    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2,2),(0,0)) #Energy loss
    ax2 = plt.subplot2grid((2,2),(1,0)) #Momentum loss
    ax3 = plt.subplot2grid((2,2),(0,1),rowspan=2) #R-Z position

    parts = [key for key in self.sp.keys()]
    missing = []
    for i in (parts):
        if not self.sp[i].missing:
            ax1.plot(self.sp[i].t,self.sp[i].E/self.sp[i].E[0] - 1)
            ax2.plot(self.sp[i].t,self.sp[i].Ptor/self.sp[i].Ptor[0] - 1)
            ax3.plot(self.sp[i].R,self.sp[i].Z)
        else: #skip missing particles
            missing += [i]
    
    ax1.set_xlabel("t")
    ax1.set_ylabel(r"$\Delta E/E_0$")
    ax1.ticklabel_format(axis='both',style='sci',scilimits=(0,0),useMathText=True)

    ax2.set_xlabel("t")
    ax2.set_ylabel(r"$\Delta P_\phi/P_{\phi,0}$")
    ax2.ticklabel_format(axis='both',style='sci',scilimits=(0,0),useMathText=True)

    ax3.axis('equal')
    ax3.set_xlabel("R")
    ax3.set_ylabel("Z")

    fig.tight_layout()
    
    if missing != []: #let the user know if any particles are not plotted
        print(str(len(missing))+" missing particles not plotted.")

    if show:
        plt.show()
    return fig


def plot_cartesian(self,show=1):
    """
    plot_cartesian(self,show=1)

    Plot the particles position in cartesian space
    """
    fig = plt.figure()
    ax = Axis3D(fig)

    parts = [key for key in self.sp.keys()]
    missing = []
    for i in parts:
        if not self.sp[i].missing:
            ax.plot(self.sp[i].x,self.sp[i].y,self.sp[i].z)
        else:
            missing += [i]
    
    if show:
        plt.show()
    return fig


