from neuron import h
from genrn import genrn

hGlobals = {#'cai0_ca_ion': 0.000136,
            'celsius': 22.0,
            #'cli0_cl_ion': 40.0,
            #'clo0_cl_ion': 145.0,
            'ki0_k_ion': 140.0,
            'ko0_k_ion': 5.0,
            'nao0_na_ion': 150.0,
            'v_init': -53.5}

customCellRule = {
 'globals': hGlobals,
 'secLists': {},
 'secs': {'sec': {'geom': {'L': 24.0, 'Ra': 100.0, 'cm': 1.5481245576786977, 'diam': 24.0, 'nseg': 1},
                  'ions': {'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
                           'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
                           'na': {'e': 68.83, 'i': 10.0, 'o': 150.0}},
                  'mechs': {'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
                            'kaslow': {'gbar': 0.00136}, 'kdr': {'gbar': 0.002688},
                            'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
                            'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
                            'nattxs': {'gbar': 0.0001},
                            'nav1p8': {'gbar': 0.0087177},
                            'nav1p9': {'gbar': 1e-05},
                            'pas': {'g': 0.0001, 'e': -41.583}},
                  'topol': {},
                  'vinit': -53.5}}
}

# Mandge and Machanda 2019 model
bladderCellRule = {
 'globals': hGlobals,
 'secLists': {},
 'secs': {'sec': {'geom': {'L': 24.0, 'Ra': 100.0, 'cm': 1.5481245576786977, 'diam': 24.0, 'nseg': 1},
                  'ions': {'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
                           'caer': {'e': 0.0, 'i': 0.4, 'o': 1.0},
                           'caip3r': {'e': 0.0, 'i': 0.000136, 'o': 1.0},
                           'camt': {'e': 0.0, 'i': 0.0002, 'o': 1.0},
                           'cl': {'e': -32.7, 'i': 40.0, 'o': 145.0},
                           'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
                           'ip3': {'e': 0.0, 'i': 1.0, 'o': 1.0},
                           'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
                           'na': {'e': 68.83, 'i': 10.0, 'o': 150.0}},
                  'mechs': {'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
                            'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
                            'CaPQ': {'pmax': 8e-06}, 'CaR': {'pmax': 1e-08}, 'CaT': {'pmax': 1e-08},
                            'bkca': {'gbar': 0.0009},
                            'cacc': {'gbar': 1e-06},
                            'cadyn': {'Bmer': 10.0, 'Bmmt': 0.065,
                                      'Kmer': 0.5, 'Kmmt': 1e-05,
                                      'jmaxsr': 3.5e-06,
                                      'k1': 37400000.0, 'k2': 250000.0, 'k3': 500.0, 'k4': 5.0,
                                      'kactip3': 0.0003, 'kcicr': 0.00198, 'kinhip3': 0.0002,
                                      'kip3': 0.0008, 'kmcu': 0.000606, 'kna': 8.0,
                                      'kncx': 0.035, 'konip3': 2.7, 'kpsr': 0.00027,
                                      'ktcicr': 0.0006, 'nmcu': 2.3, 'pump0': 4.232e-13,
                                      'vcicr': 5e-07, 'vmaxsr': 3.75e-06, 'vmcu': 1.4468e-06,
                                      'vncx': 6e-05},
                            'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
                            'ip3dif': {},
                            'kaslow': {'gbar': 0.00136}, 'kdr': {'gbar': 0.002688},
                            'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
                            'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
                            'nattxs': {'gbar': 0.0001},
                            'nav1p8': {'gbar': 0.0087177},
                            'nav1p9': {'gbar': 1e-05},
                            'ncxsoma': {'ImaxNax': 1.1e-05, 'KcNacx': 1.38, 'KnNacx': 87.5},
                            'pas': {'g': 0.0001, 'e': -41.583},
                            'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                                      'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0},
                            'soce': {'pmax': 1e-09},
                            'trpm8': {'C': 67.0, 'em8': 0.0, 'gbar': 1e-07,
                                      'p_ca': 0.01, 'z': 0.65}},
                  'topol': {},
                  'vinit': -53.5}}
}

bcr = bladderCellRule['secs']['sec']

bladderCellArgs = {
    'h'    : h,
    'secs' : {'soma': bcr['geom']},
    'mechs': bcr['mechs'],
    'ions' : bcr['ions'],
    'cons' : ()
}

tjCellArgs= {
    'h'   : h,
    'secs': {'peri': { 'nseg': 257, 'L': 5000, 'diam': 0.8 , 'cm': 1.5481245576786977 },
             'stem': { 'nseg': 3  , 'L': 75  , 'diam': 1.4 , 'cm': 1.5481245576786977 },
             'soma': { 'nseg': 1  , 'L': 24.0, 'diam': 24.0, 'cm': 1.5481245576786977 },
             'cntr': { 'nseg': 363, 'L': 5000, 'diam': 0.4 , 'cm': 1.5481245576786977 }},
    'mechs': bcr['mechs'],
    'ions' : bcr['ions'],
    'cons' : (('stem', 'peri'),
              ('soma', 'stem'),
              ('cntr', 'peri'))
}


def hInit():
    h.load_file('stdrun.hoc')
    h.load_file('tautables.hoc')
    for var in hGlobals:
        execstr = 'h.%s = %s' %(var, hGlobals[var])
        print('exec: %s' %(execstr))
        exec(execstr)

def npSoma( mulnattxs = 1, mulnav1p8 = 1 , mulnav1p9 = 1 ):
    hInit()
    cell = genrn(**bladderCellArgs)
    cell.soma.gbar_nattxs *= mulnattxs
    cell.soma.gbar_nav1p8 *= mulnav1p8
    cell.soma.gbar_nav1p9 *= mulnav1p9
    # inflammatory changes
    # cell.soma.gbar_nav1p8 = 0.06   # 0.0087177 -> 0.06
    # cell.soma.gbar_kaslow = 0.0001 # 0.00136   -> 0.0001
    # cell.soma.gbar_kdr    = 0.001  # 0.002688  -> 0.001
    return cell

def npSomaMut( wtp = 1 ):
    hInit()
    cell = genrn(**bladderCellArgs)
    gbar_nattxs = 0.0001 * (wtp)
    gbar_navmut = 0.0001 * (1 - wtp)
    cell.edit_mechs('all', 'nattxs', 'gbar', gbar_nattxs)
    cell.insert_mech(sec='soma', mech='navmut', ions={'nak': {'e': -15.87}}, params={'gbar': gbar_navmut})
    return cell

def npTJ( mulnattxs = 1, mulnav1p8 = 1, mulnav1p9 = 1 ):
    hInit()
    cell = genrn(**tjCellArgs)
    gbar_nattxs = 0.0001 * mulnattxs
    gbar_nav1p8 = 0.0087177 * mulnav1p8
    gbar_nav1p9 = 1e-5 * mulnav1p9
    cell.edit_mechs('all', 'nattxs', 'gbar', gbar_nattxs)
    cell.edit_mechs('all', 'nav1p8', 'gbar', gbar_nav1p8)
    cell.edit_mechs('all', 'nav1p9', 'gbar', gbar_nav1p9)
    return cell

if __name__=='__main__':
#    from pprint import pprint
    soma = npSomaMut()
    print(soma)
#    pprint(soma.get_dict())
