# create a deep copy of a cellParams dictionary.
from copy import deepcopy as dcp
def cell_copy(cell):
    copy = {'secs': {}, 'secLists': {}, 'globals': {}}

    for sec in cell['secs']:
        copy['secs'][sec] = {'geom': dcp(cell['secs'][sec]['geom']),
                             'topol': dcp(cell['secs'][sec]['topol']),
                             'mechs': {}, 'ions': {} }
        for mech in cell['secs'][sec]['mechs']:
            copy['secs'][sec]['mechs'][mech] = dcp(cell['secs'][sec]['mechs'][mech])
        for ion in cell['secs'][sec]['ions']:
            copy['secs'][sec]['ions'][ion] = dcp(cell['secs'][sec]['ions'][ion])

    return copy