#plot function
import matplotlib.pyplot as plt

#tracegroups = {'current'  : {'rgx': re.compile('(NaV)|K')   , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' }}
#tracecells = {"vclamp": {'conds': lambda id: id == 0}}
#   plot_groups(data=sim.allSimData, keys=cfg.recordTraces.keys(), tracegroups=<see groups>, tracecells=<see cells>[, cmSeq=<see sequence>, cmDelta=<integer>])
def plot_groups(data               , keys                        , tracegroups             , tracecells            , *args):
    if   len(args) == 2:
        cmseq = args[0]
        cmdelta = args[1]
    elif len(args) == 1:
        cmseq = args[0]
        cmdelta = 10
    else:
        cmseq = ['Blues', 'Greens', 'Reds', 'winter', 'RdPu', 'autumn']
        cmdelta = 10

    gcv = lambda cmap, i: plt.get_cmap(cmap)((256 - cmdelta * i) / 256)

    xdata = data['t']
    for group in tracegroups:
        grp = tracegroups[group]
        #reinitialize tracecells labels, ydatas, colors to empty lists
        for trace in tracecells:
            tracecells[trace]['labels'], tracecells[trace]['ydatas'], tracecells[trace]['colors'] = [], [], []

        cmsi = 0
        for key in keys:
            # traces for specific group - [labels, ydatas]
            if grp['rgx'].search(key):
                for cell in data[key]:
                    # filter out specific cells.
                    id = int(cell[5:])
                    for trace in tracecells:
                        if grp['conds'](id) and tracecells[trace]['conds'](id):
                            tracecells[trace]['labels'].append("%s:%s" % (cell, key))
                            tracecells[trace]['ydatas'].append(data[key][cell])
                            tracecells[trace]['colors'].append(gcv(cmseq[cmsi], id))
                cmsi = (cmsi + 1) % len(cmseq)
        for trace in tracecells:
            trc = tracecells[trace]
            if trc['ydatas']:
                print("plotting data: %s:%s:%s" %(group, trace, trc['labels']))
                plot_data(title="%s_%s" % (group, trace), xaxis=grp['xaxis'], yaxis=grp['yaxis'], labels=trc['labels'],
                          xdatas=xdata, ydatas=trc['ydatas'], colors=trc['colors'])

def plot_data(xdatas=[[0]], ydatas=[[0]], labels=None, prefix='data/', title='title', xaxis='xlabel', yaxis='ylabel', colors=None):
    # if y is a single data series, only plot it.
    if not hasattr(ydatas[0], '__iter__'):
        ydatas = [ydatas]
    # use default colormap 'C0' through 'C9'
    if not colors:
        colors = ["C%i" %(i%10) for i in range(len(ydatas))]
    fig, ax = plt.subplots(figsize=(12, 9))

    ax.set_title(title)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.ticklabel_format(useOffset=False, style='plain')

    if hasattr(xdatas[0], '__iter__'):
        for xdata, ydata, color in zip(xdatas, ydatas, colors):
            ax.plot(xdata, ydata, color=color)
    else:
        for ydata, color in zip(ydatas, colors):
            ax.plot(xdatas, ydata, color=color)

    if labels:
        ax.legend(labels)

    ax.minorticks_on()
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    plt.margins(x=0, y=0.0125)
    plt.savefig("%s%s.png" %(prefix, title), bbox_inches='tight', pad_inches=0.075)

    plt.cla()
    plt.clf()
    plt.close()
