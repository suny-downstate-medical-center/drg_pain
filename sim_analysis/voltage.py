import pickle as pkl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import matplotlib.gridspec as gridspec
from cfg import cfg

fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.simLabel)
fptr = open("data/sim.pkl", "rb")
pkld = pkl.load(fptr)

fptr.close()
net = pkld['net']
sim = pkld['simData']

thrsh = -40
dt = cfg.recordStep

xvar = 'mut'
yvar = 'amp'

window = int( 100 / dt )

for cell in net['cells']:
    if (cell['tags']['cellType']['amp'] == 0.2):
        plt.figure(figsize=(16,12))
        id = cell.gid
        v = np.array(sim['v_cntr']['cell_%i' %(id)])
        for i in np.arange(0, 4000, 1000):
            i = int( i / dt )
            arr = v[ i : i + (2 * window) ]
            edge = np.where( (arr[:-1] < thrsh) & (arr[1:] >= thrsh) )
            try: 
                start = edge[0][0]
                plt.plot(np.linspace(0,300, window), arr[start:start+window], label = i * dt)
            except:
                pass
        plt.legend()
        label = "v_cntr_mut%s.png" %(cell['tags']['cellType']['mut'])
        plt.savefig(label)

