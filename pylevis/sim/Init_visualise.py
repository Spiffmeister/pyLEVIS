import matplotlib.pyplot as plt


def plot_s_distribution(new_simulation):
    plt.plot(new_simulation.particles[:,2])