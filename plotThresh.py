from data import DataHandler
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product
from plot import plot_data, plot_groups
# from cfg import cfg
from cfgIC import cfg

freqs, npulses, amps, durs, mttxss, mn1p8s, mn1p9s = cfg.freqs, cfg.npulsess, cfg.amps, cfg.durs, cfg.mttxss, cfg.mn1p8s, cfg.mn1p9s

# label
# '<celltype>(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
dh = DataHandler()
dh('data/dataIC.json', 'IC')

#for label, chan in [ ['NaV1.7', 'nattxs'], ['NaV1.8', 'nav1p8'] ]:
#    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}

ixssoma   = '\(mn1p7:(.....)x\)\(mn1p8:(.....)x\)\((.....)nAx.*_soma'

soma = dh.return_arr(ixssoma, lambda x: x.max())

def create_surface(amp):
    surface = np.zeros((len(mn1p8s), len(mttxss)))
    for i, mttxs in enumerate(mttxss):
        for j, mn1p8 in enumerate(mn1p8s):
            surface[j][i] = soma[mttxs][mn1p8][amp]['val']
    return surface

mshmttxss, mshmn1p8s = np.meshgrid(mttxss, mn1p8s)

for amp in amps:
    title = "v_max(%.3fnA)" % (amp)
    fig = plt.figure()
    ax  = fig.gca(projection='3d')
    vmax = create_surface(amp)
    ax.plot_wireframe(mshmttxss, mshmn1p8s, vmax, label='v_max', cmap=cm.coolwarm)
    ax.set_title(title)
    ax.set_xlim(1.0, 0.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel('NaV1.7')
    ax.set_ylabel('NaV1.8')
    ax.ticklabel_format(useOffset=False, style='plain')

    plt.savefig("data/%s.png" % (title), bbox_inches='tight', pad_inches=0.075)

    plt.cla()
    plt.clf()
    plt.close()