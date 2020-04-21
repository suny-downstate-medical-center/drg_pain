#plot function
import matplotlib.pyplot as plt

def plot_data(xdatas=[[0]], ydatas=[[0]], labels=None, prefix='data/', title='title', xaxis='xlabel', yaxis='ylabel'):
    if not hasattr(ydatas[0], '__iter__'):
        ydatas = [ydatas]

    fig, ax = plt.subplots(figsize=(12, 9))

    ax.set_title(title)
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)

    if hasattr(xdatas[0], '__iter__'):
        for xdata, ydata in zip(xdatas, ydatas):
            ax.plot(xdata, ydata)
    else:
        for ydata in ydatas:
        ax.plot(xdatas, ydatas)

    if labels:
        ax.legend(labels)

    ax.minorticks_on()
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    plt.margins(x=0, y=0.0125)
    plt.savefig("%s%s.png" %(prefix,data), bbox_inches='tight', pad_inches=0.075)

    plt.cla()
    plt.clf()
    plt.close()
