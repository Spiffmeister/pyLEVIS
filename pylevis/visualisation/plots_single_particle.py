'''
Plotting the energy and toroidal momentum conservation
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axis3d
# import pympl

# plt.rc('text',usetex=True) ## ISSUE WITH SUBPLOTS AND TEX??
plt.rc('text',usetex=True)
plt.rc('preamble')
plt.rcParams.update({
'text.usetex':True,
'pgf.preamble':["\\usepackage"]
})


def plot_spconservation(self,parts=[],show=True):
    """
    plot_spconservation(self,show=1)

    Plot the energy (top left) and momentum (top right) conservation and R-Z position of the particles
    """
    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2,2),(0,0)) #Energy loss
    ax2 = plt.subplot2grid((2,2),(1,0)) #Momentum loss
    ax3 = plt.subplot2grid((2,2),(0,1),rowspan=2) #R-Z position

    if parts == []:
        parts = [key for key in self.sp.keys()]
    
    ax1, missing = __plot_particle_conservation(self,"E",parts,ax=ax1,show=False)
    ax2, missing = __plot_particle_conservation(self,"Ptor",parts,ax=ax2,show=False)
    ax3, missing = __plot_particle_property(self,"R","Z",parts,ax=ax3,show=False)

    ax1.ticklabel_format(axis='both',style='sci',scilimits=(0,0),useMathText=True)
    ax2.ticklabel_format(axis='both',style='sci',scilimits=(0,0),useMathText=True)
    ax3.axis('equal')

    fig.tight_layout()
    
    if missing != []: #let the user know if any particles are not plotted
        print(str(len(missing))+" missing particles not plotted.")

    if show:
        plt.show()
    return fig


def plot_cartesian(self,parts=[],show=True):
    """
    plot_cartesian(self,show=1)

    Plot the particles position in cartesian space
    """
    fig = plt.figure()
    ax = axis3d(fig)

    if parts == []:
        parts = [key for key in self.sp.keys()]
    
    missing = []
    for i in parts:
        if not self.sp[i].missing:
            ax.plot(self.sp[i].x,self.sp[i].y,self.sp[i].z)
        else:
            missing += [i]
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    if show:
        plt.show()
    return fig


def plot_RZ(self,parts=[],ax=None,show=True):
    """
    plot_RZ(self,parts=[],show=1,ax=None)
    """
    if ax == None:
        ax = plt.gca()
    
    if parts == []:
        parts = [key for key in self.sp.keys()]
    
    for i in parts:
        ax.plot(self.sp[i].R,self.sp[i].Z)
    
    ax.set_xlabel('R')
    ax.set_ylabel('Z')

    if show:
        ax.show()

    return ax


def __plot_particle_conservation(self,property,parts=[],ax=None,show=True):
    """
    __plot_particle_conservation(self,property,parts=[],ax=None,show=True)

    Plot the conservatino of a particles "property" (i.e. property="E")
    """
    if ax == None:
        ax = plt.gca()
    
    if parts == []:
        parts = [key for key in self.sp.keys()]

    missing = []
    for i in parts:
        if not self.sp[i].missing:
            prop = getattr(self.sp[i],property)
            ax.plot(self.sp[i].t,prop/prop[0] - 1)
        else:
            missing += [i]
    
    ax.set_xlabel('t')
    ax.set_ylabel(r"$\Delta "+property+"/"+property+"_0$")
    
    if show:
        ax.show()
    
    return ax, missing

def __plot_particle_property(self,xprop,yprop,parts=[],ax=None,show=True):
    """
    __plot_particle_property(self,xprop,yprop,parts=[],ax=None,show=True)

    Hidden function for generating plots of of given properties
    """
    if ax == None:
        ax = plt.gca()
    
    if parts == []:
        parts = [key for key in self.sp.keys()]
    
    missing = []
    for i in parts:
        if not self.sp[i].missing:
            x = getattr(self.sp[i],xprop)
            y = getattr(self.sp[i],yprop)
            ax.plot(x,y)
        else:
            missing += [i]
    
    ax.set_xlabel("${0}$".format(xprop))
    ax.set_ylabel("${0}$".format(yprop))
    
    return ax, missing


def plot_initial_dist():
    pass