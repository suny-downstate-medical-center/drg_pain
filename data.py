"""
Code to handle save data from netpyne
"""

import json
import pickle
import numpy as np
import re
from itertools import product


class DataHandler():
    def __init__(self, output='analysis/', delim='_'):
        self.output = output
        self.data = {}
        self.traces = {}
        self.delim = delim
        self.dotre = re.compile('\.')
        self.usre = re.compile('_')
        self.delimre = re.compile(re.escape(delim))

    def load_file(self, filename, prepend=None, filetype=None):
        splitarr = self.dotre.split(filename)
        if not prepend:
            prepend = splitarr[0]
        if not filetype:
            filetype = splitarr[1]
        try:
            if filetype == 'pkl':
                fp = open(filename, 'rb')
                data = pickle.load(fp)
            elif filetype == 'json':
                fp = open(filename, 'r')
                data = json.load(fp)
            else:
                return False
        except Exception as exstr:
            print(exstr)
            return False
        self.load_npnData(data, prepend)
        return True

    def load_npnData(self, data, prepend):
        self.data[prepend] = data
        for key in data['simData']:
            if isinstance(data['simData'][key], dict):
                for cell in data['simData'][key]:
                    cellid = int(self.usre.split(cell)[1])
                    pop = data['net']['cells'][cellid]['tags']['pop']
                    # self.data['%s%s%s%s%s' %(prepend, self.delim, pop, self.delim, key)] = np.array(data['simData'][key][cell])
                    self.traces['%s%s%s%s%s' % (prepend, self.delim, pop, self.delim, key)] = np.array(
                        data['simData'][key][cell])
            else:
                self.data['%s%s%s' % (prepend, self.delim, key)] = data['simData'][key]

    def filter_traces(self, filter):
        group = {}
        if isinstance(filter, str):
            filterre = re.compile(filter)
            for key in self.traces:
                if filterre.search(key): group[key] = self.traces[key]
        elif isinstance(filter, re.Match):
            for key in self.traces:
                if filter.search(key): group[key] = self.traces[key]
        elif callable(filter):
            for key in self.traces:
                if filter(key): group[key] = self.traces[key]
        return group

    def keys(self):
        return {'data': self.data.keys(), 'traces': self.traces.keys()}

    def __getitem__(self, item):
        if item in self.data: return self.data[item]
        if item in self.traces: return self.traces[item]
        return self.filter_traces(item)

    def __call__(self, filename, prepend=None, filetype=None):
        return self.load_file(filename, prepend, filetype)


    def return_arr(self, ixsre, get_val=lambda x: x):
        if isinstance(ixsre, str): ixsre = re.compile(ixsre)
        arr = {}
        for key in self.traces:
            mobj = ixsre.search(key)
            if mobj:
                val = get_val(self.traces[key])
                tmparr = arr
                for ix in mobj.groups():
                    ix = float(ix)
                    if ix not in tmparr: tmparr[ix] = {}
                    otmparr = tmparr
                    tmparr = tmparr[ix]
                otmparr[ix] = {'key': key, 'val': val}
        return arr

if __name__ == "__main__":
    dh = DataHandler()
    dh('data/n1p7.json', 'n1p7')
    ixsre = re.compile('mn1p7:(...).*(.....)nAx(...)ms.*_terminal')
    arr = dh.return_arr(ixsre, lambda x: x.max())
