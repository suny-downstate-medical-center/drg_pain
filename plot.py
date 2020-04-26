#plot function
import matplotlib.pyplot as plt

#tracegroups = {'current'  : {'rgx': re.compile('(NaV)|K')   , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' }}
#tracecells = {"vclamp": {'conds': lambda id: id == 0}}
#   plot_groups(data=sim.allSimData, keys=cfg.recordTraces.keys(), tracegroups=<see groups>, tracecells=<see cells>[, cmseq=<see sequence>, cmdelta=<integer>, showmins=<True/False>, showmaxs=<True/False>])
def plot_groups(data               , keys                        , tracegroups             , tracecells            ,
                cmseq = ['Blues', 'Greens', 'Reds', 'winter', 'RdPu', 'autumn'], cmdelta = 10, showmins = False, showmaxs = False
                ):

    gcv = lambda cmap, i: plt.get_cmap(cmap)((256 - cmdelta * i) / 256)

    xdata = data['t']
    for group in tracegroups:
        grp = tracegroups[group]
        #reinitialize tracecells labels, ydatas, colors to empty lists
        for trace in tracecells:
            tracecells[trace]['labels'], tracecells[trace]['ydatas'], tracecells[trace]['colors'], tracecells[trace]['lines'] = [], [], [], []

        cmsi = 0
        for key in keys:
            # traces for specific group - [labels, ydatas]
            if grp['rgx'].search(key):
                for cell in data[key]:
                    # filter out specific cells.
                    id = int(cell[5:])
                    for trace in tracecells:
                        if grp['conds'](id) and tracecells[trace]['conds'](id):
                            trc = tracecells[trace]
                            ydata = data[key][cell]
                            hlines = []
                            trc['labels'].append("%s:%s" % (cell, key))
                            trc['ydatas'].append(ydata)
                            trc['colors'].append(gcv(cmseq[cmsi], id))
                            trc['lines'].append("-")
                            if showmins:
                                hlines.append([min(ydata)] * len(xdata))
                            if showmaxs:
                                hlines.append([max(ydata)] * len(xdata))
                            for hline in hlines:
                                trc['labels'].append("%s" %(hline[0]))
                                trc['ydatas'].append(hline)
                                trc['colors'].append('g')
                                trc['lines'].append(":")
                cmsi = (cmsi + 1) % len(cmseq)
        for trace in tracecells:
            trc = tracecells[trace]
            if trc['ydatas']:
                print("plotting data: %s:%s:%s" %(group, trace, trc['labels']))
                plot_data(title="%s_%s" % (group, trace), xaxis=grp['xaxis'], yaxis=grp['yaxis'], labels=trc['labels'],
                          xdatas=xdata, ydatas=trc['ydatas'], colors=trc['colors'], lines=trc['lines'])

def plot_data(xdatas=[[0]], ydatas=[[0]], labels=None, prefix='data/', title='plot', xaxis='time (ms)', yaxis='ylabel', colors=None, lines=None):
    # if y is a single data series, only plot it.
    if not hasattr(ydatas[0], '__iter__'):
        ydatas = [ydatas]
    # if x is only a single data series, use it for all y's
    if not hasattr(xdatas[0], '__iter__'):
        xdatas = [xdatas] * len(ydatas)
    # use default colormap 'C0' through 'C9'
    if not colors:
        colors = ["C%i" %(i%10) for i in range(len(ydatas))]
    fig, ax = plt.subplots(figsize=(12, 9))
    if not lines:
        lines = ['-' for i in range(len(ydatas))]

    ax.set_title(title)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.ticklabel_format(useOffset=False, style='plain')

    for xdata, ydata, color, line in zip(xdatas, ydatas, colors, lines):
        ax.plot(xdata, ydata, color=color, linestyle=line)

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
