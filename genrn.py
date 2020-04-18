'''
c neuron
generic neuron model containing t-junction morphology--
peripheral fiber, drg with soma, central fiber
properties taken from Waxman
'''
from neuron import h

# section morphologies
#        sec         dimensions
# from tjunction paper
#secs = {'axnperi': {'nseg':100, 'L':5000, 'diam': 0.8 },
#        'drgperi': {'nseg':100, 'L':100,  'diam': 0.8 },
#        'drgstem': {'nseg':100, 'L':75,   'diam': 1.4 },
#        'drgsoma': {'nseg':1,   'L':25,   'diam': 25  },
#        'drgcntr': {'nseg':100, 'L':100,  'diam': 0.4 },
#        'axncntr': {'nseg':100, 'L':5000,  'diam': 0.4 }}

# our values:
# nseg with frequency<50, d_lambda 0.1
# use cal_nseg(sec, 50, 0.1) for values
secs = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8 },
        'drgstem': {'nseg':3,   'L':75,    'diam': 1.4 },
        'drgsoma': {'nseg':1,   'L':30,    'diam': 23  },
        'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4 }}

# section mechanisms
mechs = {'nav17': {'gnabar': 0.018 },
         'nav18': {'gnabar': 0.026 },
         'kdr'  : {'gkbar' : 0.0035},
         'ka'   : {'gkbar' : 0.0055},
         'pas'  : {'g': 5.75e-5, 'e': -58.91}}

# ion reversal potentials
ions  = {'na':  67.1,
         'k' : -84.7 }

# section properties
props = {'cm': 1.2,
         'Ra': 123}

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

class genrn():

    def __init__(self,x=0,y=0,z=0,ID=0,
                 secs  = secs,
                 props = props,
                 mechs = mechs,
                 ions  = ions,
                 cons  = cons):

        self.tags = {'all': []}
        # secs -> pointer
        self.secs = self.tags['all']
        self.init_morphology(secs)
        self.set_props('all', props)
        self.insert_mechs('all', mechs, ions)        
        self.connect_secs(cons)

    def init_morphology(self, secs):
        for sec in secs:
            self.add_comp(sec, sec[0:3], 'all')
            self.set_geom(sec = sec, **secs[sec])

    def add_comp(self, sec, *tags):
        sec_ = h.Section(name=sec)
        # sec_ -> pointer
        self.__dict__[sec] = sec_
        for tag in tags:
            try:
                self.tags[tag].append(sec_)
            except:
                self.tags[tag] = [sec_]

    def set_geom(self, sec, L, diam, nseg):
        self.__dict__[sec].L    = secs[sec]['L']
        self.__dict__[sec].diam = secs[sec]['diam']
        self.__dict__[sec].nseg = secs[sec]['nseg']

    def set_props(self, tag, props):
        for sec in self.tags[tag]:
            for prop in props:
                setattr(sec, '%s' %(prop), props[prop])

    def fset_prop(self, sec, prop, func):
        #set properties of the segment, diam
        for seg in sec:
            val = func(seg.x)
            setattr(seg, prop, val)

    def insert_mechs(self, tag, mechs, ions):
        for sec in self.tags[tag]:
            for mech in mechs:
                sec.insert(mech)
                for param in mechs[mech]:
                    setattr(sec, '%s_%s' %(param, mech), mechs[mech][param])
            for ion in ions:
                setattr(sec, 'e%s' %(ion), ions[ion])

    def fset_mech(self, sec, mech, param, func):
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
            setattr(sec, '%s_%s' %(param, mech), value)

    def fedit_mechs(self, tag, mech, param, func):
        for sec in self.tags[tag]:
            for seg in sec:
                val = func(seg.x)
                setattr(seg, '%s_%s' %(param, mech), val)

    def get_dict(self, tag = 'all'):
        rpr = {}
        for sec in self.tags[tag]:
            rpr[sec] = sec.psection()
        return rpr

    def __gt__(self, tag):
        #retrieve sections in a tag using '>' operator (i.e. self>'all')
        return self.tags[tag]

    def __call__(self, item):
        #can do self(tag) to return sections associated with string or self(index) to return a section at index
        try:
            return self.tags[item]
        except:
            return self.secs[item]

    def __getitem__(self, item):
        #indices for sections (sections stored in order of creation)
        return self.secs[item]

    def __repr__(self):
        #printing a shows consolidated information about class
        rpr = ''
        for sec in self.secs:
            r = sec.psection()
            rpr += '%s\n' %(sec)
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

