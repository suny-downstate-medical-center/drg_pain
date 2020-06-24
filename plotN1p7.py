from data import DataHandler
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product

dh = DataHandler()
#dh('data/n1p7.json', 'n1p7')
dh('data/n1p8.json', 'n1p8')
#                mul ,    amp
#ixsre = 'mn1p7:(.....).*(.....)nAx.*'
ixsre = 'mn1p8:(.....).*(.....)nAx.*'
data = dh.return_arr(ixsre, lambda x: x.max())

def arr(start, end, incr):
    return np.array([float("%.3f" %(x)) for x in np.arange(start, end+incr/2, incr)])

amps = arr(0.14, 0.26, 0.005)
mttxss = arr(0.0, 1.0, 0.05)
mn1p8s = arr(0.0, 1.0, 0.05)
#muls = mttxss
muls = mn1p8s
def create_surface(muls, amps):
    surface = np.zeros( (len(amps), len(muls)) )
    for i, mul in enumerate(muls):
        for j, amp in enumerate(amps):
            surface[j][i] = data[mul][amp]['val']
    return surface

mmuls, mamps = np.meshgrid(muls, amps)

fig = plt.figure()
ax  = fig.gca(projection='3d')
v_soma = create_surface(muls, amps)
ax.plot_surface(mmuls, mamps, v_soma, label='v_soma', cmap=cm.coolwarm)
ax.set_xlim(muls.max(), muls.min())
ax.set_ylim(amps.min(), amps.max())
ax.set_xlabel('NaV1.8')
ax.set_ylabel('nA')
plt.show()

