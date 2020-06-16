"""
Code to handle save data from netpyne
"""

import json
import pickle
import numpy as np
import re

_lfc = {
    'pkl': lambda fp: pickle.load(fp)
    'json': lambda fp: json.load(fp)
}

class data():
    def __init__(self, output = 'analysis/', delim = '_'):
        self.output = output
        self.data = {}
        self.delim = delim

    def load_data(self, filename, filetype = None, prepend = None):
        if not prepend:
            prepend = "%s%s" %(filename)
        if not filetype:
            filetype = re.split('.', filename)[1]
        try:
            _lfc[filetype](filename)
                data
        except:
            return False
        data = _lfc[filetype](fp)
        self.load_simData(data)
        return True
        
    def load_pkl(self, filename, prepend = None):
        if not prepend:
            prepend = "%s%s" %(filename)
        try:
            with open(filename, 'rb') as fp:
                data = pickle.load(fp)
        except:
            return False
        self.load_simData(data) 
        return True

    def load_simData(self, data):
        self.data[prepend] = data
        for key in data['simData']:
            if isinstance(data['simData'][key], dict):
                for cell in data['simData'][key]:
                    cellid = int(re.split('_', cell)[1])
                    pop = data['net']['cells'][cellid]
                    self.data['%s%s%s%s%s%s%s' %(prepend, self.delim, pop, self.delim, cellid, self.delim, key)] = data['simData'][key][cell]
            else:
                self.data['%s%s%s' %(prepend, self.delim, key)] = self.data['simData'][key]
        
    def group_traces(self, gfunction):
        group = {}
        for key in self.data:
            if gfunction(key):
                group[key] = self.data[key]
        return group