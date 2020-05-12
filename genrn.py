'''
generic neuron modelling class

calling from python calls genrn with t-junction electrophysiology and morphology--
peripheral fiber, drg with soma, central fiber
properties taken from Waxman
'''
from neuron import h
import logging as lgg
import re

class gesec():

    def __init__(self, name='sec', ions={'na': 58, 'k': -92, 'ca': -129, 'cl': -89}):
        self.name  = name
        self.sec   = h.Section(name=name)
        self.mechs = []
        self.pps   = []
        self.ions  = {}
        for ion in ions:
            self.ions[ion] = {'e': ions[ion], 'mechs': []}
        self.insert = self.im = self.insert_mech
        self.ims = self.insert_mechs
        self.gm = self.get_mechs
        self.gs = self.get_sec

    def insert_mechs(self, mechs, *mmechs):
        if isinstance(mechs, str):
            self.insert_mech(mechs)
            for mech in mmechs:
                self.insert_mech(mech)
        else:
            for mech in mechs:
                if 'ions' not in mech and 'params' not in mech:
                    self.insert_mech(mech, params = mechs[mech])
                else:
                    mech = mechs[mech]
                    if 'ions' not in mech: mech['ions'] = {}
                    if 'params' not in mech: mech['params'] = {}
                    self.insert_mech(mech, mechs[mech]['ions'], mechs[mech]['params'])

    def insert_mech(self, mech, ions = {}, params = {}):
        # TODO ->DONE does sec.insert(mech) insert mech if the mechanism already exists in section?
        # answer from NEURON: it shouldn't
        # if not self.sec.has_membrane(mech):
        #     self.sec.insert(mech)
        self.sec.insert(mech)
        self.mechs.append(mech)
        islst = isinstance(ions, (list, set, tuple))
        # use list, set, tuple or dictionary.
        for ion in ions:
            if ion not in self.ions:
                if islst: self.ions[ion] = {'e': False, 'mechs': []}
                else: self.ions[ion] = {'e': ions[ion], 'mechs': []}
            if islst: pass
            else:
                # post is the Nernst potential.
                post = ions[ion]
                if hasattr(self.sec, 'e%s' %(ion)) & post:
                    pre = getattr(self.sec, 'e%s' %(ion))
                    if (pre != post):
                        lgg.info("Note: replacing Nernst potential %s mV -> %s mV" %(pre, post))
                        setattr(self.sec, 'e%s' %(ion), post)
        for param in params:
            # if there is a function for the parameter, call it
            if not callable(params[param]): setattr(self.sec, '%s_%s' %(param, mech), params[param])
            else: self.fset_mech(mech, param, params[param])
        # add mech to any ionlist
        for ion in self.ions.keys():
            if hasattr(self.sec, "i%s_%s" %(ion, mech)):
                self.ions[ion]['mechs'].append(mech)

    def fset_mech(self, mech, param, func):
        for seg in self.sec:
            val = func(seg.x)
            setattr(seg, '%s_%s' %(param, mech), val)

    def set_props(self, props):
        for prop in props:
            if callable(props[prop]):
                self.fset_prop(self.sec, prop, props[prop])
            else:
                setattr(self.sec, '%s' %(prop), props[prop])

    def fset_prop(self, prop, func):
        #set properties of the segment, diam
        for seg in self.sec:
            val = func(seg.x)
            setattr(seg, prop, val)

    def get_mechs(self):
        return self.mechs

    def set_nernsts(self):
        # set Nernst for all ions
        for ion in self.ions:
            post = self.ions[ion]['e']
            if post and hasattr(self.sec, "e%s" %(ion)):
                pre = getattr(self.sec, 'e%s' % (ion))
                if (pre != post):
                    lgg.info("Note: replacing Nernst potential %s mV -> %s mV" % (pre, post))
                    setattr(self.sec, 'e%s' % (ion), post)

    def get_sec(self):
        return self.sec

    def __lt__(self, mechs):
        self.insert_mechs(mechs)

    def __call__(self, item):
        return self.sec(item)

#    def __iter__(self):
#    def __next__(self):
#    def __getitem__(self, item):

class genrn():

    def __init__(self,x=0,y=0,z=0,ID=0,v_init=None,
                 secs  = {'genrn': {}},
                 mechs = {},
                 ions  = {},
                 cons  = ()):
        self.tags = {'all': []}
        # secs -> pointer
        self.secs = {}
        self.gesecs = self.tags['all']
#        self.useions = re.compile("USEION ([A-Za-z0-9]+)")
        self.init_cell(secs, ions)
        self.initialize_mechs('all', mechs, ions)
        self.connect_secs(cons)
        self.v_init = v_init

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
            self.add_comp(sec, ions, sec[0:3])
            self.set_props(sec = sec, props = secs[sec])

    def add_comp(self, sec, ions, *tags):
        sec_ = gesec(sec, ions)
        # sec_ -> pointer
        self.secs[sec] = (sec_)
        self.tags['all'].append(sec_)
        self.__dict__[sec] = sec_.sec
        for tag in tags:
            try: self.tags[tag].append(sec_)
            except: self.tags[tag] = [sec_]

    def set_props(self, sec, props):
        sec = self.return_gesec(sec)
        sec.set_props(props)

    def tag_set_props(self, tag, props):
        for sec in self.tags[tag]:
            for prop in props:
                setattr(sec.sec, '%s' %(prop), props[prop])

    def fset_prop(self, sec, prop, func):
        sec = self.return_gesec(sec)
        #set properties of the segment, diam
        sec.fset_prop(prop, func)

    def insert_mech(self, sec, mech, ions={}, params={}):
        sec = self.return_gesec(sec)
        sec.insert_mech(mech, ions, params)

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
        sec = self.return_gesec(sec)
        sec.fset_mech(mech, param, func)

    def connect_secs(self, cons):
        for con in cons:
            try:
                exestr = 'self.%s.connect(self.%s)' %(con[0], con[1])
                exec(exestr)
                lgg.info('%s[1] -> %s[0]' %(con[1], con[0]))
            except:
                lgg.info('failed to connect: %s[1] -> %s[0]' %(con[1], con[0]))

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

# additional not called init functions
    def init_nernsts(self):
        for sec in self.secs:
            self.secs[sec].set_nernsts()


    def init_pas(self, v_init, set_pas = False):
        e = {}
        h.finitialize(v_init)
        h.fcurrent()
        i_net = 0
        lgg.info("fcurrent() values (%s mV)" %(v_init))
        for sec in self.secs:
            for mech in sec.mechs:
                for ion in sec.ions:
                    try:
                        i = getattr(sec.sec, 'i%s_%s' %(ion, mech))
                        lgg.info("(%s)->%s:->%s=%s mA/cm2" %(sec.name, mech, ion, i))
                        i_net += i
                    except: pass
            lgg.info("(%s)->i_net = %s" %(sec.name, i_net))
            try:
                e_pas = sec.sec.v + i_net / sec.g_pas
                lgg.info("(%s)->e_pas calculated at %s mV" %(e_pas))
                if set_pas:
                    sec.sec.e_pas = e_pas
            except: pass

## OoOP: indexing>function>unary>power>mul>add>bitshift>and>xor>or>gt
    def __truediv__(self, item):
        return self.secs[item]

    def __gt__(self, item):
        #retrieve gesec objects in a tag using '>' operator, by tag or section name (i.e. self>'all')
        try: return self.tags[item]
        except KeyError: return self.secs[item]


    def __rshift__(self, tag):
        #retrieve section objects in a tag using '>>' operator (i.e. self>>'all)
        return [sec.sec for sec in self.tags[tag]]

    def __call__(self, item):
        #returns the gesec items of a specific tag
        try: return self.tags[item]
        except KeyError: return self.secs[item]

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
if __name__ == '__main__':# section morphologies
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

    args = {'secs': secs, 'mechs': mechs, 'ions': ions, 'cons': cons}
    test = genrn(**args)
    print(test.get_dict())
