TITLE Slow KA Current for bladder small DRG neuron soma model
COMMENT
KA current from modeldb #243448
Computational model of bladder small DRG neuron soma (Mandge & Manchanda 2018)
ENDCOMMENT

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
	(S) = (siemens)
}

NEURON {
	SUFFIX kam
	USEION k READ ek WRITE ik
	RANGE gkbar, gk, ik
	RANGE ninf, ntau, hinf, htau, uinf, utau
	THREADSAFE
}
 
PARAMETER {
        gkbar = 0.00136 (S/cm2)
}
 
STATE {
        n 	: activation
		h  : fast inactivation
		u	: slow inactivation
}
 
ASSIGNED {
	v (mV)
	ek (mV)
	gk (S/cm2)
    ik (mA/cm2)
	    
    ninf (1)
	ntau (ms)
	hinf (1)
	htau (ms)
    uinf (1)
	utau (ms)
}
 
BREAKPOINT {
	SOLVE states METHOD cnexp
	gk = gkbar*n*(h*0.3+u*0.7)
	ik = gk*(v - ek)
}
 
INITIAL {
	rates(v)
	
	n = ninf
	h = hinf
	u = uinf
}

DERIVATIVE states {  
	rates(v)
	
	n'  = (ninf-n)/ntau
	h' = (hinf-h)/htau
	u' = (uinf-u)/utau
}
 
PROCEDURE rates(v(mV)) {
    TABLE ninf, ntau, hinf, htau, uinf, utau
    FROM -100 TO 100 WITH 200

		ninf = (1/(1+exp((-40.8-v)/9.5)))  		: Data fit: Yoshimura et al., 1996
		ntau = 1.1972 + 2.56*exp(-2*((v+60)/45.75992)^2)	: Data fit: Yoshimura et al., 2006
		
		hinf = 1/(1 + exp((v+74.2)/9.6))  		: Data fit: Yoshimura et al., 1996
		htau = 25.46 + 67.41*exp(-2*((v+50)/21.95)^2) : Both h1tau and h2tau Data fit: Yoshimura et al., 2006

        uinf = hinf
		utau = 200 + 587.4*exp(-((v-0)/47.77)^2)	
}