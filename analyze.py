import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from cfg import cfg
fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.simLabel)
fptr = open("data/sim.pkl", "rb")
pkld = pkl.load(fptr)
fptr.close()
net = pkld['net']
sim = pkld['simData']

voltage = {}
current = {}

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val']
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'i':
            spikes = 0
            for spkid in sim['spkid']:
                if id == spkid:
                    spikes = spikes + 1
            model = cell['tags']['cellType']['model']
            if model in current:
                current[model].append([ stim, spikes ])
            else:
                current[model] = [[ stim, spikes ]]
    except:
        pass

plt.title("# spikes")
for model in current:
    x, y = zip(*current[model])
    plt.plot( x, y, label=model)
plt.legend()
plt.xlabel("current")
plt.ylabel("# spikes")
plt.show()

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 70
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.7']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.7' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 70
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.8']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.8' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 70
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.8T']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.8T' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass 

plt.title("NaV peak current")
for model in voltage:
    x , y = zip(*voltage[model])
    plt.plot( x, y, label=model)
plt.legend()
plt.xlabel("voltage clamp (mV)")
plt.ylabel("peak current (mA/cm2)")
plt.show()

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 70
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.7']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.7' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass
        
fig = plt.figure()
fig.suptitle('Voltage Response (AP)')
gs = gridspec.GridSpec(2, 1, hspace=0, wspace=0, figure = fig)
custom = fig.add_subplot(gs[0,0])
mandge = fig.add_subplot(gs[1,0])
t = sim['t']
for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val']
        id = cell.gid
        if stim in [ 0.2 , 0.24, 0.28, 0.32, 0.36 ]:
            if cell['tags']['cellType']['stim'] == 'i':
                model = cell['tags']['cellType']['model']
                if model == 'customSoma':
                    trace = np.array( sim['v']['cell_%i' %(id)] )
                    custom.plot(sim['t'], trace, label = 'custom:%f mA/cm2' %(stim) )
                if model == 'mandge':
                    trace = np.array( sim['v']['cell_%i' %(id)] )
                    mandge.plot(sim['t'], trace, label = 'mandge:%f mA/cm2' %(stim) )
    except:
        pass
custom.legend()
mandge.legend()
custom.set_xlim(250,300)
mandge.set_xlim(250,300)
plt.xlabel("time (ms)")
plt.ylabel("voltage (mV)")
plt.show()    


#del(net)
#del(sim)
