'''
c neuron
generic neuron model containing t-junction morphology--
peripheral fiber, drg with soma, central fiber
properties taken from Waxman
'''
from neuron import h
import re
# section morphologies
#        sec         dimensions
# from tjunction paper
#secs = {'axnperi': {'nseg':100, 'L':5000, 'diam': 0.8, 'cm': 1.2, 'Ra': 123 },
#        'drgperi': {'nseg':100, 'L':100,  'diam': 0.8, 'cm': 1.2, 'Ra': 123 },
#        'drgstem': {'nseg':100, 'L':75,   'diam': 1.4, 'cm': 1.2, 'Ra': 123 },
#        'drgsoma': {'nseg':1,   'L':25,   'diam': 25 , 'cm': 1.2, 'Ra': 123 },
#        'drgcntr': {'nseg':100, 'L':100,  'diam': 0.4, 'cm': 1.2, 'Ra': 123 },
#        'axncntr': {'nseg':100, 'L':5000, 'diam': 0.4, 'cm': 1.2, 'Ra': 123 }}

# our values:
# nseg with frequency<50, d_lambda 0.1
# use cal_nseg(sec, 50, 0.1) for values
# props for the sections
secs = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8, 'cm': 1.2, 'Ra': 123 },
        'drgstem': {'nseg':3  , 'L':75  ,  'diam': 1.4, 'cm': 1.2, 'Ra': 123 },
        'drgsoma': {'nseg':1  , 'L':30  ,  'diam': 23 , 'cm': 1.2, 'Ra': 123 },
        'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4, 'cm': 1.2, 'Ra': 123 }}

# section mechanisms
mechs = {'nav17m' : {'gnabar': 0.018 },
         'nav18m' : {'gnabar': 0.026 },
         'kdr'    : {'gkbar' : 0.0035},
         'ka'     : {'gkbar' : 0.0055},
         'pas'    : {'g': 5.75e-5, 'e': -58.91}}

# ion reversal potentials
ions  = {'na':  67.1,
         'k' : -84.7 }

# connection list

#------------------------------------------------------------#
#                                                            #
#           What the morphology looks like (paper)           #
#                            [1]                             #
#                          drgsoma                           #
#                            [0]                             #
#                            [1]                             #
#                          drgstem                           #
#                            [0]                             #
# [0]anxperi[1]-[0]drgperi[1]-^-[0]drgscntr[1]-[0]axncntr[1] #
#                                                            #
#              ^                              ^              #
#              |     axon initial segment     |              #
#                                                            #
#------------------------------------------------------------#
#            0    ->    1

#cons = (('drgperi', 'axnperi'),
#        ('axncntr', 'drgcntr'),
#        ('drgstem', 'drgperi'),
#        ('drgsoma', 'drgstem'),
#        ('drgcntr', 'drgperi'))

# simplified connection list
cons = (('drgstem', 'drgperi'),
        ('drgsoma', 'drgstem'),
        ('drgcntr', 'drgperi'))
class gesec():

    def __init__(self, name='sec', ions=['na', 'k', 'ca', 'cl']):
        self.sec   = h.Section(name=name)
        self.mechs = []
        self.pps   = []
        self.ions  = {}
        for ion in ions:
            self.ions[ion] = []
        self.insert = self.im = self.insert_mech
        self.gm = self.get_mechs
        self.gs = self.get_sec

    def insert_mech(self, mech, ions = {}):
        self.sec.insert(mech)
        self.mechs.append(mech)
        for ion in ions:
            if ion not in self.ions:
                self.ions[ion] = []
        for ion in self.ions:
            if hasattr(self.sec, "i%s_%s" %(ion, mech)):
                self.ions[ion].append(mech)

    def get_mechs(self, mech):
        return self.mechs

    def get_sec(self):
        return self.sec

    def __call__(self, item):
        return self.sec(item)

#    def __iter__(self):
#    def __next__(self):
#    def __getitem__(self, item):

class genrn():

    def __init__(self,x=0,y=0,z=0,ID=0,
                 secs  = {},
                 mechs = {},
                 ions  = {},
                 cons  = ()):

        self.tags = {'all': []}
        # secs -> pointer
        self.secs = {}
#        self.useions = re.compile("USEION ([A-Za-z0-9]+)")
        ionstrs = ions.keys()
        self.init_cell(secs, ionstrs)
        self.initialize_mechs('all', mechs, ions)
        self.connect_secs(cons)

    def return_sec(self, sec):
        if isinstance(sec, type(h.Section())): return sec
        elif isinstance(sec, str): return self.secs[sec].sec
        elif isinstance(sec, type(gesec())): return sec.sec
        raise TypeError

    def return_gesec(self, sec):
        if isinstance(self, type(h.Section())): return self.secs[sec.name]
        elif isinstance(sec, str): return self.secs[sec]
        elif isinstance(sec, type(gesec())): return sec
        raise TypeError

    def init_cell(self, secs, ions):
        for sec in secs:
            self.add_comp(sec, ions, sec[0:3], 'all')
            self.set_props(sec = sec, props = secs[sec])

    def add_comp(self, sec, ions, *tags):
        sec_ = gesec(sec, ions)
        # sec_ -> pointer
        self.secs[sec] = sec_
        self.__dict__[sec] = sec_.sec
        for tag in tags:
            try:
                self.tags[tag].append(sec_)
            except:
                self.tags[tag] = [sec_]

    def set_props(self, sec, props):
        sec = self.return_sec(sec)
        for prop in props:
            setattr(sec, prop, props[prop])

    def tag_set_props(self, tag, props):
        for sec in self.tags[tag]:
            for prop in props:
                setattr(sec.sec, '%s' %(prop), props[prop])

    def fset_prop(self, sec, prop, func):
        sec = self.return_sec(sec)
        #set properties of the segment, diam
        for seg in sec:
            val = func(seg.x)
            setattr(seg, prop, val)

    def insert_mech(self, sec, mech, ions):
        sec = self.return_gesec(sec)
        sec.insert(mech, ions)
        for ion in ions:
            setattr(sec.sec, 'e%s' %(ion), ions[ion])

    def initialize_mechs(self, tag, mechs, ions):
        for sec in self.tags[tag]:
            for mech in mechs:
                sec.insert(mech)
                for param in mechs[mech]:
                    setattr(sec.sec, '%s_%s' %(param, mech), mechs[mech][param])
            for ion in ions:
                try: setattr(sec.sec, 'e%s' %(ion), ions[ion])
                except: pass

    def fset_mech(self, sec, mech, param, func):
        sec = self.return_sec(sec)
        for seg in sec:
            val = func(seg.x)
            setattr(seg, '%s_%s' %(param, mech), val)

    def connect_secs(self, cons):
        for con in cons:
            try:
                exestr = 'self.%s.connect(self.%s)' %(con[0], con[1])
                exec(exestr)
                print('%s[1] -> %s[0]' %(con[1], con[0]))
            except:
                pass

    def edit_mechs(self, tag, mech, param, value):
        for sec in self.tags[tag]:
            setattr(sec.sec, '%s_%s' %(param, mech), value)

    def tag_fedit_mechs(self, tag, mech, param, func):
        for sec in self.tags[tag]:
            for seg in sec.sec:
                val = func(seg.x)
                setattr(seg, '%s_%s' %(param, mech), val)

    def get_dict(self, tag = 'all'):
        rpr = {}
        for sec in self.tags[tag]:
            rpr[sec.sec] = sec.sec.psection()
        return rpr

    def __gt__(self, tag):
        #retrieve gesec objects in a tag using '>' operator (i.e. self>'all')
        return self.tags[tag]

    def __rshift__(self, tag):
        #retrieve section objects in a tag using '>>' operator (i.e. self>>'all)
        return [sec.sec for sec in self.tags[tag]]

    def __call__(self, item):
        #returns the gesec items of a specific tag
        try:
            return self.tags[item]
        except KeyError:
            return self.secs[item]

    def __getitem__(self, item):
        #indices for sections (sections stored in order of creation)
        return self.tags['all'][item].sec

    def __repr__(self):
        #printing a shows consolidated information about class
        rpr = ''
        for sec in self.tags['all']:
            r = sec.sec.psection()
            rpr += '%s\n' %(sec.sec.name())
            rpr += 'parent:\t%s\n' %(r['morphology']['parent'])
            rpr += 'morphology:\tL:%f\tdiam:%f\n' %(r['morphology']['L'], max(r['morphology']['diam']))
            rpr += 'mechs:\t%s\n\n' %(list(r['density_mechs'].keys()))
        return rpr

def cal_nseg( sec, freq, d_lambda ):
#neuron+python of https://www.neuron.yale.edu/neuron/static/docs/d_lambda/d_lambda.html
    nseq = lambda fc_: int((sec.L / (d_lambda * fc_) + 0.9) / 2) * 2 + 1
    fpfrc = 4 * h.PI * freq * sec.Ra * sec.cm
    h.define_shape()
    fc = 0
    n3d = sec.n3d()
    if n3d < 2:
        fc = 1e5 * h.sqrt(sec.diam / (fpfrc))
        return nseq(fc)

    x1 = sec.arc3d(0)
    d1 = sec.diam3d(0)

    for i in range(n3d):
        x2 = sec.arc3d(i)
        d2 = sec.diam3d(i)
        fc += (x2 - x1) / h.sqrt(d1 + d2)
        x2 = x1
        d2 = d1

    fc *= h.sqrt(2) * 1e-5 * h.sqrt(fpfrc)
    return nseq(sec.L/fc)

# for debugging
if __name__ == '__main__':
    args = {'secs': secs, 'mechs': mechs, 'ions': ions, 'cons': cons}
    test = gesec(**args)
    print(test.get_dict())
