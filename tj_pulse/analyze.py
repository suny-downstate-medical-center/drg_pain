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

thrsh = 0
dt = cfg.recordStep

xvar = 'mut'
yvar = 'amp'

X = []
Y = []
Z = {}

Xf = {}
for var in ['v_peri', 'v_cntr']:
    Z[var] = []

for cell in net['cells']:
    id = cell.gid
    x = cell['tags']['cellType'][xvar]
    X.append(x)
    if x not in Xf:
        Xf[x] = {yvar: []}
        for var in Z.keys():
            Xf[x][var] = []
    y = cell['tags']['cellType'][yvar]
    Y.append(y)
    Xf[x][yvar].append(y)
    for var in Z.keys():
        arr = np.array(sim[var]['cell_%i' %(id)])
        aps = np.where((arr[:-1] < thrsh) & (arr[1:] >= thrsh))[0].size
        Z[var].append(aps)
        Xf[x][var].append(aps)

for x in Xf:
    for var in Z.keys():
        plt.plot(Xf[x][yvar], Xf[x][var], label="%s:%f   %s" %(xvar, x, var))

plt.show()
plt.legend()
# fig = plt.figure()
# ax = plt.axes(projection = '3d')
#
# for var in Z.keys():
#     ax.scatter(X, Y, Z[var], label=var)
# #plt.axis( [1.0, 0, .20, 0.4])
# ax.set_title("AP at central axon")
# ax.set_xlabel("Percentage mutated NaV1.7")
# ax.set_ylabel("Stimulus amplitude (nA)")
# ax.set_zlabel("# APs at central axon")
# plt.show()
# plt.legend()
# plt.savefig("dddd.png")
