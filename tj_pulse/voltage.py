import pickle as pkl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits import mplot3d
from cfg import cfg

fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.simLabel)
fptr = open("data/sim.pkl", "rb")
pkld = pkl.load(fptr)

fptr.close()
net = pkld['net']
sim = pkld['simData']

thrsh = -40
dt = cfg.recordStep

xvar = 'mul'
#xvar = 'mut'
yvar = 'amp'

window = np.array([ 3000, 3100 ])
t = np.arange(0, window[1] - window[0], cfg.recordStep)
window = (window / dt).astype(int)

traces = list(cfg.recordTraces.keys())

traces = [ traces[0], traces[3], traces[6], traces[9], traces[-1], traces[12] ]
print(traces)

for index in range(len(cfg.amps)):
    fig, axs = plt.subplots(5, 5, figsize=(20,10))
    plt.subplots_adjust(wspace=0, hspace=0)

    for cell in net['cells']:
        if (cell['tags']['cellType']['amp'] == cfg.amps[index]):
            id = cell.gid
            for x, trace in enumerate(traces):
                v = np.array(sim[trace]['cell_%i' %(id)][window[0]:window[1]])
                y = 4 - int(np.round( cell['tags']['cellType'][xvar] / 0.25))
                print('(%i, %i)' %(x,y))
                print(cell['tags']['cellType'])
                axs[x,y].plot(t, v)
                axs[x,y].set_ylim( -90, 90)
                axs[x,y].grid()


    plt.savefig("%s_%1.2f.png" %(xvar, np.round(cfg.amps[index], 2)), bbox_inches='tight')

        #    edge = np.where( (arr[:-1] < thrsh) & (arr[1:] >= thrsh) )
        #plt.legend()
        #label = "vt_%s_%s.png" %(cfg.amps[index]  ,1 - cell['tags']['cellType']['mul'])
        # plt.show()
        #plt.savefig(label)

