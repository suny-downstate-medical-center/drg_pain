TITLE KNa channels for bladder small DRG neuron soma model

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
	(molar)  =  (1/liter)
	(mM) =  (millimolar)
}
 
NEURON {
        SUFFIX knatype
        USEION k READ ek WRITE ik
		USEION na READ nai
        RANGE gbar, ik, winf, tau
		RANGE w
		RANGE tadj, q10
        THREADSAFE
}
 
PARAMETER {
        gbar = 1e-5 (S/cm2)	<0,1e9>
		q10 = 2.5 (1)
}

ASSIGNED {
		celsius (degC)
		tadj (1)

        v 	(mV)
        ek	(mV)   
        ik 	(mA/cm2)
		nai	(mM)
		winf (1)
		tau  (ms)
}

STATE{
	w
}

BREAKPOINT {
       SOLVE state METHOD cnexp
		rates(nai)
		ik = gbar*w*(v - ek)
}
 
DERIVATIVE state{
	w' = (winf-w)/tau * tadj
}

INITIAL{
	tadj = q10 ^ ((celsius - 22) / 10)
	rates(nai)
	w = winf
}

PROCEDURE rates(nai(mM)){
    TABLE winf, tau
    FROM 5 TO 15 WITH 50

	winf = 1/(1+(38.7(mM)/nai)^3.5) : Biscoff et al., 1998
													
	tau = 1(ms)
}