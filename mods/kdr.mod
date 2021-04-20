TITLE KDR Current for bladder small DRG neuron soma model
: Author: Darshan Mandge (darshanmandge@iitb.ac.in)
: Computational Neurophysiology Lab
: Indian Institute of Technology Bombay, India 

: For details refer: 
: A biophysically detailed computational model of bladder small DRG neuron soma 
: Darshan Mandge and Rohit Manchanda, PLOS Computational Biology (2018)


UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(S) = (siemens)
}

NEURON {
        SUFFIX kdr
        USEION k READ ek WRITE ik
        RANGE gbar, g, ik
        RANGE ninf, ntau
		RANGE n
		RANGE tadj, q10
		THREADSAFE
}
 
PARAMETER {
		gbar = 0.002688 (S/cm2)
		q10 = 2.5 (1)
}
 
STATE {
        n
}
 
ASSIGNED {
		celsius (degC)
		tadj (1)

        v (mV)
        ek (mV)

		g (S/cm2)
		ik (mA/cm2)

		ninf
		ntau (ms)
}
 

BREAKPOINT {
        SOLVE states METHOD cnexp
        g = gbar*n*n*n*n
		ik = g*(v - ek)     
}
 
 
INITIAL {
	tadj = q10 ^ ((celsius - 22) / 10)
	rates(v)
	n = ninf
}


DERIVATIVE states {  
        rates(v)
        n' = (ninf-n)/ntau * tadj
}
 

PROCEDURE rates(v(mV)) {

UNITSOFF
    TABLE ninf, ntau
    FROM -100 TO 100 WITH 200
        :"n" potassium activation system
        ninf = 1/(1+exp(-(v+35)/15.4)) :Sheets et al., 2007 supplement
		ntau = 7.14085 + (636.5557/(17.07686*sqrt(3.14/2)))*exp(-2*((v+19.99951)/17.07686)^2): by fitting data from Yoshimura et al., 2006
}
 
UNITSON
