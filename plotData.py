from data import DataHandler
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product

amps = np.linspace(0.16, 0.18, 5)
durs = np.linspace(1, 5, 5)
mttxss = np.linspace(0.5, 1.0, 6)
mn1p8s = np.linspace(0.5, 1.0, 6)

amps = np.array([.16, .165, .17, .175, .18])
durs = np.array([1, 2, 3, 4, 5])
mttxss = np.array([.5, .6, .7, .8, .9, 1])
mn1p8s = np.array([.5, .6, .7, .8, .9, 1])

mamps, mdurs = np.meshgrid(amps, durs)
dh = DataHandler()
dh('data/n1p7.json', 'n1p7')
dh('data/n1p8.json', 'n1p8')

#               mul ,   amp ,    dur
ixsre = 'mn1p7:(...).*(.....)nAx(...)ms.*_terminal'
arr = dh.return_arr(ixsre, lambda x: x.max())

def create_surface(arr, mul, amps, durs):
    surface = np.zeros( (len(amps), len(durs)) )
    for x, amp in enumerate(amps):
        for y, dur in enumerate(durs):
            surface[x][y] = arr[mul][amp][dur]['val']
    return surface

for mttxs in mttxss:
    fig = plt.figure()
    ax  = fig.gca(projection='3d')
    v_terminal = create_surface(arr, mttxs, amps, durs)
    ax.plot_surface(mamps, mdurs, v_terminal, label='v_terminal', cmap=cm.coolwarm)
    ax.set_xlim(amps.max(), amps.min())
    ax.set_xlabel('nA')
    ax.set_ylabel('ms')
