#usage:
#from analysis import analysis
#a0 = analysis(<<input file>>, <<output string>>)
#a0.set_window(<<start time (ms)>>, <<stop time (ms)>>)
#a0.plot_traces(<<title>>, <<y unit>>, <<variable string>>)

import json
import pickle
import csv
import numpy as np
import re
import matplotlib.pyplot as plt
#from batch_cfg import cfg
from cfg import cfg

class analysis():
    def __init__(self, output = "analysis/"):
        self.data = {}
        self.dt   = cfg.recordStep
        self.labels = [ '0' ]
        self.xdatas = [ [0] ]
        self.ydatas = [ [0] ]
        self.spikes = {}
        self.fexist = False
        self.set_window( 0 , cfg.duration )
        self.output = output
        self.cells  = {}
        self.cell   = '' 
    
    def load_json(self, filename):
        data = {}
        self.fexist = True
        try:
            with open(filename, 'r') as fp:
                jdata = json.load(fp)
                for var in jdata['simData']:
                    try:
                        cells = jdata['simData'][var].keys() 
                        #handle multiple cells
                        for cell in cells:
                            #for now get the cell id
                            cellid = int(cell[5:])
                            if cellid in self.cells:
                                self.cells[cellid]["%s" %(var)] = np.array(jdata['simData'][var][cell])
                            else:
                                self.cells[cellid] = {"%s" %(var): np.array(jdata['simData'][var][cell])}
                            print("succeeded load: var %s (%i points of data)" %(var, len(data[var])))
                    except:
                        data["%s" %(var)] = np.array(jdata['simData'][var])
        except:
            print("error retrieving json")
            self.fexist = False
        self.data = data

    def load_pkl(self, filename):
        data = {}
        self.fexist = True


    def load_csv(self, filename):
    # import data from a csv (engauge with older trace data)
        data = {}
        try:
            with open(filename) as fp:
                ri = csv.reader(fp)
                keys = next(ri)
                for key in keys:
                    data[key] = []
                    # working with arrays is faster.
                for line in ri:
                    for i, val in enumerate(line):
                        data[keys[i]].append(float(val))
                for key in keys:
                    self.data[key] = np.array(data[key])
        except:
            print("file not found")
            return False
        for var in data.keys():
            print("succeeded load: var %s (%i points of data)" %(var, len(data[var])))
        return True

    def set_window(self, start, stop):
        self.start = self.get_index(start)
        self.stop  = self.get_index(stop)

    def rst_window(self):
        self.set_window(0, cfg.duration) 

    def get_index(self, time):
        return int(time / self.dt)

    def get_spike( self, trace = 'vs', movepast = 0 ):
        ydata = self.data[trace][self.start:self.stop]
        self.start += np.argmax(ydata) + int(movepast/self.dt)
        self.spikes[trace] = {  'peak': max(ydata),
                                'time': self.data['t'][self.start]  }
        return self.spikes[trace]

    def get_vel( self, start = 0, stop = cfg.duration, trx0 = 'cell_0v1', trx1 = 'cell_0v9', dx = 8000 * 1e-6):
        self.set_window(start, stop)
        vs   = self.get_spike(trx0)
        vf   = self.get_spike(trx1)
        # convert to seconds
        dt   = ( vf['time'] - vs['time'] ) * 1e-3
        if dt == 0:
            return False
        vel  = dx / dt
        return vel

    def plot_soma( self, start = 0, stop = cfg.duration, pre = -3, post = 12 ):
        self.set_window(start, stop)
        vs   = self.get_spike('cell_0vs')
        sstart = vs['time'] + pre
        sstop  = vs['time'] + post
        self.set_window(sstart, sstop)

        fig, axs = plt.subplots(2, 1, figsize=(12,9), sharex=True)

        ax0 = axs[0]
        ax1 = axs[1]
        fig.suptitle( "traces at soma" )
        #plot for soma specifically with subplots for voltage and current

        self.get_traces("0i")
        ax0.set_ylabel("current (ma/cm2)")
        for i, label in enumerate(self.labels):
            ax0.plot(self.xdata, self.ydatas[i], label = label)

        self.get_traces("0vs")
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("voltage (mv)")
#        ax1.set_title("soma")
        for i, label in enumerate(self.labels):
            ax1.plot(self.xdata, self.ydatas[i], label = label)
        
        plt.subplots_adjust(hspace=0)
        for ax in axs:
            ax.legend()
            ax.minorticks_on()
            ax.grid(which='major', linestyle='-')
            ax.grid(which='minor', linestyle=':')

        plt.margins(x = 0, y = 0.0125)
        plt.savefig( self.output + "soma.png", bbox_inches = 'tight', pad_inches = 0.075)

        plt.cla()
        plt.clf()
        plt.close()

        self.plot_traces(title = "soma(v)", yu = "mv", idstr = "0vs")
        self.plot_traces(title = "soma(i)", yu = "ma/cm2" , idstr = '0i')

    def get_propts( self ):
        propts = {}
        propts['soma_pkv'] = max(self.data['vs'])
        propts['soma_pkt'] = self.data['t'][np.argmax(self.data['vs'])]
        propts['soma_ahp'] = min(self.data['vs'])
        return propts

    def plot_data( self, title = "title", xaxis = "xlabel", yaxis = "ylabel", labels = ['0'], xdatas = [ [0] ], ydatas = [ [0] ] ):
        fig, ax = plt.subplots(figsize=(12,9))
        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.set_title(title)

        for i, label in enumerate(labels):
            ax.plot(xdatas[i], ydatas[i], label = label)

        ax.legend()
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-')
        ax.grid(which='minor', linestyle=':')

        plt.margins(x = 0, y = 0.0125)
        plt.savefig( self.output + title + ".png", bbox_inches = 'tight', pad_inches = 0.075)

        plt.cla()
        plt.clf()
        plt.close()

    def plot_traces( self, title = "current", yu = "ma/cm2", idstr = "i" ):
        self.get_traces(idstr)
        self.plot_data( title, "time (ms)", "%s (%s)" %(title, yu), self.labels, [self.xdata] * len(self.labels), self.ydatas )

    def get_traces( self, idstr = 'i'):
        sstr = re.compile(idstr)
        labels = [key for key in self.data.keys() if re.search(sstr, key)]
        xdata  = self.data['t'][self.start:self.stop]
        ydatas = [self.data[i][self.start:self.stop] for i in labels ]
        bounds = {}
        for i, label in enumerate(labels):
            bounds[label] = [min(ydatas[i]), max(ydatas[i])]
        
        self.labels = labels
        self.xdata  = xdata
        self.ydatas = ydatas
        return bounds

    def find_where(self, trace = 'vc', value = -30):
        # look for recurrences of a value up to certain precision. 
        gt = self.data[trace] > value
        return np.where(np.bitwise_xor(gt[1:], gt[:-1]))[0]
#        wixs = np.where( self.data[trace] >= value )[0]
#        # for adjacent values, get the closest one
#        edgs = [True] + (np.diff(wixs) > 1).tolist()
#        # have to convert to list anyways (why though)
#        #edgs[-1] = True
#        ixs  = wixs[edgs]
#        return ixs, wixs, edgs
        
    def find_argmax(self, trace = 'vc', threshold = -30):
        # look for when a trace paces threshold for first time. 
        pix = np.argmax(self.data[trace] >= threshold)
        if self.data[trace][pix] - threshold <= threshold - self.data[trace][pix-1]:
            return pix
        else:
            return pix-1

    def compare_traces(self, te, ye, ys, match):
        #function to compare experimental trace described by xe, ye
        #to simulation trace 
        #function to match times in t closest to dt interval
        cli = lambda x, dx: ( int(x/dx) + ( (x%dx > dx/2) ) )
        #move time vector to start at 0
        t0tv = self.data[te] - self.data[te][0]
        #remap to closest index of trace1
        t0iv = np.array([cli(t, self.dt) for t in t0tv])


        #displace traces to start at similar times based on AP crossing a value.
        
        #get the indexes where both traces are closest to match using argmax function
        #(faster of two)
        t0ixm = self.find_argmax(ye, match)
        t1ixm = self.find_argmax(ys, match)

        #reposition trace 1 window
        t0pre  = t0iv[t0ixm]
        t0post = t0iv[-1] - t0iv[t0ixm]
        
        #get window before and after threshold
        t1pre  = t1ixm - t0pre
        t1post = t1ixm + t0post

        #set window
        t1vv = self.data[ys][t1pre:t1post]
        
        #now we can do a comparison of both
        t0vv = self.data[ye]

        sdiff = 0

        for i, j in enumerate(t0iv):
            sdiff += abs(t0vv[i] - t1vv[j])

        t0tv = np.array([ x * self.dt for x in t0iv])
        t1tv = np.array([ x * self.dt for x in range(len(t1vv))])
        #for plotting purposes, return appropriate time vectors
        t0tv = [ i * self.dt for i in t0iv]
        t1tv = [ i * self.dt for i in range(t0iv[-1])]
        return {'diff':sdiff, 'x0':t0tv,  'y0':t0vv, 'x1':t1tv, 'y1':t1vv}
        #just reframe so both pass through the point at the same time.

def plot_data( title = "title", xaxis = "xlabel", yaxis = "ylabel", labels = ['0'], xdatas = [ [0] ], ydatas = [ [0] ] ):
    fig, ax = plt.subplots(figsize=(12,9))
    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)
    ax.set_title(title)
    for i, label in enumerate(labels):
        ax.plot(xdatas[i], ydatas[i], label = label)
    ax.legend()
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')
    plt.margins(x = 0, y = 0.0125)
    plt.savefig( title + ".png", bbox_inches = 'tight', pad_inches = 0.075)
    plt.cla()
    plt.clf()
    plt.close()


if __name__ == "__main__":
    an = analysis("adata/")
    an.load_json('cndct_0_0.json')
    print("velocity is %f m/s" %(an.get_vel()) )
    bounds = an.find_where('cell_0vs')
    an.plot_soma()
#    an.set_window(cfg.delay[0]-5, cfg.delay[-1]+25)
#    an.plot_traces( "voltage", "mv", "v")
#    an.plot_soma(cfg.delay[-1]-5, cfg.delay[-1]+25, -3, 7)
#
#    start = int( (cfg.delay[-1]  - 3) / cfg.recordStep )
#
#    print("RMP: %f" %(an.data['vs'][start]))
#
#    print(an.get_propts())