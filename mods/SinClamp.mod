: sine pulse driven by event.

NEURON {
	POINT_PROCESS SinClamp
	RANGE dur, i, amp, t0
	ELECTRODE_CURRENT i
}

UNITS {
	(nA) = (nanoamp)
  PI = (pi) (1)
}

PARAMETER {
	dur = 1 (ms)	
	amp = 0.1 (nA)
}

ASSIGNED {
	i (nA)
	toff (ms)
  t0 (ms)
}

INITIAL {
	i = 0
  toff = -1
}

NET_RECEIVE(weight (uS)) {
  t0 = t
	toff = t + dur
}

BREAKPOINT {
  at_time(t0)
  at_time(toff)
  i = 0
  if (t0 < t && t < toff) {
    i = amp * sin(PI * ((t - t0) / dur))
  }
}