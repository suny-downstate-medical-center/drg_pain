'''
generic neuron modelling class

calling from python calls genrn with t-junction electrophysiology and morphology--
peripheral fiber, drg with soma, central fiber
properties taken from Waxman
'''
from neuron import h as h
import logging as lgg
#import re

def loose_set(object, attribute, value):
    try: 
        setattr(object, attribute, value)
        return True
    except: 
        print("%s.%s does not exist" %(object, attribute))
        return False

def loose_get(object, attribute):
    try: 
        return getattr(object, attribute)
    except: 
        print("%s.%s does not exist" %(object, attribute))
        return False

class gesec():

    def __init__(self, h=h, name='sec', ions={'na': 58, 'k': -92, 'ca': -129, 'cl': -89}):
        self.h=h
        self.name  = name
        self.sec   = self.h.Section(name=name)
        self.mechs = []
        self.pps   = {}
        self.ions  = {}
        # self.rgxions = {}
        for ion in ions:
            self.create_ion(ion, ions[ion])
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

    def insert_pp(self, pp, loc, ions = {}, params = {}):
        if pp not in self.pps:
            self.pps[pp] = {}
        if loc not in self.pps:
            self.pps[pp][loc] = []
        ppf = getattr(self.h, pp)
        ppo = ppf(self.sec(loc))
        for ion in ions:
            if ion not in self.ions:
                if isinstance(ions, dict): self.create_ion(ion, ions[ion])
                else: self.create_ion(ion, None)
                for prop in self.ions[ion]['props']:
                    if prop == 'e': loose_set(self.sec, 'e%s' %(ion), self.ions[ion]['props']['e'])
                    else: loose_set(self.sec, '%s%s' %(ion, prop), self.ions[ion]['props'][prop])
        for param in params:
            loose_set(ppo, param, params[param])
        self.pps[pp][loc].append(ppo)

    def create_ion(self, ion, props = None):
        iondict = {'mechs': [], 'props': {}}
        if isinstance(props, dict):
            iondict['props'] = props
        elif props:
            iondict['props']['e'] = props
        self.ions[ion] = iondict
        # self.rgxions[ion] = re.compile("USEION %s" %(ion))

    def insert_mech(self, mech, ions = {}, params = {}):
        # TODO ->DONE does sec.insert(mech) insert mech if the mechanism already exists in section?
        # answer from NEURON: it shouldn't
        # if not self.sec.has_membrane(mech):
        #     self.sec.insert(mech)
        self.sec.insert(mech)
        self.mechs.append(mech)
        # use list, set, tuple or dictionary.
        for ion in ions:
            if ion not in self.ions:
                if isinstance(ions, dict): self.create_ion(ion, ions[ion])
                else: self.create_ion(ion, None)
                for prop in self.ions[ion]['props']:
                    if prop == 'e': loose_set(self.sec, 'e%s' %(ion), self.ions[ion]['props']['e'])
                    else: loose_set(self.sec, '%s%s' %(ion, prop), self.ions[ion]['props'][prop])
        for param in params:
            # if there is a function for the parameter, call it
            if not callable(params[param]): loose_set(self.sec, '%s_%s' %(param, mech), params[param])
            else: self.fset_mech(mech, param, params[param])
        # add mech to any ionlist
        # Section object gets dereferenced and destroyed if there's a gc
        isec = self.h.Section()
        isec.insert(mech)
        iions = isec.psection()['ions'].keys()
        # version if using later versions of neuron, may not even be faster so just use psection instead
        # for ion in self.rgxions:
        #     if self.rgxions[ion].search(getattr(self.h, mech).code):
        #         self.ions[ion]['mechs'].append(mech)
        # less good version for earlier versions of neuron
        for ion in self.ions:
            if ion in iions:
                self.ions[ion]['mechs'].append(mech)

    def fset_mech(self, mech, param, func):
        for seg in self.sec:
            val = func(seg.x)
            loose_set(seg, '%s_%s' %(param, mech), val)

    def set_props(self, props):
        for prop in props:
            if callable(props[prop]):
                self.fset_prop(self.sec, prop, props[prop])
            else:
                loose_set(self.sec, '%s' %(prop), props[prop])

    def fset_prop(self, prop, func):
        # set properties of the segment, diam
        for seg in self.sec:
            val = func(seg.x)
            loose_set(seg, prop, val)

    def get_mechs(self):
        return self.mechs

    def set_ionprops(self):
        # set properties for all ions
        for ion in self.ions:
            for prop in self.ions[ion]['props']:
                if prop == 'e':
                    loose_set(self.sec, 'e%s' %(ion), self.ions[ion]['props'][prop])
                else:
                    loose_set(self.sec, '%s%s' %(ion, prop), self.ions[ion]['props'][prop])

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

    def __init__(self, h=h, x=0, y=0, z=0,ID=0,v_init=None,
                 secs  = {'genrn': {}},
                 mechs = {},
                 ions  = {},
                 cons  = ()):
        """
        __init__(self, h=h, x=0, y=0, z=0,ID=0,v_init=None,
                 secs  = {'genrn': {}},
                 mechs = {},
                 ions  = {},
                 cons  = ()):
        secs, mechs, and ions are all dictionaries containing properties as either constants or functions. These are applied globally during initialization.
        sec names are by default added to a taglist (consisting of the first three characters of the sec name, which allows for easier editing of a group of sections. This can be done through:
        cell = genrn(...secs={'dnd0', 'dnd1', 'dnd2', 'soma', 'ais', 'axon'}...)
        for sec in cell>>’dnd’:
        for sec in cell.tags[‘dnd’]:
        to modify properties in all ‘dnd’ (dendrite) tagged sections

        of note, all sections are also accessible as dictionary entries:
        cell[‘dnd0’]
        cell.dnd0
        """
        self.h = h
        self.tags = {'all': []}
        # secs -> pointer
        self.secs = {}
        self.gesecs = self.tags['all']
        # self.useions = re.compile("USEION ([A-Za-z0-9]+)")
        self.init_cell(secs, ions)
        self.initialize_mechs('all', mechs)
        self.initialize_ionprops()
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
        """
        add_comp(self, sec, ions, *tags):
        add a section with sec properties (L, diam, nseg, cm, Ra) and ions
        """
        sec_ = gesec(self.h, sec, ions)
        # sec_ -> pointer
        self.secs[sec] = (sec_)
        self.tags['all'].append(sec_)
        self.__dict__[sec] = sec_.sec
        for tag in tags:
            try: self.tags[tag].append(sec_)
            except: self.tags[tag] = [sec_]

    def set_props(self, sec, props):
        """
        set_props(self, sec, props):
        set properties (L, diam, nseg, cm, Ra) of a section
        """
        sec = self.return_gesec(sec)
        sec.set_props(props)

    def tag_set_props(self, tag, props):
        """
        tag_set_props(self, tag, props):
        set properties (L, diam, nseg, cm, Ra) of a group of sections that have been attached to a tag
        """
        for sec in self.tags[tag]:
            for prop in props:
                loose_set(sec.sec, '%s' %(prop), props[prop])

    def fset_prop(self, sec, prop, func):
        sec = self.return_gesec(sec)
        # set properties of the segment, diam
        sec.fset_prop(prop, func)

    def insert_mech(self, sec, mech, ions={}, params={}):
        sec = self.return_gesec(sec)
        sec.insert_mech(mech, ions, params)

    def initialize_mechs(self, tag, mechs, ions = {}):
        for sec in self.tags[tag]:
            for mech in mechs:
                sec.insert_mech(mech, ions, mechs[mech])

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

    def initialize_ionprops(self):
        for sec in self.tags['all']:
            sec.set_ionprops()

    def edit_mechs(self, tag, mech, param, value):
        for sec in self.tags[tag]:
            loose_set(sec.sec, '%s_%s' %(param, mech), value)

    def tag_fedit_mechs(self, tag, mech, param, func):
        for sec in self.tags[tag]:
            for seg in sec.sec:
                val = func(seg.x)
                loose_set(seg, '%s_%s' %(param, mech), val)

# additional not called init functions
    def init_nernsts(self):
        for sec in self.secs:
            self.secs[sec].set_nernsts()


    def init_v(self, v_init, ions = ['ca', 'cl', 'k', 'na'], set_pas = False):
        fcdict = {}
        self.h.finitialize(v_init)
        self.h.fcurrent()
        i_net = 0
        print("fcurrent() values (%s mV)" %(v_init))
        lgg.info("fcurrent() values (%s mV)" % (v_init))
        for sec in self.secs:
            sec = self.secs[sec]
            fcdict[sec.name] = {}
            for mech in sec.mechs:
                fcdict[sec.name][mech] = {}
                for ion in sec.ions:
                    try:
                        i = getattr(sec.sec, 'i%s_%s' %(ion, mech))
                        print("(%s)->%s:->%s=%s mA/cm2" %(sec.name, mech, ion, i))
                        lgg.info("(%s)->%s:->%s=%s mA/cm2" %(sec.name, mech, ion, i))
                        fcdict[sec.name][mech][ion] = i
                        if ion in ions:
                            i_net += i
                    except: pass
            fcdict[sec.name]['i_net'] = i_net
            print("(%s)->i_net = %s" %(sec.name, i_net))
            lgg.info("(%s)->i_net = %s" %(sec.name, i_net))
            try:
                fcdict[sec.name]['e_pas'] = e_pas
                e_pas = sec.sec.v + i_net / sec.sec.g_pas
                print(e_pas)
                print("(%s)->e_pas calculated at %s mV" %(e_pas, v_init))
                lgg.info(e_pas)
                if set_pas:
                    sec.sec.e_pas = e_pas
            except:
                fcdict[sec.name]['e_pas'] = [None]
        return fcdict

    def get_dict(self, tag = 'all'):
        rpr = {}
        for sec in self.tags[tag]:
            rpr[sec.sec] = sec.sec.psection()
        return rpr

## OoOP: indexing>function>unary>power>mul>add>bitshift>and>xor>or>gt
    def __truediv__(self, item):
        return self.secs[item]

    def __gt__(self, item):
        # retrieve gesec objects in a tag using '>' operator, by tag or section name (i.e. self>'all')
        try: return self.tags[item]
        except KeyError: return self.secs[item]

    def __rshift__(self, tag):
        # retrieve section objects in a tag using '>>' operator (i.e. self>>'all')
        return [sec.sec for sec in self.tags[tag]]

    def __call__(self, item):
        # returns the gesec items of a specific tag
        try: return self.tags[item]
        except KeyError: return self.secs[item]

    def __getitem__(self, item):
        # indices for sections (sections stored in order of creation)
        return self.tags['all'][item].sec

    def __repr__(self):
        # printing a shows consolidated information about class
        rpr = ''
        for sec in self.tags['all']:
            r = sec.sec.psection()
            rpr += '%s\n' %(sec.sec.name())
            rpr += 'parent:\t%s\n' %(r['morphology']['parent'])
            rpr += 'morphology:\tL:%f\tdiam:%f\n' %(r['morphology']['L'], max(r['morphology']['diam']))
            rpr += 'ions:\n'
            for ion in sec.ions:
                rpr += '%s: {' %(ion)
                for prop in sec.ions[ion]['props']:
                    rpr +='%s: %s, ' %(prop, sec.ions[ion]['props'][prop])
                rpr += '}'
                if len(sec.ions[ion]['mechs']) > 0:
                    rpr += '\n\t'
                    for mech in sec.ions[ion]['mechs']:
                        rpr +='%s, ' %(mech)
                rpr += '\n'
        return rpr

def cal_nseg( sec, freq, d_lambda ):
# neuron+python of https://www.neuron.yale.edu/neuron/static/docs/d_lambda/d_lambda.html
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
