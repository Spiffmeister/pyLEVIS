import matplotlib.pyplot as plt

# plt.rc('text',usetex=True) ## ISSUE WITH SUBPLOTS AND TEX??
plt.rc('text',usetex=True)
# plt.rc('preamble')
# plt.rcParams.update({
# 'text.usetex':True,
# 'pgf.preamble':["\\usepackage"]
# })


def plot_spconservation(self,show=1):
    fig = plt.figure()
    
    ax1 = plt.subplot2grid((2,2),(0,0))
    ax2 = plt.subplot2grid((2,2),(1,0))
    ax3 = plt.subplot2grid((2,2),(0,1),rowspan=2)

    for i in range(self.params["nparts"]):
        # TODO: avoid empty particles causing issues
        ax1.plot(self.sp[i].t,self.sp[i].E/self.sp[i].E[0] - 1)

        ax2.plot(self.sp[i].t,self.sp[i].Ptor/self.sp[i].Ptor[0] - 1)

        ax3.plot(self.sp[i].R,self.sp[i].Z)
    

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
    

    plt.show()
    return fig



