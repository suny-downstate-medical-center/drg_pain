TITLE Nav1.9 Channel for bladder small DRG neuron soma model
:Model adapted from Baker, 2005

: For details refer: 
: A biophysically detailed computational model of bladder small DRG neuron soma 
: Darshan Mandge and Rohit Manchanda, PLOS Computational Biology (2018)

NEURON {
	SUFFIX nav1p9
	USEION na READ ena WRITE ina
	RANGE gbar, ena, ina
	RANGE mtau, htau, minf, hinf
	RANGE m, h
	RANGE tadj, q10
}

UNITS {
	(S) = (siemens)
	(mV) = (millivolts)
	(mA) = (milliamp)
}

PARAMETER {
	q10 = 2.5 (1)

	gbar = 1e-5 (S/cm2)

	A_am9 = 1.548 (/ms) : A for alpha m(9 etc ...)
	B_am9 = -11.01 (mV)
	C_am9 = -14.871 (mV)

	A_ah9 = 0.2574 (/ms) : A for alpha h
	B_ah9 = 63.264 (mV)
	C_ah9 = 3.7193 (mV)

	A_bm9 = 8.685 (/ms) : A for beta m
	B_bm9 = 112.4 (mV) 	: table has minus sign typo (Baker, personal comm.)
	C_bm9 = 22.9 (mV)

	A_bh9 = 0.53984 (/ms)   : A for beta h
	B_bh9 = 0.27853 (mV)
	C_bh9 = -9.0933 (mV)
}

ASSIGNED {
	celsius (degC)
	tadj (1)

	v	(mV) 
	ina	(mA/cm2)
	ena	(mV)

	g	(S/cm2)
	htau	(ms)
	mtau	(ms)
	minf
	hinf
}

STATE { m h }

BREAKPOINT {
	SOLVE states METHOD cnexp
	g = gbar * m * h
	ina = g * (v-ena)
}

INITIAL {
	tadj = q10 ^ ((celsius - 22) / 10)
	rates(v)
	: assume that equilibrium has been reached
	m = minf
	h = hinf
}

DERIVATIVE states {
	rates(v)
	m' = (minf - m)/mtau * tadj
	h' = (hinf - h)/htau * tadj
}

PROCEDURE rates(v(mV)) (/ms) {
	LOCAL alpham, betam, alphah, betah
    TABLE mtau, minf, htau, hinf
	DEPEND A_am9, B_am9, C_am9, A_ah9, B_ah9, C_ah9, A_bm9, B_bm9, C_bm9, A_bh9, B_bh9, C_bh9
    FROM -100 TO 100 WITH 200

	alpham=A_am9/(1+exp((v+B_am9)/C_am9))
	betam=A_bm9/(1+exp((v+B_bm9)/C_bm9))

	alphah=A_ah9/(1+exp((v+B_ah9)/C_ah9))
	betah=A_bh9/(1+exp((v+B_bh9)/C_bh9))

	mtau = 1.0 / (alpham + betam)
	minf = alpham * mtau

	htau = 1.0 / (alphah + betah)
	hinf = alphah * htau

}