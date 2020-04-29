TITLE KDR Current, utilizing equations from Sheets et al., 2007
COMMENT
KDR current, Sheets et al., 2007.
ENDCOMMENT

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(S) = (siemens)
}

NEURON {
    SUFFIX kdr
    USEION k READ ek WRITE ik
    RANGE gkbar, gk, ik
    GLOBAL ninf, ntau
}
 
PARAMETER {
    gkbar = 0.002688 (S/cm2)
}

STATE {
    n
}
 
ASSIGNED {
    v (mV)
    ek (mV)

	gk (S/cm2)
	ik (mA/cm2)

	ninf (1)
	ntau (ms)
}
 
BREAKPOINT {
    SOLVE states METHOD cnexp
    gk = gkbar*n*n*n*n
	ik = gk*(v - ek)     
}
  
INITIAL {
	rates(v)
	n = ninf
}

DERIVATIVE states {  
    rates(v)
    n' = (ninf-n)/ntau
}
 
PROCEDURE rates(v(mV)) {
    TABLE ninf, ntau
    FROM -100 TO 100 WITH 200
    :"n" potassium activation system
    ninf = 1/(1+exp(-(v+35)/15.4)) :Sheets et al., 2007 supplement
	ntau = 7.14085 + (636.5557/(17.07686*sqrt(3.14/2)))*exp(-2*((v+19.99951)/17.07686)^2): by fitting data from Yoshimura et al., 2006
}
