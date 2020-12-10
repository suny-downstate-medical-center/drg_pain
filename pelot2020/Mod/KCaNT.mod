: Based on Schild et al 1994

: Calcium Activated Potassium Channel

: Coded and modified by Nathan Titus 2018
: Development Notes: cao, nao, and ko are actually 
: concentrations in the perineuronal space
:
: Used Alpha and beta for now because cai tied into alpha only

NEURON {
	SUFFIX kcaNT
	USEION k READ ek WRITE ik
	USEION ca READ cai
	RANGE ik
	RANGE gbar, ikca, ninf, ntau, beta
	RANGE gp, alpha, g
}

UNITS {
    (molar) = (1/liter)                     : moles do not appear in units
    (mM)    = (millimolar)             	
	(uA) = (microamp)
	(mA) = (milliamp)
	(mV) = (millivolt)
	(um) = (micron)
	(S) = (siemens)

}

PARAMETER {
	gbar = 6.5e-9 (S/cm2) :from Schild et al 1994
}

ASSIGNED {
	v (mV)
	celsius (degC)
	g (S/cm2)
	gp
	ninf
	ntau
	cai (mM)
	ik (mA/cm2)
	ikca (mA/cm2)
	alpha
	beta
	ek (mV)
	T (degC)
	q10
}


INITIAL {
	rates(v)
	n = ninf
}

STATE {
	n
}

BREAKPOINT {
	SOLVE states METHOD cnexp
	gp = n
	g = gbar*gp
	ik = g*(v-ek)

}

DERIVATIVE states {
	rates(v)
	n' = (ninf - n)/ntau      
}

? rates
PROCEDURE rates(Vm (mV)) {
	LOCAL ab
UNITSOFF	
	T = 273 + celsius 
	q10 = (2.3*(T-296)+(310-T))/14
	
	alpha = 750*cai*exp((Vm-10)/12)
	beta = 0.05*exp(-1*(Vm-10)/60)
	ab = alpha + beta
	
	ninf = alpha / ab
	ntau = 4.5/(ab)/q10
}
UNITSON
