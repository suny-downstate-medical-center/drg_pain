: current pulse driven by event.

NEURON {
	POINT_PROCESS IPClamp
	RANGE dur, i, amp
	ELECTRODE_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	dur = 1 (ms)	
	amp = 0.1 (nA)
}

ASSIGNED {
	i (nA)
	toff (ms)
}

INITIAL {
	i = 0
    toff = -1
}

NET_RECEIVE(weight (uS)) {
    i = amp
	toff = t + dur
}

BREAKPOINT {
	at_time(toff)
    if (t > toff && toff > 0) {
        i = 0
        toff = -1
    }
}