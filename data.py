"""
Code to handle save data from netpyne
"""

import json
import pickle
import numpy as np
import re

class data():
    def __init__(self, output = 'analysis/', delim = '_'):
        self.output = output
        self.data = {}
        self.delim = delim
        self.regex = {}

    def load_pkl(self, filename, prepend = None):
        if not prepend:
            prepend = "%s%s" %(filename)
        try:
            with open(filename, 'rb') as fp:
                data = pickle.load(fp)
        except:
            return False
        self.data[prepend] = data
        for key in data['simData']:
            if isinstance(data['simData'][key], dict):
                for cell in data['simData'][key]:
                    cellid = int(re.split('_', cell)[1])
                    pop = data['net']['cells'][cellid]
                    self.data['%s%s%s%s%s%s%s' %(prepend, self.delim, pop, self.delim, cellid, self.delim, key)] = data['simData'][key][cell]
            else:
                self.data['%s%s%s' %(prepend, self.delim, key)] = self.data['simData'][key]
        return True

    def create_regroup(self):
        re.compile()
    def group_traces(self, gfunction):
        for

